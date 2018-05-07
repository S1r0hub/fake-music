# Fake Music

The aim is to let the computer generate **nice** music for us.


<br/>

## Roadmap

- [X] Information Retrieval (Tools, ...)
- [X] Converting Input Data
  - [X] Parse single files
  - [X] Parse all files of a folder
- [ ] Preprocessing (Normalization, ...)
- [ ] **Building a LSTM**
  - [ ] Layer Architecture
  - [ ] Configuration + Optimization
- [ ] Generate Music Data
- [ ] Convert back to Music File Format (MIDI, MP3, ...)


<br/>

## Setup

You can install each dependency manually or just run...
```
pip install -r requirements.txt
```
...in the according folder (for example in [./midi-parser](/midi-parser)).

The manual installation progress is described below.


<br/>

#### Installing [TensorFlow](https://www.tensorflow.org) (Python)

You can simply [install TensorFlow](https://www.tensorflow.org/install/install_linux#install_tensorflow) using pip:
```
pip install tensorflow
```

#### Installing [Keras](https://keras.io/) (Python)

```
pip install keras
```

#### Installing [Music21](http://web.mit.edu/music21/) (Python)

```
pip install music21
```


<br/>

## Features

#### Note

- Duration
- Pitch
- Velocity


<br/>

## Useful Links

- [TensorFlow - RNNs](https://www.tensorflow.org/tutorials/recurrent)
- [Keras](https://keras.io/)
- [Music21](http://web.mit.edu/music21/) - [DOC](http://web.mit.edu/music21/doc/index.html)
- [Generating Music with an LSTM](https://towardsdatascience.com/how-to-generate-music-using-a-lstm-neural-network-in-keras-68786834d4c5?gi=96843f92db52)


<br/>

## More Useful Links

- [FREEMIDI - TOP](https://freemidi.org/topmidi)
- [MIDI - Visualizer 1](https://qiao.github.io/euphony/#15)
- [MIDI - Visualizer 2](https://onlinesequencer.net/import2/923f3ffa04375e7d54cff3b73aa49c1b?title=sweet-home-alabama.mid)
- [C++ Midifile Parser](https://midifile.sapp.org/) - [GIT](https://github.com/craigsapp/midifile)
- [Run C++ Program and get its output (Python)](https://stackoverflow.com/questions/7604621/call-external-program-from-python-and-get-its-output) - [DOCS](https://docs.python.org/3/library/subprocess.html#subprocess.check_output)
- [MIDI-JSON-API](https://github.com/rakannimer/midi-to-json-api/blob/master/index.js)
- [Understanding LSTM Networks](https://colah.github.io/posts/2015-08-Understanding-LSTMs/)


<br/>

## MIDI Specifications

![MIDI SPECS](http://www.cs.uccs.edu/~cs525/midi/midiFileFormat.png)  
`Graphic Source: http://www.cs.uccs.edu/~cs525/midi/midiFileFormat.png`
