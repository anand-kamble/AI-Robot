# Importing required packages
import multiprocessing
from re import search
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

port = 5000
hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)
print(f'\n\n[SERVER IP] : http://{local_ip}:{port}\n\n\n')
sio = socketio.Server(cors_allowed_origins="*")
staticFiles = { 
      '/': {'content_type': 'text/html', 'filename': 'static/index.html'},
      '/socket.io.min.js': {'content_type': 'text/javascript ', 'filename': 'static/socket.io.min.js'},
      '/jquery-3.6.0.min.js': {'content_type': 'text/javascript ', 'filename': 'static/jquery-3.6.0.min.js'}
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

def processImage(imageString):
    currenttime = time.time()
    #print(imageString)
    imgBuffer = base64.b64decode(imageString);
    #imgBytes =  Image.open(io.BytesIO(imgBuffer));
    NumArray = np.frombuffer(imgBuffer, dtype=np.uint8)  #cv2.cvtColor(np.array(imgBytes), cv2.COLOR_BGR2RGB)
    #print(len(NumArray[0]))
    frame = cv2.imdecode(NumArray, 1)
    
    #cv2.imshow('IMAGEE' , frame)
    #cv2.waitKey(1)

    ClassIndex, confidence, bbox = model.detect(frame,confThreshold=0.5)
    frameH , frameW , frameCh = frame.shape
    #print ('FH %d FW %d' %(frameH,frameW))

    frameWparts = frameW // 3
    #cv2.line(frame, (frameWparts,0),(frameWparts,frameH), (255, 255, 255), thickness=1)
    #cv2.line(frame, (frameWparts*2,0),(frameWparts*2,frameH), (255, 255, 255), thickness=1)

    #print(ClassIndex)
    if (len(ClassIndex)!=0):
        for ClassInd, conf, boxes in zip(ClassIndex.flatten(), confidence.flatten(), bbox):
            #print(boxes)
            #print(len(boxes))
            if(ClassInd <= 80):
                foundItem = classLabels[ClassInd-1].split(',')
                if ClassInd == 44:
                    is_Bottle_in_sight = True
                    centerPoint = [int((boxes[1]+boxes[3]/2)),int(boxes[0]+boxes[2]/2)]
                    if(centerPoint[1] >= frameW):
                        centerPoint[1] = frameW-1
                    if(centerPoint[0] >= frameH):
                        centerPoint[0] = frameH-1
                    #print(centerPoint)
                    cv2.line(frame, (boxes[0], boxes[1]),(boxes[0]+boxes[2],boxes[1]+boxes[3]), (0, 0, 255), thickness=1)
                    cv2.line(frame, (boxes[0], boxes[1]+boxes[3]),(boxes[0]+boxes[2],boxes[1]), (0, 0, 255), thickness=1)
                    frame[centerPoint[0],centerPoint[1]] = [255,255,255]
                    position = centerPoint[1]//frameWparts 
                    if(position == 0):
                        print('Bot needs to turn left  \r', end="\r", flush=True)
                        sio.emit('keydownSearch','a')
                    if(position == 1):
                        print('Bot needs to go straight  \r', end="\r", flush=True)
                        sio.emit('keydownSearch','w')
                    if(position == 2):
                        print('Bot needs to turn right  \r', end="\r", flush=True)
                        sio.emit('keydownSearch','d')
                #else:
                    #search FOr Bottle
                   # print('No bottle In sight',end="\r", flush=True)
                    #sio.emit('keydown','d')
                #if(len(foundItem)>1):
                    #print("[SUCCESS] Found a item belonging to class : %s" %Classes[int(foundItem[1])])
                #else:
                    #print("[WARNING] Found a item Which is not sorted: %s" %foundItem[0])
                cv2.rectangle(frame,boxes,(255,0,0),)
                cv2.putText(frame,classLabels[ClassInd-1],(boxes[0],boxes[1]+40), font, fontScale=font_scale, color=(0,255,0), thickness=3)
    print('FPS : %d' %(1/(time.time() - currenttime)),end="\r")
    cv2.imshow('Obj Detection',frame)
    cv2.waitKey(1)
    sio.emit('givemenextframe')



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
      #sio.emit('sres',msg,room=room)

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
def keyup(sID,room):
      sio.emit('keyend',room=room)

@sio.on('ping')
def ping(sID,ping):
      sio.emit("latency",ping)

@sio.on('pong')
def pong(sID,data):
      sio.emit("pingres",data)

@sio.on('liveimage')
def liveimg(sID,data):
      sio.emit('takeliveimg',data)
      processImage(data)

@sio.on('imageFailed')
def imageFailed(sID,data):
      print('[ERROR] Robot Failed to capture image.')
      sio.emit('givemenextframe')

if __name__ == '__main__':
      eventlet.wsgi.server(eventlet.listen(('',port )),app, log=None)
      #print('[LISTENING ON PORT] Number = %d' %port)  
