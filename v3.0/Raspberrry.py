import cv2
from requests import get
import socketio
import base64
import time

serverUrl = 'http://192.168.1.211:5000'


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
        retval , buffer = cv2.imencode('.jpg',frame)
        encodedImage = base64.b64encode(buffer)
        try:
            sio.emit('liveimage',encodedImage)
        except:
            pass



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

trigger = 40
echo = 38

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
    #robotMovement(data)
    time.sleep(1/15)
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

# Function which handles global variables
def globalvariables(buffer , want):
    connected = False

# Fuctions which initiates movement of the Robot in given Direction
def robotMovement(direction):

    #Check Distance with UltraSonic Sensor
    GPIO.output(trigger,True)
    time.sleep(0.00001)
    GPIO.output(trigger, False)
    while GPIO.input(echo)==0:
        pulse_start = time.time()
    while GPIO.input(echo)==0:
        pulse_end = time.time()

    distance = (pulse_end - pulse_start) * 17150
    print(distance)
    if distance > 20 :
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


    if distance <= 20:
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.LOW)
        GPIO.output(in3,GPIO.LOW)
        GPIO.output(in4,GPIO.LOW)         




#sio.connect('https://airobotserver.herokuapp.com')
sio.connect(serverUrl)
sio.wait()
