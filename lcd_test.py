#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Encoding: UTF-8

from luma.core.interface.serial import spi
from luma.core.render import canvas
from luma.lcd.device import st7735

from math import *


import time

serial = spi(port=0, device=0, gpio_DC=23, gpio_RST=24)
device = st7735(serial)

# rotate
# device = st7735(serial, rotate=1)

# while True:
#    # hello world

with canvas(device) as draw:
    # draw.rectangle(device.bounding_box, outline="white", fill="black")
    # draw.text((30, 40), "Hello World", fill="red")

    # Draw some shapes
    # First define some constants to allow easy resizing of shapes
    padding = 2
    shape_width = 20

    top = padding
    bottom = device.height - padding - 1

    # Move left to right keeping track of the current x position for drawing shapes
    x = padding

    # draw.line((x, bottom, x + shape_width, top), fill="yellow")
    # draw.line((x, top, x + shape_width, bottom), fill="yellow")

    # rectangle
    # draw.rectangle((10, 10, 30, 30), outline="white", fill="red")
    # time.sleep(2)

    '''draw.point((10, 50), fill="white")
    
    draw.point((0, 0), fill="red")
    draw.point((device.width - 1, 0), fill="yellow")
    draw.point((device.width - 1, device.height - 1), fill="green")
    draw.point((0, device.height - 1), fill="blue")'''

    Fs = 8000
    f = 100
    sample = device.width
    y = [0]*sample

    for x in range(0, sample, 1):
        y_sin = sin(2*pi*f*x/Fs)

        y[x] = round((y_sin * device.height / 2 + device.height / 2) * 0.99)

        # y = device.height / 2 + x / 10
        # print(x - 1, "\t", round(y_sin, 2), "\t", y, "\t", round(y))

        # print(x, "\t", round(y[x]))
        if x == 0:
            print(x, "\t", y)
        else:
            print(x - 1, "\t", y[x - 1], "\t",
                  x, "\t", y[x])

        if x == 0:
            draw.point((x, y[x]), fill="white")
        else:
            draw.line((x - 1, y[x - 1], x, y[x]), fill="white")

        # draw.line((x, bottom, x + shape_width, top), fill="yellow")

print("\n", device.width, "\t", device.height, "\n")

time.sleep(60)
