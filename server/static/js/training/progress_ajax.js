// REQUIRES socket-io!
// <script type="text/javascript" src="//cdnjs.cloudflare.com/ajax/libs/socket.io/1.3.6/socket.io.min.js"></script>
// REQUIRES progressUpdate.js!


// enable or disable the ajax update script
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
                //console.log("Refreshing status.");
                updateProgress(jData);
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


// start interval for the progress bar update
if (enabled) {
    var timer = setInterval(getTrainingStatus, refreshTime * 1000);

    // refresh right now
    if (refreshTime > 0.5) {
        getTrainingStatus();
    }
}
