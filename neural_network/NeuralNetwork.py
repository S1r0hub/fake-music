# -*- coding: utf-8 -*-
"""
Created on Sun May 13 16:33:10 2018

@author: Marcel Himmelreich
"""

import pandas
from keras import layers
from keras import models
from keras import losses
from keras.callbacks import ModelCheckpoint
from keras import Sequential
from keras.utils import plot_model


class NeuralNetwork():
    def __init__(self):
        self._model = None
        self._callbacks = []
        
    def createModel(self,input_data, output_data):
        """ Input and Output Data can be single or multi data (lists)"""
        return Models.Model(inputs=input_data, outputs=output_data)
    
    def createSequentialModel(self):
        """ Create Empty Sequential Model, additional Layers are required"""
        try:
            self._model = Sequential()
        except Exception as n:
            print("Creating Sequential Model failed")
            print(n)

    def getCallbacks(self):
        return self._callbacks
    
    def getModel(self):
        return self._model

    def add(self, layer):
        try:
            self._model.add(layer)
        except Exception as e:
            print("Failed to add layer!")
            print(e)
            
    def getWeights(self):
        """ Return Weights"""
        try:
            return _model.get_weights()
        except Exception as n:
            print(n)
            
    def fit(self, _x, _y, _batch_size=None, _epochs=1, _verbose=1, _validation_split=0.2):
        """ Fit the given Model"""
        """
            _x = networkinput
            _y = networkoutput
        """
        try:
            return self._model.fit(x=_x, y=_y, batch_size=_batch_size, epochs=_epochs, verbose=_verbose, callbacks=self._callbacks, validation_split=_validation_split)
            
        except Exception as n:
            print("Fit Model Failed!")
            print(n)
            
    def compile(self, _optimizer = None, _loss = None, _metrics= None):
        """ Compile the given Model"""
        """ Loss Functions:
    
            mean_squared_error
            mean_absolute_error
            mean_absolute_percentage_error
            mean_squared_logarithmic_error
            squared_hinge
            hinge
            categorical_hinge
            logcosh
            
            Optimizers:
              SGD  
              RMSprop
              Adadelta
              Adam
              Adamax
              Nadam
              TFOptimizer
              
           Metrics:
            binary_accuracy
            categorical_accuracy
            sparse_categorical_accuracy
            top_k_categorical_accuracy
            sparse_top_k_categorical_accuracy
        """
        try:
            self._model.compile(optimizer=_optimizer, loss=_loss, metrics=_metrics)

            # TODO: make path changable
            filepath = "./data/weights/weights-improvement-{epoch:02d}-{loss:.4f}-bigger.hdf5"

            checkpoint = ModelCheckpoint(
                filepath,
                monitor='loss',
                verbose=0,
                save_best_only=True,
                mode='min'
            )

            self._callbacks.append(checkpoint)

        except Exception as n:
            print("Compiling Model Failed!")
            print(n)
            
    def evaluate(self, _x, _y,_batch_size=None, _verbose=1, _sample_weight=None, _steps=None):
        """ Evaluate the Model"""
        try:
            scores = self._model.evaluate(_x,_y,batch_size=_batch_size, 
                                          verbose=_verbose, sample_weight=_sample_weight, steps=_steps)
            return "\n%s: %.2f%%".format(_model.metrics_names[1], scores[1]*100)
        except Exception as n:
            print("Evaluation Failed!")
            print(n)
            
    def predict_Model(self, _x,_batch_size=None, _verbose=0, _steps=None):
        """ Predict the Model with given Data"""
        try:
            x_new = self._model.predict(x=_x,batch_size=_batch_size,verbose=_verbose,steps=_steps)
            return x_new
        except Exception as n:
            print("Prediction Failed")
            print(n)
            
    def plotModel(self, filename):
        """ Plot the given Model an create an image"""
        try:
            return plot_model(self._model, to_file=filename)
        except Exception as n:
            print("Unable to plot model!")
            print(n)

    def load_weights(self, path):
        '''
        Try to load weights from file.
        Returns True if successful or False otherwise.
        '''

        try:
            self._model.load_weights(path)
            return True
        except Exception as e:
            print("Failed to load weights from path: " + path)
            print(e)
            return False


"""

## Example Neural Network

model = Sequential()
model.add(Dense(12, input_dim=8, activation='relu'))    INPUT LAYER   12 DIMENSION
model.add(Dense(8, activation='relu'))                  HIDDEN LAYER  8 NEURON
model.add(Dense(8, activation='relu'))                  HIDDEN LAYER  8 NEURON
model.add(Dense(1, activation='sigmoid'))               OUTPUT LAYER  1 NEURON



## Long Short-Term Memory layer - Hochreiter 1997

units: Positive integer, dimensionality of the output space.
activation: Activation function to use (see activations).
Default: hyperbolic tangent (tanh). If you pass None, no activation is applied (ie. "linear" activation: a(x) = x).
recurrent_activation: Activation function to use for the recurrent step (see activations).
Default: hard sigmoid (hard_sigmoid). If you pass None, no activation is applied (ie. "linear" activation: a(x) = x).
use_bias: Boolean, whether the layer uses a bias vector.
kernel_initializer: Initializer for the kernel weights matrix, used for the linear transformation of the inputs. (see initializers).
recurrent_initializer: Initializer for the recurrent_kernel weights matrix, used for the linear transformation of the recurrent state. (see initializers).
bias_initializer: Initializer for the bias vector (see initializers).
unit_forget_bias: Boolean. If True, add 1 to the bias of the forget gate at initialization. Setting it to true will also force bias_initializer="zeros". This is recommended in Jozefowicz et al.
kernel_regularizer: Regularizer function applied to the kernel weights matrix (see regularizer).
recurrent_regularizer: Regularizer function applied to the recurrent_kernel weights matrix (see regularizer).
bias_regularizer: Regularizer function applied to the bias vector (see regularizer).
activity_regularizer: Regularizer function applied to the output of the layer (its "activation"). (see regularizer).
kernel_constraint: Constraint function applied to the kernel weights matrix (see constraints).
recurrent_constraint: Constraint function applied to the recurrent_kernel weights matrix (see constraints).
bias_constraint: Constraint function applied to the bias vector (see constraints).
dropout: Float between 0 and 1. Fraction of the units to drop for the linear transformation of the inputs.
recurrent_dropout: Float between 0 and 1. Fraction of the units to drop for the linear transformation of the recurrent state.
implementation: Implementation mode, either 1 or 2. Mode 1 will structure its operations as a larger number of smaller dot products and additions, whereas mode 2 will batch them into fewer, larger operations. These modes will have different performance profiles on different hardware and for different applications.
return_sequences: Boolean. Whether to return the last output in the output sequence, or the full sequence.
return_state: Boolean. Whether to return the last state in addition to the output.
go_backwards: Boolean (default False). If True, process the input sequence backwards and return the reversed sequence.
stateful: Boolean (default False). If True, the last state for each sample at index i in a batch will be used as initial state for the sample of index i in the following batch.
unroll: Boolean (default False). If True, the network will be unrolled, else a symbolic loop will be used. Unrolling can speed-up a RNN, although it tends to be more memory-intensive. Unrolling is only suitable for short sequences.



## Neural Network Information:        

Usage of initializers
Initializations define the way to set the initial random weights of Keras layers.

The keyword arguments used for passing initializers to layers will depend on the layer. 
Usually it is simply kernel_initializer and bias_initializer

https://keras.io/initializers/

"""
