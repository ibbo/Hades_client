from client.gpio import *
import signal
import sys
from client.eventClient import EventClient

LIGHT_PIN = 7
setPinMode(OUTPUT, LIGHT_PIN)

def lightSwitchHandler(data):
    if not data:
        return
    s = data.split(':')
    switchId = int(s[0])
    switchState = s[1].strip() == 'true'
    if switchState:
        setPinData(HIGH, LIGHT_PIN)
    else:
        setPinData(LOW, LIGHT_PIN)

def signal_handler(signal, frame):
    setPinData(LOW, LIGHT_PIN)
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    ec = EventClient("192.168.1.137", 18000)
    ec.connect()
    ec.pollEvents(lightSwitchHandler)
