#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Encoding: UTF-8

from urllib.parse import urlunsplit, urlencode
import configparser
import os

config = configparser.ConfigParser()  # define config file
config.read(os.path.join(os.path.dirname(
    os.path.realpath(__file__)), 'config.ini'))  # read config file

# print(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config.ini'))

# database
db_host = config.get('db', 'db_host').strip()
db_user = config.get('db', 'db_user').strip()
db_password = config.get('db', 'db_password').strip()
db_name = config.get('db', 'db_name').strip()
db_port = int(config.get('db', 'db_port').strip())

# surcharges
spot_surcharge = float(config.get('extra_fees', 'spot_surcharge').strip())
certificate_fee = float(config.get('extra_fees', 'certificate_fee').strip())
trading_fee = float(config.get('extra_fees', 'trading_fee').strip())

transfer = float(config.get('extra_fees', 'transfer').strip())

tax = float(config.get('extra_fees', 'tax').strip())

VAT = float((int(config.get('extra_fees', 'VAT').strip())))

# charts
chart_width = int(config.get('charts', 'chart_width').strip())
chart_height = int(config.get('charts', 'chart_height').strip())

# screen
screen_type = config.get('screen', 'type')

# ili9341
ili9341_port = int(config.get('ili9341', 'port').strip())
ili9341_device = int(config.get('ili9341', 'device').strip())
ili9341_gpio_DC = int(config.get('ili9341', 'gpio_DC').strip())
ili9341_gpio_RST = int(config.get('ili9341', 'gpio_RST').strip())
ili9341_bus_speed_hz = int(config.get('ili9341', 'bus_speed_Hz').strip())
ili9341_gpio_LIGHT = int(config.get('ili9341', 'gpio_LIGHT').strip())
ili9341_width = int(config.get('ili9341', 'width').strip())
ili9341_height = int(config.get('ili9341', 'height').strip())
ili9341_rotate = int(config.get('ili9341', 'rotate').strip())
ili9341_active_low = int(config.get('ili9341', 'active_low').strip())

#####################
# elprisetjustnu.se #
#####################
elpris_SCHEME = os.environ.get(
    "API_SCHEME", config.get('elpris', 'elpris_scheme').strip())
elpris_NETLOC = os.environ.get(
    "API_NETLOC", config.get('elpris', 'elpris_url').strip())


def build_elpris_url(year, month, day):

    path = (config.get('elpris', 'elpris_api').strip() + 
            "/" + year + 
            "/" + month + "-" + day + 
            "_" + config.get('elpris', 'area').strip() + 
            "." + config.get('elpris', 'type').strip())

    # https://www.elprisetjustnu.se/api/v1/prices/2024/02-13_SE3.json

    return urlunsplit((elpris_SCHEME, elpris_NETLOC, path, "", ""))


#################
# temperatur.nu #
#################
temperatur_SCHEME = os.environ.get("API_SCHEME", config.get(
    'temperatur', 'temperatur_scheme').strip())
temperatur_NETLOC = os.environ.get(
    "API_NETLOC", config.get('temperatur', 'temperatur_url').strip())


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

    return urlunsplit((temperatur_SCHEME, temperatur_NETLOC, path, "", ""))


##################
# open-meteo.com #
##################
openmeteo_SCHEME = os.environ.get("API_SCHEME", config.get(
    'openmeteo', 'openmeteo_scheme').strip())
openmeteo_NETLOC = os.environ.get(
    "API_NETLOC", config.get('openmeteo', 'openmeteo_url').strip())


def build_openmeteo_url_short():

    path = (config.get('openmeteo', 'openmeteo_api').strip())

    # https://api.open-meteo.com/v1/forecast

    return urlunsplit((openmeteo_SCHEME, openmeteo_NETLOC, path, "", ""))


openmeteo_latitude = float(config.get(
    'openmeteo', 'openmeteo_latitude').strip())
openmeteo_longitude = float(config.get(
    'openmeteo', 'openmeteo_longitude').strip())

openmeteo_hourly = (config.get(
    'openmeteo', 'openmeteo_hourly').replace(" ", ""))
openmeteo_daily = (config.get(
    'openmeteo', 'openmeteo_daily').replace(" ", ""))

openmeteo_ws_unit = (config.get(
    'openmeteo', 'openmeteo_ws_unit').strip())

openmeteo_timezone = config.get('openmeteo', 'openmeteo_timezone').strip()
openmeteo_forecast_days = int(config.get(
    'openmeteo', 'openmeteo_forecast_days').strip())

openmeteo_tilt = int(config.get(
    'openmeteo', 'openmeteo_tilt').strip())
openmeteo_azimuth = int(config.get(
    'openmeteo', 'openmeteo_azimuth').strip())


def build_openmeteo_url(latitude, longitude, hourly, daily, ws_unit, timezone, days, tilt, azimuth):

    path = (config.get('openmeteo', 'openmeteo_api').strip() + 
            "?latitude=" + str(latitude) + 
            "&longitude=" + str(longitude) + 
            "&hourly=" + hourly + 
            "&daily=" + daily + 
            "&wind_speed_unit=" + ws_unit + 
            "&timezone=" + timezone + 
            "&forecast_days=" + str(days) + 
            "&tilt=" + str(tilt) + 
            "&azimuth=" + str(azimuth))

    # https://open-meteo.com/en/docs/#hourly=temperature_2m,rain,wind_speed_10m,global_tilted_irradiance_instant&daily=sunrise,sunset&wind_speed_unit=ms&timezone=Europe%2FBerlin&forecast_days=3&tilt=15&azimuth=5
    # https://api.open-meteo.com/v1/forecast?latitude=58.74&longitude=16.91&hourly=temperature_2m,rain,wind_speed_10m,global_tilted_irradiance_instant&daily=sunrise,sunset&wind_speed_unit=ms&timezone=Europe%2FBerlin&forecast_days=3&tilt=15&azimuth=5

    # https://api.open-meteo.com/v1/forecast?
    # latitude=58.74&
    # longitude=16.91&
    # hourly=temperature_2m,rain,wind_speed_10m,global_tilted_irradiance_instant&
    # daily=sunrise,sunset
    # &wind_speed_unit=ms&
    # timezone=Europe%2FBerlin&
    # forecast_days=3&
    # tilt=15&
    # azimuth=5

    return urlunsplit((openmeteo_SCHEME, openmeteo_NETLOC, path, "", ""))
