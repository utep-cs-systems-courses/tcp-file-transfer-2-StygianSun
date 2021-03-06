import re

class EncapSock:
    def __init__(self, sockAddr):
        self.sock, self.addr = sockAddr
        self.rbuf = b""
    def close(self):
        return self.sock.close()
    def send(self, payload, debug=0):
        if debug: print("encapSend: sending %d byte mesage" % len(payload))
        msg = str(len(payload)).encode() + b":" + payload
        while len(msg):
            nsent = self.sock.send(msg)
            msg = msg[nsent:]
    def receive(self, debug=0):
        state = "getLength"
        msgLength = -1
        while True:
            if(state == "getLength"):
                match = re.match(b'([^:]+):(.*)', self.rbuf, re.DOTALL | re.MULTILINE)
                if match:
                    lengthStr, self.rbuf = match.groups()
                    try:
                        msgLength = int(lengthStr)
                    except:
                        if len(self.rbuf):
                            print("Badly formed message length:", lengthStr)
                            return None
                    state = "getPayload"
            if(state == "getPayload"):
                if len(self.rbuf) >= msgLength:
                    payload = self.rbuf[0:msgLength]
                    self.rbuf = self.rbuf[msgLength:]
                    return payload
            r = self.sock.recv(100)
            self.rbuf += r
            if len(r) == 0:
                if len(self.rbuf) != 0:
                    print("encapReceive: incomplete message.\n state=%s, length=%d, self.rbuf=%s" % (state, msgLength, self.rbuf))
                return None
            if debug: print("encapReceive: state=%s, length=%d, rbuf=%s" % (state, msgLength, self.rbuf))
