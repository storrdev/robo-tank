from evdev import InputDevice, categorize, ecodes, list_devices

class XboxOneController:
  def __init__(self, input, callback):
    self.gamepad = InputDevice(input)
    self.state = {
      'leftJoy': {
        'x': 0,
        'y': 0
      }
    }

    for event in self.gamepad.read_loop():
      if event.type == ecodes.EV_ABS: # Analog stuff
        # print(event.code)
        if event.code == 0:
          self.state['leftJoy']['x'] = event.value
        elif event.code == 1:
          self.state['leftJoy']['y'] = event.value

      callback(self.state)