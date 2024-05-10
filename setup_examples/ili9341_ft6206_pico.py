# ili9341_ft6206_pico.py Customise for your hardware config

# Released under the MIT License (MIT). See LICENSE.
# Copyright (c) 2021-2024 Peter Hinch

# As written, supports:
# ili9341 240x320 displays on Pi Pico.
# FT6206 touch controller.
# https://www.adafruit.com/product/1947
# Edit the driver import for other displays.

# Demo of initialisation procedure designed to minimise risk of memory fail
# when instantiating the frame buffer. The aim is to do this as early as
# possible before importing other modules.

# WIRING
# Pico      Display
# GPIO Pin
# 3v3  36   Vin
# IO6   9   CLK  Hardware SPI0
# IO7  10   DATA (AKA SI MOSI)
# IO8  11   Rst
# IO9  12   DC
# Gnd  13   Gnd
# IO10 14   CS
# IO26 31   Touch SDA
# IO27 32   Touch SCL

from machine import Pin, I2C, SPI, freq
import gc
from drivers.ili93xx.ili9341 import ILI9341 as SSD

freq(250_000_000)  # RP2 overclock
# Create and export an SSD instance
prst = Pin(7, Pin.OUT, value=1)
pdc = Pin(15, Pin.OUT, value=0)  # Arbitrary pins
pcs = Pin(17, Pin.OUT, value=1)
spi = SPI(0, sck=Pin(18), mosi=Pin(19), miso=Pin(16), baudrate=30_000_000)
gc.collect()  # Precaution before instantiating framebuf
ssd = SSD(spi, pcs, pdc, prst, height=240, width=320, usd=True)  # 240x320 default
from gui.core.tgui import Display, quiet

quiet()  # Comment this out for periodic free RAM messages
# Touch configuration
from touch.ft6206 import FT6206

i2c = I2C(1, scl=Pin(27), sda=Pin(26), freq=100_000)
tpad = FT6206(i2c, ssd)
# To create a tpad.init line for your displays please read SETUP.md
# The FT6206 is pre-calibrated: the purpose of running touch.setup is to match
# the chosen screenorientation. Numeric args may be as below.
# tpad.init(240, 320, 0, 0, 240, 320, True, True, False)

display = Display(ssd, tpad)
