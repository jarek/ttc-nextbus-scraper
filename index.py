#!/usr/bin/env python

import urllib2,sys

def parseUrl(address):
	# grab the html
	html = urllib2.urlopen(address).read()

	# grab the table with time estimations
	index = html.find('<table cellpadding')
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
	url = 'http://www.nextbus.com/wireless/miniPrediction.shtml?a=ttc'
	url += '&r=' + `route`
	url += '&d=' + `route` + '_' + direction
	url += '&s=' + stop

	if (escaped != False):
		url = url.replace('&', '&amp;') # poor man's urlencode...

	return url

def printStop(name, route, direction, stop):
	stopUrl = makeStopUrl(route, direction, stop)
	escapedUrl = makeStopUrl(route, direction, stop, True)

	print '<p><a href="' + escapedUrl + '">' + name + '</a>:'
	print parseUrl(stopUrl)

def printHeader():
	print '''<!doctype html>

<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>TTC</title>

<style type="text/css">
	body		{ background: #fff; color: #222; font-family: trebuchet ms, serif; }
</style>
'''


print 'Content-type: text/html\n'

printHeader();

print '<h2>505 Dundas @ Huron</h2>'
printStop('Eastbound', 505, '0_505_conSun', '1479')
printStop('Westbound', 505, '1_505_conSun', '7867')

print '<h2>510 Spadina @ Sullivan</h2>'
printStop('Northbound', 510, '1_510', '1288')
printStop('Southbound', 510, '0_510', '2097')

print '<h2>501 Queen</h2>'
printStop('Eastbound @ Peter', 501, '0_501Sun', '7060')
printStop('Westbound @ Soho', 501, '1_501Sun', '704')

print '\n<hr>\n'

print '<h2>506 College @ Spadina</h2>'
printStop('Eastbound', 506, '0_506Sun', '1010')
printStop('Westbound', 506, '1_506Sun', '9193')

print '\n<hr>\n'

print '<h2>506 + 510</h2>'
printStop('506 Eastbound @ Dufferin', 506, '0_506Sun', '1861')
printStop('510 Southbound @ College (+12 minutes)', 510, '0_510', '3323')

