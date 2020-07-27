#!/home/pi/robocar/bin/python3
from flask import Flask, render_template, Response, request, redirect, url_for
import move
import time
import os
import numpy as np
import cv2
import imutils
app = Flask(__name__)
cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
#cam.set(cv2.CAP_PROP_FPS, 20)
prev_move="stop"
curr_move="stop"
sec=0.3
@app.route("/")
def index():
    return render_template('index.html')

@app.route("/forward/", methods=['POST'])
def move_forward():
    #Moving forward code
    global curr_move
    global prev_move
    message = "Moving Forward..."
    prev_move=curr_move
    curr_move="forward"
    if prev_move=="reverse":
        move.stop()
        time.sleep(0.5)
    move.forward()
    return render_template('index.html', message=message)

@app.route("/reverse/", methods=['POST'])
def move_reverse():
    #Moving reverse code
    global curr_move
    global prev_move
    prev_move=curr_move
    curr_move="reverse"
    message = "Moving backwards..."
    if prev_move=="forward":
        move.stop()
        time.sleep(0.5)
    move.backward()
    return render_template('index.html', message=message)

@app.route("/left/", methods=['POST'])
def move_left():
    #Moving forward code
    message = "Moving left..."
    if curr_move=="forward":
      move.forward_left(sec)
      move.forward()
    elif curr_move=="reverse":
      move.reverse_left(sec)
      move.backward()
    elif curr_move=="stop":
      move.forward_left(sec)
      move.stop()
    else:
      print("error! curr_move not set")
      move.stop()
    return render_template('index.html', message=message)

@app.route("/right/", methods=['POST'])
def move_right():
    #Moving forward code
    message = "Moving right..."
    if curr_move=="forward":
      move.forward_right(sec)
      move.forward()
    elif curr_move=="reverse":
      move.reverse_right(sec)
      move.backward()
    elif curr_move=="stop":
      move.forward_right(sec)
      move.stop()
    else:
      print("error! curr_move not set")
      move.stop()
    return render_template('index.html', message=message)

@app.route("/stop/", methods=['POST'])
def move_stop():
    #Moving forward code
    global curr_move
    global prev_move
    prev_move=curr_move
    curr_move="stop"
    message = "Stopping..."
    move.stop()
    return render_template('index.html', message=message)

@app.route("/shutdown/", methods=['POST'])
def shutdown():
    os.system("sudo init 0")
    return render_template('shutdown.html', message=message)

def gen():
    """Video streaming generator function."""
    while True:
        rval, frame = cam.read()
        img = imutils.rotate(frame, 180)
        cv2.imwrite('t.jpg', img)
        yield (b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + open('t.jpg', 'rb').read() + b'\r\n')
    cam.release()

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(),mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
