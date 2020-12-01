#!/usr/bin/env python3

import threading
import time
import cv2

from utils.image_utils import *

class Detector(threading.Thread):

    def __init__(self, getFunc):

        self.baseFrame = None
        self.stopFlage = False
        self.getFunc = getFunc        
        self.count = 0
        self.motionDetected = False
        
        threading.Thread.__init__(self)

    def shutdown(self):

        self.stopFlage = True

    def run(self):

        while not self.stopFlage:

            self.detect_movement()
            time.sleep(0.1)
                   
    def detect_movement(self):
        
        frame = self.getFunc()

        if frame is None:
            return

        frame = resize_image(40, frame)

        # Convert to gray and apply gaussian blur to smoothen        
        grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        grayFrame = cv2.GaussianBlur(grayFrame, (25,25), 0)

        # Set the base frame if not done
        if self.baseFrame is None or self.count >= 1000:
            self.baseFrame = grayFrame
            self.count = 0;
        
        # Get the different pixels
        delta = cv2.absdiff(self.baseFrame, grayFrame)
        threshold = cv2.threshold(delta, 30, 255, cv2.THRESH_BINARY)[1]
        (contours,_) = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            if cv2.contourArea(contour) < 5000:
                continue
            
            self.motionDetected = True  
            (x, y, w, h) = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 1)

        #cv2.imshow("gray_frame Frame",grayFrame)
        #cv2.imshow("Delta Frame",delta)
        #cv2.imshow("Threshold Frame",threshold)
        cv2.imshow("Color Frame",frame)

        self.count += 1

        if cv2.waitKey(1) & 0xff == ord('q'):
            self.stopFlage = True
        
