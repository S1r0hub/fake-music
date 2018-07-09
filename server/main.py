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


app = Flask(__name__)


####################################################

DEBUG = True

TITLE = "Summaery 2018 - Fake Music"
PORT = 8080

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(["midi", "mid"])

# for template (html)
ACCEPTED_FILE_EXTENSIONS = "audio/midi"

####################################################


def main():

    app.debug = DEBUG
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.run(host='0.0.0.0', port=PORT)


@app.route("/", methods=["GET", "POST"])
def submit():
    
    if request.method == "GET":
        return render_template('index.html', title=TITLE, accept=ACCEPTED_FILE_EXTENSIONS)

    if request.method == "POST":

        print("Got form files:")
        print(request.files)

        if len(request.files) <= 0:
            # TODO: redirect to main page and insert error
            return "No files!"

        #filename = secure_filename(file.filename)
        #file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename)))
        filePaths = validateFiles(request.files.getlist("file"))
        print("Files uploaded: {}\n{}".format(len(filePaths), filePaths))

        return "POST"


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


if __name__ == '__main__':
    main()
