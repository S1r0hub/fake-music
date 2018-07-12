// Requires MIDIjs to work!
// Get it here: https://github.com/mudcube/MIDI.js

// TODO

/*
MIDI.Player.currentTime = integer; // time we are at now within the song.
MIDI.Player.endTime = integer; // time when song ends.
MIDI.Player.playing = boolean; // are we playing? yes or no.
MIDI.Player.loadFile(file, onsuccess); // load .MIDI from base64 or binary XML request.
MIDI.Player.start(); // start the MIDI track (you can put this in the loadFile callback)
MIDI.Player.resume(); // resume the MIDI track from pause.
MIDI.Player.pause(); // pause the MIDI track.
MIDI.Player.stop(); // stops all audio being played, and resets currentTime to 0.
*/

function loadMidiJS() {
    console.log("Loading MIDIjs plugin..");
    MIDI.loadPlugin({
    soundfontUrl: "soundfont/",
    instrument: "acoustic_grand_piano",
    onsuccess: function() {
    var delay = 0; // play one note every quarter second
    var note = 50; // the MIDI note
    var velocity = 127; // how hard the note hits
    // play the note
    MIDI.setVolume(0, 127);
    //MIDI.noteOn(0, note, velocity, delay);
    //MIDI.noteOff(0, note, delay + 0.75);
    MIDI.Player.loadFile("mysong.mid",MIDI.Player.start);
    }
    });
}


function playMidiFile(file) {
    if (MIDI.Player.playing) {
        stopMidiFile();
    }

    file = file.substring(1); // remove leading dot
    var filepath = 'http://' + document.domain + ':' + location.port + file;
    console.log("Loading MIDI file from " + filepath);
    MIDI.Player.loadFile(filepath, midiFileLoaded);
}


function stopMidiFile() {
    if (MIDI.Player.playing) {
        var timeCur = MIDI.Player.currentTime;
        MIDI.Player.stop();
        console.log("Stopped playing MIDI file at: " + String(timeCur));
    }
    else {
        console.log("There is no MIDI file playing.");
    }
}


function midiFileLoaded() {
    console.log("Playing MIDI file...");
    MIDI.Player.start();
}


document.addEventListener("load", loadMidiJS);
