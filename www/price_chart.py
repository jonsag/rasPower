#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Encoding: UTF-8

from sql import do_sql

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

print("['Hour', 'SEK'],")
sql = ("SELECT hour, SEK_per_kWh FROM price")

answer = do_sql(sql)

for line in answer:
    print(f'["{line[0]}", {line[1]}],')
print("]);")

print()
print("var options = {")
print("title: 'Electricity price/hour',")
#print("curveType: 'function',")
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
print("<div id='curve_chart' style='width: 1200px; height: 700px'></div>")
print("</body>")
print("</html>")
