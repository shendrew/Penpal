from flask import Flask, jsonify
import serial
from flask_cors import CORS
import tensorflow as tf
import numpy as np
import time

app = Flask(__name__)
CORS(app)

# model = tf.keras.Sequential([
#     tf.keras.layers.Reshape((28, 28, 1), input_shape=(28, 28)),  # Reshape input images to (28, 28, 1)
#     tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
#     tf.keras.layers.MaxPooling2D((2, 2)),
#     tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
#     tf.keras.layers.MaxPooling2D((2, 2)),
#     tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
#     tf.keras.layers.Flatten(),
#     tf.keras.layers.Dense(128, activation='relu'),
#     tf.keras.layers.Dense(62, activation='softmax')  # 62 classes for multiclass classification
# ])

# model.load_weights('../emnist_model.h5')

# @app.route("/api/home", methods=['GET'])
# def return_home():
#     return jsonify({
#         "message":"hello world"
#     })

# @app.route('/process_data', methods=['GET'])
# def process_data():
    # read from serial monitor
    
    # ser = serial.Serial(port='/dev/tty6', baudrate=9600, timeout=0.1)

    # put data through neural netwrok
    # processed_data = ...

    #return jsonify(processed_data)

# if __name__ == "__main__":
#     app.run(debug=True, port=8080)


def integrate_acceleration(a, dt):
    v = np.cumsum(a, axis=0) * dt
    d = np.cumsum(v, axis=0) * dt
    return np.cumsum(d, axis=0)

ser = serial.Serial(port='COM6', baudrate=9600, timeout=0.05)
acceleration = np.array([[]])
while (True):
    data = []
    if ser.in_waiting:
        data = ser.readline().decode("utf-8").split()
    
    if (data == []):                                        # no input
        # print("A")
        pass    
    elif (data[0] == 'end'):                                  # end of contact
        # print(acceleration)
        displacement = integrate_acceleration(acceleration, 0.01)
        # print(displacement)
        # print("=========================")
        acceleration = np.array([[]])
        # print("B")
    elif (acceleration.size == 0):                              # first point
        acceleration = np.array([[float(i) for i in data]])
        # print("C")
    else:                                                   # add data point
        acceleration = np.append(acceleration, [[float(i) for i in data]], axis=0)
        # print(acceleration.shape)
    time.sleep(0.01)                                         # sleep to be in sync with arduino