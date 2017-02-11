// Get audioContext
window.AudioContext = window.AudioContext || window.webkitAudioContext;
audioContext = new AudioContext();

// IR data
var data = {
    'h2e1': {'ir':'./data/ir/h2e1.wav', 'image':'content/images/main/h2e1.png'},
    's2e1': {'ir':'./data/ir/s2e1.wav', 'image':'content/images/main/s2e1.png'},
    'e3': {'ir':'./data/ir/e3.wav',   'image':'content/images/main/e3.png'},
    's3': {'ir':'./data/ir/s3.wav',   'image':'content/images/main/s3.png'},
};

// HRTF files
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

// Create Audio Nodes
var auralizr = new Auralizr({audioContext: audioContext});

var BinauralNet = new BinauralNet({ 
                                        audioContext: audioContext,
                                        locations_coordinates: [[0,1,1],[1,0,1],[1,1,0]],
                                        hrtfDataset: hrtfs,
                                        });

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

// create Audio Nodes
var mediaElement = document.getElementById('source');
var player = audioContext.createMediaElementSource(mediaElement);

// player = this.audioContext.createOscillator();
// player.start(0);



// connect Audio Nodes
BinauralNet.connect_from(player)
BinauralNet.connect_from(auralizr)
BinauralNet.connect_to(audioContext.destination);

// set binaural positions (azimuth, elevation, distance)
BinauralNet.setPositions(1, 0, 0.5);


$(".vs1").val(0);
// listeners of the knobs
$(".vs1").knob({
    'change': function(value) {
        console.log("azimuth : " +value);
        BinauralNet.setPositions_azimuth(value)
    }
});

$('.vs3').on("input", function(evt) {
    console.log("elevation : " +evt.target.value);
    BinauralNet.setPositions_elevation(evt.target.value)
});

$('.vs4').on("input", function(evt) {
    console.log("distance : " +evt.target.value);
    BinauralNet.setPositions_distance(evt.target.value)
});
