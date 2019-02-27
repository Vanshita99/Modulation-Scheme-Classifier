from keras.models import model_from_json
import matlab.engine
import numpy as np
import h5py 
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from flask_socketio import SocketIO, emit
from flask import Flask, render_template, url_for, copy_current_request_context
from random import random
from time import sleep
from threading import Thread, Event
from scipy.io import loadmat
import numpy as np
import h5py 
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from io import BytesIO
import base64
from flask import send_file
from flask import Response
import time









__author__ = 'slynn'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True

#turn the flask app into a socketio app
socketio = SocketIO(app)

#random number Generator Thread
thread = Thread()
thread_stop_event = Event()

class RandomThread(Thread):
    def __init__(self):
        self.delay = 1
        super(RandomThread, self).__init__()
        
    def numeric_to_string(self,label):
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
    
    def loading_model(self):
        json_file = open('model.json', 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        loaded_model = model_from_json(loaded_model_json)
        # load weights into new model
        loaded_model.load_weights("./Coms_d1.hdf5")
        print("Loaded model from disk")
        # evaluate loaded model on test data
        loaded_model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
        return loaded_model
    
    def classifier(self,to_be_classified,loaded_model):
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
        k=0
        i=0
        fig = plt.figure()
        ax = fig.add_subplot(111)
        while not thread_stop_event.isSet():
            plt.pause(1)
            v,w,x,BW,z=eng.testFunction(nargout=5)
            band_idx=np.asarray(v)
            band_idx=band_idx.reshape((band_idx.shape[1],1))
            bar_height=np.asarray(w)
            bar_height=bar_height.reshape((bar_height.shape[1],1))
            x_signal=np.asarray(x)
            x_signal=x_signal.reshape((18271,))
            to_be_classified=np.asarray(z)
    #have got to plot x_signal without boxes
    
            loaded_model=self.loading_model()
            modulation_schemes=self.classifier(to_be_classified,loaded_model)
            x=np.arange(x_signal.shape[0])
            y=x_signal
            ax.plot(x,y)
            if i%2==1:   
                for j in range(2):
                    BN1=band_idx[j][0]
                    BW1=BW
                    height=bar_height[j][0]
                    ax.add_patch(Rectangle(xy=(BW1*(BN1-1),0) ,width=BW1, height=height, linewidth=1, color='red', fill=False))
                    ax.text(BW1*(BN1-1), height+30, modulation_schemes[j][0])  # just plug modulation_schemes instead of ms here

                k=k+1
            fig.savefig("test.png")
            socketio.emit('newnumber', {'number': "test.png"}, namespace='/test')
            ax.clear()
            i=i+1
            if i==4:
                i=0
            if k==4:
                k=0
            
            
            
            
            
        
     
        
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

    #Start the random number generator thread only if the thread has not been started before.
    if not thread.isAlive():
        print("Starting Thread")
        thread = RandomThread()
        thread.start()

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')

@app.route("/get_image")
def get_image():
    #return send_file("test.png", mimetype='image/png')
    fp=open("test.png","rb")
    data=fp.read()
    fp.close()
    x= base64.b64encode(data)

if __name__ == '__main__':
    socketio.run(app)

