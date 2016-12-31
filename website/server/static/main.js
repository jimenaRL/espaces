var auralizr = new Auralizr();

var data = {
    'h2e1' : {'ir':'content/ir/ecm_20160719/h2e1.wav', 'image':'content/images/background/h2e1.png'},
    's2e1' : {'ir':'content/ir/ecm_20160719/s2e1.wav', 'image':'content/images/background/s2e1.png'},
    'e3'   : {'ir':'content/ir/ecm_20160719/e3.wav',   'image':'content/images/background/e3.png'},
    's3'   : {'ir':'content/ir/ecm_20160719/s3.wav',   'image':'content/images/background/s3.png'},
};

if (auralizr.userMediaSupport){
    var onAuralizrLoad = function (key){
            var element = document.getElementsByClassName(key)[0];
            if (element) {
                enableClickFunctionality(data[key]['image'],element,key);
                element.innerHTML = '▶';
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
        if (element.innerHTML === '❚❚')
            element.innerHTML = '▶';
    });
}

function enableThisSpan(element){
    element.classList.add('enabled');
    element.innerHTML = '❚❚';
}

function enableClickFunctionality(url_str,element,key){
    element.addEventListener('click',function(event){

        console.log('load image from '+url_str)
        document.body.style.backgroundImage = "url('"+url_str+"')"

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