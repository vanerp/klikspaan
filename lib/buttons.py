import time
import board
import digitalio
import microcontroller


def set_button(pin: microcontroller.Pin, pull: digitalio.Pull) -> digitalio.DigitalInOut:
    btn = digitalio.DigitalInOut(pin)
    btn.pull = pull
    return btn

KEY_A = set_button(board.GP15, digitalio.Pull.UP)
KEY_B = set_button(board.GP17, digitalio.Pull.UP)
KEY_UP = set_button(board.GP2, digitalio.Pull.UP)
KEY_DOWN = set_button(board.GP18, digitalio.Pull.UP)



