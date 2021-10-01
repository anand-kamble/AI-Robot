from logging import debug
import socketio
import eventlet
import json
sio = socketio.Server(cors_allowed_origins="*")
staticFiles = { '/': {'content_type': 'text/html', 'filename': 'static/index.html'}}
app = socketio.WSGIApp(sio , static_files=staticFiles)

onlineRobos = []


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


if __name__ == '__main__':
  eventlet.wsgi.server(eventlet.listen(('',5000)),app)