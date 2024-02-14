#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Encoding: UTF-8

from sql import do_sql

import sqlparse
import os

from datetime import date, timedelta, datetime

sql1 = ("SELECT * FROM surcharges ORDER BY time DESC LIMIT 1;")
answer = do_sql(sql1)
for line in answer:
    #    print(f'{line[0]}, {line[1]}, {line[2]}, {line[3]}, {line[4]}, {line[5]}, {line[6]}')
    surcharges = line[1] + line[2] + line[3] + line[4] + line[5]
    VAT = line[6]


def construct_sql(day, number):

    last = day + timedelta(days = int(number) - 1)

    sql = ("SELECT hour, SEK_per_kWh FROM price WHERE DATE(hour) >= '" +
           str(day) + "' AND DATE(hour) <= '" + str(last) + "'")

    return sql


def webpage(sql, day, number):

    print("Content-Type: text/html")
    print()
    print("<html>")
    print("<head>")
    print("<script type='text/javascript' src='https://www.gstatic.com/charts/loader.js'></script>")
    print("<script type='text/javascript'>")
    print("google.charts.load('current', {'packages':['corechart']});")
    print("google.charts.setOnLoadCallback(drawChart);")
    print()
    print("function drawChart() {")
    print("var data = google.visualization.arrayToDataTable([")

    print("['Hour', 'SEK', 'Total'],")

    answer = do_sql(sql)

    for line in answer:
        print(
            f'["{line[0]}", {line[1]}, {(line[1] + surcharges) * (1 + VAT / 100)}],')
    print("]);")

    print()
    print("var options = {")
    print("title: 'Electricity price/hour',")
    # print("curveType: 'function',")
    print("legend: { position: 'bottom' }")
    print("};")
    print()
    print("var chart = new google.visualization.LineChart(document.getElementById('curve_chart'));")
    print()
    print("chart.draw(data, options);")
    print("}")
    print("</script>")
    print("</head>")
    print("<body>")

    print("Day: %s \t No: %s <br>\n" % (day, number))

    print(sqlparse.format(sql, reindent=True, keyword_case='upper'))
    print()

    print("<div id='curve_chart' style='width: 1200px; height: 700px'></div>")

    print("</body>")
    print("</html>")


def cli_arguments(argv):
    day = date.today()
    number = 1

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


def cgi_arguments(arguments):
    day = date.today()
    number = 1

    for opt in arguments.keys():
        if opt == '-h':
            print(
                f'{os.path.basename(sys.argv[0])} -d <date> -n <number of days>')
            sys.exit()
        elif opt in ("d", "day"):
            try:
                day = datetime.strptime(
                    arguments[opt].value, '%Y-%m-%d').date()
            except:
                print("Error\nEnter date in the format YYYY-MM-DD")
                sys.exit(3)
        elif opt in ("n", "number"):
            number = arguments[opt].value

    return day, number


if __name__ == "__main__":
    if os.getenv("REQUEST_METHOD"):
        # print("running as CGI")
        import cgi
        day, number = cgi_arguments(cgi.FieldStorage())

    else:
        # print("not running as CGI")
        import sys
        import getopt
        day, number = cli_arguments(sys.argv[1:])

    sql = construct_sql(day, number)

    webpage(sql, day, number)
