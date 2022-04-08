def processImage(imageString):
    currenttime = time.time()
    imgBuffer = base64.b64decode(imageString);
    NumArray = np.frombuffer(imgBuffer, dtype=np.uint8)
    frame = cv2.imdecode(NumArray, 1)
    ClassIndex, confidence, bbox = model.detect(frame,confThreshold=0.5)
    frameH , frameW , frameCh = frame.shape
    frameWparts = frameW // 3
    if (len(ClassIndex)!=0):
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
                    if(position == 0):
                        print('Bot needs to turn left  \r', end="\r", flush=True)
                        sio.emit('keydownSearch','a')
                    if(position == 1):
                        print('Bot needs to go straight  \r', end="\r", flush=True)
                        sio.emit('keydownSearch','w')
                    if(position == 2):
                        print('Bot needs to turn right  \r', end="\r", flush=True)
                        sio.emit('keydownSearch','d')
                cv2.rectangle(frame,boxes,(255,0,0),)
                cv2.putText(frame,classLabels[ClassInd-1],(boxes[0],boxes[1]+40), font, fontScale=font_scale, color=(0,255,0), thickness=3)
    print('FPS : %d' %(1/(time.time() - currenttime)),end="\r")
    cv2.imshow('Obj Detection',frame)
    retval , buffer = cv2.imencode('.jpg',frame)
    if retval is True:
      encodedImage = base64.b64encode(buffer)
      sio.emit('takeliveimg',encodedImage)
    cv2.waitKey(1)
    sio.emit('givemenextframe')