#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Encoding: UTF-8

from sql import do_sql

import sqlparse
import os

from datetime import date, timedelta, datetime


def construct_sql(day, number):
    last = day + timedelta(days=int(number) - 1)

    sql = ("SELECT time, AVG(temp) AS temp, AVG(wind) AS wind FROM forecast " +
           "WHERE DATE_SUB(`time`,INTERVAL 1 HOUR) AND " +
           "DATE(time) >= '" + str(day) +
           "' AND DATE(time) <= '" + str(last) +
           "'GROUP BY DATE(time), HOUR(time)")

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

    print("['Time', 'Temp', 'Wind'],")

    answer = do_sql(sql)

    for line in answer:
        print(f'["{line[0]}", {line[1]}, {line[2]}],')
    print("]);")

    print()
    print("var options = {")
    print("title: 'Weather forecast',")
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

    print(sqlparse.format(sql, reindent=True))  # , keyword_case='upper'))

    print("<div id='curve_chart' style='width: 1200px; height: 700px'></div>")
    print("</body>")
    print("</html>")


def cli_arguments(argv, day, number):

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


def cgi_arguments(arguments, day, number):

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
    day = date.today()
    number = 2

    if os.getenv("REQUEST_METHOD"):
        # print("running as CGI")
        import cgi
        day, number = cgi_arguments(cgi.FieldStorage(), day, number)

    else:
        # print("not running as CGI")
        import sys
        import getopt
        day, number = cli_arguments(sys.argv[1:], day, number)

    sql = construct_sql(day, number)

    webpage(sql, day, number)
