import pandas
from sklearn import preprocessing


class Preprocessing():
    def __init__(self, path):
        _path = path
        _dataset = None
        print("test")

    def Load(self,_orient = None):
    """ Load Dataset with Pandas into Dataframe"""
        try:
            _dataset = pandas.read_json(_path, orient=_orient)
            print("test")
        except Exception as n:
            print(n)

    def Standardize(self, column = None):
    """ Scale Dataset quick and easy :D"""
        try:
            if column == None:
                _dataset = preprocessing.scale(_dataset)
            else
                _dataset[column] = preprocessing.scale(_dataset[column])
        except Exception as n:
            print("Scaling failed!")
            print(n)
            
    def MinMaxScale(self,column = None):
    """ Scale Dataset between 0 and 1 range"""
        try:
            if column == None:
                min_max_scaler = preprocessing.MinMaxScaler()
                _dataset = min_max_scaler.fit_transform(_dataset)
            else
                min_max_scaler = preprocessing.MinMaxScaler()
                _dataset[column] = min_max_scaler.fit_transform(_dataset[column])
        except Exception as n:
            print("MinMaxScaling failed!")
            print(n)

    def Normalize(self, column = None):
    """ Scaling individual samples to have unit norm"""
        try:
            if column == None:
                _dataset = preprocessing.normalize(_dataset)
            else
                _dataset[column] = preprocessing.normalize(_dataset[column])
        except Exception as n:
            print("Normalize failed!")
            print(n)


    def Binarize(self, column = None):
    """ Feature Binarization, tresholding numerical features 
        to get boolean values"""
        try:
            if column == None:
                _dataset = preprocessing.normalize(_dataset)
            else
                _dataset[column] = preprocessing.binarize(_dataset[column])
        except Exception as n:
            print("Binarize failed!")
            print(n)

    def OneHotEncode(self, column = None):
    """ Encoding Categorical Features with OneHotEncode"""
        try:
            if column == None:
                _onehot = preprocessing.OneHotEncoder()
                _dataset = _onehot.fit_transform(_dataset)
            else
                _onehot = preprocessing.OneHotEncoder()
                _dataset[column] = _onehot.fit_transform(_dataset[column])
        except Exception as n:
            print("OneHotEncode failed!")
            print(n)

        
    def Export(self,_orient = None):
    """Export the Dataframe to Json File with given Orientation"""
        try:
            _dataset.to_json(orient=_orient)
            print("Export succesful!")
        except Exception as n:
            print("Export Failed!")
            print(n)
        
    def PrintHead(self, count = None):
    """ Print the Dataset with the first N Values"""
        return _dataset.head(count)

