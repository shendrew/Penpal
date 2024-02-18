from flask import Flask, jsonify
import serial
from flask_cors import CORS
import tensorflow as tf
import numpy as np

app = Flask(__name__)
CORS(app)

model = tf.keras.Sequential([
    tf.keras.layers.Reshape((28, 28, 1), input_shape=(28, 28)),  # Reshape input images to (28, 28, 1)
    tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(62, activation='softmax')  # 62 classes for multiclass classification
])

model.load_weights('../emnist_model.h5')

@app.route("/api/home", methods=['GET'])
def return_home():
    return jsonify({
        "message":"hello world"
    })

@app.route('/process_data', methods=['GET'])
def process_data():
    # read from serial monitor
    ser = serial.Serial('COM3', 9600)
    data = ser.readline()
    print(data)

    # put data through neural netwrok
    # processed_data = ...

    #return jsonify(processed_data)

if __name__ == "__main__":
    app.run(debug=True, port=8080)