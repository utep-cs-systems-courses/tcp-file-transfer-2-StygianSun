#! /usr/bin/env python3

import socket, sys, re
import os.path
from os import path
from os.path import exists
sys.path.append("../lib")
import params

from framedSock import framedSend, framedReceive

switchesVarDefaults = (
    (('-s', '--server'), 'server', "127.0.0.1:50001"),
    (('-d', '--debug'), 'debug', False),
    (('-?', '--usage'), 'usage', False),
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
    print("Can't parse server:port from '%s'" % server)
    sys.exit(1)

addrFamily = socket.AF_INET
socktype = socket.SOCK_STREAM
addrPort = (serverHost, serverPort)

s = socket.socket(addrFamily, socktype)

if s is None:
    print("Could not open socket.")
    sys.exit(1)

s.connect(addrPort)
run = True
while run:
    toSend = input("What file would you like to send? Enter $exit to exit the file client. ")
    if toSend == "$exit":
        print("Exiting")
        run = False
        sys.exit(1)
    if exists(toSend):
        file = open(toSend, 'r')
        fileData = file.read()
        if len(fileData) == 0:
            print("'%s' did not send because it is empty." % toSend)
            pass
        else:
            framedSend(s,toSend.encode(),debug)
            fileCheck = framedReceive(s,debug).decode()
            if fileCheck == "True":
                print("'%s' did not send because it is already in the server." % toSend)
                pass
            else:
                try:
                    framedSend(s, str.encode(fileData), debug)
                except:
                    print("Connection to the server was lost...")
                    sys.exit(0)
                try:
                    servMsg = framedReceive(s,debug).decode()
                    print("Server reports: %s" % servMsg)
                except:
                    print("Connection to the server was lost...")
                    sys.exit(0)
    else:
        print("'%s' did not send because it doesn't exist." % toSend)
        
