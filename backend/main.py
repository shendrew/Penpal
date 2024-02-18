from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import threading
import time
from model import use_model

app = Flask(__name__)
socketio = SocketIO(app)

def get_data():
    while True:
        data = use_model
        socketio.emit('update', data)
        # time.sleep(0.01)  

# start data generator in a separate thread
thread = threading.Thread(target=get_data)
thread.daemon = True
thread.start()

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    socketio.run(app)
