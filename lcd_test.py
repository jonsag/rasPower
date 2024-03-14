#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Encoding: UTF-8

from luma.core.interface.serial import spi
from luma.core.render import canvas
from luma.lcd.device import st7735, pygame

from math import *

import time

serial = spi(port=0, device=0, gpio_DC=23, gpio_RST=24)
#device = st7735(serial)
device = pygame

with canvas(device) as draw:

    Fs = 8000
    f = 100
    sample = device.width
    y = [0]*sample

    for x in range(0, sample, 1):
        y_sin = sin(2*pi*f*x/Fs)

        y[x] = round((y_sin * device.height / 2 + device.height / 2) * 0.99)

        if x == 0:
            print(x, "\t", y)
        else:
            print(x - 1, "\t", y[x - 1], "\t",
                  x, "\t", y[x])

        if x == 0:
            draw.point((x, y[x]), fill="white")
        else:
            draw.line((x - 1, y[x - 1], x, y[x]), fill="white")


print("\n", device.width, "\t", device.height, "\n")

time.sleep(60)
