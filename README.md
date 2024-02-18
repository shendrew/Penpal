# Penpal
Penpal is a web application that helps people who are injured and disabled spell. 
It utilizes an **Arduino Uno**, **accelerometer**, **gyroscope**, and software to write letters.&nbsp

Using the measurements derived from the hardware, we approximate the position of the finger in space.
We then utilize **OpenCV** to preprocess the data and draw the air hand-drawn letters to a pixelated grid. 
The pixelated image is resolved into a 28 by 28 pixel image and fed into a trained a Neural Network trained on the EMIST dataset that achieved 85% accuracy.

We employ **WebSockets** in Socket.io to connect our **Flask** backend and **React.js/Next.js** frontend in order to get real-time updates in statistics.

