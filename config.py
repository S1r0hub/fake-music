# -*- coding: utf-8 -*-

import json
import glob
"""
Created on Tue Jul  3 20:41:01 2018

@author: Marcel Himmelreich
"""

"""
Config Layout

Network Setting

Network Layout
"""

class Config():
    def __init__(self):
        self._epochs = 10
        self._sequence_length = 100
        self._batch_size = 128
        self._validation = False
        self._validation_split = None
        self._activation = 'softmax'
        self._optimizer = 'rmsprop'
        self._loss = 'categorical_crossentropy' 
        self._metrics = ['accuracy']
        self._layout = 'default'
        self._config = None    
        
    def saveConfig(self, filepath):
        try:
            setting = {
                    'epoch' : self._epochs,
                    'sequencelength' : self._sequence_length,
                    'batchsize' : self._batch_size,
                    'validatoin' : self._validation,
                    'validationsplit' : self._validation_split,
                    'activation' : self._activation,
                    'optimizer' : self._optimizer,
                    'loss' : self._loss,
                    'metrics' : self._metrics,  
                    'layout' : self._layout
                    }
            
            self._config = {
                    'setting' : setting,
                    }
            
            filenameout = filepath + "/config" + ".jsonl"

            with open(filenameout, "w") as outfile:
                outfile.write(json.dumps(self._config))
                outfile.write("\n")
                    
        except:
            print("Writing Config Failed!")
        
    def loadConfig(self, filepath):
        try:
            with open(filepath + "*.jsonl", "r") as jsonfile:
                jdata = json.loads(jsonfile)
                self._config = jdata
                
                setting = jdata['setting']
                self._epochs = setting['epoch']
                self._sequence_length = setting['sequencelength']
                self._batch_size =  setting['batchsize']
                self._validation = setting['validation']
                self._validation_split = setting['validationsplit']
                self._activation = setting['activation']
                self._optimizer = setting['optimizer']
                self._loss = setting['loss']
                self._metrics = setting['metrics']
                self._layout = setting['layout']
                
                print("Config Loaded...")
        except:
            print("Unable to load config")
        
    def loadMultipleConfig(self,filepath):
        try:
            settings = None
            
            for file in glob.glob(filepath + "*.jsonl"):
                with open(file, "r") as jsonfile:
                    for index, item in enumerate(jsonfile):
                        jdata = json.loads(item)
                        
            return settings
        except:
            print("error")