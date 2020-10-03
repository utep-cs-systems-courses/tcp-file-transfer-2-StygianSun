#! /usr/bin/env python3

import socket, sys, re
import os.path
from os import path

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
sentFiles = []
files = ["testFile.txt","ghostFile.txt","testFile2.txt","testFile3.txt"]

def is_empty_file(filename):
    return (os.path.isfile(filename) and (os.path.getsize(filename) > 0))

for file in files:
    if not path.isfile(file):
        print("'%s' did not send becuase it doesn't exist." % file)
        pass
    elif not is_empty_file(file):
        print("'%s' did not send because it is empty." % file)
        pass
    else:
        if file in sentFiles:
            print("'%s' was already sent to server." % file)
            pass
        else:
            print("Sending %s to Server..." % file)
            framedSend(s, str.encode(file),debug)
            #sentFiles.append(file)
            try:
                msg = "$exit"
                with open(file, "r") as f:
                    for line in f:
                        framedSend(s,str.encode(line),debug)
                        print("Server Received: ", framedReceive(s,debug))
                    print("Server Coppied: '%s'\n" % file)
                framedSend(s,str.encode(msg),debug)
                f.close()
            except IOError:
                print("'%s' could not be found and wasn't opened." % file)
f.close()
s.close()
