#!/usr/bin/env python3

# sys imports
import sys
import threading
import json

# custom imports
from autobahn.twisted.websocket import WebSocketServerProtocol, WebSocketServerFactory
from twisted.python import log
from twisted.internet import reactor

getFunc = {}
stopFlag = False
connectedClients = 0


class WebsocketWorker(WebSocketServerProtocol):

    stillConnected = False

    def onConnect(self, request):
        #global connectedClients
        global connectedClients
        connectedClients += 1
        print("Client connecting: {0}  Clients: {1}".format(
            request.peer, connectedClients))

    def onOpen(self):
        print("WebSocket connection open.")
        self.stillConnected = True
        self.sendImageData()

    def onClose(self, wasClean, code, reason):
        global connectedClients

        if connectedClients >= 1:
            connectedClients -= 1
            
        print("WebSocket connection closed: {0} Clients: {1}".format(reason, connectedClients))        
        self.stillConnected = False        

    def sendImageData(self):

        if not self.stillConnected or stopFlag:
            return

        global connectedClients            
        data = getFunc()

        if data == None:
            self.factory.reactor.callLater(0.5, self.sendImageData)
            return

        dict = {       
               'img': data,
               'watching': connectedClients       
            }

        json_data = json.dumps(dict).encode('utf-8')        
        self.sendMessage(json_data)
        self.factory.reactor.callLater(0.1, self.sendImageData)
       

def shutdown():
    global stopFlag
    stopFlag = True

def start(func, ip="127.0.0.1", port=9090):

    address = "wss://" + ip + ":" + str(port)
    global getFunc
    getFunc = func

    log.startLogging(sys.stdout)

    factory = WebSocketServerFactory(address)
    factory.protocol = WebsocketWorker    

    reactor.listenTCP(port, factory)        
    reactor.run()
