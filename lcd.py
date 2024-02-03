#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Encoding: UTF-8

from luma.core.interface.serial import spi
from luma.core.render import canvas
from luma.lcd.device import st7735

serial = spi(port=0, device=0, gpio_DC=23, gpio_RST=24)
device = st7735(spi)
