from flask import Flask, jsonify
import serial
from flask_cors import CORS
import tensorflow as tf
import numpy as np
import time

import serial.tools.list_ports

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