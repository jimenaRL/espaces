;(function(){

    function BinauralNet(options) {

        var self = this;
        this.audioContext = options.audioContext;
        this.hrtfDataset = options.hrtfDataset;
        this.index_list = options.index_list;
        this.tiling_cube = options.tiling_cube;

        // creates locations
        this.locations = []
        for (var i = 0; i < this.index_list.length; i++) {
            var binauralFIRNode = new BinauralFIR({ 
                                        audioContext: this.audioContext,
                                        index: this.index_list[i],
                                        tiling_cube : this.tiling_cube,
                                        });
            binauralFIRNode.set_hrtfs(this.hrtfDataset);
            binauralFIRNode.setPosition(1, 0, 0.5);
            this.locations.push(binauralFIRNode)
        }

        this.setPositions = function (azimuth, elevation, distance) {
            for (var i = 0; i < this.locations.length; i++) {
                binauralFIRNode = this.locations[i]
                binauralFIRNode.setPosition(azimuth, elevation, distance);
            }
        };

        this.setPositions_azimuth = function (azimuth) {
            for (var i = 0; i < this.locations.length; i++) {
                binauralFIRNode = this.locations[i]
                elevation = binauralFIRNode.getPosition().elevation
                distance = binauralFIRNode.getPosition().distance
                binauralFIRNode.setPosition(azimuth, elevation, distance);
            }
        };

        this.setPositions_elevation = function (elevation) {
            for (var i = 0; i < this.locations.length; i++) {
                binauralFIRNode = this.locations[i]
                azimuth = binauralFIRNode.getPosition().azimuth
                distance = binauralFIRNode.getPosition().distance
                binauralFIRNode.setPosition(azimuth, elevation, distance);
            }
        };

        this.setPositions_distance = function (distance) {
            for (var i = 0; i < this.locations.length; i++) {
                binauralFIRNode = this.locations[i]
                azimuth = binauralFIRNode.getPosition().azimuth
                elevation = binauralFIRNode.getPosition().elevation
                binauralFIRNode.setPosition(azimuth, elevation, distance);
            }
        };

        this.connect_from = function(node) {
            for (var i = 0; i < this.locations.length; i++) {
                node.connect(this.locations[i].input);
            }
        };

        this.connect_to = function(node) {
            for (var i = 0; i < this.locations.length; i++) {
                this.locations[i].connect(node);
            }
        };

        this.show_locations_coordinates = function() {
            for (var i = 0; i < this.locations.length; i++) {
                console.log(this.locations_coordinates[i]);
            }
        };

        this.show_locations = function() {
            for (var i = 0; i < this.locations.length; i++) {
                console.log(this.locations[i].position);
            }
        };

        console.log("New BinauralNet initialized with tiling_cube ["+this.tiling_cube +"].");

    };

    /* Expose 'BinauralNet' */
    if ('undefined' == typeof module) {
      window.BinauralNet = BinauralNet;
    } else {
      module.exports = BinauralNet;
    }

})();
