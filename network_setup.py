import os
#os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

import tensorflow as tf
import numpy as np
import time, datetime
import config as con

from keras.layers import LSTM, Dense, Dropout, Activation, Bidirectional
from data_processing.preprocessing import Preprocessor
from neural_network.NeuralNetwork import NeuralNetwork
from data_processing.postprocessing import Postprocessor
from neural_network.StateCallback import StateCallback

# currently unused
#import plotter as plt
#from midi_parser.parse_midi import MIDI_Converter as MC


#gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.7)
#sess = tf.Session(config=tf.ConfigProto(gpu_options=gpu_options))


def basicSetup(
    logger,
    jsonFilesPath,
    weightsOutPath,
    midiOutPath,
    notes,
    configPath=None,
    weightsInPath=None,
    callbacks=[],
    continue_training=False):
    '''
    This is the basic setup method used by the main.py file.
    - logger
    - configPath: path where to store configuration file
    - jsonFilesPath: where to find json files
    - weightsInPath: where to load weights from
    - weightsOutPath: where to store weight files
    - callbacks: callbacks to be added to the network
    - midiOutPath: where to export final midi
    - notes: how many notes to predict
    - continue_training: if we want to continue training after loading weights

    This method checks if the paths to the folder exist
    so that you don't have to take care of that.

    Returns the path to the predicted notes midi file or None.
    '''

    if logger is None:
        print("Missing logger!")
        return


    # check for correctness and create folder if missing
    midiOutPath = validateFolderPath(midiOutPath, logger)
    configPath = validateFolderPath(configPath, logger)
    weightsOutPath = validateFolderPath(weightsOutPath, logger)


    # initialize default configuration
    config = con.Config()

    # load configuration from file if given
    if configPath:
        print("Loading configuration file...")
        config.loadConfig(configPath)  


    # add additional callbacks
    if callbacks is None:
        callbacks = []

    # a simple callback that will put the current training state in a json file and update it accordingly
    stateCallback = StateCallback(filepath="./state", logger=logger, epochs_total=config._epochs)
    callbacks.append(stateCallback)


    # get preprocessor
    preprocessor = performPreprocessing(logger=logger, jsonFilesPath=jsonFilesPath, config=config)
    if preprocessor is None:
        return


    # get the network
    network = createNetworkLayout(logger=logger, preprocessor=preprocessor, weightsPath=weightsOutPath, config=config, callbacks=callbacks)
    net_fit = False


    # load weights
    if not weightsInPath is None:
        if network.load_weights(weightsInPath):
            logger.info("Weights loaded.")

            # if we want to continue the training
            if continue_training:
                result = fitNetwork(logger=logger, network=network, preprocessor=preprocessor, config=config)
            net_fit = True
        else:
            logger.error("Failed to load weights from file: " + weightsInPath)
    else:
        result = fitNetwork(logger=logger, network=network, preprocessor=preprocessor, config=config)
        net_fit = True
        

    # exit if errors occured
    if result is None:
        net_fit = False
        # for now exit the script
        return


    #Plot History
    #plot = plt.Plotter(result)
    #plot.plotLoss("./data/results/")
    #plot.plotAccuracy("./data/results/")
    
    # save network configuration
    # TODO: when?
    #if configPath:
    #    config.saveConfig(configPath)

    # start prediction
    if net_fit and notes > 0:

        # plot the model
        #network.plotModel("./data/plotted.png")

        # predicting
        predicted_notes = predictNotes(logger, preprocessor, network, notes)
        postprocessor = Postprocessor(logger)
        logger.debug("Predicted notes:\n{}".format(predicted_notes))

        # export the generated notes
        logger.info("Exporting notes...")
        timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H-%M-%S')
        outPath = midiOutPath + "midi_result_{}".format(timestamp)
        postprocessor.export_midi(predicted_notes, outPath)
        outPath += ".mid"
        logger.info("MIDI file exported to: {}".format(outPath))
        return outPath

    if notes > 0:
        logger.warning("Finished without results!")
    else:
        logger.info("Finished without results. (Notes to predict: 0)")

    return None


def externalSetup(
    logger,
    jsonFilesPath,
    weightsOutPath,
    midiOutPath,
    settings,
    callbacks=[],
    configPath=None):
    '''
    This is the method for an external setup (done by another application).
    We are using it for the setup with the web-service.
    External setup doesnt support continuing training.
    - logger
    - jsonFilesPath: where to find json files
    - weightsOutPath: where to store weight files
    - midiOutPath: where to export final midi
    - callbacks: callbacks to be added to the network
    - notes: how many notes to predict
    - settings: a set of key-value pairs
      supported is:
      - notes
      - epochs
      - sequences

    This method checks if the paths to the folder exist
    so that you don't have to take care of that.

    Returns the path to the predicted notes midi file or None.
    '''

    if logger is None:
        print("Missing logger!")
        return


    # initialize default configuration
    config = con.Config()
    notes = 100


    # load configuration if given
    if configPath:
        print("Loading configuration file...")
        config.loadConfig(configPath)  


    # load settings
    logger.info("Loading settings...")
    try:
        if "epochs" in settings:
            config._epochs = int(settings['epochs'])

        if "notes" in settings:
            notes = int(settings['notes'])

        if "sequences" in settings:
            config._sequence_length = int(settings['sequences'])

        if "layout" in settings:
            config._layout = str(settings['layout'])

    except Exception as e:
        logger.error("Failed to apply settings! ({})".format(str(e)))


    # check for correctness and create folder if missing
    logger.info("Validating paths...")
    weightsOutPath = validateFolderPath(weightsOutPath, logger)
    midiOutPath = validateFolderPath(midiOutPath, logger)


    # get preprocessor
    preprocessor = performPreprocessing(logger=logger, jsonFilesPath=jsonFilesPath, config=config, verbose=True)
    if preprocessor is None:
        return


    # get the network
    network = createNetworkLayout(logger=logger, preprocessor=preprocessor, weightsPath=weightsOutPath, config=config, callbacks=callbacks)
    net_fit = True


    # fit network (training)
    result = fitNetwork(logger=logger, network=network, preprocessor=preprocessor, config=config)
    
    if result is None:
        net_fit = False


    # start prediction
    if net_fit and notes > 0:

        # predicting
        logger.info("Predicting notes...")
        predicted_notes = predictNotes(logger, preprocessor, network, notes)
        postprocessor = Postprocessor(logger)

        # export the generated notes
        logger.info("Exporting notes...")
        timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H-%M-%S')
        outPath = midiOutPath + "midi_result_{}".format(timestamp)
        postprocessor.export_midi(predicted_notes, outPath)
        outPath += ".mid"
        logger.info("MIDI file exported to: {}".format(outPath))
        return outPath

    return None


def validateFolderPath(path, logger=None):
    '''
    Checks for correctness and creates folders if missing.
    Returns the valid path.
    '''

    if path is None:
        return None

    if not path.endswith("/"):
        path += "/"

    if not os.path.exists(path):
        if logger:
            logger.info('Missing path "{}" - creating it.'.format(path))
        os.makedirs(path)

    return path


def fitNetwork(logger, network, preprocessor, config):
    logger.info("Fitting model...")
    return network.fit(_x=preprocessor.getNetworkData()["input"], _y=preprocessor.getNetworkData()['output'], _epochs=config._epochs, _batch_size=config._batch_size, _validation_split=config._validation_split)


def performPreprocessing(logger, jsonFilesPath, config, verbose=False):
    '''
    Performs preprocessing and returns the preprocessor.
    '''

    # check for correctness and create folder if missing
    jsonFilesPath = validateFolderPath(jsonFilesPath)


    preprocessor = Preprocessor(logger)
    preprocessor.concatFiles(jsonFilesPath)

    if verbose:
        logger.debug("Preprocessor got dataset of length: {}".format(len(preprocessor.getDataset())))


    if len(preprocessor.getDataset()) <= 0:
        logger.error("Preprocessing failed! (dataset is empty)")
        return None


    preprocessor.labelEncode()
    inv = preprocessor.labelEncode(True, preprocessor.getDataset())
    normds = preprocessor.normalizeDataset()

    # how many notes to predict a new note
    preprocessor.setSequenceLength(config._sequence_length)

    # create sequences (network data) (n-grams..) + one-hot-encoding
    network_data = preprocessor.createNetworkData()

    if verbose:
        logger.debug("Classes:\n{}".format(preprocessor.getLabelEncoder().classes_))
        logger.debug("Inv:\n{}".format(inv[:100]))
        logger.debug("Dataset:\n{}".format(preprocessor.getDataset()[:100]))
        logger.debug("Dataset-Normalized:\n{}".format(normds[:100]))
        logger.debug("Network Data:\n{}".format(network_data))

    return preprocessor


def createNetworkLayout(logger, preprocessor, weightsPath, config, callbacks=[]):
    '''
    Creates the network layout.
    Will validate the weightsPath so you dont have to take care of that.
    Returns the network with the specified layout.
    '''

    # check for correctness and create folder if missing
    weightsPath = validateFolderPath(weightsPath, logger)


    # Create Neural Network
    network = NeuralNetwork()
    network.createSequentialModel()
    
    input_shape = (preprocessor.getNetworkData()['input'].shape[1], preprocessor.getNetworkData()['input'].shape[2])
    vokab_length = len(preprocessor.getLabelEncoder().classes_)


    # Add Layers

    # units = how many nodes a layer should have
    # input_shape = shape of the data it will be training
    layout = config._layout
    
    if layout == 'default':
        network = defaultLayout(network, input_shape)
    elif layout == 'triple':
        network = tripleLSTMlayout(network, input_shape)
    elif layout == 'bidirectional':
        network = bidirectionalLayout(network, input_shape)
    #elif layout == 'attention':
    #    network = attentionLayout(network, input_shape)

    # units of last layer should have same amount of nodes as the number of different outputs that our system has
    # last layers are the same for every layout
    # -> assures that the output of the network will map to our classes
    network.add(Dense(units=vokab_length))
    network.add(Activation(config._activation))
    

    # compile network
    logger.info("Compiling model...")
    network.compile(_loss=config._loss, _path=weightsPath, _optimizer=config._optimizer, _metrics=config._metrics, _callbacks=callbacks)

    logger.info("Finished compiling.")
    logger.info("Model Layers: \n[]".format(network._model.summary()))

    return network

def defaultLayout(network, input_shape):
    network.add(LSTM(units=256, input_shape=input_shape))
    network.add(Dropout(rate=0.3))
    return network
    
def tripleLSTMLayout(network, input_shape):
    network.add(LSTM(units=256, input_shape=input_shape))
    network.add(Dropout(rate=0.3))
    network.add(LSTM(units=512, return_sequences=True))
    network.add(Dropout(rate=0.3))
    network.add(LSTM(units=256))
    network.add(Dense(units=256))
    network.add(Dropout(rate=0.3))
    return network
    
def bidirectionalLayout(network, input_shape):
    network.add(Bidirectional(LSTM(units=256, input_shape=input_shape)))
    network.add(Dropout(rate=0.3))
    return network
    
def attentionLayout(network, input_shape):
    #TODO
    pass

def predictNotes(logger, preprocessor, network, n_notes):
    '''
    Predicts notes and returns them as a list.
    '''

    vokab_length = len(preprocessor.getLabelEncoder().classes_)
    network_input = preprocessor.getNetworkData()['input']
    start = np.random.randint(0, len(network_input) - 1)

    # as many notes as the used sequence length
    pattern = network_input[start]
    output = []

    logger.info("Predicting {} notes...".format(n_notes))

    for i in range(n_notes):

        # reshape to row-vector
        p_input = np.reshape(pattern, (1, len(pattern), 1))

        # normalize input
        p_input = p_input / vokab_length

        # make a prediction
        # (array of predictions for all available classes of label encoding)
        prediction = network._model.predict(p_input, verbose=0)

        # get class index in label encoding / note with the highest probability
        note_index = np.argmax(prediction)
        output.append(note_index)

        # add index to pattern and remove the first entry
        pattern = np.append(pattern, note_index)
        pattern = pattern[1:]

    #logger.info("OUTPUT:\n{}".format(output))

    # get the according notes
    output = preprocessor.labelEncode(invert=True, invert_data=output)

    return output
