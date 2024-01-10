# traffic-lights
  
## Required Files
Download yolo3.weights from <a href="https://pjreddie.com/media/files/yolov3.weights" download>here.</a>  
Download coco.names from [here](https://github.com/pjreddie/darknet/blob/master/data/coco.names)     
Download yolo3.cfg from [here](https://github.com/pjreddie/darknet/blob/master/cfg/yolov3.cfg)   
  
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
  
### Ver 1.2.3 (21/10/2023):
Improved upon the written code to count the number of cars and detect ambulances from the given camera and output the number of cars and ambulances in the video in the terminal.  
  
### Break to the project until Arduino ESP Camera arrives

### Ver 1.2.4 (09/01/2024):
Changed object_detector.py to take video input from local streaming url.  
  
### Ver 1.3.0:  
Wrote the logic for lane priority.  
Automatically takes into consideration the number of vehicles, ambulances and allots priority in a list.(currently slow af)  

### Ver 1.3.1:  
Sent the priority lane list to arduino.  
which has logic for traffic light timings.  
changes the lights according to alloted time.  
  
## The project code is done
