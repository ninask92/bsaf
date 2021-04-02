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
#import bsafMainNew
#from bsafMainNew import bsaf_main
#import mp
#from mp import createAvro
#import mapa
#from mapa import drawMap 
import bsafMainNew
from bsafMainNew import bsaf_main
import mp
from mp import createAvro
import cpu_mem
from cpu_mem import measureCpuMem

def createInput(id, longitude, latitude, speed, destination_longitude, destination_latitude):

	a1 = {"stationID": 100001, "EmV_current_longitude": longitude, "EmV_current_latitude": latitude, "Destination_longitude": destination_longitude, "Destination_latitude": destination_latitude, "speed": speed}
	#c = {"CAMv2": a1}

	#content['BSAF_out'].append({'stationID': 100001,'seqNumber': 1001,'EmV_currrentl_ongitude': longitude,'EmV_current_latitude': latitude,'Destination_longitude': destination_longitude,'Destination_latitude': destination_latitude,'Destination_altitude': 200,'ETA': eta,'relevanceDistance': 3,'speed': speed, 'heading': 1000, 'dissemination_area': dissemination_area})
	#content = str(content)
	#content_new = json.loads(content, object_pairs_hook=OrderedDict)

	main_path = '/home/dockerized/vanetza-v1/build/bin/'
	addon = main_path + 'CAMv' + str(id) + '.json'
	f = open(addon, 'w')
	json.dump(a1, f)
	#json.dump(a1, f, sort_keys=True, indent = 4)
	f.close()
	return a1


def loadMap():
	gpx_file = open('map_new.gpx', 'r', encoding="utf-8")  # Data from the E313 highway
	gpx = gpxpy.parse(gpx_file)               # this will read all data points from .gpx file
	map_loaded = []
	for track in gpx.tracks:
		for segment in track.segments:
			for point in segment.points:
				pair = [point.latitude, point.longitude]
				map_loaded.append(pair)
	return map_loaded

def generateCAM(emv_id, frequency, map):
	area1 = [46.9917970, 11.4989080]
	area2 = [46.9969320, 11.5030600]
	area3 = [47.0022330, 11.5070870]
	area4 = [47.0083850, 11.5085370]
	area5 = [47.0143620, 11.5077130]
	area6 = [47.0198840, 11.5050900]

	disseminationAreas = [area1, area2, area3, area4, area5, area6]
	if frequency == 1:
		delay = 10
		sleep = 1
	elif frequency == 5:
		delay = 5
		sleep = 0.2
	else:
		delay = 1
		sleep = 0.1
	print(delay)
	for i in range(0, len(map), 2):
		start_time = time.time()
		print(i, map[i])
		location = {"id": emv_id, "location_longitude": map[i][1], "location_latitude": map[i][0]}
		r = requests.put("http://localhost:5000/api/v1/state/location", json=location)
		speed = 30
		destination = {"destination_latitude": 47.02202690, "destination_longitude": 11.50231930}
		testic = createInput(emv_id, map[i][1], map[i][0], speed, destination["destination_longitude"], destination["destination_latitude"])
		main_path = '/home/dockerized/vanetza-v1/build/bin/'
		addon = main_path + 'CAMv' + str(emv_id) + '.json'
		etas = bsaf_main(addon, emv_id)
		createAvro(emv_id, etas, location, destination, speed, disseminationAreas)
		duration = time.time() - start_time
		computingDelay_json = {"instanceID": 1, "computingDelay": duration}
		r = requests.put("http://localhost:5000/api/v1/results/computingDelay", json=computingDelay_json)
		measureCpuMem()
		#time.sleep(0.5)


#mapa = loadMap()
#generateCAM(1, 1, mapa)













