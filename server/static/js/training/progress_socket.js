// REQUIRES socket-io!
// <script type="text/javascript" src="//cdnjs.cloudflare.com/ajax/libs/socket.io/1.3.6/socket.io.min.js"></script>
// REQUIRES progressUpdate.js!


// enable or disable the update script
var enabled = true;

// refresh time in seconds
var refreshTime = 2;


function createSocket() {
    var url = 'http://' + document.domain + ':' + location.port;
    var socket = io.connect(url);

    socket.on('connect', function() {
        console.log("Socket connection established.");
        //socket.emit('test', {data: 'I\'m connected!'});
    });

    /*
    socket.on('test', function(msg) {
        console.log("Server response:");
        console.log(msg);
    });
    */

    socket.on('status', function(status) {
        //console.log("Got status update from server!");
        //console.log(status);
        updateProgress(status);
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
    createSocket();
}
