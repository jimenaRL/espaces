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
        this.hrtfDataset = [];
        this.hrtfDatasetLength = 0;
        this.tree = undefined;
        this.position = {};
        this.crossfadeDuration = 0.02;
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

        console.log("BinauralFIR initialized.")
    };

    BinauralFIR.prototype.connect = function(node) {
        this.convolverA.connect(node);
        this.convolverB.connect(node);
        return this;
    };

    BinauralFIR.prototype.disconnect = function(node) {
        this.convolverA.disconnect(node);
        this.convolverB.disconnect(node);
        return this;
    };

    BinauralFIR.prototype.distance = function(a, b) {
      // No need to compute square root here for distance comparison, this is more efficient.
      return Math.pow(a.x - b.x, 2) + Math.pow(a.y - b.y, 2) + Math.pow(a.z - b.z, 2);
    };

    BinauralFIR.prototype.setPosition = function (azimuth, elevation, distance) {
        // console.log(">>>>")
        // console.log("realPosition    a e d : "+azimuth+" "+elevation+" "+distance)
        // Calculate the nearest position for the input azimuth, elevation and distance
        var nearestPosition = this.getRealCoordinates(azimuth, elevation, distance);
        // console.log("nearestPosition a e d : "+nearestPosition.azimuth+" "+nearestPosition.elevation+" "+nearestPosition.distance)
        // console.log("<<<<")
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
    };

     BinauralFIR.prototype._crossfadeTo = function(target, position) {
        // console.log('_crossfade in ' + target+' at  '+ position.distance)

        // Set the new target position
        this.position = position;
        this.target = target;
        var hrtf = this.getHRTF(this.position.azimuth, this.position.elevation, this.position.distance);
        var now = this.audioContext.currentTime;
        var next = now + this.crossfadeDuration;
        switch (this.target) {
          case "A":
            this.convolverA.set_buffer(hrtf);
            this.convolverA.distanceGain().linearRampToValueAtTime(this.position.distance, next);
            this.convolverB.rampGain().linearRampToValueAtTime(0, next);
            this.convolverA.rampGain().linearRampToValueAtTime(1, next);
            break;
          case "B":
            this.convolverB.set_buffer(hrtf);
            this.convolverB.distanceGain().linearRampToValueAtTime(this.position.distance, next);
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

    BinauralFIR.prototype.setCrossfadeDuration = function(duration) {
        if (duration) {
        // Miliseconds to s
        this.crossfadeDuration = duration / 1000;
        return this;
        } else {
        throw new Error("CrossfadeDuration setting error");
        }
    };

    BinauralFIR.prototype.getCrossfadeDuration = function() {
      // Seconds to ms
      return this.crossfadeDuration * 1000;
    };

    BinauralFIR.prototype.getPosition = function () {
      return this.position;
    };

    BinauralFIR.prototype.getHRTF = function (azimuth, elevation, distance) {
        var nearest = this.getNearestPoint(azimuth, elevation, distance);
        // Return buffer of nearest position for the input values
        return nearest.buffer;
    };


    BinauralFIR.prototype.sphericalToCartesian = function (azimuth, elevation, distance) {
      return {
        x: distance * Math.cos(elevation) * Math.cos(azimuth),
        y: distance * Math.cos(elevation) * Math.sin(azimuth),
        z: distance * Math.sin(elevation),
      };
    };

    BinauralFIR.prototype.cartesianToSpherical = function (x, y, z) {
      var distance_ = Math.sqrt( Math.square(x) + Math.square(y) + Math.square(z) )
      var elevation_ = Math.asin(z/distance_);
      var azimuth_ = Math.atan(y/z);
      return {
        azimuth: azimuth_,
        elevation: elevation_,
        distance: distance_,
      };
    };

    BinauralFIR.prototype.getRealCoordinates = function(azimuth, elevation, distance) {
      // Return azimuth, elevation and distance of nearest position for the input values
      var nearest = this.getNearestPoint(azimuth, elevation, 1);
      // hack to set distance to source
      return {
        azimuth: nearest.azimuth,
        elevation: nearest.elevation,
        distance: distance
      };
    };

    BinauralFIR.prototype.getNearestPoint = function (azimuth, elevation, distance) {
      // Degrees to radians for the azimuth and elevation
      var azimuthRadians = azimuth * Math.PI / 180;
      var elevationRadians = elevation * Math.PI / 180;
      // Convert spherical coordinates to cartesian
      var cartesianCoord = this.sphericalToCartesian(azimuthRadians, elevationRadians, distance);
      // Get the nearest HRTF file for the desired position
      var nearest = this.tree.nearest(cartesianCoord, 1)[0];
      return nearest[0];
    };

    BinauralFIR.prototype.set_hrtfs = function (hrtfDataset) {
      this.hrtfDataset = hrtfDataset;
      this.hrtfDatasetLength = this.hrtfDataset.length;

      for (var i = 0; i < this.hrtfDatasetLength; i++) {
        var hrtf = this.hrtfDataset[i];
        // Azimuth and elevation to radians
        var azimuthRadians = hrtf.azimuth * Math.PI / 180;
        var elevationRadians = hrtf.elevation * Math.PI / 180;
        var catesianCoord = this.sphericalToCartesian(azimuthRadians, elevationRadians, hrtf.distance);
        hrtf.x = catesianCoord.x;
        hrtf.y = catesianCoord.y;
        hrtf.z = catesianCoord.z;
      }
      this.tree = new KdTree(this.hrtfDataset, this.distance, ['x', 'y', 'z']);
    };

    BinauralFIR.prototype.get = function () {
      return this.hrtfDataset;
    };

    /* Expose 'BinauralFIR' */
    if ('undefined' == typeof module) {
      window.BinauralFIR = BinauralFIR;
    } else {
      module.exports = BinauralFIR;
    }

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

        console.log('ConvolverAudioGraph initialized.')

    };

    ConvolverAudioGraph.prototype.connect = function(node) {
      this.distanceGainNode.connect(node);
      return this;
    };

    ConvolverAudioGraph.prototype.disconnect = function(node) {
      this.convNode.disconnect(node);
      return this;
    };

    ConvolverAudioGraph.prototype.input = function() {
      return this.rampGainNode;
    };

    ConvolverAudioGraph.prototype.rampGain = function() {
      return this.rampGainNode.gain;
    };

    ConvolverAudioGraph.prototype.distanceGain = function() {
      return this.distanceGainNode.gain;
    };

    ConvolverAudioGraph.prototype.set_buffer = function(value) {
      this.convNode.buffer = value;
    };

    /* Expose 'ConvolverAudioGraph' */
    if ('undefined' == typeof module) {
      window.ConvolverAudioGraph = ConvolverAudioGraph;
    } else {
      module.exports = ConvolverAudioGraph;
    };

})();
