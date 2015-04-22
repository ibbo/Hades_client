import socket
import time
import socketController as sc

class EventClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def connect(self):
        self.socket = socket.create_connection((self.host, self.port))

    def defaultEventHandler(data):
        print(repr(data))

    def pollEvents(self, eventHandler=defaultEventHandler):
        while True:
            data = self.socket.recv(1024)
            eventHandler(data)
            time.sleep(1)

def switchHandler(data):
    if not data:
        return
    print("Received: %s" % data)
    s = data.split(':')
    switchId = int(s[0])
    switchState = s[1].strip() == 'true'
    if switchState:
        print("Switch %d is on" % switchId)
        sc.turnOnSocket()
    else:
        print("Switch %d is off" % switchId)
        sc.turnOffSocket()

if __name__ == "__main__":
    ec = EventClient("localhost", 18000)
    ec.connect()
    ec.pollEvents(switchHandler)
