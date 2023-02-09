# Importing required packages
import multiprocessing
import cv2
from flask import Flask
from flask.helpers import send_file, send_from_directory
import socket
from multiprocessing import Process
from ctypes import c_wchar_p
from requests import get
import RPi.GPIO as GPIO
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

# Function which handles global variables
def globalvariables(buffer , want):
    globalvariables.base64Buffer = ''
    if want == False:
        globalvariables.base64Buffer = buffer
    if want == True:
        return globalvariables.base64Buffer
globalvariables('a',False)

# Fuctions which initiates movement of the Robot in given Direction
def robotMovement(direction):
    if direction == "w":               
        print("Forward")
        GPIO.output(in1,GPIO.HIGH)
        GPIO.output(in2,GPIO.LOW)
        GPIO.output(in3,GPIO.HIGH)
        GPIO.output(in4,GPIO.LOW)
    elif direction == "a":
        print("Left")
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.HIGH)
        GPIO.output(in3,GPIO.HIGH)
        GPIO.output(in4,GPIO.LOW)
    elif direction == "s":
        print("Backward")
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.HIGH)
        GPIO.output(in3,GPIO.LOW)
        GPIO.output(in4,GPIO.HIGH)
        print("Backward")
    elif direction == "d":
        print("Right")
        GPIO.output(in1,GPIO.HIGH)
        GPIO.output(in2,GPIO.LOW)
        GPIO.output(in3,GPIO.LOW)
        GPIO.output(in4,GPIO.HIGH)

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

        # Writing the processed frame to JPG file.
        cv2.imwrite('camera.jpg',frame)

    # Closing all the processes after the we have finished with processing.        
    cap.release() 
    cv2.destroyAllWindows()

# Function which handles API requests.
def server():
    # Finding Public IP of our system.
    publicIP = get('https://api.ipify.org').text

    # Finding Local IP of our system
    localIP = socket.gethostbyname("raspberrypi.local")

    # Initiating App.
    app = Flask(__name__)

    # Defining API routes
    @app.route("/") # Default URL route which serves Home Page 
    def hello_world():
        return send_file('index.html', mimetype='text/html')

    @app.route("/livefeed") # This route serves the latest frame processed by the function imagePro.
    def livefeed():
        return send_file("camera.jpg",mimetype='data/jpeg')

    @app.route("/key/<keycode>",methods=['POST']) # Route to initiate movement of robot in a perticular direction 
    def keypress(keycode):
        print('[KEY] Down : %s' %keycode)
        robotMovement(keycode)
        return "You pressed the key %s" %keycode

    @app.route("/keyup",methods=['POST']) # Route to end the movement of the robot
    def keyUP():
        print("[KEY] Up")
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.LOW)
        GPIO.output(in3,GPIO.LOW)
        GPIO.output(in4,GPIO.LOW)
        return "Up"

    @app.route("/changespeed/<speed>",methods=['POST']) # Route to change the speed of the movements of robot.
    def changeSpeed(speed):
        try:
            speedControl1.changeDutyCycle(int(speed))
            speedControl2.changeDutyCycle(int(speed))
            return "Done"
        except:
            return "Failed"

    # Starting the Server at localIP of system and Port 3000.
    app.run(host=localIP,port=3000)

if __name__=='__main__':
    manager = multiprocessing.Manager()

    # Defining functions as processes.
    process1 = Process(target=imagePro)
    process2 = Process(target=server)

    # Starting both processes simultaneously.
    process1.start()
    process2.start()