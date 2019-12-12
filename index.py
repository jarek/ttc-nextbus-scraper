#!/usr/bin/env python2

import datetime
import urllib2
import xml.etree.ElementTree as ET

HTML_URL = 'http://www.nextbus.com/predictor/adaPrediction.jsp?a=ttc&r={route}&s={stop}'
XML_URL = 'http://webservices.nextbus.com/service/publicXMLFeed?command=predictions&a=ttc&r={route}&s={stop}'

DESTINATIONS = {
    'West - 504b King towards Dufferin Gate': 'Dufferin',
    'West - 504a King towards Dundas West Station': 'Dundas West',
    'West - 304 King towards Dundas West Station': 'Dundas West',
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
<meta name="viewport" content="width=device-width">
<meta http-equiv="refresh" content="15">
<title>TTC</title>

<style type="text/css">
    body        { background: #fff; color: #222; font-family: trebuchet ms, serif; }
</style>
''')


print('Content-type: text/html\n')

print_header()

server_now = datetime.datetime.now()
toronto_now = server_now + datetime.timedelta(hours=3)
print('as of ' + toronto_now.strftime('%H:%M:%S'))

print('<h2>504 @ Shaw</h2>')
print_stop('Eastbound', 504, 5422)
print_stop('Westbound to Dundas West', 504, 8560, ['Dundas West'])

print('<h2>63 @ Sudbury</h2>')
print_stop('Northbound', 63, 8998)

print('\n<hr>\n')

print('<h2>504 @ Yonge / King Stn</h2>')
print_stop('Westbound', 504, 23884)  # this is TTC stop 15637, not sure why NextBus is different

print('\n<hr>\n')

print('<h2>63 @ Ossington Stn</h2>')
print_stop('Southbound', 63, 14265)

