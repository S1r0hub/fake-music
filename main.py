import argparse
from midi_parser.parse_midi import MIDI_Converter as MC
import midi_parser.save_to_file as stf
from data_processing.preprocessing2 import Preprocessor
from neural_network.NeuralNetwork import NeuralNetwork
import logging



# which information to write to the file
logLevelFile = logging.DEBUG



def main():

    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-l", "--logfile", required=False, help="Set the path and name of the log file", default="./output/logging/netlog.log")
    parser.add_argument("-j", "--jsonfiles", required=False, help="Folder that holds all the jsonl input data", default="./data/midi-json/country/")
    parser.add_argument("-v", "--verbose", required=False, help="Verbose output", action='store_true')

    args = parser.parse_args()
    log = str(args.logfile)


    # enable verbose output
    logLevel = logging.DEBUG
    if args.verbose:
        print("Verbose terminal output enabled.")
    else:
        print("Verbose terminal output disabled.")
        logLevel = logging.INFO


    # check if paths exist
    stf.checkPath(log)


    ###### logging configuration ######

    # create formatter
    logFormat = '%(asctime)s - [%(levelname)s]: %(message)s'
    logDateFormat = '%m/%d/%Y %I:%M:%S %p'

    formatter = logging.Formatter(fmt=logFormat, datefmt=logDateFormat)

    # create console handler (to log to console as well)
    ch = logging.StreamHandler()
    ch.setLevel(logLevel)
    ch.setFormatter(formatter)

    # configure logging, level=DEBUG => log everything
    logging.basicConfig(filename=log, level=logLevelFile, format=logFormat, datefmt=logDateFormat)

    # get the logger
    logger = logging.getLogger('musicnetlogger')
    logger.addHandler(ch)

    ###### logging configuration ######


    # print setting information
    logger.debug('Logger started.')

    # get preprocessor
    preprocessor = Preprocessor(logger)
    preprocessor.concatFiles(args.jsonfiles)
    logger.debug("Got dataset of length: {}".format(len(preprocessor.getDataset())))

    preprocessor.labelEncode()
    inv = preprocessor.labelEncode(True)
    normds = preprocessor.normalizeDataset()

    logger.info("Classes:\n{}".format(preprocessor.getLabelEncoder().classes_))
    logger.info("Inv:\n{}".format(inv[:100]))
    logger.info("Dataset:\n{}".format(preprocessor.getDataset()[:100]))
    logger.info("Dataset-Normalized:\n{}".format(normds[:100]))
    logger.info("Network Data:\n{}".format(preprocessor.createNetworkData()))
    
    #Create Neural Network
    network = NeuralNetwork()
    network.CreateSequentialModel()
    
    #Add Layers
    network.AddLSTM(_return_sequences = True)
    network.AddDropout(_rate=0.3)
    network.AddLSTM(_units=512,_return_sequences=True)
    network.AddDropout(_rate=0.3)
    network.AddLSTM(_units=256)
    network.AddDenseLayer(_units=256)
    network.AddDropout(_rate=0.3)
    network.AddDenseLayer(_units=)
    network.AddActivation('softmax')
    network.Compile(_loss='categorical_crossentropy',_optimizer='rmsprop')
    
    network.Fit(_x= preprocessor.getNetworkData()["input"], _y=preprocessor.getNetworkData()["output"],
                _epochs = 200, _batch_size=64, _callbacks=network._callbacks)
    
    logger.info("Model Layers: \n[]".format(network._model.summary())


if __name__ == "__main__":
    main()
