#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time, sys, math

# import datetime
# from luma.core import cmdline, error
from luma.core.render import canvas
from luma.lcd.device import ili9341
from luma.core.interface.serial import spi

from numpy import interp
from pathlib import Path
from PIL import ImageFont

from readConfig import screen_type

if screen_type == "ili9341":
    from readConfig import (
        ili9341_port as port,
        ili9341_device as device,
        ili9341_gpio_DC as gpio_DC,
        ili9341_gpio_RST as gpio_RST,
        ili9341_bus_speed_hz as bus_speed_hz,
        ili9341_gpio_LIGHT as gpio_LIGHT,
        ili9341_width as width,
        ili9341_height as height,
        ili9341_rotate as rotate,
        ili9341_active_low as active_low,
    )

from sql import do_sql

serial = spi(
    port=port,
    device=device,
    gpio_DC=gpio_DC,
    gpio_RST=gpio_RST,
    bus_speed_hz=bus_speed_hz,
    gpio_LIGHT=gpio_LIGHT,
)
device = ili9341(
    serial, width=width, height=height, rotate=rotate, active_low=active_low
)

graph_size = 0.8

graph_width = device.width * graph_size
graph_height = device.height * graph_size
graph_x_offset = 40
graph_y_offset = 10

hours_back = 2
hours_future = 24

# graph_y_min = -0.1

sql = f"SELECT MAX(SEK_per_kWh), MIN(SEK_per_kWh) FROM price WHERE hour > NOW() - INTERVAL {hours_back} HOUR AND hour < NOW() + INTERVAL {hours_future + 1} HOUR"
answer = do_sql(sql)
y_max = answer[0][0]
graph_y_max = round(math.ceil(y_max * 2)) / 2
y_min = answer[0][1]
graph_y_min = round(math.floor(y_min * 2)) / 2

if graph_y_min >= 0.5:
    graph_y_min = 0

print("Highest: \t%s, \tY-max: \t%s" % (y_max, graph_y_max))
print("Lowest: \t%s, \tY-min: \t%s" % (y_min, graph_y_min))
print()

graph_frame_colour = "white"
text_colour = "white"

graph_background_colour = "black"

graph_line_colour = "yellow"
graph_line_colour_now = "red"

graph_x_resolution = graph_width / (hours_back + hours_future)

graph_scale_font_path = str(
    Path(__file__).resolve().parent.joinpath("fonts", "DejaVuSansMono.ttf")
)
graph_scale_font_size = 15
graph_scale_font = ImageFont.truetype(graph_scale_font_path, graph_scale_font_size)

price_font_path = graph_scale_font_path
price_font_size = 10
price_font = ImageFont.truetype(price_font_path, price_font_size)

graph_y_scale_x_offset = 5
graph_y_scale_no_of_marks = math.ceil((graph_y_max - graph_y_min) * 2)
print("Y-scale no of marks: %s" % (graph_y_scale_no_of_marks + 1))
print()


def scale_y(y):
    return interp(
        y, [graph_y_min, graph_y_max], [graph_y_offset + graph_height, graph_y_offset]
    )


def scale_x(x):
    # return interp(x, [0, graph_x_resolution - 1], [graph_offset + 1, graph_offset + graph_width - 2])
    return graph_x_offset + x * graph_width / (hours_back + hours_future + 1)


def draw_horizontal(draw, i, line):
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

    show_price(draw, i, line)


def draw_vertical(draw, i, old_line, line):
    draw.line(
        (
            scale_x(i),
            scale_y(float(old_line)),
            scale_x(i),
            scale_y(float(line[0])),
        ),
        fill=graph_line_colour,
    )

    print(
        "| ",
        round(scale_x(i)),
        ", ",
        round(scale_y(float(old_line))),
        "\t-->\t",
        round(scale_x(i)),
        ", ",
        round(scale_y(float(line[0]))),
        "\t|",
    )


def show_price(draw, i, line):
    if is_even(i):
        y_pos = 1.5
    else:
        y_pos = -0.3

    if line[0] * 100 >= 10:
        x_pos = 0
    else:
        x_pos = 5

    draw.text(
        (
            scale_x(i) + x_pos,  # + (scale_x(i + 1) - scale_x(i)) / 2,
            scale_y(float(line[0])) - price_font_size * y_pos,
        ),
        str(round(line[0] * 100)),
        # str(scale_y(float(line[0] - 10))),
        font=price_font,
        fill=text_colour,
    )


def is_even(i):
    if i / 2 == int(i / 2):
        return True
    else:
        return False


def graph(device, draw):
    # frame around graph
    draw.rectangle(
        (
            graph_x_offset,
            graph_y_offset,
            graph_x_offset + graph_width,
            graph_y_offset + graph_height,
        ),
        # , fill=graph_background_colour)
        outline=graph_frame_colour,
    )

    # y-scale marks
    for i in range(graph_y_scale_no_of_marks + 1):
        draw.text(
            (
                graph_y_scale_x_offset,
                graph_y_offset
                - graph_scale_font_size / 2
                + i * graph_height / graph_y_scale_no_of_marks,
            ),
            str(
                round(
                    graph_y_max
                    - (graph_y_max - graph_y_min) / graph_y_scale_no_of_marks * i,
                    1,
                )
            ),
            font=graph_scale_font,
            fill=text_colour,
        )

    sql = f"SELECT SEK_per_kWh, hour FROM price WHERE hour > NOW() - INTERVAL {hours_back} HOUR AND hour < NOW() + INTERVAL {hours_future + 1} HOUR"

    answer = do_sql(sql)

    i = 0
    old_line = ""

    for line in answer:
        if i == 0:
            # Horizontal
            draw_horizontal(draw, i, line)

        elif i == hours_back - 1:
            # Vertical
            draw_vertical(draw, i, old_line, line)

            # Horizontal
            draw_horizontal(draw, i, line)

        else:
            # Vertical
            draw_vertical(draw, i, old_line, line)

            # Horizontal
            draw_horizontal(draw, i, line)

        old_line = line[0]

        i = i + 1


def main():

    with canvas(device) as draw:
        graph(device, draw)

    time.sleep(5)
    sys.exit()

    for i in range(30):
        print(30 - i)
        if i >= 15:
            device.clear()
        if i / 2 == round(i / 2, 0):
            device.backlight(False)
            time.sleep(0.2)
        else:
            device.backlight(True)
            time.sleep(0.8)

    """for i in range(30):
        print(30 - i)
        if i >= 15:
            device.clear()
        if i/2 == round(i/2, 0):
            device.hide()
        else:
            device.show()
        time.sleep(1)"""

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
