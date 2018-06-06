# -*- coding: utf-8 -*-
"""
Created on Sun May 13 16:33:10 2018

@author: Marcel Himmelreich
"""

import pandas
from keras import layers
from keras import Models
from keras import losses
from keras import callbacks
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
        self._model = None
        self._callbacks = None
        
    def CreateModel(self,input_data, output_data):
        """ Input and Output Data can be single or multi data (lists)"""
        return Models.Model(inputs=input_data, outputs=output_data)
    
    def CreateSequentialModel(self):
        """ Create Empty Sequential Model, additional Layers are required"""
        try:
            self._model = Sequential()
        except Exception as n:
            print("Creating Sequential Model failed")
            print(n)
    
    def AddLSTM(self,_input_shape= None,_units, _activation='tanh', _recurrent_activation='hard_sigmoid', 
                _use_bias=True, _kernel_initializer='glorot_uniform', 
                _recurrent_initializer='orthogonal', bias_initializer='zeros', 
                _unit_forget_bias=True, _kernel_regularizer=None, 
                _recurrent_regularizer=None, _bias_regularizer=None, 
                _activity_regularizer=None, _kernel_constraint=None, 
                _recurrent_constraint=None, _bias_constraint=None, 
                _dropout=0.0, _recurrent_dropout=0.0, _implementation=1, 
                _return_sequences=False, _return_state=False, _go_backwards=False, 
                _stateful=False, _unroll=False):
        """
            Long Short-Term Memory layer - Hochreiter 1997
    
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
        """
        try:
            self._model.add(layers.LSTM(units=_units,_input_shape= None,input_shape=_input_shape, activation=_activation, recurrent_activation=_recurrent_activation, 
                use_bias=_use_bias, kernel_initializer=_kernel_initializer, 
                recurrent_initializer=_recurrent_initializer, bias_initializer=_bias_initializer, 
                unit_forget_bias=_unit_forget_bias, kernel_regularizer=_kernel_regularizer, 
                recurrent_regularizer=_recurrent_regularizer, bias_regularizer=_bias_regularizer, 
                activity_regularizer=_activity_regularizer, kernel_constraint=_kernel_constraint, 
                recurrent_constraint=_recurrent_constraint, bias_constraint=_bias_constraint, 
                dropout=_dropout, recurrent_dropout=_recurrent_dropout, implementation=_implementation, 
                return_sequences=_return_sequences, return_state=_return_state, go_backwards=_go_backwards, 
                stateful=_stateful, unroll=_unroll))
        except Exceptions as n:
            print("Add LSTM Layer failed")
            print(n)
    
    def AddDropout(self,_rate, _noise_shape=None, _seed=None):
        """Applies Dropout to the input"""
        try:
            self._model.add(layers.Dropout(rate=_rate,input_shape=_input_shape, noise_shape=_noise_shape, 
                                      seed=_seed))
        except Exception as n:
            print("Add Dropout Layer failed")
            print(n)
            
    def AddActivation(self,_activation):
        """Applies an activation function to an output """
        """Activation Arguments:
            softmax
            softplus
            softsign
            elu
            selu
            relu
            tanh
            sigmoid
            hard_sigmoid
            linear
        """
        try:
            self._model.add(layers.Activation(_activation))
        except Exception as n:
            print("Add Activation Layer failed")
            print(n)
        
    def AddRNN(self,_cell,_input_shape= None, _return_sequences=False, _return_state=False, 
               _go_backwards=False, _stateful=False, _unroll=False):
        """ Base class for recurrent layers"""
        try:
            self._model.add(layers.RNN(cell = _cell,input_shape=_input_shape, return_sequences=_return_sequences, 
                                  return_state= _return_state, go_backwards=_go_backwards, 
                                  stateful=_stateful, unroll=_unroll))
        except Exception as n:
            print("Add RNN Layer failed")
            print(n)
    
    def AddDenseLayer(self, _units = None,_input_shape= None,_activation= None, _use_bias=True, 
                      _kernel_initializer='glorot_uniform', _bias_initializer='zeros', 
                      _kernel_regularizer=None, _bias_regularizer=None, _activity_regularizer=None, 
                      _kernel_constraint=None, _bias_constraint=None):
        """ Add Dense Layer to model with parameter"""
        """ Most important parameter:
                Units
                Activation
        """
        try:
            self._model.add(layers.Dense(units = _units,input_shape=_input_shape, activation=_activation, use_bias=_use_bias, 
              kernel_initializer=_kernel_initializer, bias_initializer=_bias_initializer, 
              kernel_regularizer=_kernel_regularizer, bias_regularizer=_bias_regularizer, 
              activity_regularizer=_activity_regularizer, kernel_constraint=_kernel_constraint, 
              bias_constraint=_bias_constraint))
        except Exception as n:
            print("Add Dense Layer Failed!")
            print(n)
            
    def GetWeights(self):
        """ Return Weights"""
        try:
            return _model.get_weights()
        except Exception as n:
            print(n)
            
    def Fit(self, _x, _y, _batch_size = None, _epochs=1, _verbose=1,_callbacks = None):
        """ Fit the given Model"""
        """
            _x = networkinput
            _y = networkoutput
        """
        try:
            self._model.fit(x=_x ,y=_y,batch_size=_batch_size, epochs=_epochs, verbose=_verbose, callbacks=_callbacks)
        except Exception as n:
            print("Fit Model Failed!")
            print(n)
            
    def Compile(self, _optimizer = None, _loss = None, _metrics= None):
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
            self._model.compile(optimizer = _optimizer, loss= _loss, metrics = _metrics)
            filepath = "weights-improvement-{epoch:02d}-{loss:.4f}-bigger.hdf5"
            self._callbacks = callbacks.ModelCheckpoint(filepath, monitor='loss', 
                                                        verbose=0, save_best_only=True, mode='min')
        except Exception as n:
            print("Compiling Model Failed!")
            print(n)
            
    def Evaluate(self, _x, _y,_batch_size=None, _verbose=1, _sample_weight=None, _steps=None):
        """ Evaluate the Model"""
        try:
            scores = self._model.evaluate(_x,_y,batch_size=_batch_size, 
                                          verbose=_verbose, sample_weight=_sample_weight, steps=_steps)
            return print("\n%s: %.2f%%" % (_model.metrics_names[1], scores[1]*100))
        except Exception as n:
            print("Evaluation Failed!")
            print(n)
            
    def Predict_Model(self, _x,_batch_size=None, _verbose=0, _steps=None):
        """ Predict the Model with given Data"""
        try:
            x_new = self._model.predict(x=_x,batch_size=_batch_size,verbose=_verbose,steps=_steps)
            return x_new
        except Exception as n:
            print("Prediction Failed")
            print(n)
            
    def PlotModel(self, filename):
        """ Plot the given Model an create an image"""
        try:
            return plot_model(self._model, to_file= filename + '.png')
        except Exception as n:
            print("Unable to plot model!")
            print(n)



""" Neural Network Information"""          

"""
Usage of initializers
Initializations define the way to set the initial random weights of Keras layers.

The keyword arguments used for passing initializers to layers will depend on the layer. 
Usually it is simply kernel_initializer and bias_initializer

https://keras.io/initializers/
"""
