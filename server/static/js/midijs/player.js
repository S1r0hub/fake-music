// Requires MIDIjs to work!
// Get it here: http://www.midijs.net/

function playMidiFile(file) {
    MIDIjs.stop();

    file = file.substring(1); // remove leading dot
    var filepath = 'http://' + document.domain + ':' + location.port + file;
    console.log("Playing MIDI file from " + filepath);
    MIDIjs.play(filepath);
}

function stopMidiFile() {
    console.log("Stopping MIDI playback.");
    MIDIjs.stop();
}
