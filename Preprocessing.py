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

    def Standardize(self, column = None, new_column=None):
    """ Scale Dataset quick and easy :D"""
        try:
            if column == None:
                _dataset = preprocessing.scale(_dataset)
            else:
                if new_column == None:
                    _dataset[column] = preprocessing.scale(_dataset[column])
                else:
                    _dataset[new_column] = preprocessing.scale(_dataset[column])
        except Exception as n:
            print("Scaling failed!")
            print(n)
            
    def MinMaxScale(self,column = None, new_column=None):
    """ Scale Dataset between 0 and 1 range"""
        try:
            min_max_scaler = preprocessing.MinMaxScaler()
            if column == None:
                _dataset = min_max_scaler.fit_transform(_dataset)
            else:
                if new_column == None:
                    _dataset[column] = min_max_scaler.fit_transform(_dataset[column])
                else:
                    _dataset[new_column] = min_max_scaler.fit_transform(_dataset[column])
        except Exception as n:
            print("MinMaxScaling failed!")
            print(n)

    def Normalize(self, column = None, new_column=None):
    """ Scaling individual samples to have unit norm"""
        try:
            if column == None:
                _dataset = preprocessing.normalize(_dataset)
            else:
                if new_column == None:
                    _dataset[column] = preprocessing.normalize(_dataset[column])
                else:
                    _dataset[new_column] = preprocessing.normalize(_dataset[column])
        except Exception as n:
            print("Normalize failed!")
            print(n)


    def Binarize(self, column = None:
    """ Feature Binarization, tresholding numerical features 
        to get boolean values"""
        try:
            if column == None:
                _dataset = preprocessing.binarize(_dataset)
            else:
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
            else:
                _onehot = preprocessing.OneHotEncoder()
                _dataset[column] = _onehot.fit_transform(_dataset[column])
        except Exception as n:
            print("OneHotEncode failed!")
            print(n)
            
    def LabelEncode(self,column, new_column= None):
    """ LabelEncode Data"""
        try:
            lb = preprocessing.LabelEncoder()
            if new_column != None:
                _dataset[_new_column] = lb.fit_transform(_dataset[column])
            else:
                _dataset[column] = lb.fit_transform(_dataset[column])
        except Exception as n:
            print("Label Encoding failed")
            print(n)

    def RemoveColumn(self, column):
        try:
            _dataset = _dataset.drop(column,1,inplace=True)
        except Exception as n:
            print("Column Remove failed!")
            print(n)
        
    def Export(self,_orient = None):
    """Export the Dataframe to Json File with given Orientation"""
        try:
            _dataset.to_json(orient=_orient)
            print("Export succesful!")
        except Exception as n:
            print("Export Failed!")
            print(n)
            
    def ExportSingleColumn(self, column, _orient=None):
        try:
            _dataset[column].to_json(orient=_orient)
        except Exception as n:
            print("Export Single Column failed")
            print(n)
        
    def PrintHead(self, count = None):
    """ Print the Dataset with the first N Values"""
        return _dataset.head(count)

