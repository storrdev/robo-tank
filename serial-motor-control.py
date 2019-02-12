import math
import serial
import xbone
from tank import Tank

# Create and connect with the tank via usb
tank = Tank('/dev/ttyUSB0')

# This function is a loop that is passed to our XboxController instance
# so we can handle the commands coming from the Xbox controller
def inputLoop(state):
    tank.convertInputsToMotorInstructions(state['leftJoy']['x'], state['leftJoy']['y'], 0, 65536)
    
# Create an instance for the Xbox controller
xboxController = xbone.XboxOneController('/dev/input/event13', inputLoop)