import cv2
import numpy as np
import requests
import socket



class Camera:
    def _init_(self, camera_number, stream_url, names_path, config_path, weights_path, conf_threshold=0.5, nms_threshold=0.3):
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
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 255), 2)
                cv2.putText(frame, f'Car {int(confs[i]*100)}%', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 255), 2)
                car_count += 1
            elif self.classNames[classIds[i]].lower() == 'truck':
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Green for ambulances
                cv2.putText(frame, f'Ambulance {int(confs[i]*100)}%', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                ambulance_count += 1

        return frame, car_count, ambulance_count

    def process_video(self):
        while True:
            frame = self.get_frame_from_stream()
            frame, car_count, ambulance_count = self.process_frame(frame)
            print(f'CameraNumber = {self.camera_number},Number of cars: {car_count}, Number of ambulances: {ambulance_count}')
            cv2.imshow('Stream', frame)
            if cv2.waitKey(30) & 0xFF == ord('q'):
                break
            
if _name_ == "_main_":
    # Example usage for streaming from ESP32
    esp32_stream_url1 = 'http://192.168.137.30:8080/'  # Modify this URL accordingly
    camera_esp32 = Camera(1,esp32_stream_url1, 'coco.names', 'yolov3.cfg', 'yolov3.weights')
    camera_esp32.process_video()