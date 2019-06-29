"""
Demo Flask application to test the operation of Flask with socket.io

Aim is to create a webpage that is constantly updated with random numbers from a background python process.

30th May 2014

===================

Updated 13th April 2018

+ Upgraded code to Python 3
+ Used Python3 SocketIO implementation
+ Updated CDN Javascript and CSS sources

"""




# Start with a basic flask app webpage.
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

    def randomNumberGenerator(self):
        """
        Generate a random number every 1 second and emit to a socketio instance (broadcast)
        Ideally to be run in a separate thread?
        """
        #infinite loop of magical random numbers

        f = h5py.File('dataset2.mat','r') 
        data1=f.get('x_signal')
        data1=np.array(data1)
        data1=data1.reshape(18271,)
        x_signal=data1

        f1 = h5py.File('data_2.mat','r') 
        data11=f1.get('x_signal')
        data11=np.array(data11)
        data11=data11.reshape(18271,)
        to_be_class=f1.get('band_idx')
        np.array(to_be_class)

        f2 = h5py.File('data_3.mat','r') 
        data21=f2.get('x_signal')
        data21=np.array(data21)
        data21=data21.reshape(18271,)
        to_be_class=f2.get('band_idx')
        np.array(to_be_class)


        f3 = h5py.File('data_4.mat','r') 
        data31=f3.get('x_signal')
        data31=np.array(data31)
        data31=data31.reshape(18271,)
        to_be_class=f3.get('band_idx')
        np.array(to_be_class)

        dataset=np.array([[data1, 1305.07142857, [[2],[5]],[[1190],[900]],[['BPSK'],['QPSK']]],
                  [data11,1305.07142857, [[3],[14]],[[430],[490]],[['QPSK'],['BPSK']]],
                  [data21,1305.07142857, [[4],[12]],[[680],[790]],[['BPSK'],['QPSK']]],
                  [data31,1305.07142857, [[1],[10]],[[850],[2990]],[['BPSK'],['QPSK']]]])
        
        k=0
        i=0
        fig = plt.figure()
        ax = fig.add_subplot(111)
        while not thread_stop_event.isSet():
            
            plt.pause(1)
            BW=dataset[k][1]
            BN=dataset[k][2]
            h=dataset[k][3]
            ms=dataset[i][4]
            x_signal=dataset[k][0]
            x=np.arange(x_signal.shape[0])
            y=x_signal

            
            ax.plot(x, y)  
            if i%2==1:   
                for j in range(2):
                    BN1=BN[j][0]
                    BW1=BW
                    height=h[j][0]
                    ax.add_patch(Rectangle(xy=(BW1*(BN1-1),0) ,width=BW1, height=height, linewidth=1, color='red', fill=False))
                    ax.text(BW1*(BN1-1), height+30, ms[j][0])  # just plug modulation_schemes instead of ms here

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
    return Response(x,mimetype="text")
if __name__ == '__main__':
    socketio.run(app)
