#! /usr/bin/env python3

import socket, sys, re
from os import path
from os.path import exists
sys.path.appen("../../lib")
import params

from encapSock import EncapSock

switchesVarDefaults = (
    (('-s', '--server'), "server", "127.0.0.1:50001"),
    (('-d', '--debug'), "debug", False),
    (('-?', '--usage'), "usage", False),
    )

progname = "fileClient"
paramMap = params.parseParams(switchesVarDefaults)

server, usage, debug = paramMap["server"], paramMap["usage"], paramMap["debug"]

if usage:
    params.usage()

try:
    serverHost, serverPort = re.split(":", server)
    serverPort = int(serverPort)
except:
    print("Can't parse server: port from '%s'" % server)
    sys.exit(1)

addrFamily = socket.AF_INET
socktype = socket.SOCK_STREAM
addrPort = (serverHost, serverPort)

s = socket.socket(addrFamily, socktype)

if s is None:
    print("Could not open socket.")
    sys.exit(1)

s.connect(addrPort)

esock = EncapSock((sock, addrPort))
run = True
while run:
    toSend = input("What file would you like to send? Enter $exit to exit the file client.")
    if toSend == "$exit":
        print("Exiting")
        run = False
        sys.exit(1)
    if exists(toSend):
        file = open(toSend, 'rb')
        payload = file.read()
        if len(payload) == 0:
            print("'%s' did not send because it is empty." % toSend)
            pass
        else:
            esock.send(fileName.encode(), debug)
            fileCheck = esock.receive(debug).decode()
            if fileCheck == "True":
                print("'%s' did not send because it is already in the server." % toSend)
                pass
            else:
                try:
                    esock.send(payload,debug)
                    print("Server reports: ", esock.receive(debug).decode())
                except:
                    print("Connection to the server was lost...")
                    sys.exit(0)
    else:
        print("'%s' does not exist." % fileName)
