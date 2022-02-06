# Importing required packages
import multiprocessing
from re import search
import threading
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
import io
from logging import debug
import logging
import eventlet
import json
import numpy as np
import flask_socketio
from PIL import Image
from logupdate import logupdate
import sys  
import socket
from threading import Timer
import multiprocessing

class Robot:
    def __init__(self , diameter , rpm , trackWidth , cof):
        """"
        :param diameter: Wheel diameter in mm
        :param rpm: RPM of the motor
        :param trackWidth: Track width in mm
        :param cof: Coefficient of friction between wheels and surface
        """
        self.diameter = diameter/1000 #m
        self.rpm = rpm 
        self.perimeter = 3.142*(self.diameter) #m
        self.DistancePerMinute = (self.perimeter*rpm) #meter per minute
        self.speed = (self.perimeter*rpm)/60  #m/s
        self.trackWidth = trackWidth/1000 #m
        self.coeffOfFriction = cof 
    def TimeforDistance (self,distance):
        ''' 
        :param distance: distance in m
        '''
        timeInSeconds = ( distance / self.speed) #sec
        return timeInSeconds
    def TimeForRotation (self,degrees):
        radian = (3.142*degrees)/180
        distanceRequired = ((self.trackWidth/2)*radian) # m
        timeInSeconds = ( distanceRequired / self.speed)
        finalTime = timeInSeconds / (1 - self.coeffOfFriction)
        return finalTime


#isScanRunning = False
port = 5000
hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)
print(f'\n\n[SERVER IP] : http://{local_ip}:{port}\n\n\n')
sio = socketio.Server(cors_allowed_origins="*")
staticFiles = { 
      '/': {'content_type': 'text/html', 'filename': 'static/index.html'},
      '/socket.io.min.js': {'content_type': 'text/javascript ', 'filename': 'static/socket.io.min.js'},
      '/jquery-3.6.0.min.js': {'content_type': 'text/javascript ', 'filename': 'static/jquery-3.6.0.min.js'},
      '/Robot top view for web.png':{'content_type': 'image/png' , 'filename':'static/Robot top view for web.png'}
}
app = socketio.WSGIApp(sio , static_files=staticFiles)

onlineRobos = []

config_file = "ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"
frozen_model = "frozen_inference_graph.pb"
model = cv2.dnn_DetectionModel(frozen_model,config_file)
fileName = 'label.txt'
with open(fileName,'rt') as fpt:
    classLabels = fpt.read().rstrip('\n').split('\n')

model.setInputSize(320,320)
model.setInputScale(1.0/127.5)
model.setInputMean((127.5,127.5,127.5))
model.setInputSwapRB(True)
font_scale = 1
font = cv2.FONT_HERSHEY_PLAIN

is_Bottle_in_sight = False
is_scan_running = False
last_detected_position = 0
is_following = False
last_servo_angle = 0
last_Image_Time = 0
fps = 0

def processImage(imageString):
    global last_detected_position
    global is_scan_running
    global is_following
    global last_servo_angle
    global fps
    global last_Image_Time
    currenttime = time.time()
    imgBuffer = base64.b64decode(imageString);
    NumArray = np.frombuffer(imgBuffer, dtype=np.uint8)
    frame = cv2.imdecode(NumArray, 1)
    ClassIndex, confidence, bbox = model.detect(frame,confThreshold=0.5)
    frameH , frameW , frameCh = frame.shape
    frameWparts = frameW // 3
    if (len(ClassIndex)!=0):
            print('Lenghth of arra',len(bbox))
            if len(bbox) > 1:
                  for ClassInd, conf, boxes in zip(ClassIndex.flatten(), confidence.flatten(), bbox):
                        if(ClassInd <= 80):
                              foundItem = classLabels[ClassInd-1].split(',')
                              if ClassInd == 1:
                                    centerPoint = [int((boxes[1]+boxes[3]/2)),int(boxes[0]+boxes[2]/2)]
                                    if(centerPoint[1] >= frameW):
                                          centerPoint[1] = frameW-1
                                    if(centerPoint[0] >= frameH):
                                          centerPoint[0] = frameH-1
                                    cv2.line(frame, (boxes[0], boxes[1]),(boxes[0]+boxes[2],boxes[1]+boxes[3]), (0, 0, 255), thickness=1)
                                    cv2.line(frame, (boxes[0], boxes[1]+boxes[3]),(boxes[0]+boxes[2],boxes[1]), (0, 0, 255), thickness=1)
                                    frame[centerPoint[0],centerPoint[1]] = [255,255,255]
                                    position = centerPoint[1]//frameWparts
                                    if is_scan_running is True:
                                          if(position == 0):
                                          #print('Bot needs to turn left'  )
                                                last_detected_position = 0
                                          # sio.emit('keydownSearch','a')
                                          if(position == 1):
                                                #print('Bot needs to go straight ' )
                                                last_detected_position = 1
                                          # sio.emit('keydownSearch','w')
                                          if(position == 2):
                                          #print('Bot needs to turn right ')
                                                last_detected_position = 2
                                          sio.emit('abortscan')
                                          sio.emit('foundObject')
                                          sio.emit('servocontrol',90)
                                          time.sleep(0.5)
                                          
                                    if is_following is True:
                                          if(position == 0):
                                                print('Bot needs to turn left'  )
                                                sio.emit('keydownSearch','a')
                                          if(position == 1):
                                                print('Bot needs to go straight ' )
                                                sio.emit('keydownSearch','w')
                                          if(position == 2):
                                                print('Bot needs to turn right ')
                                                sio.emit('keydownSearch','d')
                              else:
                                    #search FOr Bottle
                                    print('No Human In sight')
                                    print(last_servo_angle , is_following)
                                    if is_following is True:
                                          print('Searching...')
                                          if last_servo_angle < 90 :
                                                sio.emit('keydownSearch','d')
                                                print('searching in Right ')
                                          if last_servo_angle > 90 :
                                                sio.emit('keydownSearch','a')
                                                print('Searching in left ')
                                          if last_servo_angle == 90 :
                                                sio.emit('keydownSearch','w')    
                                                print('Searching in forward ') 
                                    #sio.emit('keydownSearch','d')
                              cv2.rectangle(frame,boxes,(255,0,0),)
                              cv2.putText(frame,classLabels[ClassInd-1],(boxes[0],boxes[1]+40), font, fontScale=font_scale, color=(0,255,0), thickness=3)
            else:
                  print('No Human In sight')
                  print(last_servo_angle , is_following)
                  if is_following is True:
                        print('Searching...')
                        if last_servo_angle < 90 :
                              sio.emit('keydownSearch','d')
                              print('searching in Right ')
                        if last_servo_angle > 90 :
                              sio.emit('keydownSearch','a')
                              print('Searching in left ')
                        if last_servo_angle == 90 :
                              sio.emit('keydownSearch','w')    
                              print('Searching in forward ') 
            
    print('FPS : %d' %(1/(time.time() - last_Image_Time)),end="\r")
    last_Image_Time = time.time()
    #cv2.imshow('Obj Detection',frame)
    retval , buffer = cv2.imencode('.jpg',frame)
    if retval is True:
      encodedImage = base64.b64encode(buffer)
      sio.emit('takeliveimg',encodedImage)
    cv2.waitKey(1)
    sio.emit('givemenextframe')
    

def endScanMovement(timeinSec):
      time.sleep(timeinSec)
      print('Ending Scan at : ',time.time())


def scanRoom () :
      isScanRunning = True
      sio.emit('changespeed',100)
      botRotate = Robot(70,100,238,0.8)
      timeReq = 8.75 #botRotate.TimeForRotation(360)
      
      print('DIST REQ : ',botRotate.TimeForRotation(360))
      print('SCAN TIME REQ : ',timeReq)
      
      sio.emit('scanstarted',(timeReq,botRotate.TimeforDistance(2)))
      sio.emit('keydown','d')


      print('\n\nStarting scan at : ',time.time())
      """starttime = time.time()
      while time.time()-starttime < 10:
           print('waiting\r',end="\r", flush=True)
      #sio.emit('keyend')
      sio.emit('keyend')
      print('Ending Scan at : ',time.time()) """
      #Timer(10,endmovement).start()
      
      




@sio.event
def connect(sID, environ):
      print(sID, 'connected')
  

@sio.event
def disconnect(sID):
      print(sID, 'Disconnected')
      for robo in onlineRobos:
            if sID in robo:
                  onlineRobos.remove(robo)

@sio.on("CreateAuth")
def auth(sID,auths):
      print(auths)
      toAppend = '%s,%s'%(sID,auths)
      onlineRobos.append(toAppend)
      roomname = auths.split(',')
      sio.enter_room(sID,room=roomname[0])

@sio.on("Auth")
def auth(sID,auths):
      print(auths)
      for i in range(len(onlineRobos)):
            print(onlineRobos[i])

@sio.on('message')
def handleMSG(sID,msg,room):
      print("MESSAGE : " + msg)

@sio.on('getOnlineMachines')
def SendOnlineMachines(sID):
      print("SENDING MACHINES")
      resStr = ''
      for i in range(len(onlineRobos)):
            resStr+= ','
            resStr += onlineRobos[i].split(',')[1]
      sio.emit('sres',resStr)

@sio.on('reqtoJoin')
def validateReq(sID,password):
      print("VALIDATINF")
      nameofRobo = password.split(',')[0]
      for robo in onlineRobos:
            if nameofRobo in robo:
                  print(sID)
                  if password.split(',')[1] == robo.split(',')[2]:
                        sio.emit("joinsuccess",'joined,%s' %robo.split(',')[1])
                        sio.enter_room(sID,robo.split(',')[1])
                  else:
                        sio.emit("joinsuccess",'falsePassword')
            else:
                  sio.emit("joinsuccess",'falseName')
@sio.on('keypress')
def keypress(sID,key,room):
      sio.emit('keydown',key,room=room)

@sio.on('keyup')
def keyup(sID,data):
      sio.emit('keyend')

@sio.on('ping')
def ping(sID,ping):
      sio.emit("latency",ping)

@sio.on('pong')
def pong(sID,data):
      sio.emit("pingres",data)

@sio.on('liveimage')
def liveimg(sID,data): 
      processImage(data)

@sio.on('imageFailed')
def imageFailed(sID):
      print('[ERROR] Robot Failed to capture image.')
      sio.emit('givemenextframe')

@sio.on('startscan')
def startscan(sID):
      global is_scan_running
      print('\n\nstarting Scan')
      is_scan_running = True

@sio.on('servocontrol')
def servocontrol(sID,data):
      sio.emit('servocontrol',data)

@sio.on('scanoff')
def scanoff(sID,data):
      global is_scan_running
      global last_servo_angle
      is_scan_running = False
      last_servo_angle = data

@sio.on('startfollow')
def startfollow(sID):
      global is_following
      global last_servo_angle
      global is_scan_running
      is_scan_running = False
      is_following = True
      print('Following ... for', last_servo_angle , 'is following  : ',is_following)

      
@sio.on('cancelscan')
def cancelscan(sID):
      global is_Bottle_in_sight
      global is_scan_running 
      global last_detected_position 
      global is_following 
      global last_servo_angle 
      global last_Image_Time 
      global fps 
      is_Bottle_in_sight = False
      is_scan_running = False
      last_detected_position = 0
      is_following = False
      last_servo_angle = 0
      last_Image_Time = 0
      fps = 0
      print('All values set to default.')

if __name__ == '__main__':
      eventlet.wsgi.server(eventlet.listen(('',port )),app, log=None)