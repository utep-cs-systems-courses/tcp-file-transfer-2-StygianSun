#! /usr/bin/env python3

import sys
sys.path.append("../../lib")
import re, socket, params, os
from os.path import exists

switchesVarDefaults = (
    (('-l', '--listenPort'), 'listenPort', 50001),
    (('-d', '--debug'), "debug", False),
    (('-?', '--usage'), "usage", False),
    )

progname = "threadServer"
paramMap = params.parseParams(switchesVarDefaults)

dbug, listenPort = paramMap['debug'], paramMap['listenPort']

if paramMap['usage']:
    params.usage()

listsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
bindAddr = ("127.0.0.1", listenPort)
listsock.bind(bindAddr)
listsock.listen(3)
print("Listening on: ", bindAddr)
print("Waiting for a connection...")

from threading import Thread
from encapSock import EncapSock

class Server(Thread):
    def __init__(self, sockAddr):
        Thread.__init__(self)
        self.sock, self.addr = sockAddr
        self.esock = EncapSock(sockAddr)
    def run(self):
        print("New thread handling connection from: ", self.addr)
        while True:
            filename = self.esock.receive(debug)
            print("Checking server for: ", filename.decode())
            newFile = "new" + filename.decode()
            print(newFile)
            if exists(newFile):
                self.esock.send(b"True", debug)
                payload = self.esock.receive(debug)
                outfile = open(newFile,"wb")
                outfile.write(filename)
                outfile.write(payload)
                self.esock.send(b"Wrote new file",debug)

while True:
    scokAddr = listsock.accept()
    server = Server(sockAddr)
    server.start()
