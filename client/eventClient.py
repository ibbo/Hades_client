import zmq
import socket
import time
import socketController as sc
from crontab import CronSlices
from crontab import CronTab

def defaultEventHandler(data):
    print(repr(data))

class EventClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def connect(self):
        self.socket = socket.create_connection((self.host, self.port))

    def pollEvents(self, eventHandler=defaultEventHandler):
        while True:
            data = self.socket.recv(1024)
            eventHandler(data)
            time.sleep(1)

class EventServer:
    def __init__(self, port="5556"):
        self.port = port

    def start(self, eventHandler=defaultEventHandler):
        self.context = zmq.Context()
        self.serversocket = self.context.socket(zmq.PAIR)
        self.serversocket.bind("tcp://*:%s" % self.port)
        self.run(eventHandler)

    def run(self, eventHandler):
        while True:
            data = self.serversocket.recv()
            eventHandler(data)
            
def dispatchHandler(data):
    # TODO: Change this into a more robust dispatching mechanism
    if not data:
        return
    s = data.split(':')
    if s[0].strip() is "cron":
        print("CRON MESSAGE: %s" % data)
        cronHandler(data)
    else:
        print("SWITCH MESSAGE: %s" % data)
        switchHandler(data)

def cronHandler(data):
    if not data:
        return
    s = data.split(':')
    cronCommand = s[1].strip()
    if cronCommand not in ["on", "off"]:
        print("Cron command invalid, should be 'on' or 'off'. Command: %s" % cronCommand)
        return

    cronString = s[2].strip()
    if not CronSlices.is_valid(cronString):
        print("Cron time string invalid. Time string: %s" % cronString)
        return
    
    # Now we've validated the command, set a cron job
    cron_file = CronTab(tabfile="/etc/cron.d/lazytwinkle")
    job = cron_file.new(command="python /home/pi/Hades_client/client/socketController.py %s" % cronCommand)
    job.setall(cronString)
    job.enable()
    cron_file.write()

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
