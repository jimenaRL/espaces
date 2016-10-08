var auralizr = new Auralizr();

var impulseResponses = {
    'h2e1' : 'content/ir/h.wav',
    's2e1' : 'content/ir/s2e1.wav',
    'e3'   : 'content/ir/e3.wav',
    's3'   : 'content/ir/s3.wav ',
};

if (auralizr.userMediaSupport){
    var onAuralizrLoad = function (key){
            var element = document.getElementsByClassName(key)[0];
            if (element) {
                enableClickFunctionality(element,key);
                element.innerHTML = '▶';
            }
        };
    for (var key in impulseResponses){
        auralizr.load(impulseResponses[key], key, onAuralizrLoad);
    }
}

function resetAllSpans() {
    var allPlaces =  [].slice.call(document.getElementsByClassName('place'));
    allPlaces.forEach(function(element) {
        element.classList.remove('enabled');
        if (element.innerHTML === '❚❚')
            element.innerHTML = '▶';
    });
}

function enableThisSpan(element){
    element.classList.add('enabled');
    element.innerHTML = '❚❚';
}

function enableClickFunctionality(element,key){
    element.addEventListener('click',function(event){

        url_str = "url('content/images/background/"+key+".png')"
        console.log('load image from '+url_str)
        document.body.style.backgroundImage = url_str

        if (element.innerHTML === '▶'){
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