import time
import usb_hid
import lib.buttons as b
from lib.display import display
from lib.menu import Menu, MenuItem, MenuButtons
from lib.adafruit_hid.keyboard import Keyboard
from lib.adafruit_hid.keycode import Keycode
from lib.adafruit_hid.mouse import Mouse

def click(mouse):
    mouse.click(Mouse.LEFT_BUTTON)

def send_w_s_keys(keyboard):
    keyboard.send(Keycode.W)
    time.sleep(0.5)
    keyboard.send(Keycode.S)

if __name__ == '__main__':

    print("Klikspaan 1.0 booting...")

    kbd = Keyboard(usb_hid.devices)
    m = Mouse(usb_hid.devices)

    buttons = MenuButtons(
        up=b.KEY_UP,
        down=b.KEY_DOWN,
        cancel=b.KEY_B,
        ok=b.KEY_A
    )

    menu = Menu(display=display, font="/assets/ib8x16u.bdf", buttons=buttons)
    menu.set_items([
        MenuItem(text="W/S (60s)", active=True, cb=lambda: send_w_s_keys(kbd), interval=30000),
        MenuItem(text="Muisklik (60s)", active=False, cb=lambda: click(m), interval=60000),
        MenuItem(text="Muisklik (1s)", active=False, cb=lambda: click(m), interval=1000),
    ])

    menu.display()

    while True:
        menu.listen()
        time.sleep(.1)
