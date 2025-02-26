#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014-2023 Richard Hull and contributors
# See LICENSE.rst for details.
# PYTHON_ARGCOMPLETE_OK


import time
import datetime
from lcd_opts import get_device
from luma.core.render import canvas
from numpy import interp

from sql import do_sql

'''import sys
import time
import subprocess
import digitalio
import board'''

device = get_device()

graph_size = 0.8

graph_width = device.width * graph_size
graph_height = device.height * graph_size
graph_offset = 2

graph_y_min = -0.1
graph_y_max = 1

hours_back = 2
hours_future = 12

graph_frame_colour = "white"
graph_background_colour = "black"
graph_line_colour = "yellow"
graph_line_colour_now = "red"

graph_x_resolution = graph_width / (hours_back + hours_future)


def scale_y(y):
    return interp(y, [graph_y_min, graph_y_max], [graph_offset + graph_height, graph_offset])


def scale_x(x):
    # return interp(x, [0, graph_x_resolution - 1], [graph_offset + 1, graph_offset + graph_width - 2])
    return graph_offset + x * graph_width / (hours_back + hours_future)


def graph_frame(device, draw):

    # Draw a rectangle
    # draw.rectangle((0 + graph_offset, 0+graph_offset, graph_width+graph_offset, graph_height+graph_offset),
    #               outline="white", fill="black")

    draw.rectangle((graph_offset, graph_offset,
                    graph_offset + graph_width, graph_offset + graph_height),
                   # , fill=graph_background_colour)
                   outline=graph_frame_colour)


'''    # Draw an X
    draw.line((x, bottom, x + shape_width, top), fill="yellow")
    draw.line((x, top, x + shape_width, bottom), fill="yellow")
    x += shape_width + padding

    # Write two lines of text
    left, t, right, bottom = draw.textbbox((0, 0), 'World!')
    w, h = right - left, bottom - t
    x = device.width - padding - w
    draw.rectangle((x, top + 4, x + w, top + h), fill="black")
    draw.rectangle((x, top + 16, x + w, top + 16 + h), fill="black")
    draw.text((device.width - padding - w, top + 4), 'Hello', fill="cyan")
    draw.text((device.width - padding - w, top + 16), 'World!', fill="purple")

    # Draw a rectangle of the same size of screen
    draw.rectangle(device.bounding_box, outline="white")
'''


def graph(device, draw):
    sql = (
        f'SELECT SEK_per_kWh, hour FROM price WHERE hour > NOW() - INTERVAL {hours_back} HOUR AND hour < NOW() + INTERVAL {hours_future + 1} HOUR')
    print(sql)

    answer = do_sql(sql)

    i = 0

    for line in answer:
        if i == 0:
            # Horizontal
            draw.line((scale_x(i), scale_y(float(line[0])),
                       scale_x(i + 1), scale_y(float(line[0]))),
                      fill=graph_line_colour)

            print("- ",
                  round(scale_x(i)), ", ",
                  round(scale_y(float(line[0]))), "\t-->\t",
                  round(scale_x(i + 1)), ", ",
                  round(scale_y(float(line[0]))), "\t-",
                  line[0], "kr\t",
                  line[1])

        elif i == hours_back - 1:
            # Vertical
            draw.line((scale_x(i), scale_y(float(old_line)),
                       scale_x(i), scale_y(float(line[0]))),
                      fill=graph_line_colour)

            print("| ",
                  round(scale_x(i)), ", ",
                  round(scale_y(float(old_line))), "\t-->\t",
                  round(scale_x(i)), ", ",
                  round(scale_y(float(line[0]))), "\t|")

            # Horizontal
            draw.line((scale_x(i), scale_y(float(line[0])),
                       scale_x(i + 1), scale_y(float(line[0]))),
                      fill=graph_line_colour_now)

            print("- ",
                  round(scale_x(i)), ", ",
                  round(scale_y(float(line[0]))), "\t-->\t",
                  round(scale_x(i + 1)), ", ",
                  round(scale_y(float(line[0]))), "\t-",
                  line[0], "kr\t",
                  line[1])
        else:
            # Vertical
            draw.line((scale_x(i), scale_y(float(old_line)),
                       scale_x(i), scale_y(float(line[0]))),
                      fill=graph_line_colour)

            print("| ",
                  round(scale_x(i)), ", ",
                  round(scale_y(float(old_line))), "\t-->\t",
                  round(scale_x(i)), ", ",
                  round(scale_y(float(line[0]))), "\t|")

            # Horizontal
            draw.line((scale_x(i), scale_y(float(line[0])),
                       scale_x(i + 1), scale_y(float(line[0]))),
                      fill=graph_line_colour)

            print("- ",
                  round(scale_x(i)), ", ",
                  round(scale_y(float(line[0]))), "\t-->\t",
                  round(scale_x(i + 1)), ", ",
                  round(scale_y(float(line[0]))), "\t-",
                  line[0], "kr\t",
                  line[1])

        old_line = line[0]

        i = i + 1


def main():

    with canvas(device) as draw:
        graph_frame(device, draw)

    with canvas(device) as draw:
        graph(device, draw)

    for i in range(30):
        print(30-i)
        time.sleep(1)

    '''print("Testing display ON/OFF...")
    for i in range(5):
        print(5-i)
        time.sleep(0.5)
        device.hide()

        time.sleep(0.5)
        device.show()

    print("Testing clear display...")
    time.sleep(2)
    device.clear()

    print("Testing screen updates...")
    time.sleep(2)
    for x in range(40):
        print(40-x)
        with canvas(device) as draw:
            now = datetime.datetime.now()
            draw.text((x, 4), str(now.date()), fill="white")
            draw.text((10, 16), str(now.time()), fill="white")
            time.sleep(0.1)'''


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
