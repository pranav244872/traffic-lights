import cv2
import numpy as np

cap = cv2.VideoCapture(0)
whT = 320
confThreshold = 0.5
nmsThreshold = 0.3

classesFile = '/home/pranav/Downloads/Traffic/traffic-lights-bitches/coco.names'
classNames = []
with open(classesFile, 'rt') as f:
    classNames = f.read().rstrip('\n').split('\n')

modelConfiguration = '/home/pranav/Downloads/Traffic/traffic-lights-bitches/yolov3.cfg'
modelWeights = '/home/pranav/Downloads/Traffic/traffic-lights-bitches/yolov3.weights'
net = cv2.dnn.readNetFromDarknet(modelConfiguration, modelWeights)
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

def findObjects(outputs, img):
    hT, wT, cT = img.shape
    bbox = []
    classIds = []
    confs = []
    for output in outputs:
        for det in output:
            scores = det[5:]
            classId = np.argmax(scores)
            confidence = scores[classId]
            if confidence > confThreshold:
                w, h = int(det[2] * wT), int(det[3] * hT)
                x, y = int((det[0] * wT) - w/2), int((det[1] * hT) - h/2)
                bbox.append([x, y, w, h])
                classIds.append(classId)
                confs.append(float(confidence))
    indices = cv2.dnn.NMSBoxes(bbox, confs, confThreshold, nmsThreshold)
    car_count = 0
    for i in indices:
        box = bbox[i]
        x, y, w, h = box[0], box[1], box[2], box[3]
        if classNames[classIds[i]].lower() == 'car':
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 255), 2)
            cv2.putText(img, f'Car {int(confs[i]*100)}%', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 255), 2)
            car_count += 1

    return img, car_count

while True:
    success, img = cap.read()
    blob = cv2.dnn.blobFromImage(img, 1/255, (whT, whT), [0, 0, 0], 1, crop=False)
    net.setInput(blob)
    layerNames = net.getLayerNames()
    outputLayerIndices = net.getUnconnectedOutLayers()
    outputNames = [layerNames[i-1] for i in outputLayerIndices]
    outputs = net.forward(outputNames)

    img, car_count = findObjects(outputs, img)

    print(f'Number of cars: {car_count}')

    cv2.imshow('Image', img)
    cv2.waitKey(1)