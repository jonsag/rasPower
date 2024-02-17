#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Encoding: UTF-8

import json
import requests
import sys
import getopt
import os

from datetime import date, timedelta, datetime


from readConfig import (build_temperatur_url,
                        db_name)

from sql import do_sql


def parse_temperaturnu(start_day, no_days):

    print(
        f'\nParsing temperature history for {start_day} - {start_day + timedelta(days = no_days - 1)} ...')

    s_year = str(start_day.year)
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
        e_day = str(end_day.day)

    temperatur_url = build_temperatur_url(
        s_year, s_month, s_day, e_year, e_month, e_day)
    print("\n%s" % temperatur_url)

    #    with request.urlopen(temperatur_url) as elpris_url:
    #        data = json.load(temperatur_url)
    #        print(data)

    response_API = requests.get(temperatur_url)
    data = response_API.text

    response_code = response_API.status_code
    print("Response code: %s" % response_code)

    if response_code == 200:
        data = "[" + response_API.text + "]"

        # data = [{"full_exec_time": 0.009675025939941406, "title": "Temperatur.nu API 1.17", "client": "unsigned", "stations": [{"title": "Enstaberga", "id": "enstaberga", "temp": "-0.7", "data": [{"datetime": "2024-01-01 01:00", "temperatur": "-1.4"}, {"datetime": "2024-01-01 02:00", "temperatur": "-1.5"}, {"datetime": "2024-01-01 03:00", "temperatur": "-1.6"}, {"datetime": "2024-01-01 04:00", "temperatur": "-1.6"}, {"datetime": "2024-01-01 05:00", "temperatur": "-1.8"}, {"datetime": "2024-01-01 06:00", "temperatur": "-1.9"}, {"datetime": "2024-01-01 07:00", "temperatur": "-2.0"}, {"datetime": "2024-01-01 08:00", "temperatur": "-2.1"}, {"datetime": "2024-01-01 09:00", "temperatur": "-2.0"}, {"datetime": "2024-01-01 10:00", "temperatur": "-1.9"}, {"datetime": "2024-01-01 11:00", "temperatur": "-1.9"},

        # print(data)
        # parse_json = json.loads(json.dumps(data))
        parse_json = json.loads(data)

        for y in range(len(parse_json[0]['stations'][0]['data'])):
            time = parse_json[0]['stations'][0]['data'][y]['datetime']

            temp = float(parse_json[0]['stations']
                         [0]['data'][y]['temperatur'])

            sql = (
                f"INSERT INTO {db_name}.temperature(time, temp) VALUES ('{time}', {temp}) ON DUPLICATE KEY UPDATE temp = {temp}")
            # print(sql)

            output = do_sql(sql)
            # print(output)
    else:
        print("No data yet")

    # json_formatted_str = json.dumps(parse_json, indent=2)
    # print(json_formatted_str)

    print()


def arguments(argv, day, number):

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
                f'{os.path.basename(sys.argv[0])} -d <date> -n <number of days>')
            sys.exit()
        elif opt in ("-d", "--day"):
            try:
                day = datetime.strptime(arg, '%Y-%m-%d').date()
            except:
                print("Error\nEnter date in the format YYYY-MM-DD")
                sys.exit(3)
        elif opt in ("-n", "--number"):
            number = arg

    return day, number


if __name__ == "__main__":
    day = date.today() - timedelta(days=1)
    number = 2

    day, number = arguments(sys.argv[1:], day, number)

    parse_temperaturnu(day, int(number))
