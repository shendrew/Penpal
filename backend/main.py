from flask import Flask, jsonify, render_template
from flask_socketio import SocketIO, emit
from model import use_model
import serial
import tensorflow as tf
import numpy as np
import time
import threading
import serial.tools.list_ports
import flask_cors

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
cors = flask_cors.CORS(app, resources={r'/*': {'origins': '*'}})

def integrate_acceleration(a, dt):
    v = np.cumsum(a, axis=0) * dt
    d = np.cumsum(v, axis=0) * dt
    return np.cumsum(d, axis=0)


def get_data():
    ser = serial.Serial(port='COM6', baudrate=9600, timeout=0.05)
    acceleration = np.array([[]])
    while True:
        # ml_data = use_model()
        data = []
        if ser.in_waiting:
            data = ser.readline().decode("utf-8").split()

        if (data == []):                                        # no input
            # print("A")
            pass
        elif (data[0] == 'end'):                                  # end of contact
            # print(acceleration)
            displacement = integrate_acceleration(acceleration, 0.01)
            print(displacement)
            print("=========================")
            acceleration = np.array([[]])
            # print("B")
            # add ml_data later
            socketio.emit('update', { "displacement": displacement })
        elif (acceleration.size == 0):                              # first point
            acceleration = np.array([[float(i) for i in data]])
            # print("C")
        else:                                                   # add data point
            acceleration = np.append(
                acceleration, [[float(i) for i in data]], axis=0)
            # print(acceleration.shape)
        time.sleep(0.01)

        socketio.sleep(0.01)  # non-blocking sleep


@socketio.on('connect')
def handle_connect():
    print('Client connected')


if __name__ == '__main__':
    thread = threading.Thread(target=get_data)
    thread.daemon = True
    thread.start()
    socketio.run(app)
