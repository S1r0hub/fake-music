# -*- coding: utf-8 -*-
"""
Created on Sun May 13 16:33:10 2018

@author: Marcel Himmelreich
"""

import pandas
from keras import layers
from keras import Models
from keras import Sequential
from keras.utils import plot_model

"""
Example Neural Network
model = Sequential()
model.add(Dense(12, input_dim=8, activation='relu'))    INPUT LAYER   12 DIMENSION
model.add(Dense(8, activation='relu'))                  HIDDEN LAYER  8 NEURON
model.add(Dense(8, activation='relu'))                  HIDDEN LAYER  8 NEURON
model.add(Dense(1, activation='sigmoid'))               OUTPUT LAYER  1 NEURON

"""


class NeuralNetwork():
    def __init__(self):
        _model = None
        
    def CreateModel(self,input_data, output_data):
    """ Input and Output Data can be single or multi data (lists)"""
        return Models.Model(inputs=input_data, outputs=output_data)
    
    def CreatSequentialModel(self):
    """ Create Empty Sequential Model, additional Layers are required"""
        try:
            _model = Sequential()
        except Exception as n:
            print("Creating Sequential Model failed")
            print(n)
    
    def AddDenseLayer(self, _units = None,_activation= None, _use_bias=True, 
                      _kernel_initializer='glorot_uniform', _bias_initializer='zeros', 
                      _kernel_regularizer=None, _bias_regularizer=None, _activity_regularizer=None, 
                      _kernel_constraint=None, _bias_constraint=None):
        """ Add Dense Layer to model with parameter"""
        """ Most important parameter:
                Units
                Activation
        """
        try:
            _model.add(layers.Dense(units = _units, activation=_activation, use_bias=_use_bias, 
                      kernel_initializer=_kernel_initializer, bias_initializer=_bias_initializer, 
                      kernel_regularizer=_kernel_regularizer, bias_regularizer=_bias_regularizer, 
                      activity_regularizer=_activity_regularizer, kernel_constraint=_kernel_constraint, 
                      bias_constraint=_bias_constraint))
        except Exception as n:
            print("Add Layer Failed!")
            print(n)
            
    def GetWeights(self):
    """ Return Weights"""
        try:
            return _model.get_weights()
        except Exception as n:
            print(n)
            
    def Fit(self, _x, _y, _batch_size = None, _epochs=1, _verbose=1,):
    """ Fit the given Model"""
        try:
            _model.fit(x=_x ,y=_y,batch_size=_batch_size, epochs=_epochs, verbose=_verbose)
        except Exception as n:
            print("Fit Model Failed!")
            print(n)
            
    def Compile(self, _optimizer = None, _loss = None, _metrics= None):
    """ Compile the given Model"""
        try:
            _model.compile(optimizer = _optimizer, loss= _loss, metrics = _metrics)
        except Exception as n:
            print("Compiling Model Failed!")
            print(n)
            
    def Evaluate(self, _x, _y):
    """ Evaluate the Model"""
        try:
            scores = _model.evaluate(_x,_y)
            return print("\n%s: %.2f%%" % (_model.metrics_names[1], scores[1]*100))
        except Exception as n:
            print("Evaluation Failed!")
            print(n)
            
    def Predict_X_Model(self, _x):
    """ Predict the Model with given Data"""
        try:
            return x_new = _model.predict(_x)
        except Exception as n:
            print("Prediction Failed")
            print(n)
            
    def Predict_Y_Model(self, _x_New):
    """ Predict Proba with given Prediction"""
        try:
            return y_new = _model.predict(_x_New)
        except Exception as n:
            print("Prediction Proba Failed")
            print(n)
            
    def PlotModel(self, filename):
    """ Plot the given Model an create an image"""
        try:
            plot_model(_model, to_file= filename + '.png')
        except Exception as n:
            print("Unable to plot model!")
            print(n)