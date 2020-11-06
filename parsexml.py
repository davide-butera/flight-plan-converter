import xml.etree.ElementTree as ET
import os
import pathlib
import xmltodict
from dd2dms import *

dir_path = os.path.dirname(os.path.realpath(__file__))

tree = ET.parse('KSFO-EDDF.fpl')
root = tree.getroot()

waypoints = []
for waypoint in root.iter('waypoint'):
    identifier = waypoint.find('identifier')
    wp_type = waypoint.find('type')
    lat = waypoint.find('lat')
    lon = waypoint.find('lon')
    lat_dms = dd2dms(float(lat.text), type='lat')
    lon_dms = dd2dms(float(lon.text), type='lon')

    wp = {
        "id": identifier.text,
        "ATCWaypointType": wp_type.text,
        "WorldPosition": f"{lat_dms},{lon_dms},+00"
    }
    waypoints.append(wp)
    print(wp)
    print()

tree2 = ET.parse('KSFO-EDDF.PLN')
root2 = tree2.getroot()
fp = root2.find("FlightPlan.FlightPlan")
for wp in waypoints:
    child = ET.Element("ATCWaypoint", id=wp['id'])
    fp.append(child)
    wp_type = ET.Element("ATCWaypointType")
    wp_type.text = wp['ATCWaypointType']
    wp_world_position = ET.Element("WorldPosition")
    wp_type.insert(1, wp_world_position)

    child.append(wp_type)


tree2.write("filename.xml")
