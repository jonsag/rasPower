#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Encoding: UTF-8

import configparser, os

config = configparser.ConfigParser()  # define config file
config.read("%s/config.ini" % os.path.dirname(os.path.realpath(__file__)))  # read config file

# read variables from config file
var = config.get('header', 'var').strip()

# elprisetjustnu.se
from urllib.parse import urlunsplit, urlencode

SCHEME = os.environ.get("API_SCHEME", config.get('elpris', 'scheme').strip())
NETLOC = os.environ.get("API_NETLOC", config.get('elpris', 'url').strip())

def build_api_url(year, month, day):
    SCHEME = os.environ.get("API_SCHEME", config.get('elpris', 'scheme').strip())
    NETLOC = os.environ.get("API_NETLOC", config.get('elpris', 'url').strip())  
    path = (config.get('elpris', 'api').strip() + 
            "/" + year + 
            "/" + month + "-" + day +
            "_" + config.get('elpris', 'area').strip() +
            "." + config.get('elpris', 'type').strip())
    #query = urlencode(dict(format=format, token=token))

    #return urlunsplit((SCHEME, NETLOC, path, query, ""))
    return urlunsplit((SCHEME, NETLOC, path, "", ""))

#>>> build_api_url(12, "mp3", "abbadabba")
#'https://example.com/api/v1/book/12?format=mp3&token=abbadabba'
