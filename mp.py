import requests
import json
import sys
import sqlite3
import time
import subprocess
from subprocess import check_output
from collections import OrderedDict
import time


name = sys.argv
def etaFormat(eta):
	hours = int(eta/3600)
	rest = eta - hours*3600
	minutes = int(rest/60)
	rest = rest-minutes*60
	seconds = rest

	if hours<10:
	    hours_s = str(0)+str(hours)
	else:
	    hours_s = str(hours)

	if minutes<10:
	    minutes_s = str(0)+str(minutes)
	else:
	    minutes_s = str(minutes)

	if seconds<10:
	    seconds_s = str(0)+str(seconds)
	else:
	    seconds_s = str(seconds)


	s = int(hours_s+minutes_s+seconds_s)
	return s


def createInput(longitude, latitude, speed, destination_longitude, destination_latitude, eta):
	content = {}
	content['BSAF_out'] = []
	#print(eta)
	#for i in range(len(eta)):
	#	if (eta[i] - round(eta[i]))>0.5:
	#		eta[i] = round(eta[i])+1
	#	else:
	#		eta[i] = round(eta[i])
	#	eta[i] = etaFormat(eta[i])

	a1 = (('stationID',100001),('seqNumber', 1001),('EmV_current_longitude', longitude),('EmV_current_latitude', latitude),('Destination_longitude', destination_longitude),('Destination_latitude', destination_latitude),('Destination_altitude', 200),('ETA', eta[0]),('relevanceDistance', 3),('speed', speed), ('heading', 1000), ('dissemination_area', 0))
	a2 = (('stationID',100002),('seqNumber', 2002),('EmV_current_longitude', longitude),('EmV_current_latitude', latitude),('Destination_longitude', destination_longitude),('Destination_latitude', destination_latitude),('Destination_altitude', 200),('ETA', eta[1]),('relevanceDistance', 3),('speed', speed), ('heading', 1000), ('dissemination_area', 1))
	a3 = (('stationID',100003),('seqNumber', 3003),('EmV_current_longitude', longitude),('EmV_current_latitude', latitude),('Destination_longitude', destination_longitude),('Destination_latitude', destination_latitude),('Destination_altitude', 200),('ETA', eta[2]),('relevanceDistance', 3),('speed', speed), ('heading', 1000), ('dissemination_area', 2))
	a4 = (('stationID',100004),('seqNumber', 4004),('EmV_current_longitude', longitude),('EmV_current_latitude', latitude),('Destination_longitude', destination_longitude),('Destination_latitude', destination_latitude),('Destination_altitude', 200),('ETA', eta[3]),('relevanceDistance', 3),('speed', speed), ('heading', 1000), ('dissemination_area', 3))
	a5 = (('stationID',100005),('seqNumber', 5005),('EmV_current_longitude', longitude),('EmV_current_latitude', latitude),('Destination_longitude', destination_longitude),('Destination_latitude', destination_latitude),('Destination_altitude', 200),('ETA', eta[4]),('relevanceDistance', 3),('speed', speed), ('heading', 1000), ('dissemination_area', 4))
	a6 = (('stationID',100006),('seqNumber', 6006),('EmV_current_longitude', longitude),('EmV_current_latitude', latitude),('Destination_longitude', destination_longitude),('Destination_latitude', destination_latitude),('Destination_altitude', 200),('ETA', eta[5]),('relevanceDistance', 3),('speed', speed), ('heading', 1000), ('dissemination_area', 5))

	b1 = OrderedDict(a1)
	b2 = OrderedDict(a2)
	b3 = OrderedDict(a3)
	b4 = OrderedDict(a4)
	b5 = OrderedDict(a5)
	b6 = OrderedDict(a6)


	c = {"BSAF_out": [b1, b2, b3, b4, b5, b6]}

	#content['BSAF_out'].append({'stationID': 100001,'seqNumber': 1001,'EmV_currrentl_ongitude': longitude,'EmV_current_latitude': latitude,'Destination_longitude': destination_longitude,'Destination_latitude': destination_latitude,'Destination_altitude': 200,'ETA': eta,'relevanceDistance': 3,'speed': speed, 'heading': 1000, 'dissemination_area': dissemination_area})
	#content = str(content)
	#content_new = json.loads(content, object_pairs_hook=OrderedDict)

	f = open('/home/dockerized/vanetza-v1/build/bin/BSAF_out.json', 'w')
	json.dump(c, f, indent = 4)
	#json.dump(c, f, sort_keys=True, indent = 4)
	f.close()
	return c



def createAvro(emv_id, etas, location, destination, speed, disseminationAreas):
#while True:
	#r1 =requests.get("http://217.77.85.130:31125/api/v1/appmanager/namespaces/helm-sandbox/apps/test") 
	#monitoring_input = requests.get("http://193.190.127.200:5000/api/v1/resources/nodes")
	def dict_factory(cursor, row):
    		d = {}
    		for idx, col in enumerate(cursor.description):
        		d[col[0]] = row[idx]
    		return d

	conn = sqlite3.connect('domainAdb.db')
	conn.row_factory = dict_factory
	cur = conn.cursor()

	#all_etas = cur.execute('SELECT * FROM eta;').fetchall()
	#holder = emv_id - 1
	#etas = [all_etas[1 + 6*holder]["eta"],all_etas[0 + 6*holder]["eta"],all_etas[2 + 6*holder]["eta"],all_etas[3 + 6*holder]["eta"],all_etas[4 + 6*holder]["eta"],all_etas[5 + 6*holder]["eta"]]
	#dissemination_areas = [all_etas[0]["dissemination_area"],all_etas[1]["dissemination_area"],all_etas[2]["dissemination_area"],all_etas[3]["dissemination_area"],all_etas[4]["dissemination_area"],all_etas[5]["dissemination_area"]]

	#current_state = cur.execute('SELECT * FROM state;').fetchall()
	#speed = current_state[emv_id-1]["speed"]
	#location_longitude = current_state[emv_id-1]["location_longitude"]
	#location_latitude = current_state[emv_id-1]["location_latitude"]
	#destination_latitude = current_state[emv_id-1]["destination_longitude"]
	#destination_longitude = current_state[emv_id-1]["destination_latitude"]

	location_longitude = location["location_longitude"]
	location_latitude = location["location_latitude"]
	destination_latitude = destination["destination_longitude"]
	destination_longitude = destination["destination_latitude"]




	#input_encoder = createInput(1, 1, 1, 1, 1, etas, dissemination_areas)

	input_encoder = createInput(location_longitude, location_latitude, speed, destination_longitude, destination_latitude, etas)
	#print(input_encoder)
	
	#with open('/home/dockerized/vanetza-v1/build/bin/BSAF_out.json') as json_file:
	#	input_encoder = json.load(json_file)
	subprocess.run("/home/dockerized/vanetza-v1/build/bin/socktap-denm_enc_hex")
	with open('/home/dockerized/vanetza-v1/build/bin/DENM_PDUS.json') as json_file:
		encode_output = json.load(json_file)
	#print(encode_output)
	#with open('DENM_PDU_1.bin', mode='rb') as file: # b is important -> binary
	#	fileContent = file.read()
	#print(fileContent)
	#out = check_output(["/home/dockerized/vanetza-v1/build/bin/socktap-denm_enc_hex"])
	#with open('DENM_PDU_1.bin', mode='rb') as file: # b is important -> binary
	#	fileContent = file.read()
	#print("\n")
	#print("\n")
	#print(out)
	#print("\n")
	#print("\n")

	#data_1 = {"value_schema_id": 41,"records":[{"value":{"pdu":{"bytes": encode_output["BSAF_PDUS"][0]["PDU"]},"appRequestType":"AppMessage_trigger","messageId":{"com.nokia.messageAPI.uniqueId":{"applicationId":"APP_ID-428952369","sequenceNumber": 1}},"repetitionInterval":{"int":0},"repetitionDuration":{"int":0},"validityDuration":{"int":0},"referenceTime":0,"disseminationArea":{"com.nokia.messageAPI.geoArea":{"area":"CIRCLE","latitude":input_encoder["BSAF_out"][0]["dissemination_area"],"longitude":0,"semiMajorAxis":0,"semiMinorAxis":0,"azimuthAngle":0}}}}]}
	#data_2 = {"value_schema_id": 41,"records":[{"value":{"pdu":{"bytes": encode_output["BSAF_PDUS"][1]["PDU"]},"appRequestType":"AppMessage_trigger","messageId":{"com.nokia.messageAPI.uniqueId":{"applicationId":"APP_ID-428952369","sequenceNumber": 1}},"repetitionInterval":{"int":0},"repetitionDuration":{"int":0},"validityDuration":{"int":0},"referenceTime":0,"disseminationArea":{"com.nokia.messageAPI.geoArea":{"area":"CIRCLE","latitude":input_encoder["BSAF_out"][1]["dissemination_area"],"longitude":0,"semiMajorAxis":0,"semiMinorAxis":0,"azimuthAngle":0}}}}]}
	#data_3 = {"value_schema_id": 41,"records":[{"value":{"pdu":{"bytes": encode_output["BSAF_PDUS"][2]["PDU"]},"appRequestType":"AppMessage_trigger","messageId":{"com.nokia.messageAPI.uniqueId":{"applicationId":"APP_ID-428952369","sequenceNumber": 1}},"repetitionInterval":{"int":0},"repetitionDuration":{"int":0},"validityDuration":{"int":0},"referenceTime":0,"disseminationArea":{"com.nokia.messageAPI.geoArea":{"area":"CIRCLE","latitude":input_encoder["BSAF_out"][2]["dissemination_area"],"longitude":0,"semiMajorAxis":0,"semiMinorAxis":0,"azimuthAngle":0}}}}]}
	#data_4 = {"value_schema_id": 41,"records":[{"value":{"pdu":{"bytes": encode_output["BSAF_PDUS"][3]["PDU"]},"appRequestType":"AppMessage_trigger","messageId":{"com.nokia.messageAPI.uniqueId":{"applicationId":"APP_ID-428952369","sequenceNumber": 1}},"repetitionInterval":{"int":0},"repetitionDuration":{"int":0},"validityDuration":{"int":0},"referenceTime":0,"disseminationArea":{"com.nokia.messageAPI.geoArea":{"area":"CIRCLE","latitude":input_encoder["BSAF_out"][3]["dissemination_area"],"longitude":0,"semiMajorAxis":0,"semiMinorAxis":0,"azimuthAngle":0}}}}]}
	#data_5 = {"value_schema_id": 41,"records":[{"value":{"pdu":{"bytes": encode_output["BSAF_PDUS"][4]["PDU"]},"appRequestType":"AppMessage_trigger","messageId":{"com.nokia.messageAPI.uniqueId":{"applicationId":"APP_ID-428952369","sequenceNumber": 1}},"repetitionInterval":{"int":0},"repetitionDuration":{"int":0},"validityDuration":{"int":0},"referenceTime":0,"disseminationArea":{"com.nokia.messageAPI.geoArea":{"area":"CIRCLE","latitude":input_encoder["BSAF_out"][4]["dissemination_area"],"longitude":0,"semiMajorAxis":0,"semiMinorAxis":0,"azimuthAngle":0}}}}]}
	#data_6 = {"value_schema_id": 41,"records":[{"value":{"pdu":{"bytes": encode_output["BSAF_PDUS"][5]["PDU"]},"appRequestType":"AppMessage_trigger","messageId":{"com.nokia.messageAPI.uniqueId":{"applicationId":"APP_ID-428952369","sequenceNumber": 1}},"repetitionInterval":{"int":0},"repetitionDuration":{"int":0},"validityDuration":{"int":0},"referenceTime":0,"disseminationArea":{"com.nokia.messageAPI.geoArea":{"area":"CIRCLE","latitude":input_encoder["BSAF_out"][5]["dissemination_area"],"longitude":0,"semiMajorAxis":0,"semiMinorAxis":0,"azimuthAngle":0}}}}]}
	message1 = str(encode_output["BSAF_PDUS"][0]["PDU"])
	message2 = str(encode_output["BSAF_PDUS"][1]["PDU"])
	message3 = str(encode_output["BSAF_PDUS"][2]["PDU"])
	message4 = str(encode_output["BSAF_PDUS"][3]["PDU"])
	message5 = str(encode_output["BSAF_PDUS"][4]["PDU"])
	message6 = str(encode_output["BSAF_PDUS"][5]["PDU"])

	#disseminationAreas = requests.get("http://localhost:5000/api/v1/eta")
	#disseminationAreas = disseminationAreas.json()
	#print(disseminationAreas)
	
	data_1 = {"value_schema_id": 41,"records":[{"value":{"pdu":{"bytes": message1},"appRequestType":"AppMessage_trigger","messageId":{"com.nokia.messageAPI.uniqueId":{"applicationId":"APP_ID-428952369","sequenceNumber": 1}},"repetitionInterval":{"int":0},"repetitionDuration":{"int":0},"validityDuration":{"int":0},"referenceTime":None,"disseminationArea":{"com.nokia.messageAPI.geoArea":{"area":"CIRCLE","latitude": disseminationAreas[0][0]*100000,"longitude": disseminationAreas[0][1]*100000,"semiMajorAxis":500,"semiMinorAxis":0,"azimuthAngle":0}}}}]}
	data_2 = {"value_schema_id": 41,"records":[{"value":{"pdu":{"bytes": message2},"appRequestType":"AppMessage_trigger","messageId":{"com.nokia.messageAPI.uniqueId":{"applicationId":"APP_ID-428952369","sequenceNumber": 1}},"repetitionInterval":{"int":0},"repetitionDuration":{"int":0},"validityDuration":{"int":0},"referenceTime":None,"disseminationArea":{"com.nokia.messageAPI.geoArea":{"area":"CIRCLE","latitude": disseminationAreas[1][0]*100000,"longitude": disseminationAreas[1][1]*100000,"semiMajorAxis":500,"semiMinorAxis":0,"azimuthAngle":0}}}}]}
	data_3 = {"value_schema_id": 41,"records":[{"value":{"pdu":{"bytes": message3},"appRequestType":"AppMessage_trigger","messageId":{"com.nokia.messageAPI.uniqueId":{"applicationId":"APP_ID-428952369","sequenceNumber": 1}},"repetitionInterval":{"int":0},"repetitionDuration":{"int":0},"validityDuration":{"int":0},"referenceTime":None,"disseminationArea":{"com.nokia.messageAPI.geoArea":{"area":"CIRCLE","latitude": disseminationAreas[2][0]*100000,"longitude": disseminationAreas[2][1]*100000,"semiMajorAxis":500,"semiMinorAxis":0,"azimuthAngle":0}}}}]}
	data_4 = {"value_schema_id": 41,"records":[{"value":{"pdu":{"bytes": message4},"appRequestType":"AppMessage_trigger","messageId":{"com.nokia.messageAPI.uniqueId":{"applicationId":"APP_ID-428952369","sequenceNumber": 1}},"repetitionInterval":{"int":0},"repetitionDuration":{"int":0},"validityDuration":{"int":0},"referenceTime":None,"disseminationArea":{"com.nokia.messageAPI.geoArea":{"area":"CIRCLE","latitude": disseminationAreas[3][0]*100000,"longitude": disseminationAreas[3][1]*100000,"semiMajorAxis":500,"semiMinorAxis":0,"azimuthAngle":0}}}}]}
	data_5 = {"value_schema_id": 41,"records":[{"value":{"pdu":{"bytes": message5},"appRequestType":"AppMessage_trigger","messageId":{"com.nokia.messageAPI.uniqueId":{"applicationId":"APP_ID-428952369","sequenceNumber": 1}},"repetitionInterval":{"int":0},"repetitionDuration":{"int":0},"validityDuration":{"int":0},"referenceTime":None,"disseminationArea":{"com.nokia.messageAPI.geoArea":{"area":"CIRCLE","latitude": disseminationAreas[4][0]*100000,"longitude": disseminationAreas[4][1]*100000,"semiMajorAxis":500,"semiMinorAxis":0,"azimuthAngle":0}}}}]}
	data_6 = {"value_schema_id": 41,"records":[{"value":{"pdu":{"bytes": message6},"appRequestType":"AppMessage_trigger","messageId":{"com.nokia.messageAPI.uniqueId":{"applicationId":"APP_ID-428952369","sequenceNumber": 1}},"repetitionInterval":{"int":0},"repetitionDuration":{"int":0},"validityDuration":{"int":0},"referenceTime":None,"disseminationArea":{"com.nokia.messageAPI.geoArea":{"area":"CIRCLE","latitude": disseminationAreas[5][0]*100000,"longitude": disseminationAreas[5][1]*100000,"semiMajorAxis":500,"semiMinorAxis":0,"azimuthAngle":0}}}}]}
	
	endpoint = "http://80.159.227.35:8082/topics/MESSAGE_AVRO_DATA"
	headers = {'Content-Type': 'application/vnd.kafka.avro.v2+json','Accept': 'application/vnd.kafka.v2+json'}
	#r1 = requests.post(endpoint, data=json.dumps(data_1), headers=headers)
	#r2 = requests.post(endpoint, data=json.dumps(data_2), headers=headers)
	#r3 = requests.post(endpoint, data=json.dumps(data_3), headers=headers)
	#r4 = requests.post(endpoint, data=json.dumps(data_4), headers=headers)
	#r5 = requests.post(endpoint, data=json.dumps(data_5), headers=headers)
	#r6 = requests.post(endpoint, data=json.dumps(data_6), headers=headers)

	#print(data_1)
	#print(data_2)
	#print(data_3)
	print(data_4)
	print(data_5)
	print(data_6)

	#print(r1)
	#print(r2)
	#print(r3)
	#print(r4)
	#print(r5)
	#print(r6)
	#print("\n")
	#ts = time.time()
	#ts_readable = time.ctime(ts)
	#print(ts_readable)
	#time.sleep(5)
#createAvro()








