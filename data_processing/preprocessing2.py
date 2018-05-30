import glob
import json
from sklearn import preprocessing


class Preprocessor():

    def __init__(self, logger=None):
        self._logger = logger
        self._dataset = None
        self._dataset_normalized = None
        self._labelencoder = preprocessing.LabelEncoder()
        self._sequence_length = 100


    def getDataset(self):
        return self._dataset


    def getNormalizedDataset(self):
        return self._dataset_normalized


    def getLabelEncoder(self):
        return self._labelencoder


    def setSequenceLength(self, length):
        if (length > 0):
            self._sequence_length = length


    def concatFiles(self, folder_path):
        ''' Concatenate the json files. '''

        output = []
        pitchkey = 'pitch'

        for file in glob.glob(folder_path + "*.jsonl"):
            with open(file, "r") as jsonfile:
                for line in jsonfile:
                    jdata = json.loads(line)
                    if pitchkey in jdata:
                        output.append(jdata[pitchkey])

        self._dataset = output


    def labelEncode(self, invert=False):
        ''' LabelEncode Data '''

        try:
            if invert:
                return self._labelencoder.inverse_transform(self._dataset)
            else:
                self._dataset = self._labelencoder.fit_transform(self._dataset)
        except Exception as n:
            print("Label Encoding failed")
            print(n)


    def normalizeDataset(self):
        ''' Normalize the dataset and store it in the normalized dataset variable. '''

        self._dataset_normalized = self._dataset / float(max(self._dataset))
        return self._dataset_normalized


    def getNetworkData(self):
        ''' Returns the network input and output data. '''

        network_input = []
        network_output = []

        # create input sequences and the corresponding outputs
        for i in range(0, len(self._dataset) - self._sequence_length, 1):
            network_input.append(self._dataset[i:i + self._sequence_length])
            network_output.append(self._dataset[i + self._sequence_length])

        return {
            'input': network_input,
            'output': network_output
        }
