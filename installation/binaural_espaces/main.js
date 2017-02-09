// Get audioContext
window.AudioContext = window.AudioContext || window.webkitAudioContext;
audioContext = new AudioContext();

// Create Audio Nodes
var auralizr = new Auralizr({audioContext: audioContext});
var binauralFIRNode = new BinauralFIR({audioContext: audioContext});

// auralizr IRs loading
var data = {
    'h2e1' : {'ir':'./data/ir/h2e1.wav', 'image':'content/images/main/h2e1.png'},
    's2e1' : {'ir':'./data/ir/s2e1.wav', 'image':'content/images/main/s2e1.png'},
    'e3'   : {'ir':'./data/ir/e3.wav',   'image':'content/images/main/e3.png'},
    's3'   : {'ir':'./data/ir/s3.wav',   'image':'content/images/main/s3.png'},
};

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

// HRTF files loading and setting

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

//Create Audio Nodes
var mediaElement = document.getElementById('source');
var player = audioContext.createMediaElementSource(mediaElement);

//Set HRTF dataset
binauralFIRNode.set_hrtfs(hrtfs);


// connect Audio Nodes
player.connect(binauralFIRNode.input);

auralizr.connect(binauralFIRNode.input);
binauralFIRNode.connect(audioContext.destination);

// set binaural positions
binauralFIRNode.setPosition(0, 0, 1);

$(".vs1").val(0);
//Listeners of the knobs
$(".vs1").knob({
    'change': function(v) {
        // console.log(v);
        // console.log(binauralFIRNode.getPosition().elevation);
        // console.log(binauralFIRNode.getPosition().distance);
        binauralFIRNode.setPosition(v, binauralFIRNode.getPosition().elevation, binauralFIRNode.getPosition().distance);
    }
});

$('.vs3').on("input", function(evt) {
    // console.log(evt.target.value);
    // console.log(binauralFIRNode.getPosition().azimuth);
    // console.log(binauralFIRNode.getPosition().distance);
    binauralFIRNode.setPosition(binauralFIRNode.getPosition().azimuth, evt.target.value, binauralFIRNode.getPosition().distance);
});



