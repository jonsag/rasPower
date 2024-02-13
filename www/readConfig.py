#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Encoding: UTF-8

from urllib.parse import urlunsplit, urlencode
import configparser
import os

config = configparser.ConfigParser()  # define config file
# config.read("%s/config.ini" % os.path.dirname(os.path.realpath(__file__)))  # read config file
config.read("config.ini")  # read config file

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

VAT = float((int(config.get('extra_fees', 'VAT').strip())))


# elprisetjustnu.se
elpris_SCHEME = os.environ.get("API_SCHEME", config.get('elpris', 'elpris_scheme').strip())
elpris_NETLOC = os.environ.get("API_NETLOC", config.get('elpris', 'elpris_url').strip())


def build_elpris_url(year, month, day):
    path = (config.get('elpris', 'elpris_api').strip() +
            "/" + year +
            "/" + month + "-" + day +
            "_" + config.get('elpris', 'area').strip() +
            "." + config.get('elpris', 'type').strip())
    # query = elpris_urlencode(dict(format=format, token=token))

    # return elpris_urlunsplit((SCHEME, NETLOC, path, query, ""))
    return urlunsplit((elpris_SCHEME, elpris_NETLOC, path, "", ""))

# temperatur.nu
temperatur_SCHEME = os.environ.get("API_SCHEME", config.get('temperatur', 'temperatur_scheme').strip())
temperatur_NETLOC = os.environ.get("API_NETLOC", config.get('temperatur', 'temperatur_url').strip())


def build_temperatur_url(s_year, s_month, s_day, e_year, e_month, e_day):
    path = (config.get('temperatur', 'temperatur_api').strip() +
            "?p=" + config.get('temperatur', 'temperature_location').strip() + 
            "&cli=" + config.get('temperatur', 'temperature_client').strip() + 
            "&data" + 
            "&start=" + s_year + "-" + s_month + "-" + s_day +
            "-00-00" + 
            "&end=" + e_year + "-" + e_month + "-" + e_day + 
            "-00-00") 

        # https://api.temperatur.nu/tnu_1.17.php?p=enstaberga&cli=rasPower&data&start=2024-01-01-00-00&end=2024-01-02-00-00

    # return elpris_urlunsplit((SCHEME, NETLOC, path, query, ""))
    return urlunsplit((temperatur_SCHEME, temperatur_NETLOC, path, "", ""))