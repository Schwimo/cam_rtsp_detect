#!/usr/bin/env python3

import json
import sys    
import threading
import cv2
import base64
import numpy as np
import os

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
        
        self.url = "rtsp://" + self.username + ":" + self.password + "@" + \
            self.ip + ":" + str(self.port) + "//h264Preview_01_" + profile

        self.cap = cv2.VideoCapture(self.url)

    def shutdown(self):

        self.stopFlag = True

    def run(self):

        while not self.stopFlag:

            ret, self.frame = self.cap.read()

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
        
        self.cap.release()

        if self.hasDisplay:
            cv2.destroyAllWindows()

    def resizeImage(self, frame, scalePercentage):

        width = int(frame.shape[1] * scalePercentage / 100)
        height = int(frame.shape[0] * scalePercentage / 100)
        dim = (width, height)

        # resize image
        resized = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)
        return resized    

    def get(self):

        if hasattr(self, 'frame'):            
            
            if np.shape(self.frame) == ():
                return None

            data = self.resizeImage(self.frame, self.scalePercent)
            dict = {       
                'img': base64.b64encode(cv2.imencode('.jpg', data)[1]).decode()
            }   
            retVal = json.dumps(dict).encode('utf-8')
            return retVal

        else:
            return None
