# traffic-lights
  
## Required Files
Download yolo3.weights from <a href="https://pjreddie.com/media/files/yolov3.weights" download>here.</a>  
Download coco.names <a href="blob:https://github.com/516335cd-7c8e-4628-a551-27b05452edf8" download>here.</a>  
Download yolo3.cfg <a href="blob:https://github.com/f42f5760-69c3-4e9a-957e-0e1c39d297ca" download>here.</a>  
  
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