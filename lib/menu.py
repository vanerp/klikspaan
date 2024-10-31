from adafruit_st7735r import ST7735R
import displayio
from lib.adafruit_bitmap_font import bitmap_font
from lib.adafruit_display_text import label
import time
import terminalio

COLOR = 0xFFFFFF
ACTIVE_COLOR = 0xFFFF00
RUNNING_COLOR = 0xF00FF

class MenuButtons:
    def __init__(self, up, down, cancel, ok):
        self.cancel = cancel
        self.down = down
        self.up = up
        self.ok = ok


class MenuItem:
    def __init__(self, text: str, active: bool, cb, interval):
        self.cb = cb
        self.active = active
        self.text = text
        self.interval = interval #ms


class Menu:
    def __init__(self, display: ST7735R, font: str, buttons: MenuButtons):
        self._font = bitmap_font.load_font(font)
        self._display = display
        self._items = []
        self.buttons = buttons
        self.index = 0
        self.previous_index = 0
        self.current_action = None
        self.current_action_last_run = None
        self.current_action_index = None
        self.current_action_interval = None
        self.button_states = {
            "ok": {
                "state": False,
                "previous": False
            },
            "cancel": {
                "state": False,
                "previous": False
            },
            "down": {
                "state": False,
                "previous": False
            },
            "up": {
                "state": False,
                "previous": False
            },
        }
        self.clear()

    def set_items(self, items: []):
        self._items = items

    def display_row(self, item: MenuItem, row_nr: int):
        y = (row_nr + 1) * 20

        text = f"  {item.text}"
        color = COLOR
        if item.active:
            text = f"> {item.text}"
            color = ACTIVE_COLOR

        if self.current_action is not None and self.current_action_index == row_nr:
            color = RUNNING_COLOR

        text_area = label.Label(self._font, text=text, color=color)
        text_area.x = 10
        text_area.y = y
        self._display.root_group.append(text_area)

    def reset(self):
        self.index = 0
        self.current_action = None
        self.clear()
        self.display()

    def clear(self):
        splash = displayio.Group()
        self._display.root_group = splash

    def display(self):
        row_nr = 0
        for idx, i in enumerate(self._items):
            self._items[idx].active = False
            if idx == self.index:
                self._items[idx].active = True
            self.display_row(i, row_nr)
            row_nr = row_nr + 1

    def get_current_action(self):
        return self._items[self.index].interval, self._items[self.index].cb

    def run_action(self):
        if self.current_action is not None:
            if self.current_action_last_run is None:
                self.current_action()
                self.current_action_last_run = self.ns_to_ms(time.monotonic_ns())
            else:
                diff = self.ns_to_ms(time.monotonic_ns()) - self.current_action_last_run
                if diff >= self.current_action_interval:
                    self.current_action()
                    self.current_action_last_run = self.ns_to_ms(time.monotonic_ns())

    @staticmethod
    def ns_to_ms(ns):
        return ns / 1_000_000

    def listen(self):

        self.button_states["cancel"]["state"] = not self.buttons.cancel.value
        if self.button_states["cancel"]["state"] == False and self.button_states["cancel"]["previous"] == True:
            print("reset")
            self.reset()
        self.button_states["cancel"]["previous"] = self.button_states["cancel"]["state"]

        self.button_states["ok"]["state"] = not self.buttons.ok.value
        if self.button_states["ok"]["state"] == False and self.button_states["ok"]["previous"] == True:
            self.current_action_index = self.index
            self.current_action_interval, self.current_action = self.get_current_action()
        self.button_states["ok"]["previous"] = self.button_states["ok"]["state"]

        self.button_states["down"]["state"] = not self.buttons.down.value
        if self.button_states["down"]["state"] == False and self.button_states["down"]["previous"] == True:
            self.index = self.index + 1
        self.button_states["down"]["previous"] = self.button_states["down"]["state"]

        self.button_states["up"]["state"] = not self.buttons.up.value
        if self.button_states["up"]["state"] == False and self.button_states["up"]["previous"] == True:
            self.index = self.index - 1
        self.button_states["up"]["previous"] = self.button_states["up"]["state"]

        if self.index >= len(self._items):
            self.index = 0
        if self.index < 0:
            self.index = len(self._items) - 1

        if self.previous_index != self.index:
            self.clear()
            self.display()
            self.previous_index = self.index

        self.run_action()