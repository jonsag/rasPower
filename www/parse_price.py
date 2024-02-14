#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Encoding: UTF-8

import json
import requests
import sys
import getopt
import os

from datetime import date, timedelta, datetime


from readConfig import (build_elpris_url,
                        db_name,
                        spot_surcharge, certificate_fee, trading_fee,
                        transfer, tax,
                        VAT)

from sql import do_sql


def parse_elprisetjustnu(start_day, no_days):

    print(f'Parsing prices for {start_day} - {start_day + timedelta(days = no_days - 1)}')

    for x in range(no_days):
        when = start_day + timedelta(days = x)
        print(x)

        year = str(when.year)
        if when.month < 10:
            month = "0" + str(when.month)
        else:
            month = str(when.month)
        if when.day < 10:
            day = "0" + str(when.day)
        else:
            day = str(when.day)

        print(when)
        elpris_url = build_elpris_url(year, month, day)
        print(elpris_url)

    #    with request.urlopen(elpris_url) as elpris_url:
    #        data = json.load(elpris_url)
    #        print(data)

        response_API = requests.get(elpris_url)
        data = response_API.text

        response_code = response_API.status_code
        print(response_code)

        if response_code == 200:
            data = response_API.text
            #print(data)
            parse_json = json.loads(data)

            for y in range(24):
                hour = parse_json[y]['time_start']

                price_SEK = parse_json[y]['SEK_per_kWh']
                additional_fees = (
                    spot_surcharge + certificate_fee + trading_fee)

                subtotal = (price_SEK + additional_fees) * (1 + VAT)

                taxes = (price_SEK + additional_fees + transfer + tax) * VAT

                total = (price_SEK + additional_fees +
                         transfer + tax) * (1 + VAT)

                # print(taxes)
                #print(f'Hour: {hour:25}, Spot price: {price_SEK:8f}, Our Price: {subtotal:8f}, Taxes: {taxes:8f}, Total: {total:8f},')

                sql = (
                    f"INSERT INTO {db_name}.price(hour, SEK_per_kWh) VALUES ('{hour[:10]} {hour[11:13]}', {price_SEK:f}) ON DUPLICATE KEY UPDATE SEK_per_kWh = {price_SEK}")
                #print(sql)
                output = do_sql(sql)
                #print(output)
        else:
            print("No data yet")

        # json_formatted_str = json.dumps(parse_json, indent=2)
        # print(json_formatted_str)

        print()


def arguments(argv):
    day = date.today()
    number = 2

    try:
        opts, args = getopt.getopt(argv,
                                   "hd:n:",
                                   ["help", "day=", "number="])
    except getopt.GetoptError:
        print('Error\ntest.py -d <date> -n <number of days>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print(f'{os.path.basename(sys.argv[0])} -d <date> -n <number of days>')
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
    day, number = arguments(sys.argv[1:])
    
    parse_elprisetjustnu(day, int(number))
