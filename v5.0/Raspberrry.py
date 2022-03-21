# Importing required packages
#import multiprocessing
from warnings import catch_warnings
import cv2
#from flask import Flask 
#from flask.helpers import send_file, send_from_directory
#import socket
#from multiprocessing import Process
#from ctypes import c_wchar_p
from requests import get
import socketio
import base64
import time

import RPi.GPIO as GPIO

serverUrl = 'http://192.168.0.6:5000/'

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    cap = cv2.videoCapture(1) 
if not cap.isOpened():
    raise IOError("Cannot Open Video") 

font_scale = 3
font = cv2.FONT_HERSHEY_PLAIN

print("Image Recognition initiated.")

def imagePro():
    ret,frame = cap.read()

    if not ret:
        print("[ERROR] Can't receive frame.")
        sio.emit('imageFailed')
    else:
        print(frame.shape)
        retval , buffer = cv2.imencode('.jpg',frame)
        encodedImage = base64.b64encode(buffer)
        try:
            sio.emit('liveimage',encodedImage)
        except:
            pass


def servoControl(degreee):
    ''' 
    :param degreee: position of servo motor in degrees. 
     '''
    if degreee >= 0 and degreee <= 180:
        percentage = (degreee / 180) * 100
        print('Percentage Revolution :',percentage)
        duty = (percentage/10) + 2
        print('Duty Cycle will be',duty)
        #servocontrol.ChangeDutyCycle(duty)
        time.sleep(0.1)
        #servocontrol.ChangeDutyCycle(0)








# GPIO pins to be used 11,12,13,15 
# GPIO17,GPIO18,GPIO27,GPIO22
# Declaring Variables for GPIO PINS in use.
in1 = 11
in2 = 12
in3 = 13 
in4 = 15
pwm1 = 16
pwm2 = 18

trigger = 40
echo = 38

servo = 37

# Setting Mode of Numbering system used on GPIO Pins
GPIO.setmode(GPIO.BOARD)

# Setting GPIO Pins as OUTPUT
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(in3,GPIO.OUT)
GPIO.setup(in4,GPIO.OUT)
GPIO.setup(pwm1,GPIO.OUT)
GPIO.setup(pwm2,GPIO.OUT)
GPIO.setup(trigger,GPIO.OUT)
GPIO.setup(echo,GPIO.IN) 
GPIO.setup(servo,GPIO.OUT)


# Setting Output of GPIO Pins to LOW
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
GPIO.output(in3,GPIO.LOW)
GPIO.output(in4,GPIO.LOW)
GPIO.output(pwm1,GPIO.HIGH)
GPIO.output(pwm2,GPIO.HIGH)

# Setting PWM on the pins assigned for PWM control along with it's frequency. 
speedControl1 = GPIO.PWM(pwm1,1000)
speedControl2 = GPIO.PWM(pwm2,1000) 
servocontrol = GPIO.PWM(servo,50)

# Starting the PWN with Duty Cycle 100%
speedControl1.start(100)
speedControl2.start(100)   
servocontrol.start(0) 



''' 
username = input("Create a Display name for this Machine : ")
if len(username) == 0:
    username = input("Display name is mandatory : ")
password = input("Create a password for this Machine : ")
if len(password) == 0:
    password = 'none'
if password == 'none':
    password = input("Please input a stronger password : ") '''


authOBJ = 'a' ''' username + ','+ password '''

sio = socketio.Client()
isSocketConnected = False
@sio.event
def connect():
    print("I'm connected!")
    sio.emit('CreateAuth',authOBJ )
    #sio.emit('getOnlineMachines')
    imagePro()

@sio.event
def connect_error(data):
    global serverUrl
    print("The connection failed!")
    print(f'Server URL [{serverUrl}]')
    confirmation = input('Confirm the server URL [Y/N] : ')
    if confirmation == 'Y' or confirmation == 'y':
        
        sio.connect(serverUrl)
        sio.wait()
    if confirmation == 'N' or confirmation == 'n':
        newUrl = input('Enter the server URL : ');
        serverUrl = newUrl
        sio.connect(serverUrl)
        sio.wait()


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
    #sio.emit(b'ping')

@sio.on('keydownSearch')
def keydownSearch(data):
    print('Moving '+data)
    robotMovement(data)
    time.sleep(1/5)
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.LOW)
    GPIO.output(in3,GPIO.LOW)
    GPIO.output(in4,GPIO.LOW)
    print('Ending Movemnet')


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

@sio.on('givemenextframe')
def nextframe():
    imagePro()

@sio.on('changespeed')
def changespeed(speed):
        pulseWidth = int(speed)
        speedControl1.ChangeDutyCycle(pulseWidth)
        speedControl2.ChangeDutyCycle(pulseWidth)


@sio.on('servocontrol')
def servo(rotation):
    servoControl(rotation)

# Function which handles global variables
def globalvariables(buffer , want):
    connected = False


# Check Distance with UltraSonic Sensor
maxSafeDistance = 20


def MeasureSafeDist():
    GPIO.output(trigger,True)
    time.sleep(0.00001)
    GPIO.output(trigger, False)
    while GPIO.input(echo)==0:
        pulse_start = time.time()
    while GPIO.input(echo)==1:
        pulse_end = time.time()
    distance = (pulse_end - pulse_start) * 17150
    if distance > maxSafeDistance :
        return True
    else:
        return False


def checkDistAhead():
    if not MeasureSafeDist():
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.LOW)
        GPIO.output(in3,GPIO.LOW)
        GPIO.output(in4,GPIO.LOW) 


# Fuctions which initiates movement of the Robot in given Direction
def robotMovement(direction):
    MeasureSafeDist()
    if direction == "w":     
        if MeasureSafeDist():          
            print("[Movement] : Forward")
            GPIO.output(in1,GPIO.HIGH)
            GPIO.output(in2,GPIO.LOW)
            GPIO.output(in3,GPIO.HIGH)
            GPIO.output(in4,GPIO.LOW) 
        else:
            GPIO.output(in1,GPIO.LOW)
            GPIO.output(in2,GPIO.LOW)
            GPIO.output(in3,GPIO.LOW)
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



            




#sio.connect('https://airobotserver.herokuapp.com')
sio.connect(serverUrl)
sio.wait()