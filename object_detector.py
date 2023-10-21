import cv2
import numpy as np

class Camera:
    def __init__(self, camera_id, names_path, config_path, weights_path, conf_threshold=0.5, nms_threshold=0.3):
        self.camera_id = camera_id
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
                    confs.append(float(confidence)
        )

        indices = cv2.dnn.NMSBoxes(bbox, confs, self.confThreshold, self.nmsThreshold)
        car_count = 0
        for i in indices:
            box = bbox[i]
            x, y, w, h = box[0], box[1], box[2], box[3]
            if self.classNames[classIds[i]].lower() == 'car':
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 255), 2)
                cv2.putText(frame, f'Car {int(confs[i]*100)}%', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 255), 2)
                car_count += 1

        return frame, car_count

    def process_video(self):
        cap = cv2.VideoCapture(self.camera_id)
        while True:
            success, frame = cap.read()
            if not success:
                break
            frame, car_count = self.process_frame(frame)
            print(f'Camera {self.camera_id}: Number of cars: {car_count}')
            cv2.imshow(f'Camera {self.camera_id}', frame)
            cv2.waitKey(1)

if __name__ == "__main__":
    # Example usage for camera 0
    camera0 = Camera(0, '/home/pranav/Downloads/Traffic/traffic-lights-bitches/coco.names',
                     '/home/pranav/Downloads/Traffic/traffic-lights-bitches/yolov3.cfg',
                     '/home/pranav/Downloads/Traffic/traffic-lights-bitches/yolov3.weights')
    camera0.process_video()