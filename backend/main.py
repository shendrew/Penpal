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
import cv2


app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
cors = flask_cors.CORS(app, resources={r'/*': {'origins': '*'}})

# def integrate_acceleration(a, dt):
#     v = np.cumsum(a, axis=0) * dt
#     d = np.cumsum(v, axis=0) * dt
#     return np.cumsum(d, axis=0)

def rescale_image(d):
    
    # col1 = integrate(-d[:,2])
    # col2 = integrate(d[:,0])
    col1 = -d[:,2]
    col2 = d[:,0]
    #print(col1)
    # print(cols)
    # col2 = d[:,1]
    # dir = np.where(col1 > col2, col1, col2)
    
    
    pos = [336, 336]
    
    image = np.ones((672, 672,1), np.uint8)*255

    # # Draw points on the image
    for i in range(d.shape[0]):
        if np.abs(col1[i]) != 0:
            pos[0] += 1* col1[i]
            # pos[0] += 3* col1[i] / np.abs(col1[i])
        if np.abs(col2[i]) != 0:
            pos[1] += 1* col2[i]
            # pos[1] += 3* col2[i] / np.abs(col2[i])
        cv2.circle(image, (int(pos[0]), int(pos[1])), radius=5, color=(i%255,i%255, i%255), thickness=-1)  # Draw filled circles
    
    cv2.imwrite("test.jpg", image)
    return cv2.resize(image, (28, 28))
        
    # first_column = d[:, 0]
    # third_column = d[:, 1]

    # max_x, min_x = np.max(first_column), np.min(first_column)
    # max_y, min_y = np.max(third_column), np.min(third_column)

    # rescale_x = 28   # 24x24 picture padded with 4x4 empty
    # rescale_y = 28 
    
    # # print('column1')
    # # print(first_column)
    # # print(
    # #     'column3'
    # # )
    # # print(third_column)

    # # first_column = first_column/ (max_x - min_x)
    # # first_column = (first_column - min_x) * (224 / max_x)
    # # third_column = (third_column - min_y) * 224 / max_y
    
    # first_column = (first_column - min_x) * 672 / (max(max_x - min_x, 0.1))
    # third_column = (third_column - min_y) * 672 / (max(max_y - min_y, 0.1))
    # print('column1')
    # print(first_column)
    # print(
    #     'column3'
    # )
    # print(third_column)
    # image = np.ones((672, 672,1), np.uint8)*255

    # # Draw points on the image
    # for i in range(d.shape[0]):
    #     cv2.circle(image, (int(first_column[i]), int(third_column[i])), radius=1, color=(i%255,i%255, i%255), thickness=-1)  # Draw filled circles
    
    # cv2.imwrite("test.jpg", image)
        
    # return image
    
def integrate(a):
    return np.cumsum(a) * 0.1

alphabet = [letter for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'] + [letter for letter in 'abcdefghijklmnopqrstuvwxyz'] + [num for num in '0123456789']
def get_data():
    ser = serial.Serial(port='COM6', baudrate=9600, timeout=0.2)
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
            # displacement = integrate_acceleration(acceleration, 0.1)
            # displacement = integrate_acceleration(acceleration, 0.01)
            # print(displacement)
            # rescale_image(acceleration)
            # print("=========================")
            # print("B")
            # add ml_data later
            # print(integrate(acceleration))
            graphic = rescale_image(acceleration)
            result = use_model(graphic.reshape(1, 28, 28))
            letter = alphabet[np.argmax(result)]
            print(letter)
            # socketio.emit('update', { "displacement": displacement.tolist() })
            socketio.emit('update', { "displacement": letter })
            acceleration = np.array([[]])
        elif (acceleration.size == 0):                              # first point
            acceleration = np.array([[float(i) for i in data]])
            # print("C")
        else:                                                   # add data point
            acceleration = np.append(
                acceleration, [[float(i) for i in data]], axis=0)
            # print(acceleration.shape)
        # time.sleep(0.1)
        time.sleep(0.01)

        # socketio.sleep(0.1)  # non-blocking sleep
        socketio.sleep(0.01)  # non-blocking sleep


@socketio.on('connect')
def handle_connect():
    print('Client connected')


if __name__ == '__main__':
    thread = threading.Thread(target=get_data)
    thread.daemon = True
    thread.start()
    socketio.run(app)
