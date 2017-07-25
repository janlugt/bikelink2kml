import ast
import re
import simplekml
import urllib2

response = urllib2.urlopen('https://www.bikelink.org/map')
html = response.read()
lines = html.splitlines()
location_strings = filter(lambda x:'bl_map.add_location' in x, lines)
locations = []
for str in location_strings:
  dict_search = re.search('bl_map.add_location\((.*)\);', str, re.IGNORECASE)
  dict = dict_search.group(1) \
    .replace(':null,', ':None,') \
    .replace(':false,', ':False,') \
    .replace(':true,', ':True,')
  locations.append(ast.literal_eval(dict))

kml = simplekml.Kml()
for l in locations:
  kml.newpoint(name=l['street_address'], coords=[(l['longitude'], l['latitude'])])
  
kml.save('bikelink.kml')
