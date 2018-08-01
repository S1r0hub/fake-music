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
- [X] **Building a LSTM**
  - [X] Layer Architecture
  - [X] Callbacks (Keras ModelCheckpoints)
  - [X] Configuration
  - [X] Prediction
- [X] Generate Music Data
  - [X] Model prediction
  - [X] Decoding predicted results
  - [X] Convert back to Music File Format (MIDI, MP3, ...)
- [ ] Optimization
  - [ ] Use only a single instrument
  - [X] Add chords
  - [X] Add duration
  - [X] Add offset
  - [ ] LSTM optimization
  - [X] Converting midi to mp3 and export
  - [X] JSON file to load all the settings from


<br/>

## Getting Started

First of all, make sure you have all the dependencies installed (see [Setup](#setup)).  
Once you completed this step, you should be able to run the [main.py](./main.py) file with `Python 3`.  

There are default folder structures set. You can see them running:
```
python3 main.py -h
```

The help section also shows you possible configurations.  
To change `batch size` or similar attributes, you currently have to edit the [config.py](./config.py) file accordingly.  

**There is an easy way to test this software!**  
We implemented a web application that provides a simple interface and allows you to test this software  
without having to write lots of console commands.  
To use it, just make sure that the [main.py](./server/main.py) of the [server](./server/) can be executed  
by installing possible missing dependencies.  
You can find a [README](./server/README.md) in the server folder.  
Once started, the interface will be accessible at:
```
localhost:8080/
```


<br/>

## Setup

One requirement is that you have [Python 3](https://www.python.org/downloads/release/python-352/) installed.  
This code is based on it.

You can install each python dependency manually or just run...
```
pip install -r requirements.txt
```
...in the according folder (for example in [./midi-parser](/midi-parser)).

The manual installation progress is described below.


<br/>

### Manual Installation

#### Installing [Keras](https://keras.io/)

```
pip install keras
```

#### Installing [Music21](http://web.mit.edu/music21/)

```
pip install music21
```

#### Installing [Scikit](http://scikit-learn.org/stable/index.html)

```
pip install scikit-learn
pip install sklearn
```

#### Installing [Flask](http://flask.pocoo.org/)

```
pip install flask
pip install flask-socketio
```

#### Installing [Tensorflow-GPU](https://pypi.org/project/tensorflow-gpu/) (v 1.8.0)

```
pip install tensorflow-gpu
```

#### Installing [Matplotlib](https://matplotlib.org/)

```
pip install matplotlib
```

If you just want to run the software without GPU-support, just install `tensorflow`.  
This dependency may already be installed by keras.

If you have trouble executing the software (**libcublas error** or similar),
make sure you have the [NVIDIA CUDA TOOLKIT](https://developer.nvidia.com/cuda-downloads)  
as well as the correct [NVIDIA CUDNN](https://developer.nvidia.com/cudnn) version installed on your system.  

If things still dont work, have a look at the [error section](#known-problems).


<br/>

## Features

#### Note

For training, we use the following information:  
- Duration
- Pitch
- Offset

#### Web-Service

We currently work on integrating a web service that will provide a simple interface.  
This interface allows to upload a single or multiple midi files and change network settings.  
After the configuration, the user will have the option to submit this data to the server.  
It will then start a training process in a new thread and show the results.

The files as well as the README are located in the [server](./server/) folder.


<br/>

## Useful Links

- [TensorFlow - RNNs](https://www.tensorflow.org/tutorials/recurrent)
- [TensorFlow GPU Installation](http://www.python36.com/install-tensorflow-using-official-pip-pacakage/)
- [Keras](https://keras.io/)
- [Music21](http://web.mit.edu/music21/) - [DOC](http://web.mit.edu/music21/doc/index.html)
- [Generating Music with an LSTM](https://towardsdatascience.com/how-to-generate-music-using-a-lstm-neural-network-in-keras-68786834d4c5?gi=96843f92db52)
- [Table of Pitch Notations](https://en.wikipedia.org/wiki/Musical_note#Note_designation_in_accordance_with_octave_name)
- [One-Hot Encoding Explained](https://machinelearningmastery.com/why-one-hot-encode-data-in-machine-learning/)
- [Introduction to Cross-Entropy Loss](https://rdipietro.github.io/friendly-intro-to-cross-entropy-loss/)
- [RMSProp Optimizer](https://stackoverflow.com/a/41308962)
- [Neural Networks FAQs](http://www.faqs.org/faqs/ai-faq/neural-nets/part2/)
- [Deep Learning Glossary](https://deeplearning4j.org/glossary) (Iterations vs Epochs...)
- [MIDI File Format](https://www.csie.ntu.edu.tw/~r92092/ref/midi/) and [MIDI File Format Specification](https://github.com/colxi/midi-parser-js/wiki/MIDI-File-Format-Specifications) and [MIDI Format](http://www.larsrichter-online.de/lmids/midformat.htm)
- [Bidirectional Usage](https://www.quora.com/When-should-one-use-bidirectional-LSTM-as-opposed-to-normal-LSTM)


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
- [MIDI File Time Division](http://www.recordingblogs.com/wiki/time-division-of-a-midi-file)
- [MIDI Event List](http://www.onicos.com/staff/iz/formats/midi-event.html)
- [Attention Mechanism](https://machinelearningmastery.com/attention-long-short-term-memory-recurrent-neural-networks/)
- [Bidirectional Wrapper](https://keras.io/layers/wrappers/)
- [Optimizer Comparison](https://towardsdatascience.com/types-of-optimization-algorithms-used-in-neural-networks-and-ways-to-optimize-gradient-95ae5d39529f)


<br/>

## Known Problems

#### Fix [Cuda Problem](https://stackoverflow.com/questions/42013316/after-building-tensorflow-from-source-seeing-libcudart-so-and-libcudnn-errors) (Linux)
Type in terminal before executing the program

```
export PATH=/usr/local/cuda/bin${PATH:+:${PATH}}
export LD_LIBRARY_PATH=/usr/local/cuda/lib64${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
```

If you have trouble finding the correct versions, [see here](https://stackoverflow.com/questions/48575900/how-to-install-tensorflow-gpu-with-cuda8-0).  
For example: tensorflow-gpu-1.4.1 uses CUDA-8.0 and CUDNN-6.0


<br/>

## API Documentation

- [Scikit - Preprocessing](http://scikit-learn.org/stable/modules/preprocessing.html#preprocessing)
- [Keras - Layers](https://keras.io/layers/about-keras-layers/)
- [Pandas - Indexing and Selecting Data](https://pandas-docs.github.io/pandas-docs-travis/indexing.html)


<br/>

## MIDI Specifications

![MIDI SPECS](http://www.cs.uccs.edu/~cs525/midi/midiFileFormat.png)  
> Graphic Source: http://www.cs.uccs.edu/~cs525/midi/midiFileFormat.png
