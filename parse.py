#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Encoding: UTF-8

import json, requests

from datetime import date, timedelta

#from urllib import request

from readConfig import var, build_api_url

print(var)

today = date.today()

for when in today, today + timedelta(days=1):
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
    
    print(response_API.status_code)
    
    data = response_API.text
    parse_json = json.loads(data)
    
    info = parse_json[0]['time_start']
    print(info)
    
    #json_formatted_str = json.dumps(parse_json, indent=2)
    #print(json_formatted_str)
    
    print