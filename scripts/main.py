
#!/usr/bin/env python3

# system imports
import argparse
import sys

# custom iports
from rtsp.rtsp_worker import RtspWorker
from websocket.ws_worker import WebsocketWorker

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
        print(f"No useranme given, exiting application.")
        sys.exit()

    if not args.Password:
        print(f"No password given, exiting application.")
        sys.exit()

    if args.Detection:
        print(f"Starting the detection... TBD")

    rtsp_worker = RtspWorker(args.Address, args.Username, args.Password, args.HideOutput)
    rtsp_worker.start()

    ws_worker = WebsocketWorker(rtsp_worker.get())
    ws_worker.start_blocking()
    
    rtsp_worker.shutdown()
    ws_worker.shutdown()

    print("Shutdown everything and close app.")