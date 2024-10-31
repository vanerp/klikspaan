import time
import board
import digitalio
import microcontroller

# KEY_UP = Pin(2,Pin.IN,Pin.PULL_UP)
# KEY_DOWN = Pin(18,Pin.IN,Pin.PULL_UP)
# KEY_LEFT= Pin(16,Pin.IN,Pin.PULL_UP)
# KEY_RIGHT= Pin(20,Pin.IN,Pin.PULL_UP)
# KEY_CTRL=Pin(3,Pin.IN,Pin.PULL_UP)
# KEY_A=Pin(15,Pin.IN,Pin.PULL_UP)
# KEY_B=Pin(17,Pin.IN,Pin.PULL_UP)


def set_button(pin: microcontroller.Pin, pull: digitalio.Pull) -> digitalio.DigitalInOut:
    btn = digitalio.DigitalInOut(pin)
    btn.pull = pull
    return btn

KEY_A = set_button(board.GP15, digitalio.Pull.UP)
KEY_B = set_button(board.GP17, digitalio.Pull.UP)
KEY_UP = set_button(board.GP2, digitalio.Pull.UP)
KEY_DOWN = set_button(board.GP18, digitalio.Pull.UP)



