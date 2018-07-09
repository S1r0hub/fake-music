$('#settings').on('shown.bs.collapse', settingsClosed);
$('#settings').on('hidden.bs.collapse', settingsOpened);

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

// check if collapsed by default and set button text accordingly
function init() {
    var isCollapsed = $('#settings').hasClass('collapse');
    collapsed(isCollapsed);
}

init();
