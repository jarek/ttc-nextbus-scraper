#!/usr/bin/env python2

import urllib2
import xml.etree.ElementTree as ET

HTML_URL = 'http://www.nextbus.com/predictor/adaPrediction.jsp?a=ttc&r={route}&s={stop}'
XML_URL = 'http://webservices.nextbus.com/service/publicXMLFeed?command=predictions&a=ttc&r={route}&s={stop}'

DESTINATIONS = {
    'West - 504b King towards Dufferin Gate': 'Dufferin',
    'West - 504a King towards Dundas West Station': 'Dundas West',
    'East - 504b King towards Broadview Station': 'Broadview',
    'East - 504a King towards Distillery': 'Distillery'
}

def parse_url(address):
    # grab the xml
    text = urllib2.urlopen(address).read()
    root = ET.fromstring(text)

    directions = root[0]

    results = {}

    for destination in directions:
        if destination.tag != 'direction': continue

        dest_text = destination.attrib['title']
        # fall check if there is a better text, back to provided if not
        dest_name = DESTINATIONS.get(dest_text, dest_text)

        results[dest_name] = [
                int(prediction.attrib['minutes'])
                for prediction in destination]

    return results

def print_stop(name, route, stop, destinations=None):
    result = ''

    html_url = HTML_URL.format(route=route, stop=stop)
    escaped_url = html_url.replace('&', '&amp;')  # good enough here

    result += '<p><a href="' + escaped_url + '">' + name + '</a>: '

    xml_url = XML_URL.format(route=route, stop=stop)

    try:
        data = parse_url(xml_url)

        if not destinations:
            predictions_for_destinations = sorted(
                    time
                    for times in data.values()
                    for time in times)
        else:
            predictions_for_destinations = sorted(
                    time
                    for destination, times in data.items()
                    for time in times
                    if destination in destinations)

        result += ', '.join(str(p) for p in predictions_for_destinations)
        result += ' minutes'

    except:
        result += ' unable to fetch'

    print(result)

def print_header():
    print('''<!doctype html>

<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>TTC</title>

<style type="text/css">
    body        { background: #fff; color: #222; font-family: trebuchet ms, serif; }
</style>
''')


print('Content-type: text/html\n')

print_header()

print('<h2>504 @ Shaw</h2>')
print_stop('Eastbound', 504, 5422)
print_stop('Westbound to Dundas West', 504, 8560, ['Dundas West'])

print('\n<hr>\n')

print('<h2>504 @ Dundas West Stn</h2>')
print_stop('Eastbound (+15 min)', 504, 14186)

print('\n<hr>\n')

print('<h2>63 @ Sudbury</h2>')
print_stop('Northbound', 63, 8998)

"""
print_stop('26 Westbound @ Ossington (+20? min)', 26, 9808)

print('\n<hr>\n')

print('<h2>26 to 63</h2>')
print_stop('26 Eastbound @ Edwin', 26, 3828)
print_stop('63 Southbound @ Dupont (+12? min)', 63, 2197)
"""

