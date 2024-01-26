#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Encoding: UTF-8

import configparser, os

config = configparser.ConfigParser()  # define config file
config.read("%s/config.ini" % os.path.dirname(os.path.realpath(__file__)))  # read config file

# database
db_host = config.get('db', 'db_host').strip()
db_user = config.get('db', 'db_user').strip()
db_password = config.get('db', 'db_password').strip()
db_name = config.get('db', 'db_name').strip()
db_port = int(config.get('db', 'db_port').strip())

spot_surcharge = float(config.get('extra_fees', 'spot_surcharge').strip())
certificate_fee = float(config.get('extra_fees', 'certificate_fee').strip())
trading_fee = float(config.get('extra_fees', 'trading_fee').strip())

transfer = float(config.get('extra_fees', 'transfer').strip())
tax = float(config.get('extra_fees', 'tax').strip())

VAT = float((int(config.get('extra_fees', 'VAT').strip())) / 100)


# elprisetjustnu.se
from urllib.parse import urlunsplit, urlencode

SCHEME = os.environ.get("API_SCHEME", config.get('elpris', 'scheme').strip())
NETLOC = os.environ.get("API_NETLOC", config.get('elpris', 'url').strip())

def build_api_url(year, month, day):
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
