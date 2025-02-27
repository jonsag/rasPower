#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014-2023 Richard Hull and contributors
# See LICENSE.rst for details.
# PYTHON_ARGCOMPLETE_OK

import time
#import datetime
from luma.core.render import canvas
from numpy import interp
from pathlib import Path
from PIL import ImageFont

from sql import do_sql
from lcd_opts import get_device

"""import sys
import time
import subprocess
import digitalio
import board"""

device = get_device()

graph_size = 0.8

graph_width = device.width * graph_size
graph_height = device.height * graph_size
graph_x_offset = 40
graph_y_offset = 10

graph_y_min = -0.1
graph_y_max = 2.5

hours_back = 2
hours_future = 12

graph_frame_colour = "white"
text_colour = "white"

graph_background_colour = "black"

graph_line_colour = "yellow"
graph_line_colour_now = "red"

graph_x_resolution = graph_width / (hours_back + hours_future)

graph_font_path = str(
    Path(__file__).resolve().parent.joinpath("fonts", "DejaVuSansMono.ttf")
)
graph_font_size = 15
graph_font = ImageFont.truetype(graph_font_path, graph_font_size)

graph_y_scale_x_offset = 5
graph_y_scale_no_of_marks = 4


def scale_y(y):
    return interp(
        y, [graph_y_min, graph_y_max], [graph_y_offset + graph_height, graph_y_offset]
    )


def scale_x(x):
    # return interp(x, [0, graph_x_resolution - 1], [graph_offset + 1, graph_offset + graph_width - 2])
    return graph_x_offset + x * graph_width / (hours_back + hours_future + 1)


def graph(device, draw):
    # frame around graph
    draw.rectangle(
        (
            graph_x_offset, graph_y_offset,
            graph_x_offset + graph_width, graph_y_offset + graph_height,
        ),
        # , fill=graph_background_colour)
        outline=graph_frame_colour,
    )
    # y-scale marks
    for i in range(graph_y_scale_no_of_marks + 1):
        draw.text(
            (
                graph_y_scale_x_offset,
                graph_y_offset - graph_font_size / 2 + i * graph_height / graph_y_scale_no_of_marks,
            ),
            str(round(graph_y_max - graph_y_max / graph_y_scale_no_of_marks * i, 1)),
            font=graph_font,
            fill=text_colour,
        )

    sql = f"SELECT SEK_per_kWh, hour FROM price WHERE hour > NOW() - INTERVAL {hours_back} HOUR AND hour < NOW() + INTERVAL {hours_future + 1} HOUR"
    print(sql)

    answer = do_sql(sql)

    i = 0
    old_line = ""

    for line in answer:
        if i == 0:
            # Horizontal
            draw.line(
                (
                    scale_x(i), scale_y(float(line[0])),
                    scale_x(i + 1), scale_y(float(line[0])),
                ),
                fill=graph_line_colour,
            )

            print(
                "- ",
                round(scale_x(i)), ", ",
                round(scale_y(float(line[0]))), "\t-->\t",
                round(scale_x(i + 1)), ", ",
                round(scale_y(float(line[0]))), "\t-",
                line[0], "kr\t",
                line[1],
            )

        elif i == hours_back - 1:
            # Vertical
            draw.line(
                (
                    scale_x(i), scale_y(float(old_line)),
                    scale_x(i), scale_y(float(line[0])),
                ),
                fill=graph_line_colour,
            )

            print(
                "| ",
                round(scale_x(i)), ", ",
                round(scale_y(float(old_line))), "\t-->\t",
                round(scale_x(i)), ", ",
                round(scale_y(float(line[0]))), "\t|",
            )

            # Horizontal
            draw.line(
                (
                    scale_x(i), scale_y(float(line[0])),
                    scale_x(i + 1), scale_y(float(line[0])),
                ),
                fill=graph_line_colour_now,
            )

            print(
                "- ",
                round(scale_x(i)), ", ",
                round(scale_y(float(line[0]))), "\t-->\t",
                round(scale_x(i + 1)), ", ",
                round(scale_y(float(line[0]))), "\t-",
                line[0], "kr\t",
                line[1],
            )
        else:
            # Vertical
            draw.line(
                (
                    scale_x(i), scale_y(float(old_line)),
                    scale_x(i), scale_y(float(line[0])),
                ),
                fill=graph_line_colour,
            )

            print(
                "| ",
                round(scale_x(i)), ", ",
                round(scale_y(float(old_line))), "\t-->\t",
                round(scale_x(i)), ", ",
                round(scale_y(float(line[0]))), "\t|",
            )

            # Horizontal
            draw.line(
                (
                    scale_x(i),
                    scale_y(float(line[0])),
                    scale_x(i + 1),
                    scale_y(float(line[0])),
                ),
                fill=graph_line_colour,
            )

            print(
                "- ",
                round(scale_x(i)),
                ", ",
                round(scale_y(float(line[0]))),
                "\t-->\t",
                round(scale_x(i + 1)),
                ", ",
                round(scale_y(float(line[0]))),
                "\t-",
                line[0],
                "kr\t",
                line[1],
            )

        old_line = line[0]

        i = i + 1


def main():

    with canvas(device) as draw:
        graph(device, draw)

    for i in range(30):
        print(30 - i)
        time.sleep(1)

    """print("Testing display ON/OFF...")
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
            time.sleep(0.1)"""


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
