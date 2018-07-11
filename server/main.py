#!/usr/bin/env python3

# http://flask.pocoo.org/
from flask import Flask

# http://flask.pocoo.org/docs/1.0/api/#flask.request
from flask import request

# http://flask.pocoo.org/docs/1.0/tutorial/templates/
from flask import render_template
from flask import redirect

from werkzeug.utils import secure_filename

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
import network_setup

# import midi parser
from midi_parser.parse_midi import MIDI_Converter

# import server settings (global variables)
from settings import *


app = Flask(__name__)

TRAINING_THREAD = None

# holds start time in string format
TIMESTAMP_SERVER_START = None

LOGGER = None


def main():

    # get current time for log-files and more in string format
    TIMESTAMP_SERVER_START = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')


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
        LOGGER.warning('Missing path "{}" - creating it.'.format(logPath))
        os.makedirs(logPath)

    logFileName = LOG_FILENAME
    if logFileName is None or logFileName == "":
        logFileName = "log_{}.log"

    # place timestamp
    logFileName = logFileName.format(TIMESTAMP_SERVER_START)


    # configure logging, level=DEBUG => log everything
    logging.basicConfig(filename=logPath+logFileName, level=logging.DEBUG, format=logFormat, datefmt=logDateFormat)

    # get the logger
    global LOGGER
    LOGGER = logging.getLogger('musicnet-webservicelogger')
    LOGGER.addHandler(ch)
    LOGGER.debug('Logger started.')

    ###### logging configuration ######


    app.debug = DEBUG
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.run(threaded=True, host='0.0.0.0', port=PORT)


# injects all the setting variables
# see http://flask.pocoo.org/docs/1.0/templating/#context-processors
@app.context_processor
def inject_settings():
    return dict(SETTINGS)


@app.route("/", methods=["GET", "POST"])
def submit():

    if request.method == "GET":
        return render_template('index.html',
            title=TITLE,
            accept=ACCEPTED_FILE_EXTENSIONS
        )

    if request.method == "POST":

        LOGGER.debug("Got files: {}".format(request.files))
        LOGGER.debug("Got settings: {}".format(request.form))

        if len(request.files) <= 0:
            # TODO: redirect to main page and insert error
            return "No files!"

        #filename = secure_filename(file.filename)
        #file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename)))
        filePaths = validateFiles(request.files.getlist("file"))
        uploaded = len(filePaths)

        LOGGER.info("Files uploaded: {}\n{}".format(uploaded, filePaths))

        if uploaded <= 0:
            # TODO: redirect to main page and insert error
            return "No files!"

        # validate settings
        settings = validateSettings(settings_in=request.form)

        # add filepaths to settings
        settings['filepaths'] = filePaths

        LOGGER.info("Using settings: {}".format(settings))


        # start new thread to train the network
        global TRAINING_THREAD

        if not TRAINING_THREAD is None:
            LOGGER.debug("User tried to start a new training process but am still training...")
            # TODO: nice error website or navigate to training
            return "There is still a training running..\nPlease wait before starting a new one..."

        TRAINING_THREAD = Thread(target=train_network, args=[settings])
        TRAINING_THREAD.start()


        # redirect to training page
        return redirect("./training", code=303)


@app.route("/training", methods=["GET"])
def training():

    return render_template('training.html',
        title=TITLE + " - Training"
    )


@app.route("/training/state", methods=["GET"])
def training_state():

    running = True
    if TRAINING_THREAD is None:
        running = False

    return json.dumps({ 'running': running })


def train_network(args):
    '''
    Function that will run in a separate thread to train the network.
    '''

    global training_thread

    # get settings
    settings = args[0]

    # convert midi files to json
    try:
        filePaths_midi = settings['filepaths']
        filePaths_json = convertFiles(filePaths_midi)
    except Exception as e:
        LOGGER.error("Failed to convert MIDI to JSON! ({})".format(str(e)))
        training_thread = None

    LOGGER.info("Training network...")
    LOGGER.info("- Settings: {}".format(settings))

    #i = 0
    #while i < 99999:
    #    i += 0.001

    # this will start training the network
    #externalSetup(
    #    LOGGER,
    #    filePaths_json,#

    #   )

    LOGGER.info("Training finished!")

    # tell that the thread is done
    training_thread = None


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def validateFiles(files):
    '''
    Validates the uploaded files and returns their paths as a set.
    (Style: filename = path)
    See http://flask.pocoo.org/docs/1.0/patterns/fileuploads/
    '''

    LOGGER.info("Files: {}".format(files))

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
            LOGGER.warning("File invalid: {}".format(file))
            continue

        if allowed_file(file.filename):
            # get a secure filename
            # see here: http://werkzeug.pocoo.org/docs/0.14/utils/#werkzeug.utils.secure_filename
            filename = secure_filename(file.filename)

            # save file to upload folder
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path)
            LOGGER.info("File saved: {}".format(path))

            # save path
            filesOut[filename] = path
        else:
            LOGGER.warning("Filename not allowed: {}".format(file))


    if emptyName > 0:
        LOGGER.warning("Files with empty name: {}".format(emptyName))

    return filesOut


def validateSettings(settings_in):
    '''
    Validates and returns the settings as an array of JSON objects.
    (key=value pairs)
    '''

    settings = []

    for key in SETTINGS['keys']:
        setting = settings_in.getlist(key)

        if len(setting) <= 0:
            return "Missing key {}!".format(key)

        value = 0
        try:
            value = int(setting[0])
        except Exception as e:
            LOGGER.error("Exception converting value! {}".format(str(e)))
            return "Wrong setting format for key {}!".format(key)

        if (value < SETTINGS[key + "_min"] or
            value > SETTINGS[key + "_max"]):
            return "Value for key {} out of bounds!".format(key)

        settings.append({key: value})
        LOGGER.info("Validating key {}={} was successful.".format(key, value))

    return settings


def convertFiles(filePaths_midi):
    '''
    Converts the MIDI files to JSON.
    Returns the paths to the converted JSON files.
    '''

    converter = MIDI_Converter()
    conResult = converter.convertFiles(inputPath=filePaths_midi, outputPath=JSON_FOLDER, logger=LOGGER)

    if conResult['success'] == False:
        raise Exception("Failed to convert midi files!")

    return conResult['data']


if __name__ == '__main__':
    main()
