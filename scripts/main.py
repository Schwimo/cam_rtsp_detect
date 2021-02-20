#!/usr/bin/env python3

# system imports
import argparse
import sys
import time
import threading
import logging
import os

# custom iports
from rtsp.rtsp_worker import RtspWorker
import websocket.ws_worker
from detection.animal_detector import Detector

shutdown = False
            
if __name__ == '__main__':

    # Initialize parser
    msg = "Example Usage " \
          " Startup only rtsp: "  \
          " python rtsp.py -"
    parser = argparse.ArgumentParser(description = msg)

    # Adding optional argument
    parser.add_argument("-u", "--Username", help = "Username for the rtsp stream")
    parser.add_argument("-p", "--Password", help = "Password for the rtsp stream")
    parser.add_argument("-a", "--Address", help = "Adress for the rtsp ip cam")
    parser.add_argument("-d", "--Detection", help = "Start the detection or not", action='store_true')
    parser.add_argument("-ho", "--HideOutput", help = "Hide the output", action='store_false')

    args = parser.parse_args()
    
    if not args.Username:
        print("No useranme given, exiting application.")
        sys.exit()

    if not args.Password:
        print("No password given, exiting application.")
        sys.exit()

    dirPath = os.path.dirname(os.path.realpath(__file__)) + "/watchdog_log"
    logging.basicConfig(filename=dirPath, level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%d-%m-%Y %H:%M:%S')
    logging.info("Starting application.")

    # Start the rtsp stream
    rtsp_worker = RtspWorker(args.Address, args.Username, args.Password, args.HideOutput)
    rtsp_worker.start()

    logging.info("Started the rtsp worker.")
    
    # Start the detection
    if args.Detection:        
        det_worker = Detector(rtsp_worker.get_image)
        det_worker.start()          
        logging.info("Movement detection started.")

    # Start the websocket factory    
    websocket.ws_worker.start(rtsp_worker.get_data)    

    # Shutdown everything
    if args.Detection:        
        det_worker.shutdown() 
        
    rtsp_worker.shutdown()
    websocket.ws_worker.shutdown()
    
    print("Shutdown everything and close app.")