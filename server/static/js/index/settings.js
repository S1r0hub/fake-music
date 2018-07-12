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
}

// call init once the DOM content is loaded
document.addEventListener("DOMContentLoaded", init);
