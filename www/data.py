#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Encoding: UTF-8

from sql import do_sql

print("Content-Type: text/html")
print()
print("<html><head>")
print("</head><body>")

print("Hello World!")

sql = ("SELECT hour, SEK_per_kWh FROM price")

answer = do_sql(sql)

for line in answer:
    print(f'{line[0]}, {line[1]}')

print("</body></html>")
