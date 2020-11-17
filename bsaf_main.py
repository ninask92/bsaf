#The Python code describing the Estimated time of arrival process is given as below.
#In order to simplify the understanding of this code,
#we explained each line of the code.  Here it is applied the Kalman filter to predict and estimate the ETA.
# Also a comparison between the estimated and the measured data is done.


import numpy as np
import pymap3d as pm
import math
import time
import threading
import json
import requests
import gpxpy 
import gpxpy.gpx 
import ijson

#read json
import json


def pairs(list1, list2):
     pair = []
     for i in range(len(list1)):
          pair.append([list1[i], list2[i]])
     return pair

def fileWatcher():
     global comandos, comandosText
     comandosText = {'random': 1}
     while True:
          start = time.time()
          f = open('/home/dockerized/vanetza-v1/build/bin/CAMv2.json')
          content = f.read()
          f.close()

          if content != comandosText:
            #print("File was modified! Reloading it...")
               lat = []                 # Latitude of interested points ETA 1
               lon = []                 # Longitude of interested points
               distance = []            # distance between two points of interest
               ETA_t = []               # Estimated Time of Arrival
               ETA_Measured = []        # Measured Time of Arrival
               ETA_Measured_Interval_Data = []   # Measured Time of Arrival per Interval  1 and 2
               P = []                   # The error covariance
#from jsonstreamer import JSONStreamer
               comandos = json.loads(content)
               comandosText = content
               data = comandos
               longitude = data['EmV_current_longitude']
               latitude = data['EmV_current_latitude']
               #lat_e = float(latitude) /10000000  #
               #lon_e = float(longitude)/10000000
               lat_e = latitude
               lon_e = longitude
               speed = data['speed']
               emvID = data['stationID']
               location = {"longitude": lon_e, "latitude": lat_e}
               speed_json  = {"speed": speed}
               emvID = {"emvID": emvID}

            #destination
            #
               longitude = data['Destination_longitude']
               latitude = data['Destination_latitude']

               destination = {"longitude": longitude, "latitude": latitude}

            #This part of the code is useful for importing all data points (nodes) in which the emergency vehicle is supposed to drive.
            #Please add route in which the emergency vehicle will have to drive
               gpx_file = open('map.gpx', 'r', encoding="utf-8")  # Data from the E313 highway
               gpx = gpxpy.parse(gpx_file)               # this will read all data points from .gpx file
               for track in gpx.tracks:
                    for segment in track.segments:
                         for point in segment.points:
                              lat.append(point.latitude)   #this will save all latitude points in an array
                              lon.append(point.longitude)  #this will save all longitude points in an array

               speed = 23 # since its zero
#This part of the code will use latitude and longitude points to convert them in x, y, z
               [xe, ye, ze] = pm.geodetic2ned(lat_e, lon_e, 0, lat[0], lon[0], 0)   #Position of emergency vehicle in x, y, z
               [xn, yn, zn] = pm.geodetic2ned(lat, lon, 0, lat[0], lon[0], 0)


# Initialization of state condition
               A = 1 #The transition factor, one element since ETA denote travel times and is one-dimensional
               B = 1 #The input effect, one element since ETA denote travel times and is one-dimensional
               U = 1/speed #The control input
               H = 1 #The control which relates the state to the data measurement, one element since ETA denote travel times and is one-dimensional
               Q = 3 #The process noise covariance Q
               R = 12#The measurement noise covariance R
               ETA_tp = 0  #The ETA of the first step
               P_tp = 0  #The state covariance of the first step
               d1 = 0
               d_t1 = []
               start = 1
               ETA_Measured_Interval_Data = []
#In our study,  no additional traffic parameter other than travel time is involved

#the travel time of the energency vehicle to the first node. This value should be zero or near zero,
# since the vehicle will start to drive from the nearest node.

               ETA_Measured_Interval_Data_tp =(math.sqrt((xn[0] - xe)**2 + (yn[0] - ye)**2 + (zn[0] - ze)**2))/speed
               dd1 =  (math.sqrt((xn[0] - xe)**2 + (yn[0] - ye)**2 + (zn[0] - ze)**2))
               ddp =  (math.sqrt((xn[0] - xe)**2 + (yn[0] - ye)**2 + (zn[0] - ze)**2))

               for j in range(1, len(xn)):
                    if dd1 < 500 + ddp:
                         d = math.sqrt((xn[j] - xn[j - start]) ** 2 + (yn[j] - yn[j - start]) ** 2 + (zn[j] - zn[j - start]) ** 2)  # distance between points (nodes). This create segments of the interested roude
                         ETA_Interval_from_d = float(d) / speed  # time interval which the vehicles drives in the specific segment
                         distance.append(d)
                         ETA_Measured_Interval_Data.append(ETA_Interval_from_d)
                         dd1 = d + dd1
                         nn1 = len(ETA_Measured_Interval_Data)
                         ETA_predicted = A * ETA_tp + B * U * d  # Prediction Step
                         P_p = A * P_tp * A + Q  # The state covariance of previous step
                         KG = P_p * H / (P_p + R)  # Klaman gain which tells how much the predictions should be corrected on time step k
                         ETA_Measured1 = ETA_Measured_Interval_Data[j-1] + ETA_Measured_Interval_Data_tp  # Considering every segment data to have measured time arrival
                         ETA_update = ETA_predicted + KG * (ETA_Measured1 - H * ETA_predicted)  # Update Step
                         P_update = (1 - KG * H) * P_p
                         ETA_tp = ETA_update
                         P_tp = P_update
                         ETA_Measured_Interval_Data_tp = ETA_Measured1
                         ETA_t.append(ETA_update)  # adding result to the existing list for ETA
                         P.append(P_tp)  # adding result to the existing list for covariance P
                         ETA_Measured.append(ETA_Measured1)  # adding result to the existing list for ETA_Measured
                         d_t1.append(dd1)
                         Dis0 = float(d_t1[0])
                         ETA_0 = ETA_t[0]

                    if 500 +ddp <= dd1 < 1000 +ddp:
                         d = math.sqrt((xn[j] - xn[j - start]) ** 2 + (yn[j] - yn[j - start]) ** 2 + (zn[j] - zn[j- start]) ** 2)  # distance between points (nodes). This create segments of the interested roude
                         ETA_Interval_from_d = float(d) / speed  # time interval which the vehicles drives in the specific segment
                         distance.append(d)
                         ETA_Measured_Interval_Data.append(ETA_Interval_from_d)
                         dd1 = d + dd1
                         nn2 = len(ETA_Measured_Interval_Data)
                         ETA_predicted = A * ETA_tp + B * U * d  # Prediction Step
                         P_p = A * P_tp * A + Q  # The state covariance of previous step
                         KG = P_p * H / (P_p + R)  # Klaman gain which tells how much the predictions should be corrected on time step k
                         ETA_Measured1 = ETA_Measured_Interval_Data[j - 1] + ETA_Measured_Interval_Data_tp  # Considering every segment data to have measured time arrival
                         ETA_update = ETA_predicted + KG * (ETA_Measured1 - H * ETA_predicted)  # Update Step
                         P_update = (1 - KG * H) * P_p
                         ETA_tp = ETA_update
                         P_tp = P_update
                         ETA_Measured_Interval_Data_tp = ETA_Measured1
                         ETA_t.append(ETA_update)  # adding result to the existing list for ETA
                         P.append(P_tp)  # adding result to the existing list for covariance P
                         ETA_Measured.append(ETA_Measured1)  # adding result to the existing list for ETA_Measured
                         d_t1.append(dd1)
                         Dis1 = d_t1[nn1]
                         ETA_1 = ETA_t[nn1]

                    if 1000 +ddp <= dd1 < 1500 +ddp:
                         d = math.sqrt((xn[j] - xn[j - start]) ** 2 + (yn[j] - yn[j - start]) ** 2 + (zn[j] - zn[j - start]) ** 2)  # distance between points (nodes). This create segments of the interested roude
                         ETA_Interval_from_d = float(d) / speed  # time interval which the vehicles drives in the specific segment
                         distance.append(d)
                         ETA_Measured_Interval_Data.append(ETA_Interval_from_d)
                         dd1 = d + dd1
                         nn3 = len(ETA_Measured_Interval_Data)
                         ETA_predicted = A * ETA_tp + B * U * d  # Prediction Step
                         P_p = A * P_tp * A + Q  # The state covariance of previous step
                         KG = P_p * H / (P_p + R)  # Klaman gain which tells how much the predictions should be corrected on time step k
                         ETA_Measured1 = ETA_Measured_Interval_Data[j - 1] + ETA_Measured_Interval_Data_tp  # Considering every segment data to have measured time arrival
                         ETA_update = ETA_predicted + KG * (ETA_Measured1 - H * ETA_predicted)  # Update Step
                         P_update = (1 - KG * H) * P_p
                         ETA_tp = ETA_update
                         P_tp = P_update
                         ETA_Measured_Interval_Data_tp = ETA_Measured1
                         ETA_t.append(ETA_update)  # adding result to the existing list for ETA
                         P.append(P_tp)  # adding result to the existing list for covariance P
                         ETA_Measured.append(ETA_Measured1)  # adding result to the existing list for ETA_Measured
                         d_t1.append(dd1)
                         Dis2 = d_t1[nn2]
                         ETA_2 = ETA_t[nn2]

                    if 1500 +ddp <= dd1 < 2000 +ddp:
                         d = math.sqrt((xn[j] - xn[j - start]) ** 2 + (yn[j] - yn[j - start]) ** 2 + (zn[j] - zn[j - start]) ** 2)  # distance between points (nodes). This create segments of the interested roude
                         ETA_Interval_from_d = float(d) / speed  # time interval which the vehicles drives in the specific segment
                         distance.append(d)
                         ETA_Measured_Interval_Data.append(ETA_Interval_from_d)
                         dd1 = d + dd1
                         nn4 = len(ETA_Measured_Interval_Data)
                         ETA_predicted = A * ETA_tp + B * U * d  # Prediction Step
                         P_p = A * P_tp * A + Q  # The state covariance of previous step
                         KG = P_p * H / (P_p + R)  # Klaman gain which tells how much the predictions should be corrected on time step k
                         ETA_Measured1 = ETA_Measured_Interval_Data[j - 1] + ETA_Measured_Interval_Data_tp  # Considering every segment data to have measured time arrival
                         ETA_update = ETA_predicted + KG * (ETA_Measured1 - H * ETA_predicted)  # Update Step
                         P_update = (1 - KG * H) * P_p
                         ETA_tp = ETA_update
                         P_tp = P_update
                         ETA_Measured_Interval_Data_tp = ETA_Measured1

                         ETA_t.append(ETA_update)  # adding result to the existing list for ETA
                         P.append(P_tp)  # adding result to the existing list for covariance P
                         ETA_Measured.append(ETA_Measured1)  # adding result to the existing list for ETA_Measured
                         d_t1.append(dd1)
                         Dis3 = d_t1[nn3]
                         ETA_3 = ETA_t[nn3]
                    elif 2000 +ddp <= dd1 < 2500 +ddp:
                         d = math.sqrt((xn[j] - xn[j - start]) ** 2 + (yn[j] - yn[j - start]) ** 2 + (zn[j] - zn[j - start]) ** 2)  # distance between points (nodes). This create segments of the interested roude
                         ETA_Interval_from_d = float(d) / speed  # time interval which the vehicles drives in the specific segment
                         distance.append(d)
                         ETA_Measured_Interval_Data.append(ETA_Interval_from_d)
                         dd1 = d + dd1
                         nn5 = len(ETA_Measured_Interval_Data)
                         ETA_predicted = A * ETA_tp + B * U * d  # Prediction Step
                         P_p = A * P_tp * A + Q  # The state covariance of previous step
                         KG = P_p * H / (P_p + R)  # Klaman gain which tells how much the predictions should be corrected on time step k
                         ETA_Measured1 = ETA_Measured_Interval_Data[j - 1] + ETA_Measured_Interval_Data_tp  # Considering every segment data to have measured time arrival
                         ETA_update = ETA_predicted + KG * (ETA_Measured1 - H * ETA_predicted)  # Update Step
                         P_update = (1 - KG * H) * P_p
                         ETA_tp = ETA_update
                         P_tp = P_update
                         ETA_Measured_Interval_Data_tp = ETA_Measured1
                         ETA_t.append(ETA_update)  # adding result to the existing list for ETA
                         P.append(P_tp)  # adding result to the existing list for covariance P
                         ETA_Measured.append(ETA_Measured1)  # adding result to the existing list for ETA_Measured
                         d_t1.append(dd1)
                         Dis4 = d_t1[nn4]
                         ETA_4 = ETA_t[nn4]
                    elif dd1 >= 2500 +ddp:
                         d = math.sqrt ((xn[j] - xn[j - start]) ** 2 + (yn[j] - yn[j - start]) ** 2 + (zn[j] - zn[j - start]) ** 2)  # distance between points (nodes). This create segments of the interested roude
                         ETA_Interval_from_d = float(d) / speed  # time interval which the vehicles drives in the specific segment

                         distance.append(d)
                         ETA_Measured_Interval_Data.append(ETA_Interval_from_d)

                         dd1 = d + dd1
                         nn6 = len(ETA_Measured_Interval_Data)
                         ETA_predicted = A * ETA_tp + B * U * d  # Prediction Step
                         P_p = A * P_tp * A + Q  # The state covariance of previous step
                         KG = P_p * H / (P_p + R)  # Klaman gain which tells how much the predictions should be corrected on time step k
                         ETA_Measured1 = ETA_Measured_Interval_Data[j - 1] + ETA_Measured_Interval_Data_tp  # Considering every segment data to have measured time arrival
                         ETA_update = ETA_predicted + KG * (ETA_Measured1 - H * ETA_predicted)  # Update Step
                         P_update = (1 - KG * H) * P_p

                         ETA_tp = ETA_update
                         P_tp = P_update
                         ETA_Measured_Interval_Data_tp = ETA_Measured1

                         ETA_t.append(ETA_update)  # adding result to the existing list for ETA
                         P.append(P_tp)  # adding result to the existing list for covariance P
                         ETA_Measured.append(ETA_Measured1)  # adding result to the existing list for ETA_Measured
                         d_t1.append(dd1)

                         Dis5 = d_t1[nn5]
                         ETA_5 = ETA_t[nn5]
               
               d = np.cumsum(distance)  # ditance from first point to the destination
               aa = (len(distance))
               d1= np.cumsum(distance) 

               etas = [ETA_0, ETA_1, ETA_2, ETA_3, ETA_4, ETA_5]
               areas = [Dis0, Dis1, Dis2, Dis3, Dis4, Dis5]

               result = pairs(areas,etas)
               #print("\n")
               #print("[start of dissemination area, ETA]")
               #for i in range(len(result)):
               #     print(result[i])
               #     print("\n")

               eta_json  = {"data":[{"id": 1,"eta": ETA_0,"dissemination_area": Dis0},{"id":2,"eta":ETA_1,"dissemination_area":Dis1},{"id": 3,"eta": ETA_2,"dissemination_area": Dis2},{"id": 4,"eta": ETA_3,"dissemination_area": Dis3},{"id": 5,"eta": ETA_4,"dissemination_area": Dis4},{"id": 6,"eta": ETA_5,"dissemination_area": Dis5}]}

               #print(ETA_0, ETA_1, ETA_2, ETA_3, ETA_4, ETA_5 )
               #print(Dis0, Dis1, Dis2, Dis3, Dis4, Dis5)

               speed_json  = {"speed": speed}
               location = {"longitude": int(lon_e*1000000), "latitude": int(lat_e*1000000)}
               #r2 = requests.put("http://localhost:5000/api/v1/state/location", json=location)
               #r1 = requests.put("http://localhost:5000/api/v1/state/speed", json=speed_json)
               #r3 = requests.put("http://localhost:5000/api/v1/state/emvid", json=emvID)
               #r4 = requests.put("http://localhost:5000/api/v1/state/destination", json=destination)
               #r5 = requests.put("http://localhost:5000/api/v1/eta", json=eta_json)
               print(location)
               print(speed)
               print(destination)
               print(eta_json)
               #print("Time Consumed") 
               #print("% s milliseconds" % ((time.time() - start)*1000)) 
#               time.sleep(1) #Adjust this to get the best performance


threading.Thread(target=fileWatcher).start()


