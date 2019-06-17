from keras.models import model_from_json
from flask_socketio import SocketIO, emit
from flask import Flask, render_template, url_for, copy_current_request_context
from random import random
from time import sleep
from threading import Thread, Event
from scipy.io import loadmat
import numpy as np
import h5py 
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from io import BytesIO
import base64
from flask import send_file
from flask import Response
import time
import matlab.engine
import sys
from keras import backend as K



thread = Thread()
thread_stop_event = Event()
thread_loop_condition=False
selected_model = "lstm"
no_of_bands="one"


__author__ = 'slynn'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True

#turn the flask app into a socketio app
socketio = SocketIO(app)

#random number Generator Thread


class RandomThread(Thread):
    def __init__(self):
        self.delay = 1
        super(RandomThread, self).__init__()
        
    def numeric_to_string(self,label):
        if label==0:
            return "2psk"
        elif label==1:
            return "4psk"
        elif label==2:
            return "16qam"
        elif label==3:
            return "64qam"
        elif label==4:
            return "128qam"
        elif label==5:
            return "256qam"
        else :
            return "8-PAM"


    def numeric_to_string_actual(self,label):
        if label==1:
            return "2psk"
        elif label==2:
            return "4psk"
        elif label==3:
            return "16qam"
        elif label==4:
            return "64qam"
        elif label==5:
            return "128qam"
        elif label==6:
            return "256qam"
        else:
            return "8-PAM"
    
    def loading_model_cnn(self):
        json_file = open("model_cnn.json", 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        print("loading model for cnn")
        loaded_model = model_from_json(loaded_model_json)
        # load weights into new model
        print("loaded_weights cnn")
        loaded_model.load_weights("weights_cnn.hdf5")
        print("Loaded model from disk cnn")
        # evaluate loaded model on test data
        loaded_model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
        print("model_compiled for cnn")
        
        return loaded_model

    def loading_model_lstm(self):
        json_file = open("model_lstm.json", 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        print("loading model for lstm")
        loaded_model = model_from_json(loaded_model_json)
        # load weights into new model
        print("loaded_weights lstm")
        loaded_model.load_weights("weights_lstm.hdf5")
        print("Loaded model from disk lstm")
        # evaluate loaded model on test data
        loaded_model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
        print("model_compiled lstm")
        
        return loaded_model
    
    def classifier(self,to_be_classified,loaded_model):
        
        if selected_model=="cnn":
            to_be_classified = to_be_classified.reshape(2,256,2,1)
        labels=loaded_model.predict_classes(to_be_classified)
        string_labels=np.array([])
        for i in range(to_be_classified.shape[0]):
            string_labels=np.append(string_labels,self.numeric_to_string(labels[i]))
        string_labels=string_labels.reshape((to_be_classified.shape[0],1))
        return string_labels    

    def randomNumberGenerator(self):
        """
        Generate a random number every 1 second and emit to a socketio instance (broadcast)
        Ideally to be run in a separate thread?
        """
        eng = matlab.engine.start_matlab()
        band_idx=np.empty((2,1))
        bar_height=np.empty((2,1))
        y=np.empty((18271,))
        x=np.empty((18271,))
        modulation_schemes=np.empty((2,1))
        BW=1305.0714285714287   
        i=0
        fig = plt.figure()
        ax = fig.add_subplot(111)
        loaded_model_cnn=self.loading_model_cnn()
        loaded_model_lstm=self.loading_model_lstm()
        while not thread_stop_event.isSet():
            if not thread_loop_condition:
                continue
            plt.pause(1)
            if i%2==0:
                a,v,w,x,BW,z_IQ,A =eng.testFunction(nargout=7)
                actual_integer=np.asarray(a)
                actual_integer=actual_integer.reshape((actual_integer.shape[1],1))
                band_idx=np.asarray(v)
                band_idx=band_idx.reshape((band_idx.shape[1],1))
                bar_height=np.asarray(w)
                bar_height=bar_height.reshape((bar_height.shape[1],1))          
                x_signal=np.asarray(x)
                x_signal=x_signal.reshape((18271,))
                to_be_classified=np.asarray(z_IQ)
                A=np.asarray(A)
                A.shape
                print(A)

                if selected_model == "cnn":
                    modulation_schemes=self.classifier(to_be_classified,loaded_model_cnn)
                else:
                    modulation_schemes=self.classifier(to_be_classified,loaded_model_lstm)
                x=np.arange(x_signal.shape[0])
                y=x_signal
                ax.plot(x,y)
                fig.savefig("test.png")
                socketio.emit('newnumber', {'number': "test.png"}, namespace='/test')
                ax.clear()
            else:
                ax.plot(x,y)
                for j in range(2):
                    actual=self.numeric_to_string_actual(actual_integer[j][0])
                    BN1=band_idx[j][0]
                    BW1=BW
                    height=bar_height[j][0]
                    ax.add_patch(Rectangle(xy=(BW1*(BN1-1),0) ,width=BW1, height=height, linewidth=1, color='red', fill=False))
                    ax.text(BW1*(BN1-1), height+30, modulation_schemes[j][0])
                    ax.text(BW1*(BN1-1), height+60, actual)  # just plug modulation_schemes instead of ms her
                fig.savefig("test.png")
                socketio.emit('newnumber', {'number': "test.png"}, namespace='/test')
                ax.clear()
            i=i+1        
        #sys.exit()

        
            
            
            
            
            
        
     
        
    def run(self):
        self.randomNumberGenerator()


@app.route('/')
def index():
    #only by sending this page first will the client be connected to the socketio instance
    return render_template('index.html')

@socketio.on('connect', namespace='/test')
def test_connect():
    # need visibility of the global thread object
    global thread
    print('Client connected')
    #thread_stop_event.clear()
    global thread_loop_condition
    thread_loop_condition=True
    #Start the random number generator thread only if the thread has not been started before.
    if not thread.isAlive():
        print("Starting Thread")
        thread = RandomThread()
        thread.start()


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    global thread_loop_condition
    thread_loop_condition=False
    #thread_stop_event.set()
    print('Client disconnected')
    
@app.route("/settings/<string:data>")
def recieve_settings(data):
    global selected_model
    print(data)
    import json
    json_data = json.loads(data)
    print(type(json_data))
    handleBandChange(json_data)
    if json_data['cnn']:
        selected_model = "cnn"
        return Response("Backend : setting model type to cnn",mimetype="text")
    elif json_data['lstm']:
        selected_model = "lstm"
        return Response("Backend : setting model type to lstm",mimetype="text")
    return Response("I got it. But could not select anything",mimetype="text")
    
def handleBandChange(json_data):
    global no_of_bands
    print("Handling band selection")
    if json_data['band'] == 'one':
        print("Selected band = one")
        no_of_bands = "one"
    elif json_data['band'] == 'two':
        print("Selected band = two")
        no_of_bands = "two"
    elif json_data['band'] == 'three':
        print("Selected band = three")
        no_of_bands = "three"

@app.route("/get_image")
def get_image():
    #return send_file("test.png", mimetype='image/png')
    fp=open("test.png","rb")
    data=fp.read()
    fp.close()
    x= base64.b64encode(data)
    return Response(x,mimetype="text")    

if __name__ == '__main__':
    socketio.run(app, host="192.168.17.19",port=5000)

