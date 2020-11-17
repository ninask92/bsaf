import gpxpy
import gpxpy.gpx
import requests
import json
import sys
import sqlite3
import time
import subprocess
from subprocess import check_output
from collections import OrderedDict
import geopy.distance
import bsafMainNew
from bsafMainNew import bsaf_main
import mp
from mp import createAvro
#import mapa
#from mapa import drawMap 




def createInput(longitude, latitude, speed, destination_longitude, destination_latitude):

	a1 = {"stationID": 100001, "EmV_current_longitude": longitude, "EmV_current_latitude": latitude, "Destination_longitude": destination_longitude, "Destination_latitude": destination_latitude, "speed": speed}
	#c = {"CAMv2": a1}

	#content['BSAF_out'].append({'stationID': 100001,'seqNumber': 1001,'EmV_currrentl_ongitude': longitude,'EmV_current_latitude': latitude,'Destination_longitude': destination_longitude,'Destination_latitude': destination_latitude,'Destination_altitude': 200,'ETA': eta,'relevanceDistance': 3,'speed': speed, 'heading': 1000, 'dissemination_area': dissemination_area})
	#content = str(content)
	#content_new = json.loads(content, object_pairs_hook=OrderedDict)

	f = open('/home/dockerized/vanetza-v1/build/bin/CAMv2.json', 'w')
	json.dump(a1, f)
	#json.dump(a1, f, sort_keys=True, indent = 4)
	f.close()
	return a1



def main():
	lon = []
	lat = []

	destination = requests.get("http://localhost:5000/api/v1/state/destination")
	destination = destination.json()
	destination_latitude = destination["latitude"]
	destination_longitude = destination["longitude"]

	lat_previous = 46.98896020
	lon_previous = 11.49748240
	area1 = [46.9917970, 11.4989080]
	area2 = [46.9969320, 11.5030600]
	area3 = [47.0022330, 11.5070870]
	area4 = [47.0083850, 11.5085370]
	area5 = [47.0143620, 11.5077130]
	area6 = [47.0198840, 11.5050900]


	while True:
		time.sleep(5)
		gpx_file = open('map_new.gpx', 'r', encoding="utf-8")  # Data from the E313 highway
		gpx = gpxpy.parse(gpx_file)               # this will read all data points from .gpx file
		for track in gpx.tracks:
			for segment in track.segments:
				for point in segment.points:
					start_time = time.time()
					lat_current = point.latitude
					lon_current = point.longitude
					location = {"longitude": lon_current, "latitude": lat_current}
					r = requests.put("http://localhost:5000/api/v1/state/location", json=location)
					#drawMap(lat_current, lon_current)
					coords_1 = (lat_previous, lon_previous)
					coords_2 = (lat_current, lon_current)
					dist = geopy.distance.distance(coords_1, coords_2).km
					t_current = dist*1000/30
					lat.append(point.latitude)   #this will save all latitude points in an array
					lon.append(point.longitude)  #this will save all longitude points in an array
					lat_previous = lat_current
					lon_current = lon_current
					testic = createInput(point.longitude, point.latitude, 30, destination_longitude, destination_latitude)
					bsaf_main()
					createAvro()
					#time.sleep(t_current) #Adjust this to get the best performance
					ts = time.time()
					ts_readable = time.ctime(ts)
					print(ts_readable)
					duration = time.time() - start_time
					print(duration)
					time.sleep(1)
		
		eta_json  = {"data":[{"id": 1,"eta": 0,"area_latitude": area1[0], "area_longitude": area1[1]},{"id":2,"eta":0,"area_latitude": area2[0], "area_longitude": area2[1]},{"id": 3,"eta": 0, "area_latitude": area3[0], "area_longitude": area3[1]},{"id": 4,"eta": 0,"area_latitude": area4[0], "area_longitude": area4[1]},{"id": 5,"eta": 0,"area_latitude": area5[0], "area_longitude": area5[1]},{"id": 6,"eta": 0,"area_latitude": area6[0], "area_longitude": area6[1]}]}
		r = requests.put("http://localhost:5000/api/v1/eta", json=eta_json)
		time.sleep(100)
main()





