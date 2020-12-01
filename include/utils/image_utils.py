#!/usr/bin/env python3

import cv2

def resize_image(scaleFactor, frame):
        
    width = int(frame.shape[1] * scaleFactor / 100)
    height = int(frame.shape[0] * scaleFactor / 100)
    dim = (width, height)

    # resize image
    resized = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)

    return resized    
