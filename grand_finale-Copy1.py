#!/usr/bin/env python
# coding: utf-8

# In[6]:


from keras.models import model_from_json
import matlab.engine
import matplotlib
from matplotlib import pyplot as plt
#import pandas as pd
from keras import optimizers
import keras
from keras.layers import Dense, Activation, Convolution2D, Reshape, Flatten, ZeroPadding2D,ZeroPadding1D,RepeatVector,CuDNNLSTM,CuDNNGRU,LSTM,Bidirectional
from keras.layers import MaxPooling2D, UpSampling2D, Input, Dropout
from keras.models import Sequential, Model
import os
from keras.utils import np_utils
import tensorflow as tf
#from keras.layers import Conv1D,MaxPooling1D
#from keras.layers import Conv2D,MaxPooling2D
from keras import regularizers
from keras.callbacks import ModelCheckpoint
#from sklearn import svm
#from scipy import sparse
from sklearn.metrics import accuracy_score
from keras.layers.normalization import BatchNormalization
import h5py
import itertools
from sklearn import preprocessing
import numpy as np
from sklearn.model_selection import train_test_split
from scipy.io import loadmat
import numpy as np
import h5py 
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


# In[7]:


def numeric_to_string(label):
    if label==0:
        return "BPSK"
    elif label==1:
        return "QPSK"
    elif label==2:
        return "16-QAM"
    elif label==3:
        return "64-QAM"
    elif label==4:
        return "128-QAM"
    elif label==5:
        return "256-QAM"
    else :
        return "8-PAM"


# In[8]:


def classifier(to_be_classified,loaded_model):
    labels=loaded_model.predict_classes(to_be_classified)
    string_labels=np.array([])
    for i in range(to_be_classified.shape[0]):
        string_labels=np.append(string_labels,numeric_to_string(labels[i]))
    string_labels=string_labels.reshape((to_be_classified.shape[0],1))
    return string_labels


# In[9]:
def input_and_prediction():
    json_file = open('model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    # load weights into new model
    loaded_model.load_weights("./Coms_d1.hdf5")
    print("Loaded model from disk")
 
    # evaluate loaded model on test data
    loaded_model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])

    eng = matlab.engine.start_matlab()
    

    
    v,w,x,BW,z=eng.testFunction(nargout=5)
    band_idx=np.asarray(v)
    band_idx=band_idx.reshape((band_idx.shape[1],1))
    bar_height=np.asarray(w)
    bar_height=bar_height.reshape((bar_height.shape[1],1))
    x_signal=np.asarray(x)
    x_signal=x_signal.reshape((18271,))
    to_be_classified=np.asarray(z)
    modulation_schemes=classifier(to_be_classified,loaded_model)
    return modulation_schemes


# In[ ]:


from flask import Flask,jsonify

app = Flask(__name__)
    
@app.route('/get_results',methods=['GET'])
def get_classifier_results():
    return input_and_prediction()


app.run(host='0.0.0.0',port = 10000)


# In[ ]:


#

