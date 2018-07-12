// REQUIRES socket-io!
// <script type="text/javascript" src="//cdnjs.cloudflare.com/ajax/libs/socket.io/1.3.6/socket.io.min.js"></script>


// enable or disable the script
var enabled = true;

// refresh time in seconds
var refreshTime = 2;


function getTrainingStatus() {
    if (!enabled) { return; }

    var xhttp = new XMLHttpRequest();

    // set callback function
    xhttp.onreadystatechange = progressCallback;

    //var url = location.protocol + "//" + window.location.hostname;
    var url = "/training/status";

    // open(method, url, async, user, psw)
    // true for asynchronous opening
    xhttp.open("GET", url, true)
    xhttp.send();
}


function progressCallback(request) {

    if (this.readyState == 1) {
        //console.log("Requesting status...");
    }
    else if (this.readyState == 4) {
        if (this.status == 200) {
            response = this.responseText;
            var jData = JSON.parse(response);

            if (jData) {
                //console.log("Got new status: " + jData);
                console.log("Refreshing status.");
                updateProgressBar(jData);
            }
            else {
                console.warn("Failed to parse json data! (data: " + response + ")");
            }
        }
        else {
            console.log("Status error: " + this.status);
        }
    }
}


function updateProgressBar(json) {

    if (!json) { return; }


    if (json.status && json.status == "training") {
        var progress = 0;

        // calculate progress
        if (json.epoch && json.epochs) {
            progress = json.epoch / json.epochs * 100;
            progress = Math.round(progress * 10) / 10;
        }

        if (json.start) {
            var start = document.getElementById("training-start");
            if (start) {
                start.innerHTML = json.start;
            }
        }

        setProgress(progress);
    }
    else {
        setProgress(progress);
    }
}


// progress in percentage (0 - 100)
function setProgress(progress) {

    if (!progress) {
        progress = 0;
    }

    //console.log("Progress: " + progress);

    // get progress bar
    var progress_div = document.getElementById("training-progress");

    if (!progress_div) {
        console.warn("Missing progress-bar element!");
        return;
    }

    var progress_str = String(progress) + "%";
    progress_div.style.width = progress_str;
    progress_div.setAttribute("aria-valuenow", String(progress));
    progress_div.innerHTML = progress_str;
}


// start interval for the progress bar update
if (enabled) {
    var timer = setInterval(getTrainingStatus, refreshTime * 1000);
}



function createSocket() {
    var socket = io.connect('http://' + document.domain + ':' + location.port);
    socket.on('connect', function() {
        console.log("Socket connection established!");
        //socket.emit('my event', {data: 'I\'m connected!'});
    });
}

createSocket();
