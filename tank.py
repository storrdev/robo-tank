# Tank
#
# A class for interacting with my robot tank
# Stephen Orr

import math
import serial
import time

class Tank:
  def __init__(self, usb):
    # Connect with the arduino nano via usb so we can read/send commands
    self.ser = serial.Serial(usb, baudrate = 9600, timeout = 1)

    # Sleep for 3 seconds to let the arduino boot up before attempting to connect
    time.sleep(3)

    # Set flag for the arduino being ready so we can use it later to check before
    # attempting to communicate with the arduino over serial
    self.arduinoReady = False

    # Initialize motor variables
    self.leftSpeed = 0
    self.leftDirection = True

    self.rightSpeed = 0
    self.rightDirection = True

    # Wait for command from arduino to let us know that it's connected
    # via serial and ready to recieve commands
    while not (self.arduinoReady):
        ready = self.ser.readline()

        if ready.decode() == '<Arduino is ready>\r\n':
            print(ready.decode().strip('\r\n'))
            self.arduinoReady = True

  # Function sendCommand
  # 
  # This function takes an array of data and structures it to be read by
  # the arduino. It converts everything to bytes to be as efficient as possible
  # because the arduino can only read one byte at a time on the other end
  def sendCommand(self, command):
    
    byteCommand = bytes('<', 'utf-8') + bytes(command) + bytes('>', 'utf-8')

    # Sends converted command to arduino via serial communication over usb
    # and returns the amount of sent bytes
    return self.ser.write(byteCommand)

  def convertInputsToMotorInstructions(self, x, y, minVal, maxVal):
    # Reverse values because inputs start 0,0 in the top right, and max out in the bottom right of the coordinate plane
    y = maxVal - y
    x = maxVal - x

    # Calculate center
    center = (maxVal - minVal) / 2

    deltaX = (center - x) * 2
    deltaY = (center - y) * 2
    
    leftDelta = deltaX - deltaY
    rightDelta = -deltaX - deltaY

    # Convert speeds to "byte" size
    leftSpeed = int(abs((255 / maxVal) * leftDelta))
    rightSpeed = int(abs((255 / maxVal) * rightDelta))

    if leftSpeed > 255:
      leftSpeed = 255
    
    if rightSpeed > 255:
      rightSpeed = 255

    leftDirection = int(bool((leftDelta / abs(leftDelta)) > 0))
    rightDirection = int(bool((rightDelta / abs(rightDelta)) > 0))

    # Send Xbox controller commands to arduino
    self.sendCommand([leftSpeed, leftDirection, rightSpeed, rightDirection])