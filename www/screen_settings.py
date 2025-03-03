#!/usr/bin/env python
# -*- coding: utf-8 -*-

from argparse import Namespace

args = Namespace(display="ili9341", 
                interface="spi", 
                spi-bus-speed=52000000, 
                gpio-reset=24, 
                gpio-data-command=25, 
                gpio-backlight=18, 
                width=320, 
                height=240,     
                backlight-active="high", 
                gpio-reset-hold-time=0.1, 
                gpio-reset-release-time=0.1, 
               rotate=2
)