from flask import Flask, jsonify
import serial
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

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

    # put data through neural netwrok
    # processed_data = ...

    #return jsonify(processed_data)

if __name__ == "__main__":
    app.run(debug=True, port=8080)