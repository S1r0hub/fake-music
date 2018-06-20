# -*- coding: utf-8 -*-
"""
Created on Thu Jun 14 21:00:54 2018

@author: Marcel Himmelreich
"""

import datetime
import matplotlib.pyplot as plt
from keras.callbacks import History 
history = History()

class Plotter():
    def __init__(self, _network):
        self._network = _network
        print(self._network.history)
        
    def plotAccuracy(self, filepath):
        try:
            plt.plot(self._network.history['acc'])
            plt.plot(self._network.history['val_acc'])
            plt.title('model accuracy')
            plt.ylabel('accuracy')
            plt.xlabel('epoch')
            plt.legend(['train', 'test'], loc='upper left')
            plt.show()
            now = datetime.datetime.now()
            filename = filepath + "model_accuracy_"+now.month+"_"+now.year
            plt.savefig(filename + ".png")
        except Exception as e:
            print("Failed to plot accuracy/epoch plot")
            print(e)
            
    def plotLoss(self, filepath):
        try:
            plt.plot(self._network.history['loss'])
            plt.plot(self._network.history['val_loss'])
            plt.title('model loss')
            plt.ylabel('loss')
            plt.xlabel('epoch')
            plt.legend(['train', 'test'], loc='upper left')
            plt.show()
            now = datetime.datetime.now()
            filename = filepath + "model_loss_"+now.month+"_"+now.year
            plt.savefig(filename + ".png")
        except Exception as e:
            print("Failed to plot accuracy/epoch plot")
            print(e)
