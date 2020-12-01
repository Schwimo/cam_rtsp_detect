#!/usr/bin/env python3

import sys    
import threading
import cv2
import base64
import numpy as np
import os
import logging
import time

from utils.image_utils import *

class RtspWorker(threading.Thread):
    
    def __init__(self, ip, username, password, show=True, port=554, profile="main"):
        """
        :param ip: Camera IP
        :param username: Camera Username
        :param password: Camera User Password
        :param port: RTSP port
        :param profile: "main" or "sub"
        :param use_upd: True to use UDP, False to use TCP
        :param proxies: {"host": "localhost", "port": 8000}
        """
        
        self.stopFlag = False
        self.scalePercent = 100
        
        threading.Thread.__init__(self)

        self.ip = ip
        self.username = username
        self.password = password
        self.port = port
        self.hasDisplay = show        
        self.startUp = True
                
        self.url = "rtsp://" + self.username + ":" + self.password + "@" + \
            self.ip + ":" + str(self.port) + "//h264Preview_01_" + profile
        
        self.cap = cv2.VideoCapture(self.url)                

    def log_message(self, msg):

        print(msg)
        logging.info(msg)

    def shutdown(self):

        self.stopFlag = True
        self.log_message(f"{self.__class__.__name__}: Shutdown the rtsp stream.")        

    def restart(self):
        
        if self.hasDisplay:
            cv2.destroyAllWindows()            

        self.log_message(f"{self.__class__.__name__}: No valid image. Restarting the rtsp stream.")
        self.cap.release()
        self.cap = cv2.VideoCapture(self.url)           
        
    def run(self):

        while not self.stopFlag:

            ret, self.frame = self.cap.read()
            
            if not ret:
                self.restart()
                continue
                        
            try:                
                if self.hasDisplay:
                    cv2.imshow('frame', self.frame)      

                    if cv2.waitKey(1) & 0xff == ord('q'):
                        break
            except:
                self.hasDisplay = False
                pass
            
            if self.stopFlag:
                break
        
        self.stopFlag = True
        self.cap.release()

        if self.hasDisplay:
            cv2.destroyAllWindows()

    def get_image(self):

        if hasattr(self, 'frame'):   
            return self.frame
        else:
            return None

    def get_data(self):

        if hasattr(self, 'frame'):            
            
            if np.shape(self.frame) == ():
                return None

            resized_image = resize_image(self.scalePercent, self.frame)
            data = base64.b64encode(cv2.imencode('.jpg', resized_image)[1]).decode()
            return data

        else:
            return None
