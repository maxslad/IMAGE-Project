"""
Demonstration of the GazeTracking library.
Check the README.md for complete documentation.
"""

import cv2
import math
import win32api
from win32api import GetSystemMetrics
from gaze_tracking import GazeTracking

width=GetSystemMetrics(0)/2
height=GetSystemMetrics(1)/2

a=40*38
limit_x=500
limit_y=500

gaze = GazeTracking()
webcam = cv2.VideoCapture(0)
_, frame = webcam.read()
gaze.refresh(frame)
frame = gaze.annotated_frame()

#iniital values
while True:
        try: 
                initial_x,initial_y=gaze.pupil_left_coords()
                if(initial_x!=None and initial_y!=None):
                        break
        except:
                print("Eye not found")
		
while True:
        # We get a new frame from the webcam
        _, frame = webcam.read()

        # We send this frame to GazeTracking to analyze it
        gaze.refresh(frame)

        frame = gaze.annotated_frame()


        try:
                x,y=gaze.pupil_left_coords()
                if x!=None and y!=None:
                        x-=initial_x
                        y-=initial_y
                        c_x=a/math.cos(abs(x))
                        c_y=a/math.cos(abs(y))
                        b_x=math.sqrt(c_x*c_x-a*a)
                        b_y=math.sqrt(c_y*c_y-a*a)
                        if(b_x<limit_x and b_y<limit_y):
                                if x<0:
                                        p_x=width+b_x
                                else:
                                        p_x=width-b_x
                                if y<0:
                                        p_y=height-b_y
                                else:
                                        p_y=height+b_y

                                win32api.SetCursorPos((int(p_x),int(p_y)))
        except:
                print("Eye not found")
        cv2.imshow("Demo", cv2.flip(frame,1))

        if cv2.waitKey(1) == 27:
                break
