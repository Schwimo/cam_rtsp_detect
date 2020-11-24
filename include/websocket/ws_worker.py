#!/usr/bin/env python3

# sys imports
import sys

# custom imports 
from autobahn.twisted.websocket import WebSocketServerProtocol, WebSocketServerFactory
from twisted.internet.defer import Deferred, inlineCallbacks, returnValue
from twisted.python import log
from twisted.internet import reactor

class WebsocketWorker(WebSocketServerProtocol):

    def __init__(self, getFunc, ip="127.0.0.1", port=9090):
        """
        Initializes the WebsocketWorker and passes the func where to get the new data
        """

        log.startLogging(sys.stdout)

        self.getFunc = getFunc
        self.stopFlag = False
        self.port = port
        self.ip = ip
        
        address = "ws://" + self.ip + ":" + str(self.port)
        self.factory = WebSocketServerFactory(address)
        self.factory.protocol = WebsocketWorker

    def start_blocking(self):

        reactor.listenTCP(self.port, self.factory)
        reactor.run()

    def shutdown(self):

        self.stopFlag = True

    def onConnect(self, request):

        print("Client connecting: {0}".format(request.peer))

    def onOpen(self):

        print("WebSocket connection open.")

        self.still_connected = True
        self.sendImageData()   

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))
        self.still_connected = False

    def sendImageData(self):

        if not self.still_connected or self.stopFlag:
            return
        
        data = self.getFunc()
        if data != None:
            self.sendMessage(data)
        
        self.factory.reactor.callLater(0.2, self.sendImageData)
