import keras
import os
import json


class StateCallback(keras.callbacks.Callback):
    '''
    For more information see:
    https://faroit.github.io/keras-docs/1.1.0/callbacks/#create-a-callback
    '''

    def __init__(self, filepath, epochs_total, filename="state.json", logger=None):

        self.logger = logger
        self.filepath = filepath
        self.filename = filename
        self.settings = {}

        self.settings['training'] = False
        self.settings['epoch'] = 0

        if not epochs_total is None:
            self.settings['epochs'] = epochs_total
        else:
            self.settings['epochs'] = 1

        if filepath is None:
            print("Missing filepath!")
            return

        if not filepath.endswith("/"):
            filepath += "/"

        if not os.path.exists(filepath):
            if logger:
                logger.info('Missing path "{}" - creating it.'.format(filepath))
            os.makedirs(filepath)


    def on_train_begin(self, logs={}):
        if self.logger:
            self.logger.info("[BEGIN]")

        self.settings['training'] = True
        self.write()


    def on_epoch_begin(self, epoch, logs={}):
        if self.logger:
            self.logger.info("[E-BEGIN]: {}".format(epoch))
        
        self.settings['epoch'] = epoch
        self.write()


    def on_epoch_end(self, epoch, logs={}):
        if self.logger:
            self.logger.info("[E-END]: {}".format(epoch))


    def on_train_end(self, logs={}):
        if self.logger:
            self.logger.info("[BEGIN]")

        self.settings['training'] = False
        self.write()


    def write(self):
        ''' Write the current state to the file. '''

        with open(self.filepath + self.filename, "w") as file:
            file.write(json.dumps(self.settings))
