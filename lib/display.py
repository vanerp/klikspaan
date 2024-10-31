import board
import busio
import displayio
from adafruit_st7735r import ST7735R

displayio.release_displays()

tft_clk = board.GP10  # SCL pin
tft_mosi = board.GP11  # SDA pin

spi = busio.SPI(tft_clk, MOSI=tft_mosi)
tft_rst = board.GP12
tft_dc = board.GP8
tft_cs = board.GP9  # Dummy

# initialize the display bus
display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs, reset=tft_rst)

# bind the display bus to the display
display = ST7735R(
    display_bus, rotation=90, width=160, height=80, rowstart=1, colstart=26, invert=True
)
