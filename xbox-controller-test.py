import xbone

def inputEvent(state):
  print(state)

xboxController = xbone.XboxOneController('/dev/input/event13', inputEvent)