// used by progress*.js scripts
// Requires: loss_graph.js

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
    //progress_div.setAttribute("aria-valuenow", String(progress));
    progress_div.innerHTML = progress_str;

    if (progress >= 100) {
        progress_div.classList.add("progress-bar-success");
        progress_div.classList.add("progress-bar-striped");
    }
    else {
        progress_div.setAttribute("class", "progress-bar");
    }
}


// global variable
var lossgraph = null;

function updateProgress(json) {

    // get progress
    if (!json.status) { return; }

    var status = document.getElementById("training-status");
    var train_start = document.getElementById("training-start");
    var train_end = document.getElementById("training-end");
    var train_result = document.getElementById("training-result");
    var train_remaining = document.getElementById("training-remaining");
    var train_loss = document.getElementById("training-loss");
    var train_epoch = document.getElementById("training-epoch");
    var train_epochs = document.getElementById("training-epochs");
    var train_songs = document.getElementById("training-songs");

    if (json.status == "training") {

        var progress = getPercentage(json);
        updateProgressBar(progress);


        // show training start time
        if (train_start && json.start) {
            train_start.innerHTML = json.start;
            train_start.parentElement.style.display = "block";
        }
        else {
            train_start.parentElement.style.display = "none";
        }


        // show epoch
        if (train_epoch && train_epochs) {
            if (json.epoch && json.epochs) {
                train_epoch.innerHTML = json.epoch;
                train_epochs.innerHTML = json.epochs;
                train_epoch.parentElement.style.display = "block";
            }
            else {
                train_epoch.parentElement.style.display = "none";
            }
        }


        // show song count
        if (train_songs) {
            if (json.songs) {
                train_songs.innerHTML = json.songs;
                train_songs.parentElement.style.display = "block";
            }
            else {
                train_songs.parentElement.style.display = "none";
            }
        }


        // show loss value
        if (train_loss && json.loss && json.loss.current) {
            train_loss.innerHTML = json.loss.current;
            train_loss.parentElement.style.display = "block";

            // show graph
            var train_lossgraph = document.getElementById("loss-graph");
            if (json.loss.all) {
                if (!lossgraph) {
                    lossgraph = new LossGraph(json.loss.all);
                    console.log("Created new loss graph.");
                }
                else {
                    lossgraph.update(json.loss.all);
                }

                // show
                if (train_lossgraph) {
                    train_lossgraph.style.display = "block";
                }
            }
            else if (train_lossgraph) {
                // hide
                train_lossgraph.style.display = "none";
            }
        }
        else {
            train_loss.parentElement.style.display = "none";
        }


        // show remaining time
        if (train_remaining && json.remaining)  {
            var remaining_seconds = Math.round(json.remaining);
            var remaining_time = remaining_seconds + "s";


            var remaining_minutes = remaining_seconds / 60;
            if (remaining_minutes > 1) {
                
                var remaining_minutes_round = Math.floor(remaining_minutes);
                remaining_seconds = Math.round((remaining_minutes - remaining_minutes_round) * 60);
                
                remaining_time = remaining_minutes_round + "m " + remaining_seconds + "s";


                var remaining_hours = remaining_minutes_round / 60;
                if (remaining_hours > 1) {

                    var remaining_hours_round = Math.floor(remaining_hours);
                    remaining_minutes = Math.round((remaining_hours - remaining_hours_round) * 60);
                
                    remaining_time = remaining_hours_round + "h " + remaining_minutes + "m " + remaining_seconds + "s";
                

                    var remaining_days = remaining_hours_round / 24;
                    if (remaining_days > 1) {

                        var remaining_days_round = Math.floor(remaining_days);
                        remaining_hours = Math.round((remaining_days - remaining_days_round) * 24);
                
                        remaining_time = remaining_days_round + "d " + remaining_hours + "h " + remaining_minutes + "m " + remaining_seconds + "s";
                    }
                }
            }

            train_remaining.innerHTML = remaining_time;
            train_remaining.parentElement.style.display = "block";
        }
        else {
            train_remaining.parentElement.style.display = "none";
        }


        // show training end time
        if (train_end && json.end) {
            train_end.innerHTML = json.end;
            train_end.parentElement.style.display = "block";

            // hide remaining time
            if (train_remaining) {
                train_remaining.parentElement.style.display = "none";
            }
        }
        else {
            train_end.parentElement.style.display = "none";
        }
    }
    else {
        updateProgressBar(0);

        if (json.status == "converting") {
            if (train_start && json.start) {
                train_start.innerHTML = json.start;
                train_start.parentElement.style.display = "block";
            }
            else {
                train_start.parentElement.style.display = "none";
            }
        }
    }

    if (status) {
        if (json.status) {
            if (json.finished && json.finished == true) {
                status.innerHTML = "finished";
                if (train_result) {
                    if (json.result) {
                        train_result.setAttribute("href", json.result);

                        // use only the filename if slashes found
                        var resultName = json.result;
                        var resParts = json.result.split("/");
                        if (resParts.length > 0) {
                            resultName = resParts[resParts.length-1];
                        }
                        
                        train_result.innerHTML = resultName;
                        train_result.parentElement.style.display = "block";
                    }
                    else {
                        train_result.parentElement.style.display = "none";
                    }
                }
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



// add event listener for resizing the graph
document.addEventListener("DOMContentLoaded", function() {

    var body = document.querySelector("body");
    body.onresize = function() {
        if (lossgraph) {
            lossgraph.sizeUpdate(body.clientWidth);
        }
    };
});