"""
  Display image on graphic LCD using Maker Nano RP2040 and CircuitPython.

  Items:
  - Maker Pi Pico
    https://my.cytron.io/p-maker-pi-pico
  - Maker Nano RP2040
    https://my.cytron.io/maker-nano-rp2040-simplifying-projects-with-raspberry-pi-rp2040
  - 0.96" 160x80 IPS LCD (ST7735)
    https://my.cytron.io/p-0.96-inch-160x80-ips-lcd-breakout-st7735
  - USB Micro B Cable
    https://my.cytron.io/p-usb-micro-b-cable

  Libraries required from bundle (https://circuitpython.org/libraries):
  - adafruit_st7735r.mpy

  References:
  - https://learn.adafruit.com/circuitpython-display-support-using-displayio/display-a-bitmap

  Last update: 20 Dec 2021
"""

import time
import board
import busio
import displayio
from adafruit_st7735r import ST7735R

# Release any resources currently in use for the displays
displayio.release_displays()

tft_clk = board.GP10  # SCL pin
tft_mosi = board.GP11  # SDA pin

spi = busio.SPI(tft_clk, MOSI=tft_mosi)
tft_rst = board.GP12
tft_dc = board.GP8
tft_cs = board.GP9  # Dummy

display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs, reset=tft_rst)
display = ST7735R(
    display_bus, rotation=90, width=160, height=80, rowstart=1, colstart=26, invert=True
)
