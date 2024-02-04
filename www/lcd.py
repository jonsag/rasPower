#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Encoding: UTF-8

import sys

from luma.core.interface.serial import spi
from luma.core.render import canvas
from luma.lcd.device import st7735

from math import *

import time

from numpy import interp

from sql import do_sql

serial = spi(port=0, device=0, gpio_DC=23, gpio_RST=24)
device = st7735(serial)

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
    return interp(x, [0, graph_x_resolution - 1], [graph_offset, graph_offset + graph_width])


with canvas(device) as draw:

    # draw graph border
    draw.rectangle((graph_offset, graph_offset, graph_width,
                   graph_height), outline="white", fill="black")

    sql = (f'SELECT SEK_per_kWh FROM price WHERE hour > NOW() - INTERVAL {hours_back} HOUR AND hour < NOW() + INTERVAL {hours_future + 1} HOUR')
    print(sql)
    
    answer = do_sql(sql)

    i = 0

    for line in answer:
        # print(line[0])

        if i == 0:
            draw.point((scale_x(i),
                        scale_y(float(line[0]))),
                       fill="red")

            print(i, ":",
                  round(scale_x(i)), ", ",
                  round(scale_y(float(line[0]))))

        else:
            draw.line((scale_x(i - 1),
                       scale_y(old_line),
                       scale_x(i),
                       scale_y(float(line[0]))),
                      fill="red")

            print(i, ": ",
                  round(scale_x(i - 1)), ", ",
                  round(scale_y(old_line)), "\t-->\t",
                  round(scale_x(i)), ", ",
                  round(scale_y(float(line[0]))))

        old_line = line[0]

        i = i + 1

        # if i == 3:
        #    break

time.sleep(60)
