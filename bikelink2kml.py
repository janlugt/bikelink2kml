import ast
from bs4 import BeautifulSoup
import fileinput
import json
import re
import simplekml
import urllib.request

response = urllib.request.urlopen('https://www.bikelink.org/maps')
html_doc = str(response.read())
bs = BeautifulSoup(html_doc, features="lxml")
locations_text = [item["data-locations"] for item in bs.find_all() if "data-locations" in item.attrs][0]
locations = json.loads(locations_text)

#  dict = dict_search.group(1) \
#    .replace(':null,', ':None,') \
#    .replace(':false,', ':False,') \
#    .replace(':true,', ':True,')
#  locations.append(ast.literal_eval(dict))
locations.sort(key=lambda x: x['human_name'].strip())

elocker_style = simplekml.Style()
elocker_style.iconstyle.icon.href = 'https://www.bikelink.org/assets/lockers-c9deb0ef775179becfff02261c117aa4.png'
group_style = simplekml.Style()
group_style.iconstyle.icon.href = 'https://www.bikelink.org/assets/group-5637fbe44207d3fe6b92d82bc39a24bc.png'

kml = simplekml.Kml(name = 'BikeLink locations')

for loc in locations:
  # Ignore vendor locations
  loc_type = loc['location_friendly_type']
  if loc_type == 'Vendor':
    continue

  pnt = kml.newpoint(name='<![CDATA[%s]]>' % loc['human_name'].strip())
  pnt.coords = [(loc['longitude'], loc['latitude'])]
  pnt.address = '<![CDATA[%s]]>' % (loc['street_address'])
  if loc_type == 'eLocker':
    pnt.style.labelstyle.color = simplekml.Color.blue
  elif loc_type == 'Group Parking':
    pnt.style.labelstyle.color = simplekml.Color.yellow
  # TODO: add a useful description

kml.save('bikelink.kml')

# Super hacky, because simplekml seems unable to export ampersands
with open('bikelink.kml', 'r') as file:
  filedata = file.read()
filedata = filedata.replace('\u0026', '&')
with open('bikelink.kml', 'w') as file:
  file.write(filedata)
