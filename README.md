# Fake Music

The aim is to let the computer generate **nice** music for us.


<br/>

## Roadmap

- [X] Information Retrieval (Tools, ...)
- [X] Converting Input Data
  - [X] Parse single files
  - [X] Parse all files of a folder
- [X] Preprocessing
  - [X] Normalization, One-Hot Encoding, ...
  - [X] Save label encoding
  - [X] Prepare input/output data
  - [X] Reshape input data
- [X] Neural Network
  - [X] Create Layers
  - [X] Fit Model
  - [X] Compile Model
  - [X] Predict Model
  - [X] Plot Model
- [ ] **Building a LSTM**
  - [ ] Layer Architecture
  - [ ] Callbacks (Keras ModelCheckpoints)
  - [ ] Configuration + Optimization
- [ ] Generate Music Data
  - [ ] Model prediction
  - [ ] Decoding predicted results
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

#### Installing [Keras](https://keras.io/) (Python)

```
pip install keras
```

#### Installing [Music21](http://web.mit.edu/music21/) (Python)

```
pip install music21
```

#### Installing [Pandas](https://pandas.pydata.org/) (Python)

```
pip install pandas
```

#### Installing [Scikit](http://scikit-learn.org/stable/index.html) (Python)

```
pip install scikit-learn
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
- [Table of Pitch Notations](https://en.wikipedia.org/wiki/Musical_note#Note_designation_in_accordance_with_octave_name)
- [One-Hot Encoding Explained](https://machinelearningmastery.com/why-one-hot-encode-data-in-machine-learning/)


<br/>

## More Useful Links

- [FREEMIDI - TOP](https://freemidi.org/topmidi)
- [MIDI - Visualizer 1](https://qiao.github.io/euphony/#15)
- [MIDI - Visualizer 2](https://onlinesequencer.net/import2/923f3ffa04375e7d54cff3b73aa49c1b?title=sweet-home-alabama.mid)
- [C++ Midifile Parser](https://midifile.sapp.org/) - [GIT](https://github.com/craigsapp/midifile)
- [Run C++ Program and get its output (Python)](https://stackoverflow.com/questions/7604621/call-external-program-from-python-and-get-its-output) - [DOCS](https://docs.python.org/3/library/subprocess.html#subprocess.check_output)
- [MIDI-JSON-API](https://github.com/rakannimer/midi-to-json-api/blob/master/index.js)
- [Understanding LSTM Networks](https://colah.github.io/posts/2015-08-Understanding-LSTMs/)
- [Keras NP_UTILS](https://github.com/keras-team/keras/blob/master/keras/utils/np_utils.py)


<br/>

## API Doumentation

- [Scikit - Preprocessing](http://scikit-learn.org/stable/modules/preprocessing.html#preprocessing)
- [Keras - Layers](https://keras.io/layers/about-keras-layers/)
- [Pandas - Indexing and Selecting Data](https://pandas-docs.github.io/pandas-docs-travis/indexing.html)


<br/>

## MIDI Specifications

![MIDI SPECS](http://www.cs.uccs.edu/~cs525/midi/midiFileFormat.png)  
> Graphic Source: http://www.cs.uccs.edu/~cs525/midi/midiFileFormat.png
