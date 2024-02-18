from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from model import use_model 

app = Flask(__name__)
socketio = SocketIO(app)

def get_data():
    while True:
        data = use_model()  
        socketio.emit('update', data)
        socketio.sleep(0.01)  # non-blocking sleep

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    socketio.run(app)
