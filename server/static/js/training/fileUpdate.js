// REQUIRES socket-io!
// <script type="text/javascript" src="//cdnjs.cloudflare.com/ajax/libs/socket.io/1.3.6/socket.io.min.js"></script>
// REQUIRES bootstrap to work well
// REQUIRES player.js


function updateResultFiles(json) {
    
    if (!json) { return; }
    console.log("Updating MIDI file list...");

    var listDiv = document.querySelector("#songlist");
    var list = document.querySelector("#songlist > ul");
    if (!list) {
        console.warn("Missing songlist!");
        return;
    }

    // clear list
    list.innerHTML = "";
    listDiv.style.display = "none";

    for (result of json.results) {
        if (result.length <= 0) { continue; }
        
        var resultName = result;
        var resParts = result.split("/");
        if (resParts.length > 0) {
            resultName = resParts[resParts.length-1];
        }

        var entry = document.createElement("li");
        entry.setAttribute("class", "list-group-item");

        var div = document.createElement("div");
        div.setAttribute("class", "row");

        var div_outer = document.createElement("div");
        div_outer.setAttribute("class", "container");


        var name = document.createElement("a");
        name.setAttribute("class", "songlistText");
        name.setAttribute("href", result);
        name.innerHTML = resultName;

        var name_div = document.createElement("div");
        name_div.setAttribute("class", "col-8");
        name_div.appendChild(name);

        var curFile = document.getElementById("training-result");
        if (curFile && curFile.style.display != "none") {
            var curFileText = curFile.textContent;

            // split and check last element if possible
            var curFileParts = curFileText.split("/");
            if (curFileParts.length > 0) {
                curFileText = curFileParts[curFileParts.length-1];
            }

            // compare
            if (curFileText == resultName) {
                name_div.classList.add("last_file");
            }
        }


        var play = document.createElement("button");
        play.setAttribute("type", "button");
        play.setAttribute("class", "btn btn-success");
        play.setAttribute("file", result);
        play.addEventListener("click", function() {
            playMidiFile(this.getAttribute("file"));
        });
        play.innerHTML = "Play";

        var play_div = document.createElement("div");
        play_div.setAttribute("class", "col-1");
        play_div.appendChild(play);


        var stop = document.createElement("button");
        stop.setAttribute("type", "button");
        stop.setAttribute("class", "btn btn-danger");
        stop.addEventListener("click", stopMidiFile);
        stop.innerHTML = "Stop";

        var stop_div = document.createElement("div");
        stop_div.setAttribute("class", "col-1");
        stop_div.appendChild(stop);


        div.appendChild(name_div);
        div.appendChild(play_div);
        div.appendChild(stop_div);

        div_outer.appendChild(div);
        entry.appendChild(div_outer);
        list.appendChild(entry);
    }

    listDiv.style.display = "block";
}


function createFileUpdateSocket() {
    var url = 'http://' + document.domain + ':' + location.port;
    var socket = io.connect(url);

    socket.on('connect', function() {
        console.log("Socket connection established.");
        //socket.emit('test', {data: 'I\'m connected!'});
    });

    socket.on('results', function(results) {
        //console.log("Got results update from server!");
        //console.log(results);
        updateResultFiles(results);
    });


    // interval to refresh
    /*var socketTimer = setInterval(function() {
        //console.log("Sending status request to server...");
        socket.emit("status");
    },
    refreshTime * 1000);
    */
}


if (enabled) {
    document.addEventListener("DOMContentLoaded", createFileUpdateSocket);
}
