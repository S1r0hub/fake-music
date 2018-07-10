#!/usr/bin/env python

import argparse
import logging
import network_setup
import midi_parser.save_to_file as stf


# which information to write to the file
logLevelFile = logging.DEBUG


def main():
    
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    #parser.add_argument("-c", "--convertfiles", required=False, help="Folder that holds all the midi input data", default="./data/midi/country/")
    parser.add_argument("-i", "--input", required=False, help="Path to the folder that holds all the json input data", default="./data/midi-json/country/")
    parser.add_argument("-o", "--output", required=False, help="Where to export result midi files to", default="./data/export/")
    parser.add_argument("-pn", "--predict_notes", required=False, help="Number of notes to predict", type=int, default=0)
    parser.add_argument("-sw", "--storeweights", required=False, help="Path where to store weight files", default="./data/weights/")
    parser.add_argument("-lw", "--loadweights", required=False, help="Path to .hdf5 file that contains weights to load in")
    parser.add_argument("-lc", "--loadconfig", required=False, help="Path to config file that contains processing settings")
    parser.add_argument("-ct", "--continue_training", required=False, help="Continue training model based on loaded weights", action='store_true')
    parser.add_argument("-lf", "--logfile", required=False, help="Set the path and name of the log file", default="./output/logging/netlog.log")
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

    
    # get passed weights path
    weightPath = args.loadweights
    if not weightPath is None and weightPath != "":
        print("Loading weights from: " + weightPath)
    else:
        weightPath = None


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


    # check if notes to predict value is valid
    notes_to_predict = args.predict_notes
    if notes_to_predict < 0:
        logger.error("Number of notes can not be negative!")
        return


    # setup the network and start prediction
    network_setup.basicSetup(
        logger=logger,
        configPath=args.loadconfig,
        jsonFilesPath=args.input,
        midiOutPath=args.output,
        notes=notes_to_predict,
        weightsInPath = weightPath,
        weightsOutPath=args.storeweights,
        stateLogPath="state/",
        continue_training = args.continue_training)


if __name__ == '__main__':
    main()
