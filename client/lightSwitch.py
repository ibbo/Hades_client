import RPi.GPIO as GPIO
import signal
import sys
import time
from client.eventClient import EventClient


def setupGPIO():
    GPIO.setmode(GPIO.BOARD)
    # K0-K3 data inputs
    GPIO.setup(11, GPIO.OUT)
    GPIO.setup(15, GPIO.OUT)
    GPIO.setup(16, GPIO.OUT)
    GPIO.setup(13, GPIO.OUT)

    # ASK/FSK
    GPIO.setup(18, GPIO.OUT)

    # modulator
    GPIO.setup(22, GPIO.OUT)

    # Disable modulator
    GPIO.output(22, False)

    # Set modulator to ASK for On Off Keying
    # by setting MODSEL pin lo
    GPIO.output(18, False)

    # Init K0-K3 inputs of the encoder to 0000
    GPIO.output(11, False)
    GPIO.output(15, False)
    GPIO.output(16, False)
    GPIO.output(13, False)

def lightSwitchHandler(data):
    if not data:
        return
    s = data.split(':')
    switchId = int(s[0])
    switchState = s[1].strip() == 'true'
    switchLight(switchState)

def programPlug():
    switchLight(True)
    switchLight(False)
    switchAll(True)
    switchAll(False)

def switchLight(on):
    # Last pin determines on or off
    if on:
        GPIO.output(11, True)
        GPIO.output(15, True)
        GPIO.output(16, True)
        GPIO.output(13, True)
    else:
        GPIO.output(11, True)
        GPIO.output(15, True)
        GPIO.output(16, True)
        GPIO.output(13, False)

    # Send the signal by pulsing the modulator
    pulse_modulator()
    
def switchAll(on):
    if on:
        GPIO.output(11, True)
        GPIO.output(15, True)
        GPIO.output(16, False)
        GPIO.output(13, True)
    else:
        GPIO.output(11, True)
        GPIO.output(15, True)
        GPIO.output(16, False)
        GPIO.output(13, False)
    
    pulse_modulator()

def pulse_modulator():
    # let it settle, encoder requires this
    time.sleep(0.1)
    GPIO.output(22, True)
    time.sleep(0.25)
    GPIO.output(22, False)

def signal_handler(signal, frame):
    sys.exit(0)

def cleanup():
    switchLight(False)
    GPIO.cleanup()

setupGPIO()
if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    ec = EventClient("192.168.1.137", 18000)
    ec.connect()
    ec.pollEvents(lightSwitchHandler)
