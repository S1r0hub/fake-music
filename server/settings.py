####################################################
# SERVER SETTINGS
####################################################

DEBUG = True

TITLE = "Summaery 2018 - Fake Music"
PORT = 8080

LOG_FOLDER = "./logs"

# {} is a placeholder for the timestamp
# you can also remove {} to always use the same file
LOG_FILENAME = "log_{}.log"

# output paths
# optional: add "{}" to the path for timestamp
JSON_FOLDER = "./converted/{}"
WEIGHT_FOLDER = "./weights/{}"
RESULT_FOLDER = "./static/midi"

# for file uploads
UPLOAD_FOLDER = "./uploads"
ALLOWED_EXTENSIONS = set(["midi", "mid"])

# for template (html) form
ACCEPTED_FILE_EXTENSIONS = "audio/midi"

SETTINGS = {}

SETTINGS['keys'] = [
    "notes",
    "epochs",
    "sequences",
    "layout"
]

SETTINGS['notes_min'] = 10
SETTINGS['notes_max'] = 500
SETTINGS['notes_default'] = 200

SETTINGS['epochs_min'] = 1
SETTINGS['epochs_max'] = 100000
SETTINGS['epochs_default'] = 500

SETTINGS['sequences_min'] = 1
SETTINGS['sequences_max'] = 1000
SETTINGS['sequences_default'] = 100
SETTINGS['validation'] = ["Yes","No"]
SETTINGS['validation_rate'] = 0.2 

# TODO: add "attention"
SETTINGS['layout_options'] = [
    "default",
    "triple",
    "bidirectional"
]
SETTINGS['layout'] = "default"


# Add keys where a selection is included here.
# For these, there must be the selection provided
# by the key "<selectionname>_options"!
SETTINGS['selections'] = [
    "layout"
]

####################################################
