#!/usr/bin/env python

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

# for json responses
import json

# for multithreading
from threading import Thread


app = Flask(__name__)

training_thread = None


####################################################

DEBUG = True

TITLE = "Summaery 2018 - Fake Music"
PORT = 8080

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(["midi", "mid"])

# for template (html)
ACCEPTED_FILE_EXTENSIONS = "audio/midi"

SETTINGS = {}
SETTINGS['keys'] = ["notes", "epochs", "sequences"]

SETTINGS['notes_min'] = 10
SETTINGS['notes_max'] = 500
SETTINGS['notes_default'] = 200

SETTINGS['epochs_min'] = 1
SETTINGS['epochs_max'] = 100000
SETTINGS['epochs_default'] = 500

SETTINGS['sequences_min'] = 1
SETTINGS['sequences_max'] = 1000
SETTINGS['sequences_default'] = 100

####################################################


def main():

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

        print("Got files: {}".format(request.files))
        print("Got settings: {}".format(request.form))

        if len(request.files) <= 0:
            # TODO: redirect to main page and insert error
            return "No files!"

        #filename = secure_filename(file.filename)
        #file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename)))
        filePaths = validateFiles(request.files.getlist("file"))
        uploaded = len(filePaths)

        print("Files uploaded: {}\n{}".format(uploaded, filePaths))

        if uploaded <= 0:
            # TODO: redirect to main page and insert error
            return "No files!"

        # validate settings
        settings = validateSettings(settings_in=request.form)

        # print settings and redirect to training page
        print("Using settings: {}".format(settings))


        # start new thread
        global training_thread

        if not training_thread is None:
            print("Still training...")
            # TODO: nice error website or navigate to training
            return "There is still a training running..\nPlease wait before starting a new one..."


        training_thread = Thread(target=train_network, args=[settings])
        training_thread.start()


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
    if training_thread is None:
        running = False

    return json.dumps({ 'running': running })


def train_network(args):
    '''
    Function that will run in a separate thread.
    '''

    settings = args[0]

    print("Training network...")
    print("Settings: {}".format(settings))

    i = 0
    while i < 99999:
        i += 0.001

    print("Training finished!")

    global training_thread
    training_thread = None


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def validateFiles(files):
    '''
    Validates the files and returns their paths as a set.
    (Style: filename = path)
    See http://flask.pocoo.org/docs/1.0/patterns/fileuploads/
    '''

    print("Files: {}".format(files))

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
            print("File invalid: {}".format(file))
            continue

        if allowed_file(file.filename):
            # get a secure filename
            # see here: http://werkzeug.pocoo.org/docs/0.14/utils/#werkzeug.utils.secure_filename
            filename = secure_filename(file.filename)

            # save file to upload folder
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path)
            print("File saved: {}".format(path))

            # save path
            filesOut[filename] = path
        else:
            print("Filename not allowed: {}".format(file))


    if emptyName > 0:
        print("Files with empty name: {}".format(emptyName))

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
            print("Exception converting value! {}".format(str(e)))
            return "Wrong setting format for key {}!".format(key)

        if (value < SETTINGS[key + "_min"] or
            value > SETTINGS[key + "_max"]):
            return "Value for key {} out of bounds!".format(key)

        settings.append({key: value})
        print("Validating key {}={} successful.".format(key, value))

    return settings


if __name__ == '__main__':
    main()
