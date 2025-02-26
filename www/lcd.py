#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Encoding: UTF-8

import sys
import time
# import subprocess
import digitalio
import board
# import re

from PIL import Image, ImageDraw, ImageFont

from adafruit_rgb_display import ili9341

from math import *

from numpy import interp

from sql import do_sql

# suppress warning messages
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

# configuration for CS and DC pins
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = digitalio.DigitalInOut(board.D24)

# config for display baudrate (default max is 24mhz):
BAUDRATE = 24000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()

# create the display
disp = ili9341.ILI9341(
    spi,
    rotation=90,  # 2.2", 2.4", 2.8", 3.2" ILI9341
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
)

# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for full color.
if disp.rotation % 180 == 90:
    height = disp.width  # we swap height/width to rotate it to landscape!
    width = disp.height
else:
    width = disp.width  # we swap height/width to rotate it to landscape!
    height = disp.height

image = Image.new("RGB", (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
disp.image(image)

#sys.exit(0)

graph_width = 120
graph_height = 100
graph_offset = 2

graph_y_min = -0.1
graph_y_max = 1

hours_back = 2
hours_future = 8

graph_x_resolution = graph_width / (hours_back + hours_future)


def scale_y(y):
    return interp(y, [graph_y_min, graph_y_max], [graph_offset + graph_height, graph_offset])


def scale_x(x):
    return interp(x, [0, graph_x_resolution - 1], [graph_offset + 1, graph_offset + graph_width - 2])


with canvas(device) as draw:

    # draw graph border
    draw.rectangle((graph_offset, graph_offset, graph_width,
                   graph_height), outline="white", fill="black")

    sql = (
        f'SELECT SEK_per_kWh FROM price WHERE hour > NOW() - INTERVAL {hours_back} HOUR AND hour < NOW() + INTERVAL {hours_future + 1} HOUR')
    print(sql)

    answer = do_sql(sql)

    i = 0

    for line in answer:
        if i == 0:
            draw.line((scale_x(i),
                       scale_y(float(line[0])),
                       scale_x(i + 1),
                       scale_y(float(line[0]))),
                      fill="red")

            print("- ",
                  round(scale_x(i)), ", ",
                  round(scale_y(float(line[0]))), "-->",
                  round(scale_x(i + 1)), ", ",
                  round(scale_y(float(line[0]))))

        else:
            draw.line((scale_x(i),
                       scale_y(float(old_line)),
                       scale_x(i),
                       scale_y(float(line[0]))),
                      fill="red")

            print("| ",
                  round(scale_x(i)), ", ",
                  round(scale_y(float(old_line))), "-->",
                  round(scale_x(i)), ", ",
                  round(scale_y(float(line[0]))))

            draw.line((scale_x(i),
                       scale_y(float(line[0])),
                       scale_x(i + 1),
                       scale_y(float(line[0]))),
                      fill="red")

            print("- ",
                  round(scale_x(i)), ", ",
                  round(scale_y(float(line[0]))), "-->",
                  round(scale_x(i + 1)), ", ",
                  round(scale_y(float(line[0]))))

        old_line = line[0]

        i = i + 1

        # if i == 2:
        #    break

time.sleep(60)




