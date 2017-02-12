// Get audioContext
window.AudioContext = window.AudioContext || window.webkitAudioContext;
audioContext = new AudioContext();

// load IR data
var data = {
    'h2e1': {'ir':'./data/ir/h2e1.wav', 'image':'content/images/main/h2e1.png'},
    's2e1': {'ir':'./data/ir/s2e1.wav', 'image':'content/images/main/s2e1.png'},
    'e3': {'ir':'./data/ir/e3.wav',   'image':'content/images/main/e3.png'},
    's3': {'ir':'./data/ir/s3.wav',   'image':'content/images/main/s3.png'},
};

// load HRTF files
for (var i = 0; i < hrtfs.length; i++) {
    var buffer = audioContext.createBuffer(2, 512, 44100);
    var bufferChannelLeft = buffer.getChannelData(0);
    var bufferChannelRight = buffer.getChannelData(1);
    for (var e = 0; e < hrtfs[i].fir_coeffs_left.length; e++) {
        bufferChannelLeft[e] = hrtfs[i].fir_coeffs_left[e];
        bufferChannelRight[e] = hrtfs[i].fir_coeffs_right[e];
    }
    hrtfs[i].buffer = buffer;
}

// Create and connect audio nodes

/// binaural
var binauralFIRNode = new BinauralFIR({
                                        audioContext: audioContext,
                                        index: [0,0,0],
                                        tiling_cube : [1,1,1],
                                        fog : 0.01,
                                        crossfadeDuration : 0.1// original value 0.02;
                                        });
binauralFIRNode.set_hrtfs(hrtfs);
binauralFIRNode.connect(audioContext.destination);
var firstPosition = { azimuth: 0,  elevation: 0,  distance: 50,};
binauralFIRNode.setPosition(firstPosition.azimuth,
                            firstPosition.elevation,
                            firstPosition.distance
                            );


var use_oscillator = true;
var use_player = false;
var use_auralizr = false;

/// auralizr
if (use_auralizr==true) {
    var auralizr = new Auralizr({audioContext: audioContext});
    if (auralizr.userMediaSupport){
        for (var key in data){
            auralizr.load(data[key]['ir'], key, function(){});
    }
    var key = 'e3'
    if (auralizr.userMediaSupport){
        var onAuralizrLoad = function (key){
                auralizr.use(key);
                }
            };
        auralizr.load(data[key]['ir'], key, onAuralizrLoad);
    }
    auralizr.connect(binauralFIRNode.input);
}

/// player
if (use_player==true) {
    var mediaElement = document.getElementById('source');
    var player = audioContext.createMediaElementSource(mediaElement);
    player.connect(binauralFIRNode.input);
}

/// oscillator
if (use_oscillator==true) {
    var oscillator = this.audioContext.createOscillator();
    oscillator.frequency.value = 1000
    oscillator.start(0);
    oscillator.connect(binauralFIRNode.input);
}


// controls 
$(".vs1").val(firstPosition.azimuth);
$(".vs3").val(firstPosition.elevation);
$(".vs4").val(firstPosition.distance);

//Listeners of the knobs
$(".vs1").knob({
    'change': function(value) {
        console.log("azimuth : " +value);
        nearestPosition = binauralFIRNode.setPosition(value,
                                    binauralFIRNode.getPosition().elevation,
                                    binauralFIRNode.getPosition().distance);
    }
});

$('.vs3').on("input", function(evt) {
    console.log("elevation : " +evt.target.value);
    nearestPosition = binauralFIRNode.setPosition(binauralFIRNode.getPosition().azimuth,
                                evt.target.value, 
                                binauralFIRNode.getPosition().distance);
});

$('.vs4').on("input", function(evt) {
    console.log("distance : " +evt.target.value);
    nearestPosition = binauralFIRNode.setPosition(binauralFIRNode.getPosition().azimuth,
                                binauralFIRNode.getPosition().elevation,
                                evt.target.value);
});
