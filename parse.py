#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Encoding: UTF-8

import json, requests

from datetime import date, timedelta


from readConfig import (build_api_url, 
                        spot_surcharge, certificate_fee, trading_fee, 
                        transfer, tax, 
                        VAT)

today = date.today()

for x in range(2):
    when = today + timedelta(days = x)
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
    url = build_api_url(year, month, day)
    print(url)

#    with request.urlopen(url) as url:
#        data = json.load(url)
#        print(data)
 
    response_API = requests.get(url)
    data = response_API.text
    
    response_code = response_API.status_code
    print(response_code)
    
    if response_code == 200:
        data = response_API.text
        parse_json = json.loads(data)
        
        for y in range(24):
            hour = parse_json[y]['time_start']
            price_SEK = parse_json[y]['SEK_per_kWh']
            additional_fees = (spot_surcharge + certificate_fee + trading_fee)

            subtotal = (price_SEK + additional_fees) * (1 + VAT)
            
            taxes = (price_SEK + additional_fees + transfer + tax) * VAT
            
            total = (price_SEK + additional_fees + transfer + tax) * (1 + VAT)
            
            #print(taxes)
            print(f'Hour: {hour:25}, Spot price: {price_SEK:8f}, Our Price: {subtotal:8f}, Taxes: {taxes:8f}, Total: {total:8f},')
    else:
        print("No data yet")
    
    #json_formatted_str = json.dumps(parse_json, indent=2)
    #print(json_formatted_str)
    
    print()