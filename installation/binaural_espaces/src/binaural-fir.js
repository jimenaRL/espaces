;(function(){

    function BinauralFIR(options) {

        /**
         * Instanciate 2 convolver nodes
         * When moving a source, a crossfade is triggered
         * between these 2 convolvers.
         * A, B, A=>B, B=>A, A=>B+Next, B=>A+Next
         * The two latter exist in "pending mode".
         */

        var self = this;
        this.audioContext = options.audioContext;
        this.crossfadeDuration = options.crossfadeDuration;
        this.fog = options.fog;

        this.index = options.index;
        this.tiling_cube = options.tiling_cube;
        this.Lx = this.tiling_cube[0];
        this.Ly = this.tiling_cube[1];
        this.Lz = this.tiling_cube[2];
        this.location = [this.index[0]*this.Lx, this.index[1]*this.Ly, this.index[2]*this.Lz];
        this.hrtfDataset = [];
        this.hrtfDatasetLength = 0;
        this.tree = undefined;
        this.position = {};
        this.input = this.audioContext.createGain();
        this.state = "A"; // States in ["A", "B", "A2B", "B2A"]
        this.target = undefined;
        this.pendingPosition = undefined;
        this.convolverA = new ConvolverAudioGraph({
          audioContext: this.audioContext
        });
        this.convolverA.rampGain.value = 1;
        this.input.connect(this.convolverA.input());
        this.convolverB = new ConvolverAudioGraph({
          audioContext: this.audioContext
        });
        this.convolverB.rampGain.value = 0;
        this.input.connect(this.convolverB.input());


        this.connect = function(node) {
            this.convolverA.connect(node);
            this.convolverB.connect(node);
            return this;
        };


        this.disconnect = function(node) {
            this.convolverA.disconnect(node);
            this.convolverB.disconnect(node);
            return this;
        };


        this.distance = function(a, b) {
          // No need to compute square root here for distance comparison, this is more efficient.
          return Math.pow(a.x - b.x, 2) + Math.pow(a.y - b.y, 2) + Math.pow(a.z - b.z, 2);
        };


        this.proyect_torus_cube_demi_demi = function (p) {
          // COMMENTER
          // location in {-1,0,1}^3
          return {
            x: p.x-Math.floor(p.x+0.5)+this.location[0],
            y: p.y-Math.floor(p.y+0.5)+this.location[1],
            z: p.z-Math.floor(p.z+0.5)+this.location[2],
          };
        };


        this.proyect_torus_cube_zero_one = function (x, y, z) {
            // COMMENTER
            return {
                x: x%this.Lx+this.location[0],
                y: y%this.Ly+this.location[1],
                z: z%this.Lz+this.location[2],
            };
        };

        this.proyect_identity = function (x, y, z) {
            // COMMENTER
            return {x: x, y: y, z:z};
        };


        this.sphericalToCartesian = function (azimuth, elevation, distance) {
            // Trigonometric function from Math library take degrees in radians
          return {
            x: distance * Math.cos(elevation * Math.PI / 180) * Math.cos(azimuth * Math.PI / 180),
            y: distance * Math.cos(elevation * Math.PI / 180) * Math.sin(azimuth * Math.PI / 180),
            z: distance * Math.sin(elevation * Math.PI / 180),
          };
        };


        this.cartesianToSpherical = function (x, y, z) {
            // Trigonometric function from Math library take degrees in radians
            var distance_ = Math.sqrt(Math.pow(x,2)+Math.pow(y,2)+Math.pow(z,2));
            return {
                azimuth: Math.atan2(y,x) * 180 / Math.PI,
                elevation: Math.asin(z/distance_) * 180 / Math.PI,
                distance: distance_,
            };
        };


        this.setPositionCart = function (x, y, z) {
        
            cart_proy = this.proyect_identity(x, y, z);
            sph_proy = this.cartesianToSpherical(cart_proy.x, cart_proy.y, cart_proy.z);
            // Calculate the nearest position for the input azimuth, elevation and distance
            var nearestPosition = this.getRealCoordinates(sph_proy.azimuth, sph_proy.elevation, sph_proy.distance);

            console.log(">>>>")
            console.log("Index     (i, j, k): "+this.index);
            console.log("Location  (x, y, z): "+this.location);
            console.log("In        (x, y, z): ("+x+", "+y+", "+z+")");
            console.log("Proyected (x, y, z): ("+cart_proy.x+", "+cart_proy.y+", "+cart_proy.z+")");
            console.log("Nearest   (a, e, d): ("+nearestPosition.azimuth+", "+nearestPosition.elevation+", "+nearestPosition.distance+")");
            console.log("<<<<");

            // console.log('state in : ' + this.state)
            if (nearestPosition.azimuth !== this.position.azimuth || 
                nearestPosition.elevation !== this.position.elevation || 
                nearestPosition.distance !== this.position.distance) {
                switch (this.state) {
                  case "A":
                    this.state = "A2B";
                    this.pendingPosition = undefined;
                    this._crossfadeTo("B", nearestPosition);
                    break;
                  case "B":
                    this.state = "B2A";
                    this.pendingPosition = undefined;
                    this._crossfadeTo("A", nearestPosition);
                    break;
                  case "A2B":
                    this.pendingPosition = nearestPosition;
                    break;
                  case "B2A":
                    this.pendingPosition = nearestPosition;
                    break;
                }
            // console.log('state out : ' + this.state)
            }

            return nearestPosition
        };


        this.setPosition = function (azimuth, elevation, distance) {

            // Projection onto this tiling
            cart = this.sphericalToCartesian(azimuth, elevation, distance);
            // cart_proy = this.proyect_torus_cube_zero_one(cart.x, cart.y, cart.z);
            cart_proy = this.proyect_identity(cart.x, cart.y, cart.z)
            sph_proy = this.cartesianToSpherical(cart_proy.x, cart_proy.y, cart_proy.z)

            // Calculate the nearest position for the input azimuth, elevation and distance
            var nearestPosition = this.getRealCoordinates(sph_proy.azimuth, sph_proy.elevation, sph_proy.distance);

            console.log(">>>>")
            console.log("Index     (i, j, k): "+this.index);
            console.log("Location  (x, y, z): "+this.location);
            console.log("In        (a, e, d): ("+azimuth+", "+elevation+", "+distance+")");
            console.log("In        (x, y, z): ("+cart.x+", "+cart.y+", "+cart.z+")");
            console.log("Proyected (x, y, z): ("+cart_proy.x+", "+cart_proy.y+", "+cart_proy.z+")");
            console.log("Proyected (a, e, d): ("+sph_proy.azimuth+", "+sph_proy.elevation+", "+sph_proy.distance+")");
            console.log("Nearest   (a, e, d): ("+nearestPosition.azimuth+", "+nearestPosition.elevation+", "+nearestPosition.distance+")");
            console.log("<<<<");

            // console.log('state in : ' + this.state)
            if (nearestPosition.azimuth !== this.position.azimuth || 
                nearestPosition.elevation !== this.position.elevation || 
                nearestPosition.distance !== this.position.distance) {
                switch (this.state) {
                  case "A":
                    this.state = "A2B";
                    this.pendingPosition = undefined;
                    this._crossfadeTo("B", nearestPosition);
                    break;
                  case "B":
                    this.state = "B2A";
                    this.pendingPosition = undefined;
                    this._crossfadeTo("A", nearestPosition);
                    break;
                  case "A2B":
                    this.pendingPosition = nearestPosition;
                    break;
                  case "B2A":
                    this.pendingPosition = nearestPosition;
                    break;
                }
            // console.log('state out : ' + this.state)
            }

            return nearestPosition
        };


        this._crossfadeTo = function(target, position) {
            // console.log('_crossfade in ' + target+ ' at  '
            //                 + position.azimuth + ' '
            //                 + position.elevation + ' '
            //                 + position.distance 
            //                 )

            // Set the new target position
            this.position = position;
            this.target = target;
            var hrtf = this.getHRTF(this.position.azimuth, this.position.elevation, this.position.distance);
            var now = this.audioContext.currentTime;
            var next = now + this.crossfadeDuration;
            switch (this.target) {
              case "A":
                this.convolverA.set_buffer(hrtf);
                this.convolverA.distanceGain().exponentialRampToValueAtTime(
                      this.position.distance,
                      next
                    );
                this.convolverB.rampGain().linearRampToValueAtTime(0, next);
                this.convolverA.rampGain().linearRampToValueAtTime(1, next);
                break;
              case "B":
                this.convolverB.set_buffer(hrtf);
                this.convolverB.distanceGain().exponentialRampToValueAtTime(
                        this.position.distance,
                        next
                      );
                this.convolverA.rampGain().linearRampToValueAtTime(0, next);
                this.convolverB.rampGain().linearRampToValueAtTime(1, next);
                break;
            }
            // Trigger event when linearRamp is reached
            function endRamp(tg) {
              if (tg.audioContext.currentTime > next) {
                window.clearInterval(intervalID);
                // Target state is reached
                tg.state = tg.target;
                tg.target = undefined;
                // Trigger if there is a pending position
                if (tg.pendingPosition) {
                  tg.setPosition(tg.pendingPosition.azimuth, tg.pendingPosition.elevation, tg.pendingPosition.distance);
                }
              }
            }
            var intervalID = window.setInterval(endRamp, 10, this);
          };


        this.setCrossfadeDuration = function(duration) {
            if (duration) {
            // Miliseconds to s
            this.crossfadeDuration = duration / 1000;
            return this;
            } else {
            throw new Error("CrossfadeDuration setting error");
            }
        };


        this.getCrossfadeDuration = function() {
          // Seconds to ms
          return this.crossfadeDuration * 1000;
        };


        this.getPosition = function () {
          return this.position;
        };

        this.getPositionCart = function () {
          return this.sphericalToCartesian(  this.position.azimuth,
                                        this.position.elevation,
                                        this.position.distance
                                    );
        };


        this.getHRTF = function (azimuth, elevation, distance) {
            var nearest = this.getNearestPoint(azimuth, elevation, distance);
            // Return buffer of nearest position for the input values
            return nearest.buffer;
        };


        this.getRealCoordinates = function(azimuth, elevation, distance) {
          // Return azimuth, elevation and distance of nearest position for the input values
          var nearest = this.getNearestPoint(azimuth, elevation, 1);
          // hack to set distance to source in 3D
          return {
            azimuth: nearest.azimuth,
            elevation: nearest.elevation,
            distance: Math.exp(-this.fog * distance),
          };
        };


        this.getNearestPoint = function (azimuth, elevation, distance) {
            // Convert spherical coordinates to cartesian
            var cartesianCoord = this.sphericalToCartesian(azimuth, elevation, distance);
            // Get the nearest HRTF file for the desired position
            var nearest = this.tree.nearest(cartesianCoord, 1)[0];
            return nearest[0];
        };


        this.set_hrtfs = function (hrtfDataset) {
          this.hrtfDataset = hrtfDataset;
          this.hrtfDatasetLength = this.hrtfDataset.length;

          for (var i = 0; i < this.hrtfDatasetLength; i++) {
            var hrtf = this.hrtfDataset[i];
            var catesianCoord = this.sphericalToCartesian(hrtf.azimuth, hrtf.elevation, hrtf.distance);
            hrtf.x = catesianCoord.x;
            hrtf.y = catesianCoord.y;
            hrtf.z = catesianCoord.z;
          }
          this.tree = new KdTree(this.hrtfDataset, this.distance, ['x', 'y', 'z']);
        };


        this.get = function () {
          return this.hrtfDataset;
        };


        console.log("New BinauralFIR initialized at index: ["+this.index+"] with location["+this.location +"].");
    };

    function ConvolverAudioGraph(options) {

        var self = this;
        this.audioContext = options.audioContext;
        this.rampGainNode = this.audioContext.createGain();
        this.distanceGainNode = this.audioContext.createGain();
        this.distanceGainNode.gain.value = 1;
        this.convNode = this.audioContext.createConvolver();
        this.convNode.normalize = false;

        this.rampGainNode.connect(this.convNode);
        this.convNode.connect(this.distanceGainNode)

        // Hack to force audioParam active when the source is not active
        this.oscillatorNode = this.audioContext.createOscillator();
        this.gainOscillatorNode = this.audioContext.createGain();
        this.oscillatorNode.connect(this.gainOscillatorNode);
        this.gainOscillatorNode.connect(this.rampGainNode);
        this.gainOscillatorNode.gain.value = 0;
        this.oscillatorNode.start(0);

        this.connect = function(node) {
          this.distanceGainNode.connect(node);
          return this;
        };

        this.disconnect = function(node) {
          this.convNode.disconnect(node);
          return this;
        };

        this.input = function() {
          return this.rampGainNode;
        };

        this.rampGain = function() {
          return this.rampGainNode.gain;
        };

        this.distanceGain = function() {
          return this.distanceGainNode.gain;
        };

        this.set_buffer = function(value) {
          this.convNode.buffer = value;
        };

        // console.log('ConvolverAudioGraph initialized.')

    };


    /* Expose 'ConvolverAudioGraph' */
    if ('undefined' == typeof module) {
      window.ConvolverAudioGraph = ConvolverAudioGraph;
    } else {
      module.exports = ConvolverAudioGraph;
    };

    /* Expose 'BinauralFIR' */
    if ('undefined' == typeof module) {
      window.BinauralFIR = BinauralFIR;
    } else {
      module.exports = BinauralFIR;
    }


})();
