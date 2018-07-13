// Requires jQuery to work!

function settingsOpened() {
    collapsed(true);
}

function settingsClosed() {
    collapsed(false);
}

function collapsed(state) {
    var button = document.getElementById("settings_btn");
    if (!button) { return; }

    if (state == true) {
        button.textContent = "Show Settings";
    }
    else {
        button.textContent = "Hide Settings";
    }
}


// validation settings
function validationChange() {
    var validationCheckbox = document.getElementById("validation");
    var validDiv = document.getElementById("validation_rate_div");
    if (validDiv) {
        if (validationCheckbox.checked) {
            $('#validation_rate_div').collapse("show");
            //validDiv.style.display = "block";
        }
        else {
            $('#validation_rate_div').collapse("hide"); 
            //validDiv.style.display = "none";
        }
    }
}


// check if network is currently training something/available
// if not, submit the result, otherwise show a warning
function submitSettings(e) {

    // perform request
    var r = new XMLHttpRequest();

    // open(method, url, async, user, psw)
    // false for synchronous request
    var url = "/training/status";
    r.open("GET", url, false);
    r.send();

    // process response and check the status
    var resultText = r.responseText;
    var resultJSON = JSON.parse(resultText);

    // only prevent submit if this works
    if (resultJSON) {
        if (resultJSON.status && resultJSON.status == "training" && resultJSON.finished == false) {
            alert("The network is already training...\nPlease try again later!");

            // prevent sending the data directly
            if (e.preventDefault) {
                e.preventDefault();
            }
            return false;
        }
    }
    else {
        console.warn("Failed to check training status.");
    }

    // submit anyway
    console.log("Request submit ok.");
    return true;
}


// updates the info if there is currently something training
function updateInfo(json) {

    console.log("Updating training info...");
    if (!json) { return; }

    var infoEl = document.getElementById("train_info");
    if (!infoEl) {
        var headline1 = document.querySelector("main + h1");
        if (headline1) {
            var newInfoEl = document.createElement("div");
            newInfoEl.setAttribute("id", "train_info");
            document.querySelector("main").appendChild(newInfoEl);
            infoEl = newInfoEl;
        }
    }

    // make empty and hide
    infoEl.innerHTML = "";
    infoEl.style.display = "none";

    if (!json.status) { console.log("JSON got no status."); return; }
    if (json.status == "training" || json.status == "converting") {
        if ((json.status == "training" && json.finished == false) || json.status == "converting") {
            var info = document.createElement("div");

            // use bootstrap to show info element
            info.setAttribute("class", "alert alert-warning");
            
            var warn = document.createElement("strong");
            warn.innerHTML = "Warning!";
            info.appendChild(warn);
            info.innerHTML += "<br/>There is already a training running!<br/>";

            var trainLink = document.createElement("a");
            trainLink.innerHTML = "To check the current status click on this link!";
            trainLink.setAttribute("href", "./training");
            info.appendChild(trainLink);

            // add real info
            infoEl.appendChild(info);
            infoEl.style.display = "block";
        }
    }
}



// check if collapsed by default and set button text accordingly
function init() {

    // add listeners for status changes
    $('#settings').on('shown.bs.collapse', function (e) {
        if (e.target.id == "settings") {
            settingsClosed();
        }
        else {
            // other elements
        }
    })


    $('#settings').on('hidden.bs.collapse', function (e) {
        if (e.target.id == "settings") {
            settingsOpened();
        }
        else {
            // other elements
        }
    })

    // initial text for settings button
    var isCollapsed = $('#settings').hasClass('collapse');
    collapsed(isCollapsed);

    // validation checkbox listener
    var validationCheckbox = document.getElementById("validation");
    if (validationCheckbox) {
        validationCheckbox.addEventListener("change", validationChange);
    }

    // shows or hides rate based on default value
    if (validationCheckbox) {
        validationChange();
    }


    // open socket connection to the server and get the current status
    var url = 'http://' + document.domain + ':' + location.port;
    var socket = io.connect(url);

    socket.on('connect', function() {
        console.log("Socket connection established.");
    });

    // to receive current server status
    socket.on('status', function(status) {
        updateInfo(status);
    });


    // event listener for submit button click
    var settingsForm = document.getElementById("form_settings");
    if (settingsForm) {
        if (settingsForm.attachEvent) {
            settingsForm.attachEvent("submit", submitSettings);
        }
        else {
            settingsForm.addEventListener("submit", submitSettings);
        }
    }
    else {
        console.warn("Missing settings form!");
    }
}

// call init once the DOM content is loaded
document.addEventListener("DOMContentLoaded", init);
