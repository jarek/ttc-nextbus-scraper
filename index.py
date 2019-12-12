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
    'West - 504s King Short Turn towards Roncesvalles and Queen': 'Sunnyside',
    'East - 504b King towards Broadview Station': 'Broadview',
    'East - 504a King towards Distillery': 'Distillery',
    'East - 504s King Short Turn towards Broadview Ave': 'Broadview and Queen',
}

def parse_url(address):
    text = urllib2.urlopen(address).read()
    root = ET.fromstring(text)
    all_predictions = root[0]

    def _destination_name(elem):
        dest_text = elem.attrib['title']
        # check if there is a better text, fall back to provided if not
        return DESTINATIONS.get(dest_text, dest_text)

    def _predictions(elem):
        return [int(prediction.attrib['minutes']) for prediction in elem]

    results = {_destination_name(destination): _predictions(destination)
               for destination in all_predictions
               if destination.tag == 'direction'}

    return results

def format_stop(name, route, stop, destinations=None):
    result = ''

    html_url = HTML_URL.format(route=route, stop=stop)
    escaped_url = html_url.replace('&', '&amp;')  # good enough here

    result += '<p><a href="' + escaped_url + '">' + name + '</a>: '

    xml_url = XML_URL.format(route=route, stop=stop)

    try:
        data = parse_url(xml_url)

        if destinations:
            # filter to only requested destinations
            data = {destination: times for destination, times in data.items()
                    if destination in destinations}

        # collapse all destinations together and
        # sort to earliest times regardless of destination
        predictions_for_destinations = sorted(time
                                              for times in data.values()
                                              for time in times)

        result += ', '.join(str(p) for p in predictions_for_destinations)
        result += ' minutes'

    except:
        result += ' unable to fetch'

    return result

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
print(format_stop('Eastbound', 504, 5422))
print(format_stop('Westbound to Dundas West', 504, 8560, ['Dundas West']))

print('<h2>63 @ Sudbury</h2>')
print(format_stop('Northbound', 63, 8998))

print('\n<hr>\n')

print('<h2>504 @ Yonge / King Stn</h2>')
print(format_stop('Westbound', 504, 23884))  # this is TTC stop 15637, not sure why NextBus is different

print('\n<hr>\n')

print('<h2>63 @ Ossington Stn</h2>')
print(format_stop('Southbound', 63, 14265))

