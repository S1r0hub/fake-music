import glob
import json
import numpy as np
from sklearn import preprocessing
from keras.utils import np_utils


class Preprocessor():

    def __init__(self, logger=None):
        self._logger = logger
        self._dataset = None
        self._dataset_normalized = None
        self._labelencoder = preprocessing.LabelEncoder()
        self._sequence_length = 100
        self._network_data = None


    def getDataset(self):
        return self._dataset


    def getNormalizedDataset(self):
        return self._dataset_normalized


    def getLabelEncoder(self):
        return self._labelencoder


    def getNetworkData(self):
        return self._network_data


    def setSequenceLength(self, length):
        if (length > 0):
            self._sequence_length = length


    def reduceDecimal(self, number, decimals=1):
        return round(number, decimals)


    def concatFiles(self, folder_path):
        ''' Concatenate the json files. '''

        output = []
        pitch_key = 'pitch'
        duration_key = 'duration'
        duration_default = 1
        offset_key = 'offset'
        offset_default = 0.5

        for file in glob.glob(folder_path + "*.jsonl"):
            with open(file, "r") as jsonfile:
                prev_offset = None

                for index, item in enumerate(jsonfile):
                    jdata = json.loads(item)

                    duration = duration_default
                    offset = offset_default

                    # check if we got a note in our dataset
                    if not pitch_key in jdata:
                        self.logger.warning("Missing key {} in data! (file: {}) Skipping.".format(pitch_key, file))
                        continue

                    if duration_key in jdata:
                        duration = jdata[duration_key]

                    if offset_key in jdata:
                        offset = jdata[offset_key]

                    # if we are not in the first iteration (previous offset available)
                    # calculate the offset difference
                    if index > 0:
                        offset = offset-prev_offset

                    # cut of to many decimals to speed up training
                    duration = self.reduceDecimal(duration)
                    offset = self.reduceDecimal(offset)

                    # get the pitch of the note or pitch list for chords
                    pitch = jdata[pitch_key]

                    # check if we got a chord
                    if isinstance(jdata[pitch_key], list):
                        connection = "/"
                        pitch = connection.join(pitch)

                    # concatenate the data
                    output.append(pitch + "_" + str(duration) + "_" + str(offset))

                    # store previous offset for next iteration
                    prev_offset = jdata[offset_key]

        self._dataset = output


    def labelEncode(self, invert=False, invert_data=None):
        ''' Label Encode Data '''

        try:
            if invert:
                return self._labelencoder.inverse_transform(invert_data)
            else:
                self._dataset = self._labelencoder.fit_transform(self._dataset)
        except Exception as n:
            print("Label Encoding failed")
            print(n)


    def normalizeDataset(self):
        ''' Normalize the dataset and store it in the normalized dataset variable. '''

        self._dataset_normalized = self._dataset / float(max(self._dataset))
        return self._dataset_normalized


    def createNetworkData(self):
        ''' Returns the network input and output data. '''
        ''' Input is normalized and Output is One-Hot Encoded. '''

        network_input = []
        network_output = []

        dataset = self._dataset_normalized
        if self._dataset_normalized is None:
            dataset = self._dataset

        # create input sequences and the corresponding outputs
        for i in range(0, len(dataset) - self._sequence_length, 1):
            network_input.append(dataset[i:i + self._sequence_length])
            network_output.append(self._dataset[i + self._sequence_length])

        self._network_data = {
            'input': np.reshape(network_input, (len(network_input), self._sequence_length, 1)),
            'output': np_utils.to_categorical(network_output)
        }

        return self._network_data
