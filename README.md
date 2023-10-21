# traffic-lights
  
## Required Files
Download yolo3.weights from <a href="https://pjreddie.com/media/files/yolov3.weights" download>here.</a>  
Download coco.names from <a href="[https://github.com/pjreddie/darknet/blob/master/data/coco.names](https://github.com/pjreddie/darknet/blob/master/data/coco.names)" download>here.</a>  
Download yolo3.cfg from <a href="[blob:https://github.com/f42f5760-69c3-4e9a-957e-0e1c39d297ca](https://github.com/pjreddie/darknet/blob/master/cfg/yolov3.cfg)" download>here.</a>  
  
## Required Python Modules:
 1.opencv-python  
 2.numpy  
  
## How to Run?
 Install the neccessary modules and download the required files.  
 Download the object_detector.py and run it.

### Ver 1.1.1:
Wrote a basic code to start camera and detect the objects stated in coco.names using yolov3, opencv and numpy.  
Currently just detects the objects and marks them with a title and a box.  
  
### Ver 1.2.1:
Improved upon the written code to count the number of cars from the video and returns the real time count in the terminal.  
  
### Ver 1.2.2:
Improved upon the written code to ONLY count the number of cars from the video and put the code to do so in a class so that it is reusable.  
