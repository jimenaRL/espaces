;(function(){

	function Auralizr(options) {
		var self = this;
		this.userMediaSupport = false;
		this.isMicEnabled = false;
		this.irArray = {};
		this.startRequest = false;
		this.isRunning = false;

		this.decayDelay = 3;

		this.convolvers = [];
		this.faders = [];
		this.activeIndex = 0;

        this.audioContext = options.audioContext;

		// Two convolvers for cross fading
		this.convolvers[0] = this.audioContext.createConvolver();
		this.convolvers[1] = this.audioContext.createConvolver();

		this.convolvers[0].normalize = false;
		this.convolvers[1].normalize = false;

		this.faders[0] = this.audioContext.createGain();
		this.faders[1] = this.audioContext.createGain();

		this.convolvers[0].connect(this.faders[0]);
		this.convolvers[1].connect(this.faders[1]);

		if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia){
			console.error('Unfortunately, your browser doesn\'t support the getUserMedia API. You may switch to Google Chrome and if you\'re already on Chrome, you might need to turn on some flags. https://developers.google.com/web/updates/2015/10/media-devices?hl=en');
			return null;
		}

		this.userMediaSupport = true;

		var constraints = {
		    mandatory: {
		      googEchoCancellation: false,
		      googAutoGainControl: false,
		      googNoiseSuppression: false,
		      googHighpassFilter: false
		    },
		    optional: []
		};
		navigator.mediaDevices.getUserMedia({audio: constraints}).then(function (stream) {
			self.isMicEnabled = true;
			var mediaStreamSource = self.audioContext.createMediaStreamSource( stream );
			mediaStreamSource.connect(self.convolvers[0]);
			mediaStreamSource.connect(self.convolvers[1]);
			if (self.startRequest){
				self.start();
			}
		}).catch(function(){
			console.error("Error getting audio stream from getUserMedia. Make sure you're on https.");
		});
	console.log('Auralizr initialized.')
	};

	Auralizr.prototype.load=function(loadData, key, callback) {
		var self = this;
		if (typeof loadData == 'string'){
			//Loading from URL
			var ir_request = new XMLHttpRequest();
			ir_request.open("GET", loadData, true);
			ir_request.responseType = "arraybuffer";
			ir_request.onload = function () {
				self.audioContext.decodeAudioData( ir_request.response, function ( buffer ) {
					self.irArray[key] = buffer;
					if (typeof callback === 'function'){
						callback(key);
					}
				});
			};
			ir_request.send();
		}else if (loadData instanceof AudioBuffer){
			self.irArray[key] = loadData;
			callback(key);
		}
	// console.log('Auralizr loaded data: '+loadData)
	};

	Auralizr.prototype.get_audioContext = function(key) {
		return this.audioContext;
	};

	Auralizr.prototype.isReady=function(key) {
		return this.isMicEnabled && this.irArray.hasOwnProperty(key) && this.irArray[key] !== undefined;
	};

	Auralizr.prototype.use=function(key) {
		if ( this.irArray.hasOwnProperty(key) && this.irArray[key] !== undefined){

			if (this.isRunning){
				var nextIndex = +!this.activeIndex;

				this.convolvers[nextIndex].buffer = this.irArray[key];

				this.faders[this.activeIndex].gain.setTargetAtTime(0,this.audioContext.currentTime, this.decayDelay);
				this.faders[nextIndex].gain.setTargetAtTime(1,this.audioContext.currentTime,this.decayDelay);

				this.activeIndex = nextIndex;
			}else{
				this.convolvers[this.activeIndex].buffer = this.irArray[key];
			}
			// console.log('Auralizr will use: '+key)
		}
	};

	Auralizr.prototype.connect = function(node) {
		this.faders[0].connect(node);
		this.faders[1].connect(node);
	};

	Auralizr.prototype.start= function() {
		this.startRequest = true;
		if (!this.isMicEnabled){
			console.log("Couldn't start the Auralizr. Mic is not enabled");
			return;
		}
		if( this.convolvers[0].buffer === null && this.convolvers[1].buffer === null){
			console.log("Couldn't start the Auralizr. Buffer is not loaded");
			return;
		}

		this.faders[0].gain.setValueAtTime(0,this.audioContext.currentTime);
		this.faders[1].gain.setValueAtTime(0,this.audioContext.currentTime);

		this.faders[this.activeIndex].gain.setTargetAtTime(1,this.audioContext.currentTime,this.decayDelay);

		this.startRequest = false;
		this.isRunning = true;
	console.log('Auralizr started.')
	};

	Auralizr.prototype.stop= function() {
		this.startRequest = false;
		this.faders[0].disconnect();
		this.faders[1].disconnect();

		this.isRunning = false;
		console.log('Auralizr stoped.')
	};


	/* Expose 'Auralizr' */
	if ('undefined' == typeof module) {
		window.Auralizr = Auralizr;
	} else {
		module.exports = Auralizr;
	};

})();
