#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Encoding: UTF-8

import json
import requests
import sys
import getopt
import os

from datetime import date, timedelta, datetime


from readConfig import (build_openmeteo_url,
                        openmeteo_latitude, openmeteo_longitude,
                        openmeteo_hourly, openmeteo_daily,
                        openmeteo_ws_unit,
                        openmeteo_timezone, openmeteo_forecast_days,
                        openmeteo_tilt, openmeteo_azimuth,
                        db_name)

from sql import do_sql


def parse_openmeteo_forecast(no_days):
    start_day = date.today()

    print(
        f'\nParsing forecast for {start_day} - {start_day + timedelta(days = no_days - 1)}')

    '''s_year = str(start_day.year)
    if start_day.month < 10:
        s_month = "0" + str(start_day.month)
    else:
        s_month = str(start_day.month)
    if start_day.day < 10:
        s_day = "0" + str(start_day.day)
    else:
        s_day = str(start_day.day)

    end_day = start_day + timedelta(days=no_days - 1)

    e_year = str(end_day.year)
    if end_day.month < 10:
        e_month = "0" + str(end_day.month)
    else:
        e_month = str(end_day.month)
    if end_day.day < 10:
        e_day = "0" + str(end_day.day)
    else:
        e_day = str(end_day.day)'''

    openmeteo_url = build_openmeteo_url(
        openmeteo_latitude, openmeteo_longitude, openmeteo_hourly, openmeteo_daily, openmeteo_ws_unit, openmeteo_timezone, openmeteo_forecast_days, openmeteo_tilt, openmeteo_azimuth)
    print("\n%s" % openmeteo_url)

    #    with request.urlopen(temperatur_url) as elpris_url:
    #        data = json.load(temperatur_url)
    #        print(data)

    response_API = requests.get(openmeteo_url)
    data = response_API.text

    response_code = response_API.status_code
    print("Response code: %s" % response_code)

    if response_code == 200:

        data = "[" + response_API.text + "]"

        # print(data)
        # parse_json = json.loads(json.dumps(data))
        parse_json = json.loads(data)

        # json_formatted_str = json.dumps(parse_json, indent=2)
        # print("\n" + json_formatted_str + "\n")

        # print()

        for x in range(len(parse_json[0]['hourly']['time'])):
            time = parse_json[0]['hourly']['time'][x]

            temp = float(parse_json[0]['hourly']['temperature_2m'][x])
            rain = float(parse_json[0]['hourly']['rain'][x])
            wind = float(parse_json[0]['hourly']['wind_speed_10m'][x])
            gti_instant = float(
                parse_json[0]['hourly']['global_tilted_irradiance_instant'][x])

            # print(
            #    f'Time: {time} \t {time[:10]} {time[11:16]} \t Temp: {temp} \t Rain: {rain} \t Wind: {wind} \t GTI Instant: {gti_instant} ')

            sql = (
                f"INSERT INTO {db_name}.forecast(time, temp, rain, wind, gti_instant) VALUES ('{time[:10]} {time[11:16]}', {temp}, {rain}, {wind}, {gti_instant}) ON DUPLICATE KEY UPDATE temp = {temp}, rain = {wind}, wind = {wind}, gti_instant = {gti_instant}")
            print(sql)

            output = do_sql(sql)
            # print(output)

        # print()

        for y in range(len(parse_json[0]['daily']['time'])):
            day = parse_json[0]['daily']['time'][y]
            sunrise = parse_json[0]['daily']['sunrise'][y]
            sunset = parse_json[0]['daily']['sunset'][y]

            # print(
            #    f'Day: {day} \t Sunrise: {sunrise} \t {sunrise[:10]} {sunrise[11:16]} \t Sunset: {sunset} \t {sunset[:10]}  {sunset[11:16]}')

            sql = (
                f"INSERT INTO {db_name}.sun(day, sunrise, sunset) VALUES ('{day}', '{sunrise[:10]} {sunrise[11:16]}', '{sunset[:10]} {sunset[11:16]}') ON DUPLICATE KEY UPDATE sunrise = '{sunrise[:10]} {sunrise[11:16]}', sunset = '{sunset[:10]} {sunset[11:16]}'")
            # print(sql)

            output = do_sql(sql)
            # print(output)

        '''for y in range(len(parse_json[0]['stations'][0]['data'])):
            hour = parse_json[0]['stations'][0]['data'][y]['datetime']

            temp = float(parse_json[0]['stations']
                         [0]['data'][y]['temperatur'])

            sql = (
                f"INSERT INTO {db_name}.temperature(hour, temp) VALUES ('{hour}', {temp}) ON DUPLICATE KEY UPDATE temp = {temp}")
            # print(sql)

            output = do_sql(sql)
            # print(output)'''
    else:
        print("No data yet")

    # json_formatted_str = json.dumps(parse_json, indent=2)
    # print(json_formatted_str)

    print()


def arguments(argv):
    number = openmeteo_forecast_days

    try:
        opts, args = getopt.getopt(argv,
                                   "hd:n:",
                                   ["help", "day=", "number="])
    except getopt.GetoptError:
        print('Error\ntest.py -d <date> -n <number of days>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print(
                f'{os.path.basename(sys.argv[0])} -n <number of days>')
            sys.exit()
        elif opt in ("-n", "--number"):
            number = arg

    return number


if __name__ == "__main__":

    number = arguments(sys.argv[1:])

    parse_openmeteo_forecast(int(number))
