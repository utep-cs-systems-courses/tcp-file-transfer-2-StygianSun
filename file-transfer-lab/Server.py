#! /usr/bin/env python3

import sys, socket, re, os
from os.path import exists
sys.path.append("../lib")
import params
from framedSock import framedSend, framedReceive

switchesVarDefaults = (
    (('-l', '--listenPort'), 'listenPort', 50001),
    (('-d', '--debug'), 'debug', False),
    (('-?', '--usage'), 'usage', False),
    )

progname = 'echoServer'
paramMap = params.parseParams(switchesVarDefaults)

debug, listenPort = paramMap['debug'], paramMap['listenPort']

if paramMap['usage']:
    params.usage()

listsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
bindAddr = ("127.0.0.1", listenPort)
listsock.bind(bindAddr)
listsock.listen(3)
print("Listening on: ", bindAddr)
print("Waiting for a connection...")

while True:
    conn, addr = listsock.accept()
    print("Connecting to: ", addr)
    if not os.fork():
        while True:
            serverFile = open("serverFiles.txt","a+")
            serverFile.seek(0)
            serverContents = serverFile.read()
            file = framedReceive(conn,debug)
            if file is None:
                print("Done transferring files from client at: ", addr)
                break
            elif file.decode("utf-8") in serverContents:
                framedSend(conn,b"True",debug)
            else:
                framedSend(conn,b"False",debug)
                serverFile.write(file.decode("utf-8"))
                serverFile.write(": \n")
                try:
                    payload = framedReceive(conn,debug).decode()
                    if not payload or payload == "":
                        print("Done transferring file from client at: ", addr)
                        break
                    serverFile.write(payload)
                except:
                    print("Connection to the client was lost.")
                    break
                try:
                    framedSend(conn,str.encode("Server wrote file."),debug)
                except:
                    print("Connection to the client was lost.")
                    break
            serverFile.close()
