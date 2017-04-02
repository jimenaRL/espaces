var auralizr = new Auralizr();

var data = {
    'h2e1' : {'ir':'content/ir/paris/h2e1.wav', 'image':'content/images/h2e1.png'},
    's2e1' : {'ir':'content/ir/paris/s2e1.wav', 'image':'content/images/s2e1.png'},
    'e3'   : {'ir':'content/ir/paris/e3.wav',   'image':'content/images/e3.png'},
    's3'   : {'ir':'content/ir/paris/s3.wav',   'image':'content/images/s3.png'},
};

var play  = '▶';
var pause = '❚❚';

if (auralizr.userMediaSupport){
    var onAuralizrLoad = function (key){
            var element = document.getElementsByClassName(key)[0];
            if (element) {
                enableClickFunctionality(data[key]['image'],element,key);
                element.innerHTML = play;
            }
        };
    for (var key in data){
        auralizr.load(data[key]['ir'], key, onAuralizrLoad);
    }
}

function resetAllSpans() {
    var allPlaces =  [].slice.call(document.getElementsByClassName('place'));
    allPlaces.forEach(function(element) {
        element.classList.remove('enabled');
        if (element.innerHTML === pause)
            element.innerHTML = play;
    });
}

function enableThisSpan(element){
    element.classList.add('enabled');
    element.innerHTML = pause;
}

function enableClickFunctionality(url_str,element,key){
    element.addEventListener('click',function(event){

        console.log('load image from '+url_str);
        document.getElementById('img_main').src = url_str;

        if (element.innerHTML === play){
            resetAllSpans();
            auralizr.use(this.id);
            if (!auralizr.isRunning){
                auralizr.start();
            }
            enableThisSpan(element);
        }else{
            // Pause
            auralizr.stop();
            resetAllSpans();
        }
    }, false);
}