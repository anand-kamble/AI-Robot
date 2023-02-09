# This file is made for Raspberry Pi.
# If you wish to run this on other machines
# Comment or Delete the GPIO part.

# Importing required packages
import multiprocessing
import cv2
from flask import Flask
from flask.helpers import send_file, send_from_directory
import socket
from multiprocessing import Process
from ctypes import c_wchar_p
from requests import get
import socketio
import base64
import time

# Function handing Image Processing
def imagePro():

    # Loading model from respective files.
    model = cv2.dnn_DetectionModel("frozen_inference_graph.pb","ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt")
    
    # Defining classes in which items are classified.
    Classes = ["Living Thing","Vehicle","Edible","Electronic"]

    # Loading Labels for Image Detection from .txt file.
    classLabels = []
    fileName = 'label.txt'
    with open(fileName,'rt') as fpt:
        classLabels = fpt.read().rstrip('\n').split('\n')
    #print(classLabels)

    # Setting up input ParametersN
    model.setInputSize(320,320)
    model.setInputScale(1.0/127.5)
    model.setInputMean((127.5,127.5,127.5))
    model.setInputSwapRB(True)

    # Start Video capture from the camera
    cap = cv2.VideoCapture(0)

    # Check whether the Capture has initialized or not.
    if not cap.isOpened():
        cap = cv2.videoCapture(1) 
    if not cap.isOpened():
        raise IOError("Cannot Open Video") 
    
    # Setting up font properties which will be displayed on processed frame
    font_scale = 3
    font = cv2.FONT_HERSHEY_PLAIN

    print("Image Recognition initiated.")
    while True:
        # Reading the frames from camera
        ret,frame = cap.read()

        # Confirming that the frame has been read successfully.
        if not ret:
            print("[ERROR] Can't receive frame.")
            break

        # Detecting objects in the frame
        ClassIndex, confidence, bbox = model.detect(frame,confThreshold=0.55)
        
        # We will only write text on frame there are objects found in the frame
        if (len(ClassIndex)!=0):

            # Writing text for each object found in frame
            for ClassInd, conf, boxes in zip(ClassIndex.flatten(), confidence.flatten(), bbox):

                # Just so we don't exceed the number of available labels.
                if(ClassInd <= 80):
                    foundItem = classLabels[ClassInd-1].split(',')
                    cv2.rectangle(frame,boxes,(255,0,0),)
                    cv2.putText(frame,classLabels[ClassInd-1],(boxes[0],boxes[1]+40), font, fontScale=font_scale, color=(0,255,0), thickness=3)

        cv2.imshow('temp',frame)
        cv2.waitKey(2)
        # Writing the processed frame to JPG file.
        #cv2.imwrite('camera.jpg',frame)
        retval , buffer = cv2.imencode('.jpg',frame)
        encodedImage = base64.b64encode(buffer)

        time.sleep(1);
        try:
            sio.emit('liveimage',encodedImage)
            print('EMITING')
        except:
            pass
    # Closing all the processes after the we have finished with processing.        
    cap.release() 
    cv2.destroyAllWindows()


import RPi.GPIO as GPIO

sio = socketio.Client()


# GPIO pins to be used 11,12,13,15 
# GPIO17,GPIO18,GPIO27,GPIO22
# Declaring Variables for GPIO PINS in use.
in1 = 11
in2 = 12
in3 = 13 
in4 = 15
pwm1 = 16
pwm2 = 18

# Setting Mode of Numbering system used on GPIO Pins
GPIO.setmode(GPIO.BOARD)

# Setting GPIO Pins as OUTPUT
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(in3,GPIO.OUT)
GPIO.setup(in4,GPIO.OUT)
GPIO.setup(pwm1,GPIO.OUT)
GPIO.setup(pwm2,GPIO.OUT) 

# Setting Output of GPIO Pins to LOW
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
GPIO.output(in3,GPIO.LOW)
GPIO.output(in4,GPIO.LOW)

# Setting PWM on the pins assigned for PWM control along with it's frequency. 
speedControl1 = GPIO.PWM(pwm1,1000)
speedControl2 = GPIO.PWM(pwm2,1000)

# Starting the PWN with Duty Cycle 25%
speedControl1.start(25)
speedControl2.start(25)   
 
isSocketConnected = False

username = input("Create a Display name for this Machine : ")
if len(username) == 0:
    username = input("Display name is mandatory : ")
password = input("Create a password for this Machine : ")
if len(password) == 0:
    password = 'none'
if password == 'none':
    password = input("Please input a stronger password : ")


authOBJ = username + ','+ password
@sio.event
def connect():
    print("I'm connected!")
    sio.emit('CreateAuth',authOBJ )
    #sio.emit('getOnlineMachines')
    imagePro()

@sio.event
def connect_error(data):
    print("The connection failed!")

@sio.event
def disconnect():
    print("I'm disconnected!")


""" @sio.on('sres')
def tprt(data):
    print(data) """
""" 
@sio.on('message')
def prt(data):
    print(data)
"""
@sio.on('keydown')
def keypress(data):
    print('KEY PRESSED ',data)
    robotMovement(data)
    #sio.emit('ping')

@sio.on('keyend')
def keyend():
    print('[Movement] : End')
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.LOW)
    GPIO.output(in3,GPIO.LOW)
    GPIO.output(in4,GPIO.LOW)

@sio.on('latency')
def latency(data):
    sio.emit('pong',data)
# Function which handles global variables
def globalvariables(buffer , want):
    connected = False

# Fuctions which initiates movement of the Robot in given Direction
def robotMovement(direction):
    if direction == "w":               
        print("[Movement] : Forward")
        GPIO.output(in1,GPIO.HIGH)
        GPIO.output(in2,GPIO.LOW)
        GPIO.output(in3,GPIO.HIGH)
        GPIO.output(in4,GPIO.LOW)
    elif direction == "a":
        print("[Movement] : Left")
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.HIGH)
        GPIO.output(in3,GPIO.HIGH)
        GPIO.output(in4,GPIO.LOW)
    elif direction == "s":
        print("[Movement] : Backward")
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.HIGH)
        GPIO.output(in3,GPIO.LOW)
        GPIO.output(in4,GPIO.HIGH)
        print("Backward")
    elif direction == "d":
        print("[Movement] : Right")
        GPIO.output(in1,GPIO.HIGH)
        GPIO.output(in2,GPIO.LOW)
        GPIO.output(in3,GPIO.LOW)
        GPIO.output(in4,GPIO.HIGH)




sio.connect('https://airobotserver.herokuapp.com')
sio.wait()
