#! /usr/bin/env python3

import sys
sys.path.append("../lib")
import re,socket,params

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
listsock.listen(1)
print("Listening on: ", bindAddr)
print("Waiting for a connection...")

conn, addr = listsock.accept()

print(addr, "is connected to the server.")

from framedSock import framedSend, framedReceive
file = open("ServerFiles.txt", "w")
filesReceived = []

while True:
    fileName = framedReceive(conn,debug)
    if fileName in filesReceived:
        print("%s has already been received." % fileName)
        break
    elif fileName is None:
        break
    else:
        filesReceived.append(fileName)

        file.write("Contents of '%s'\n" % fileName)
        payload = framedReceive(conn, debug)
        if debug: print("Receiving:", payload)
        if not payload:
            print("Done transferring files. Disconnecting client.")
            break
        file.write(payload.decode("utf-8"))
        framedSend(conn,payload,debug)

print("Server wrote the following to ServerFiles.txt")
for x in filesReceived:
    print(x)
file.close()
listsock.close()
