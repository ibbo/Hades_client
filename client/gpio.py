#!/usr/bin/env python
import os

GPIO_MODE_PATH = os.path.normpath('/sys/devices/virtual/gpio/mode/')
GPIO_PIN_PATH = os.path.normpath('/sys/devices/virtual/gpio/pin/')
GPIO_FILENAME = "gpio"

pinMode = []
pinData = []

HIGH = "1"
LOW = "0"
INPUT = "0"
OUTPUT = "1"
INPUT_PU = "8"

def getModePath(pinNum):
  return os.path.join(GPIO_MODE_PATH, 'gpio'+str(pinNum))

def getDataPath(pinNum):
  return os.path.join(GPIO_PIN_PATH, 'gpio'+str(pinNum))

def setPinMode(mode, pinNum):
  f = file(getModePath(pinNum), 'r+')
  f.write(mode)
  f.close()

def setPinData(data, pinNum):
  try:
    [setSinglePin(data, i) for i in pinNum]
  except TypeError:
    setSinglePin(data, pinNum)

def setSinglePin(data, pinNum):
  f = file(getDataPath(pinNum), 'r+')
  f.write(data)
  f.close()
