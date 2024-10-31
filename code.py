import time
import usb_hid
import lib.buttons as b
from lib.display import display
from lib.menu import Menu, MenuItem, MenuButtons
from lib.adafruit_hid.keyboard import Keyboard
from lib.adafruit_hid.keycode import Keycode
from lib.adafruit_hid.mouse import Mouse


def click(mouse: Mouse) -> None:
    """
    Generic left button click function
    :param mouse: mouse HID device
    """
    mouse.click(Mouse.LEFT_BUTTON)

def send_w_s_keys(keyboard: Keyboard) -> None:
    """
    Send w, pause, send s to move forward and back in a game
    :param keyboard: keyboard HID device
    """
    keyboard.send(Keycode.W)
    time.sleep(0.5)
    keyboard.send(Keycode.S)

if __name__ == '__main__':

    print("Klikspaan 1.0 booting...")

    # Initialise the HID devices
    kbd = Keyboard(usb_hid.devices)
    m = Mouse(usb_hid.devices)

    # Bind the input buttons
    buttons = MenuButtons(
        up=b.KEY_UP,
        down=b.KEY_DOWN,
        cancel=b.KEY_B,
        ok=b.KEY_A
    )

    # Create the user interface menu with the correct font
    menu = Menu(display=display, font="/assets/ib8x16u.bdf", buttons=buttons)
    menu.set_items([
        MenuItem(text="W/S (60s)", active=True, cb=lambda: send_w_s_keys(kbd), interval=30000),
        MenuItem(text="Muisklik (60s)", active=False, cb=lambda: click(m), interval=60000),
        MenuItem(text="Muisklik (1s)", active=False, cb=lambda: click(m), interval=1000),
    ])

    # display the menu on the display
    menu.display()

    while True:
        # listen to button presses and perform actions
        menu.listen()

        # let's throttle a bit
        time.sleep(.1)
