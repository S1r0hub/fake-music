#!/usr/bin/env python

# -*- coding: utf-8 -*-
"""
Created on Thu Jun 14 21:00:54 2018

@author: Marcel Himmelreich
"""


import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')
from keras.callbacks import History 
history = History()

class Plotter():
    def __init__(self, history, filename):
        self._history = history
        self._filename = filename
        
    def plotAccuracy(self, filepath, val = False):
        try:
            plt.plot(self._history['acc'])
            if val:
                plt.plot(self._history['val_acc'])
                plt.legend(['train', 'test'], loc='upper left')
            plt.title('Model accuracy')
            plt.ylabel('accuracy')
            plt.xlabel('epoch')  
            filename = filepath + "model_accuracy_"+self._filename
            plt.savefig(filename + ".png")
            plt.show()
        except Exception as e:
            print("Failed to plot accuracy/epoch plot")
            print(e)
            
    def plotLoss(self, filepath, val = False):
        try:
            plt.plot(self._history['loss'])
            if val:
                plt.plot(self._history['val_loss'])
                plt.legend(['train', 'test'], loc='upper left')
            plt.title('Model loss')
            plt.ylabel('loss')
            plt.xlabel('epoch')     
            filename = filepath + "model_loss_"+self._filename
            plt.savefig(filename + ".png")
            plt.show()
        except Exception as e:
            print("Failed to plot accuracy/epoch plot")
            print(e)
            
    def plotAccLoss(self, filepath, val = False):
        try:
            print()
        except Exception as n:
            print()
