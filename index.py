#!/usr/bin/env python

import urllib2,sys

def parseUrl(address):
	# grab the html
	html = urllib2.urlopen(address).read()

	# grab the table with time estimations
	index = html.find('<table class="adaPredictionTable"')
	html = html[index:]

	index = html.find('</table>') + 8
	html = html[0:index]

	# estimate for each car is in a separate <tr>
	# formatted in a given way. do dirty text searches
	text = ''
	rowindex = html.find('<tr>')
	while (rowindex > -1):
		index = html.find('&nbsp;', rowindex) + 6
		index2 = html.find('</span>', index)
		text += html[index:index2] + ', '

		html = html[rowindex + 4:]
		rowindex = html.find('<tr>')

	text = text[:-2] + ' minutes'
	return text

def makeStopUrl(route, direction, stop, escaped = False):
	url = 'http://www.nextbus.com/predictor/adaPrediction.jsp?a=ttc'
	url += '&r=' + str(route)
	url += '&d=' + str(route) + '_' + direction
	url += '&s=' + stop

	if (escaped != False):
		url = url.replace('&', '&amp;') # poor man's urlencode...

	return url

def printStop(name, route, direction, stop):
	stopUrl = makeStopUrl(route, direction, stop)
	escapedUrl = makeStopUrl(route, direction, stop, True)

	print('<p><a href="' + escapedUrl + '">' + name + '</a>:')
	print(parseUrl(stopUrl))

def printHeader():
	print('''<!doctype html>

<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>TTC</title>

<style type="text/css">
	body		{ background: #fff; color: #222; font-family: trebuchet ms, serif; }
</style>
''')


print('Content-type: text/html\n')

printHeader()

print('<h2>504 @ Shaw</h2>')
printStop('Eastbound', 504, '504_0_504Abr', '5422')
printStop('Westbound (click through and check destination!)', 504, '504_1_504B', '8560')

print('\n<hr>\n')

print('<h2>504 @ Dundas West Stn</h2>')
printStop('Eastbound (+15 min)', 504, '504_0_504Abr', '14186')

"""
print('<h2>63 to 26</h2>')
printStop('63 Northbound @ Sudbury', 63, '63_1_63AamSun', '8998')
printStop('26 Westbound @ Ossington (+20? min)', 26, '26_1_26', '9808')

print('\n<hr>\n')

print('<h2>26 to 63</h2>')
printStop('26 Eastbound @ Edwin', 26, '26_0_26', '3828')
printStop('63 Southbound @ Dupont (+12? min)', 63, '63_0_63A', '2197')
"""

