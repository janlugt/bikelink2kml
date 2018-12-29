import ast
import fileinput
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

elocker_style = simplekml.Style()
elocker_style.iconstyle.icon.href = 'https://www.bikelink.org/assets/lockers-c9deb0ef775179becfff02261c117aa4.png'
group_style = simplekml.Style()
group_style.iconstyle.icon.href = 'https://www.bikelink.org/assets/group-5637fbe44207d3fe6b92d82bc39a24bc.png'

kml = simplekml.Kml(name = 'BikeLink locations')
locations.sort(key=lambda x: x['human_name'].strip())

for loc in locations:
  # Ignore vendor locations
  loc_type = loc['location_friendly_type']
  if loc_type == 'Vendor':
    continue

  pnt = kml.newpoint(name='<![CDATA[%s]]>' % loc['human_name'].strip())
  pnt.coords = [(loc['longitude'], loc['latitude'])]
  pnt.address = '<![CDATA[%s, %s %s]]>' % (loc['street_address'], loc['state_abbreviation'], loc['postal_code'])
  if loc_type == 'eLocker':
    pnt.style = elocker_style
  elif loc_type == 'Group Parking':
    pnt.style = group_style
  # TODO: add a useful description

kml.save('bikelink.kml')

# Super hacky, because simplekml seems unable to export ampersands
with open('bikelink.kml', 'r') as file:
  filedata = file.read()
filedata = filedata.replace('\u0026', '&')
with open('bikelink.kml', 'w') as file:
  file.write(filedata)
