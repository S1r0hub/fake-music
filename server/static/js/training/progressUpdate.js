// used by progress*.js scripts

function getPercentage(json) {

    if (!json) { return 0; }

    var progress = 0;

    // calculate progress
    if (json.epoch && json.epochs) {
        progress = json.epoch / json.epochs * 100;
        progress = Math.round(progress * 1) / 1; // append 0 for decimals
    }

    return progress;
}


// progress in percentage (0 - 100)
function updateProgressBar(progress) {

    if (!progress) {
        progress = 0;
    }

    // get progress bar
    var progress_div = document.getElementById("training-progress");

    if (!progress_div) {
        console.warn("Missing progress-bar element!");
        return;
    }

    // update progress bar status
    var progress_str = String(progress) + "%";
    progress_div.style.width = progress_str;
    progress_div.setAttribute("aria-valuenow", String(progress));
    progress_div.innerHTML = progress_str;

    if (progress >= 100) {
        progress_div.classList.add("progress-bar-success");
        progress_div.classList.add("progress-bar-striped");
    }
    else {
        progress_div.setAttribute("class", "progress-bar");
    }
}



function updateProgress(json) {

    // get progress
    if (!json.status) { return; }

    var status = document.getElementById("training-status");
    var train_start = document.getElementById("training-start");
    var train_end = document.getElementById("training-end");

    if (json.status == "training") {

        var progress = getPercentage(json);
        updateProgressBar(progress);

        if (train_start) {
            if (json.start) {
                train_start.innerHTML = json.start;
                train_start.parentElement.style.display = "block";
            }
            else {
                train_start.parentElement.style.display = "none";
            }
        }

        if (train_end) {
            if (json.end) {
                train_end.innerHTML = json.end;
                train_end.parentElement.style.display = "block";
            }
            else {
                train_end.parentElement.style.display = "none";
            }
        }
    }
    else {
        updateProgressBar(0);
    }

    if (status) {
        if (json.status) {
            if (json.finished && json.finished == true) {
                status.innerHTML = "finished";
            }
            else {
                status.innerHTML = json.status;
            }
            status.parentElement.style.display = "block";
        }
        else {
            status.parentElement.style.display = "none";
        }
    }
}
