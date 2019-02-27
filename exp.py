from keras.models import model_from_json
import matlab.engine
import numpy as np
import h5py 
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle











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
        #self.delay = 1
        super(RandomThread, self).__init__()

    def randomNumberGenerator(self):
        """
        Generate a random number every 1 second and emit to a socketio instance (broadcast)
        Ideally to be run in a separate thread?
        """
        #infinite loop of magical random numbers
        eng = matlab.engine.start_matlab()


        v,w,x,BW,z=eng.testFunction(nargout=5)
        band_idx=np.asarray(v)
        band_idx=band_idx.reshape((band_idx.shape[1],1))
        bar_height=np.asarray(w)
        bar_height=bar_height.reshape((bar_height.shape[1],1))
        x_signal=np.asarray(x)
        x_signal=x_signal.reshape((18271,))
        
        x=np.arange(x_signal.shape[0])
        y=x_signal
        b=(x,y)
        plt.plot(b[0], b[1])
        
        from io import BytesIO
        figfile = BytesIO()
        plt.savefig(figfile, format='png')
        figfile.seek(0)  # rewind to beginning of file
        import base64
        figdata_png = base64.b64encode(figfile.getvalue())
        socketio.emit('newnumber', {'number' : number}, namespace='/test')

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


if __name__ == '__main__':
    socketio.run(app)

