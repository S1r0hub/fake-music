#!/usr/bin/env python3

# http://flask.pocoo.org/
from flask import Flask

# http://flask.pocoo.org/docs/1.0/api/#flask.request
from flask import request

# http://flask.pocoo.org/docs/1.0/tutorial/templates/
from flask import render_template
from flask import redirect, Response

from werkzeug.utils import secure_filename
from keras.callbacks import LambdaCallback

# to save files
import os
import logging
from datetime import datetime

# for json responses
import json

# for multithreading
from threading import Thread

# import network setup from parent directory
# so that we can start training a network
import sys

parentPath = os.path.abspath("..")

# add parent path to sys.path for import
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)

# import this module from the parent directory
from network_setup import externalSetup

# import midi parser
from midi_parser.parse_midi import MIDI_Converter

# import server settings (global variables)
from settings import *

# for error handling
# see: https://docs.python.org/dev/library/traceback.html
# we can also use use: https://docs.python.org/2/library/repr.html
import traceback

# for listing the midi files in the result folder
import glob

# use flask-socketio for socket connection
from flask_socketio import SocketIO


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


# TRAINING_STATUS contains:
# - status (converting/training/failure)
# - finished
# - error (if errors occured)
# - epoch
# - epochs (total amount)
TRAINING_STATUS = {}
TRAINING_THREAD = None

# holds start time in string format
TIMESTAMP_SERVER_START = None

# server logger
SVR_LOGGER = None


def main():

    global SVR_LOGGER


    # get current time for log-files and more in string format
    TIMESTAMP_SERVER_START = getTimestampNow()


    ###### logging configuration ######

    # create formatter
    logFormat = '%(asctime)s - [%(levelname)s]: %(message)s'
    logDateFormat = '%m/%d/%Y %I:%M:%S %p'

    formatter = logging.Formatter(fmt=logFormat, datefmt=logDateFormat)

    # create console handler (to log to console as well)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG if DEBUG else logging.INFO)
    ch.setFormatter(formatter)

    # validate log path and filename
    logPath = LOG_FOLDER

    if logPath is None or logPath == "":
        logPath = "./"

    if not logPath.endswith("/"):
        logPath += "/"

    if not os.path.exists(logPath):
        print('[SERVER] Missing path "{}" - creating it.'.format(logPath))
        os.makedirs(logPath)

    logFileName = LOG_FILENAME
    if logFileName is None or logFileName == "":
        logFileName = "log_{}.log"

    # place timestamp
    logFileName = logFileName.format(TIMESTAMP_SERVER_START)


    # configure logging, level=DEBUG => log everything
    logging.basicConfig(filename=logPath+logFileName, level=logging.DEBUG, format=logFormat, datefmt=logDateFormat)

    # get the logger
    SVR_LOGGER = logging.getLogger('musicnet-webservicelogger')
    SVR_LOGGER.addHandler(ch)
    SVR_LOGGER.debug('Logger started.')

    ###### logging configuration ######


    # configure application
    app.debug = DEBUG
    app.jinja_env.trim_blocks = True # disable jinja2 empty lines
    app.jinja_env.lstrip_blocks = True
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    #app.run(threaded=True, host='0.0.0.0', port=PORT)
    socketio.run(app, host='0.0.0.0', port=PORT)


# injects all the setting variables
# see http://flask.pocoo.org/docs/1.0/templating/#context-processors
@app.context_processor
def inject_settings():
    ''' Will inject the SETTINGS dict for the template engine. '''

    return dict(SETTINGS)


@app.route("/", methods=["GET", "POST"])
def submit():
    ''' Serves for the main interface and submit requests. '''

    if request.method == "GET":
        return render_template('index.html',
            title=TITLE,
            accept=ACCEPTED_FILE_EXTENSIONS
        )

    if request.method == "POST":

        SVR_LOGGER.debug("Got files: {}".format(request.files))
        SVR_LOGGER.debug("Got settings: {}".format(request.form))

        if len(request.files) <= 0:
            # TODO: redirect to main page and insert error
            return "No files!"

        #filename = secure_filename(file.filename)
        #file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename)))
        filePaths = validateFiles(request.files.getlist("file"))
        SVR_LOGGER.info("Validated files: {}".format(filePaths))
        uploaded = len(filePaths)

        SVR_LOGGER.info("Files uploaded: {}\n{}".format(uploaded, filePaths))

        if uploaded <= 0:
            # TODO: redirect to main page and insert error
            return "No files!"


        # validate settings
        settings = validateSettings(settings_in=request.form)
        if not isinstance(settings, dict):
            # an error occured
            return "Settings are invalid! ({})".format(settings)

        # get only the paths (not the name which is currently the key)
        filePathsList = []
        for key in filePaths.keys():
            filePathsList.append(filePaths[key])

        # add filepaths to settings
        settings['filepaths'] = filePathsList


        SVR_LOGGER.info("Using settings: {}".format(settings))


        # start new thread to train the network
        global TRAINING_THREAD
        if not TRAINING_THREAD is None:
            SVR_LOGGER.debug("User tried to start a new training process but am still training...")
            # TODO: nice error website or navigate to training
            return "There is still a training running..\nPlease wait before starting a new one..."

        TRAINING_THREAD = Thread(target=train_network, kwargs=dict(settings=settings))
        TRAINING_THREAD.start()


        # redirect to training page
        return redirect("./training", code=303)


@app.route("/training", methods=["GET"])
def training():
    ''' Serves the training interface. '''

    return render_template('training.html',
        title=TITLE + " - Training"
    )


@app.route("/training/status", methods=["GET"])
def training_state():
    ''' Returns the current training status in JSON format. '''

    return jsonResponse(TRAINING_STATUS)


@app.route("/results")
def getResultFilepaths():
    ''' Returns the file names of all midi results as a JSON list. '''

    filePaths = []
    mainKey = "results"

    if not "RESULT_FOLDER" in globals():
        SVR_LOGGER.warning("RESULT_FOLDER variable is not defined!")
        return jsonResponse({mainKey: filePaths})

    # check result folder path
    resultPath = RESULT_FOLDER
    if not resultPath.endswith("/"):
        resultPath += "/"
    if not os.path.exists(resultPath):
        SVR_LOGGER.info("Result path does not exist yet but was requested.")
        return jsonResponse({mainKey: filePaths})

    # get all midi files from this folder and add the paths to the list
    for filepath in glob.glob(resultPath + "*.mid"):
        filePaths.append(filepath)

    return jsonResponse({'results': filePaths})


@socketio.on("message")
def handle_message(message):
    SVR_LOGGER.info("Got a socket message: {}".format(message))


def getTimestampNow():
    ''' Returns a formatted timestamp. '''

    return datetime.now().strftime('%Y-%m-%d_%H-%M-%S')


def jsonResponse(data):
    ''' Returns a JSON response for the given dictionary data. '''

    return Response(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )


def train_network(settings):
    ''' Function that will run in a separate thread to train the network. '''

    global TRAINING_THREAD
    global TRAINING_STATUS

    # set result path to be None
    resultMidiPath = None

    # try to convert midi files to json
    try:
        TRAINING_STATUS = {} # clear everything
        filePaths_midi = settings['filepaths']
        TRAINING_STATUS['status'] = "converting"
        filePath_json = convertMidiFiles(filePaths_midi)
    except Exception as e:
        errmsg = "Failed to convert MIDI to JSON! ({})".format(traceback.format_exc())
        train_network_error(errmsg, SVR_LOGGER)
        return

    try:
        SVR_LOGGER.info("Training network...")
        SVR_LOGGER.info("- Settings:  {}".format(settings))
        SVR_LOGGER.info("- JSON-Path: {}".format(filePath_json))

        # set initial status
        TRAINING_STATUS['status'] = "training"
        TRAINING_STATUS['finished'] = False
        TRAINING_STATUS['epoch'] = 1
        TRAINING_STATUS['epochs'] = settings['epochs']
        TRAINING_STATUS['start'] = getTimestampNow()

        # add additional callbacks for the status updates
        callbacks = []

        # update callback for epochs, +1 because epochs start at 0
        epoch_update_callback = LambdaCallback(
            on_epoch_begin=lambda epoch, logs: updateEpoch(epoch))
        callbacks.append(epoch_update_callback)

        # check that folders exist is done in the setup
        # this will start training the network
        resultMidiPath = externalSetup(
            logger = SVR_LOGGER,
            jsonFilesPath = filePath_json,
            weightsOutPath = WEIGHT_FOLDER.format(getTimestampNow()),
            midiOutPath = RESULT_FOLDER.format(getTimestampNow()),
            settings = settings,
            callbacks = callbacks
        )

        # check if we got results
        if resultMidiPath is None or len(resultMidiPath) == 0:
            # TODO: handle the error by showing error page
            errmsg = "Network delivered no result!"
            train_network_error(errmsg, SVR_LOGGER)

    except Exception as e:

        errmsg = "An unexpected error occured! ({})".format(traceback.format_exc())
        train_network_error(errmsg, SVR_LOGGER)
        return

    # update status
    # for pop() see https://docs.python.org/3/library/stdtypes.html#dict.pop
    SVR_LOGGER.info("Training finished!")
    TRAINING_STATUS['finished'] = True
    TRAINING_STATUS['epoch'] = settings['epochs']
    TRAINING_STATUS['end'] = getTimestampNow()
    TRAINING_STATUS.pop('error', None) # None to prevent KeyError if key not given

    # add path to result
    if not resultMidiPath is None and len(resultMidiPath) > 0:
        TRAINING_STATUS['result'] = resultMidiPath[1:] # remove "."
    else:
        train_network_error("No result.", SVR_LOGGER)
        return

    # tell that the thread is done
    TRAINING_THREAD = None


def train_network_error(errmsg, logger=None):
    ''' Adds an error message to the status and sets the thread to be None. '''

    global TRAINING_STATUS
    global TRAINING_THREAD

    if not logger is None:
        logger.error(errmsg)
    else:
        print(errmsg)

    TRAINING_STATUS = {}
    TRAINING_STATUS['status'] = "failure"
    TRAINING_STATUS['error'] = errmsg
    TRAINING_THREAD = None


def updateEpoch(epoch):
    ''' Will update the key "epoch" of the training status. '''

    global TRAINING_STATUS
    SVR_LOGGER.info("[Epoch-Begin]: {}".format(epoch))
    TRAINING_STATUS['epoch'] = int(epoch) + 1


def allowed_file(filename):
    ''' To validate uploaded files. '''
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def validateFiles(files):
    '''
    Validates the uploaded files and returns their paths as a set.
    (Style: filename = path)
    See http://flask.pocoo.org/docs/1.0/patterns/fileuploads/
    '''

    SVR_LOGGER.info("Files: {}".format(files))

    emptyName = 0
    filesOut = {}

    # http://werkzeug.pocoo.org/docs/0.14/datastructures/#werkzeug.datastructures.FileStorage
    for file in files:

        if file.filename == '':
            emptyName += 1
            continue
            #return redirect(request.url)
            #return "No file selected!"

        if not file:
            SVR_LOGGER.warning("File invalid: {}".format(file))
            continue

        if allowed_file(file.filename):
            # get a secure filename
            # see here: http://werkzeug.pocoo.org/docs/0.14/utils/#werkzeug.utils.secure_filename
            filename = secure_filename(file.filename)

            # save file to upload folder
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path)
            SVR_LOGGER.info("File saved: {}".format(path))

            # save path
            filesOut[filename] = path
        else:
            SVR_LOGGER.warning("Filename not allowed: {}".format(file))

    if emptyName > 0:
        SVR_LOGGER.warning("Files with empty name: {}".format(emptyName))

    return filesOut


def validateSettings(settings_in):
    '''
    Validates and returns the settings as an array of JSON objects.
    (key=value pairs)
    '''

    settings = {}

    for key in SETTINGS['keys']:
        setting = settings_in.getlist(key)

        if len(setting) <= 0:
            return "Missing key {}!".format(key)


        # handle and validate key types
        if key in SETTINGS['radio']:

            value = str(setting[0])
            if not value in SETTINGS[key + "_options"]:
                SVR_LOGGER.error("Invalid option for key {}".format(str(e)))
                return "Invalid option for key {}!".format(key)

        elif key in SETTINGS['checkboxes']:

            value = False
            try:
                value = bool(setting[0])
            except Exception as e:
                SVR_LOGGER.error("Exception converting value! {}".format(str(e)))
                return "Wrong format for key {}! (not bool)".format(key)

        else:

            value = 0
            try:
                valid = False

                try:
                    value = int(setting[0])
                    valid = True
                except Exception as e:
                    #SVR_LOGGER.warning("Value doesnt match int! ({})".format(str(e)))
                    valid = False

                try:
                    value = float(setting[0])
                    valid = True
                except Exception as e:
                    #SVR_LOGGER.warning("Value doesnt match float! ({})".format(str(e)))
                    valid = False

                if valid == False:
                    raise Exception("Value doesn't match type Integer or Float!")

            except Exception as e:
                SVR_LOGGER.error("Exception converting value! {}".format(str(e)))
                return "Wrong setting format for key {}!".format(key)

            if (value < SETTINGS[key + "_min"] or
                value > SETTINGS[key + "_max"]):
                return "Value for key {} out of bounds!".format(key)


        settings[key] = value
        SVR_LOGGER.info("Validating key {}={} was successful.".format(key, value))

    return settings


def convertMidiFiles(filePaths_midi):
    '''
    Converts the MIDI files to JSON.
    Returns the a path to the folder that contains the converted JSON files.
    '''

    # path to save these json files to
    outPath = JSON_FOLDER.format(getTimestampNow())

    converter = MIDI_Converter()
    SVR_LOGGER.info("Converting files...")
    conResult = converter.convertFiles(
        paths=filePaths_midi,
        outputPath=outPath,
        logger=SVR_LOGGER
    )

    if conResult['success'] == False:
        raise Exception("Failed to convert midi files!")

    #return conResult['data'] # list of paths
    return outPath


if __name__ == '__main__':
    main()
