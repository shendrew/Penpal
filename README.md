# Penpal
Penpal is a web application that helps people who are injured and disabled spell. 
It utilizes an **Arduino Uno**, **accelerometer**, **gyroscope**, and software to write letters.&nbsp

Using the measurements derived from the hardware, we utilize Riemann sums to approximate the position of the finger in space.
We then utilize **OpenCV** to preprocess the data and draw the air hand-drawn letters to a pixelated grid.

We employ **WebSockets** in Socket.io to connect our **Flask** backend and **React.js/Next.js** frontend in order to get real-time updates in statistics.

