import cv2
import numpy as np
import requests
import socket
import time

class Camera:
    def __init__(self, camera_number, stream_url, names_path, config_path, weights_path, conf_threshold=0.5, nms_threshold=0.3):
        self.stream_url = stream_url
        self.confThreshold = conf_threshold
        self.nmsThreshold = nms_threshold

        self.classesFile = names_path
        self.classNames = []
        with open(self.classesFile, 'rt') as f:
            self.classNames = f.read().rstrip('\n').split('\n')

        self.modelConfiguration = config_path
        self.modelWeights = weights_path
        self.net = cv2.dnn.readNetFromDarknet(self.modelConfiguration, self.modelWeights)
        self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
        self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
        self.camera_number = camera_number

    def get_frame_from_stream(self):
        try:    
            response = requests.get(self.stream_url)
            frame_array = np.frombuffer(response.content, dtype=np.uint8)
            frame = cv2.imdecode(frame_array, cv2.IMREAD_COLOR)
            return frame
        except Exception as e:
            print(f"Error getting frame from stream: {e}")
            return None
    
    def process_frame(self, frame):
        hT, wT, cT = frame.shape
        blob = cv2.dnn.blobFromImage(frame, 1/255, (320, 320), [0, 0, 0], 1, crop=False)
        self.net.setInput(blob)
        layerNames = self.net.getLayerNames()
        outputLayerIndices = self.net.getUnconnectedOutLayers()
        outputNames = [layerNames[i-1] for i in outputLayerIndices]
        outputs = self.net.forward(outputNames)

        bbox = []
        classIds = []
        confs = []
        car_count = 0
        ambulance_count = 0

        for output in outputs:
            for det in output:
                scores = det[5:]
                classId = np.argmax(scores)
                confidence = scores[classId]
                if confidence > self.confThreshold:
                    w, h = int(det[2] * wT), int(det[3] * hT)
                    x, y = int((det[0] * wT) - w/2), int((det[1] * hT) - h/2)
                    bbox.append([x, y, w, h])
                    classIds.append(classId)
                    confs.append(float(confidence))

        indices = cv2.dnn.NMSBoxes(bbox, confs, self.confThreshold, self.nmsThreshold)

        for i in indices:
            box = bbox[i]
            x, y, w, h = box[0], box[1], box[2], box[3]
            if self.classNames[classIds[i]].lower() == 'car':
                car_count += 1
            elif self.classNames[classIds[i]].lower() == 'truck':
                ambulance_count += 1

        return car_count, ambulance_count

    def process_video(self):
        car_count_list = []
        ambulance_count_list = []
        num_frames = 10  # Number of frames to process for averaging

        for _ in range(num_frames):
            frame = self.get_frame_from_stream()
            if frame is not None:
                car_count, ambulance_count = self.process_frame(frame)
                car_count_list.append(car_count)
                ambulance_count_list.append(ambulance_count)

        max_car_count = max(car_count_list)
        max_ambulance_count = max(ambulance_count_list)

        return max_car_count, max_ambulance_count

            

camera1 = Camera(1,'http://192.168.1.2:8080/shot.jpg', '/home/pranav/Desktop/projects/traffic/traffic-lights/coco.names', '/home/pranav/Desktop/projects/traffic/traffic-lights/yolov3.cfg', '/home/pranav/Desktop/projects/traffic/traffic-lights/yolov3.weights')
camera2 = Camera(2,'http://10.10.10.118:8080/shot.jpg', '/home/pranav/Desktop/projects/traffic/traffic-lights/coco.names', '/home/pranav/Desktop/projects/traffic/traffic-lights/yolov3.cfg', '/home/pranav/Desktop/projects/traffic/traffic-lights/yolov3.weights')
camera3 = Camera(3,'http://10.10.10.118:8080/shot.jpg', '/home/pranav/Desktop/projects/traffic/traffic-lights/coco.names', '/home/pranav/Desktop/projects/traffic/traffic-lights/yolov3.cfg', '/home/pranav/Desktop/projects/traffic/traffic-lights/yolov3.weights')
camera4 = Camera(4,'http://10.10.10.118:8080/shot.jpg', '/home/pranav/Desktop/projects/traffic/traffic-lights/coco.names', '/home/pranav/Desktop/projects/traffic/traffic-lights/yolov3.cfg', '/home/pranav/Desktop/projects/traffic/traffic-lights/yolov3.weights')

priority_list_main = []
while True:
    priority_list = []
    cars_per_road = {"A":camera1.process_video()[0],"B":2,"C":3,"D":4}
    ambulances_per_road = {"A":camera1.process_video()[1],"B":1,"C":0,"D":0}
    
    #Sorting dictionaries
    sorted_cars_per_road = dict(sorted(cars_per_road.items(), key=lambda item: item[1], reverse=True))
    print(sorted_cars_per_road)
    sorted_ambulances_per_road = dict(sorted(ambulances_per_road.items(), key=lambda item: item[1], reverse=True))
    print(sorted_ambulances_per_road)
    for i in sorted_ambulances_per_road:
        print(f'i = ', i)
        if sorted_ambulances_per_road[i] == 0:
            for j in sorted_cars_per_road:
                print(f'j =', j)
                if j in priority_list:
                    continue
                else:
                    priority_list.append(j)
                    print(priority_list)
                    continue
        else:
            priority_list.append(i)    
    priority_list_main = priority_list
    print(priority_list)