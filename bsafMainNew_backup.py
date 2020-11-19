import matplotlib.pyplot as plt
import numpy as np
import pymap3d as pm
import math
import gpxpy.gpx
import openrouteservice as ors
import folium
from geographiclib.geodesic import Geodesic
from openrouteservice.directions import directions
import openrouteservice
from openrouteservice import convert
import requests
#read json
import json
import ijson
import shapely

def bsaf_main(path, id):
     with open(path) as json_file:
         data = json.load(json_file)

     #print("File was modified! Reloading it...")
     lat = []                 # Latitude of interested points ETA 1
     lon = []                 # Longitude of interested points
     distance = []            # distance between two points of interest
     ETA_t = []               # Estimated Time of Arrival
     ETA_Measured = []        # Measured Time of Arrival
     ETA_Measured_Interval_Data = []   # Measured Time of Arrival per Interval  1 and 2
     P = []                   # The error covariance
     #from jsonstreamer import JSONStreamer

     # This part of the code is areas defination

     #Refernce points
     lat_es = 46.9889602
     lon_es = 11.49748240

     Border1 = [46.988888, 11.497493]
     A_ETA1 = [46.9917970, 11.4989080]
     Border2 = [46.994649, 11.500460]
     A_ETA2 = [46.9969320, 11.5030600]
     Border3 = [46.998704, 11.505729]
     A_ETA3 = [47.0022330, 11.5070870]
     Border4 = [47.005285, 11.508329]
     A_ETA4 = [47.0083850, 11.5085370]
     Border5 = [47.011611, 11.507491]
     A_ETA5 = [47.0143620, 11.5077130]
     Border6 = [47.017577, 11.508334]
     A_ETA6 = [47.0198840, 11.5050900]
     Border7 = [47.022423, 11.502110]

     geod = Geodesic.WGS84
     inv = geod.Inverse(A_ETA1[0], A_ETA1[1], Border2[0], Border2[1])
     azi1 = inv["azi1"]
     inv = geod.Inverse(A_ETA2[0], A_ETA2[1], Border3[0], Border3[1])
     azi2 = inv["azi1"]
     inv = geod.Inverse(A_ETA3[0], A_ETA3[1], Border4[0], Border4[1])
     azi3 = inv["azi1"]
     inv = geod.Inverse(A_ETA4[0], A_ETA4[1], Border5[0], Border5[1])
     azi4 = inv["azi1"]
     inv = geod.Inverse(A_ETA5[0], A_ETA5[1], Border6[0], Border6[1])
     azi5 = inv["azi1"]
     inv = geod.Inverse(A_ETA6[0], A_ETA6[1], Border7[0], Border7[1])
     azi6 = inv["azi1"]


     #border defination AU - IT 47.005284, 11.508331

     [x1, y1, z1] = pm.geodetic2ned(Border1[0], Border1[1], 0, lat_es, lon_es, 0)   #WP1
     [x2, y2, z2] = pm.geodetic2ned(Border2[0], Border2[1], 0, lat_es, lon_es, 0)  #WP2
     [x3, y3, z3] = pm.geodetic2ned(Border3[0], Border3[1], 0, lat_es, lon_es, 0)   #WP3
     [x4, y4, z4] = pm.geodetic2ned(Border4[0], Border4[1], 0, lat_es, lon_es, 0)   #WP4
     [x5, y5, z5] = pm.geodetic2ned(Border5[0], Border5[1], 0, lat_es, lon_es, 0)   #WP5
     [x6, y6,  z6] = pm.geodetic2ned(Border6[0], Border6[1], 0, lat_es, lon_es, 0)   #WP5


     a1 =500
     a2 = 500
     a3 = 500
     a4 = 500
     a5 = 500
     b= 0

     #border defination AU - IT 47.005284, 11.508331

     [x1, y1, z1] = pm.geodetic2ned(Border1[0], Border1[1], 0, lat_es, lon_es, 0)   #WP1
     [x2, y2, z2] = pm.geodetic2ned(Border2[0], Border2[1], 0, lat_es, lon_es, 0)  #WP2
     [x3, y3, z3] = pm.geodetic2ned(Border3[0], Border3[1], 0, lat_es, lon_es, 0)   #WP3
     [x4, y4, z4] = pm.geodetic2ned(Border4[0], Border4[1], 0, lat_es, lon_es, 0)   #WP4
     [x5, y5, z5] = pm.geodetic2ned(Border5[0], Border5[1], 0, lat_es, lon_es, 0)   #WP5
     [x6, y6,  z6] = pm.geodetic2ned(Border6[0], Border6[1], 0, lat_es, lon_es, 0)   #WP5

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
     gpx_file = open('map_new.gpx', 'r', encoding="utf-8")  # Data from the E313 highway
     gpx = gpxpy.parse(gpx_file)               # this will read all data points from .gpx file
     for track in gpx.tracks:
          for segment in track.segments:
               for point in segment.points:
                    lat.append(point.latitude)   #this will save all latitude points in an array
                    lon.append(point.longitude)  #this will save all longitude points in an array

     #This part of the code will use latitude and longitude points to convert them in x, y, z, using the refernce points
     [xe, ye, ze] = pm.geodetic2ned(lat_e, lon_e, 0, lat_es, lon_es, 0)   #Position of emergency vehicle in x, y, z
     [xn, yn, zn] = pm.geodetic2ned(lat, lon, 0, lat_es, lon_es, 0)


     #Positions of points (nodes) which the emergency vehicle has to drive to reach the destination

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
     xn1 = []
     yn1 =[]
     d3 = 0
     once = 0
     #In our study,  no additional traffic parameter other than travel time is involved
     #the travel time of the energency vehicle to the first node. This value should be zero or near zero,
     # since the vehicle will start to drive from the nearest node.

     etas = []
     for j in range(1, len(xn)):
         if xn[j-1] >= xe and x1<= xn[j-1] <x2:
                  if xe >= x1 and once ==0:
                     nn0 = 0
                     dd1 = (math.sqrt((xn[j - 1] - xe) ** 2 + (yn[j - 1] - ye) ** 2 + (zn[j - 1] - ze) ** 2))
                     ETA_Measured_Interval_Data_tp = (math.sqrt((xn[j - 1] - xe) ** 2 + (yn[j - 1] - ye) ** 2 + (zn[j - 1] - ze) ** 2)) / speed
                     once = 1
                     #print("enter 1")

                  d = math.sqrt((xn[j] - xn[j - start]) ** 2 + (yn[j] - yn[j - start]) ** 2 + (zn[j] - zn[j - start]) ** 2)
                  ETA_Interval_from_d = float(d) / speed  # time interval which the vehicles drives in the specific segment
                  distance.append(d)
                  ETA_Measured_Interval_Data.append(ETA_Interval_from_d)
                  dd1 = d + dd1
                  nn1 = len(ETA_Measured_Interval_Data)
                  ETA_predicted = A * ETA_tp + B * U * d  # Prediction Step
                  P_p = A * P_tp * A + Q  # The state covariance of previous step
                  KG = P_p * H / (P_p + R)  # Klaman gain which tells how much the predictions should be corrected on time step k
                  ETA_Measured1 = ETA_Interval_from_d + ETA_Measured_Interval_Data_tp  # Considering every segment data to have measured time arrival
                  ETA_update = ETA_predicted + KG * (ETA_Measured1 - H * ETA_predicted)  # Update Step
                  P_update = (1 - KG * H) * P_p
                  ETA_tp = ETA_update
                  P_tp = P_update
                  ETA_Measured_Interval_Data_tp = ETA_Measured1


                  ETA_t.append(ETA_update)  # adding result to the existing list for ETA
                  P.append(P_tp)  # adding result to the existing list for covariance P
                  ETA_Measured.append(ETA_Measured1)  # adding result to the existing list for ETA_Measured
                  d_t1.append(dd1)


                  Dis1 = float(d_t1[nn0])
                  ETA_1 = ETA_t[nn0]
                  #print (A_ETA1, azi1, ETA_1, a1, b)
                  etas.append(ETA_1)

         else:
                 value = 0
                 etas.append(value)



         if xn[j-1] >= xe and x2 <= xn[j-1] < x3:
                  if xe >= x2 and once ==0:
                     nn1 = 0
                     dd1 = (math.sqrt((xn[j - 1] - xe) ** 2 + (yn[j - 1] - ye) ** 2 + (zn[j - 1] - ze) ** 2))
                     ETA_Measured_Interval_Data_tp = (math.sqrt((xn[j - 1] - xe) ** 2 + (yn[j - 1] - ye) ** 2 + (zn[j - 1] - ze) ** 2)) / speed
                     once = 1
                   # print("enter2")


                  d = math.sqrt((xn[j] - xn[j - start]) ** 2 + (yn[j] - yn[j - start]) ** 2 + (zn[j] - zn[j- start]) ** 2)  # distance between points (nodes). This create segments of the interested roude
                  ETA_Interval_from_d = float(d) / speed  # time interval which the vehicles drives in the specific segment
                  distance.append(d)
                  ETA_Measured_Interval_Data.append(ETA_Interval_from_d)
                  dd1 = d + dd1
                  #print("Area 2", dd1)
                  nn2 = len(ETA_Measured_Interval_Data)
                  ETA_predicted = A * ETA_tp + B * U * d  # Prediction Step
                  P_p = A * P_tp * A + Q  # The state covariance of previous step
                  KG = P_p * H / (P_p + R)  # Klaman gain which tells how much the predictions should be corrected on time step k
                  ETA_Measured1 = ETA_Interval_from_d + ETA_Measured_Interval_Data_tp  # Considering every segment data to have measured time arrival
                  ETA_update = ETA_predicted + KG * (ETA_Measured1 - H * ETA_predicted)  # Update Step
                  P_update = (1 - KG * H) * P_p

                  ETA_tp = ETA_update
                  P_tp = P_update
                  ETA_Measured_Interval_Data_tp = ETA_Measured1

                  ETA_t.append(ETA_update)  # adding result to the existing list for ETA
                  P.append(P_tp)  # adding result to the existing list for covariance P
                  ETA_Measured.append(ETA_Measured1)  # adding result to the existing list for ETA_Measured
                  d_t1.append(dd1)


                  Dis2 = d_t1[nn1]
                  ETA_2 = ETA_t[nn1]
                  #print(A_ETA2, azi2, ETA_2, a2, b)
                  etas.append(ETA_2)

         #else:
         #        value = 0
         #        etas.append(value)


         if xn[[j-1]] >= xe and x3 <= xn[[j-1]] < x4:
                  if xe >= x3 and once ==0:
                     nn2 = 0
                     dd1 = (math.sqrt((xn[j - 1] - xe) ** 2 + (yn[j - 1] - ye) ** 2 + (zn[j - 1] - ze) ** 2))
                     ETA_Measured_Interval_Data_tp = (math.sqrt((xn[j - 1] - xe) ** 2 + (yn[j - 1] - ye) ** 2 + (zn[j - 1] - ze) ** 2)) / speed
                     once = 1
                    #print("enter3")


                  d = math.sqrt((xn[j] - xn[j - start]) ** 2 + (yn[j] - yn[j - start]) ** 2 + (zn[j] - zn[j - start]) ** 2)  # distance between points (nodes). This create segments of the interested roude
                  ETA_Interval_from_d = float(d) / speed  # time interval which the vehicles drives in the specific segment
                  distance.append(d)
                  ETA_Measured_Interval_Data.append(ETA_Interval_from_d)

                  dd1 = d + dd1
                  #print("Area 3", dd1)
                  nn3 = len(ETA_Measured_Interval_Data)
                  ETA_predicted = A * ETA_tp + B * U * d  # Prediction Step
                  P_p = A * P_tp * A + Q  # The state covariance of previous step
                  KG = P_p * H / (P_p + R)  # Klaman gain which tells how much the predictions should be corrected on time step k
                  ETA_Measured1 = ETA_Interval_from_d + ETA_Measured_Interval_Data_tp  # Considering every segment data to have measured time arrival
                  ETA_update = ETA_predicted + KG * (ETA_Measured1 - H * ETA_predicted)  # Update Step
                  P_update = (1 - KG * H) * P_p

                  ETA_tp = ETA_update
                  P_tp = P_update
                  ETA_Measured_Interval_Data_tp = ETA_Measured1

                  ETA_t.append(ETA_update)  # adding result to the existing list for ETA
                  P.append(P_tp)  # adding result to the existing list for covariance P
                  ETA_Measured.append(ETA_Measured1)  # adding result to the existing list for ETA_Measured
                  d_t1.append(dd1)

                  Dis3 = d_t1[nn2]
                  ETA_3 = ETA_t[nn2]
                  #print (A_ETA3, azi3, ETA_3, a3, b)
                  etas.append(ETA_3)

         #else:
         #        value = 0
         #        etas.append(value)


         if xn[j-1] >= xe and x4 <= xn[j-1] < x5:
                  if xe >= x4 and once == 0:
                    nn3 = 0
                    dd1 = (math.sqrt((xn[j - 1] - xe) ** 2 + (yn[j - 1] - ye) ** 2 + (zn[j - 1] - ze) ** 2))
                    ETA_Measured_Interval_Data_tp = (math.sqrt((xn[j - 1] - xe) ** 2 + (yn[j - 1] - ye) ** 2 + (zn[j - 1] - ze) ** 2)) / speed
                    once = 1
                    #print("enter 4")

                  d = math.sqrt((xn[j] - xn[j - start]) ** 2 + (yn[j] - yn[j - start]) ** 2 + (zn[j] - zn[j - start]) ** 2)  # distance between points (nodes). This create segments of the interested roude
                  ETA_Interval_from_d = float(d) / speed  # time interval which the vehicles drives in the specific segment

                  distance.append(d)
                  ETA_Measured_Interval_Data.append(ETA_Interval_from_d)

                  dd1 = d + dd1
                  #print("Area 4", dd1)
                  nn4 = len(ETA_Measured_Interval_Data)
                  ETA_predicted = A * ETA_tp + B * U * d  # Prediction Step
                  P_p = A * P_tp * A + Q  # The state covariance of previous step
                  KG = P_p * H / (P_p + R)  # Klaman gain which tells how much the predictions should be corrected on time step k
                  ETA_Measured1 = ETA_Interval_from_d + ETA_Measured_Interval_Data_tp  # Considering every segment data to have measured time arrival
                  ETA_update = ETA_predicted + KG * (ETA_Measured1 - H * ETA_predicted)  # Update Step
                  P_update = (1 - KG * H) * P_p

                  ETA_tp = ETA_update
                  P_tp = P_update
                  ETA_Measured_Interval_Data_tp = ETA_Measured1

                  ETA_t.append(ETA_update)  # adding result to the existing list for ETA
                  P.append(P_tp)  # adding result to the existing list for covariance P
                  ETA_Measured.append(ETA_Measured1)  # adding result to the existing list for ETA_Measured
                  d_t1.append(dd1)

                  Dis4 = d_t1[nn3]
                  ETA_4 = ETA_t[nn3]
                  #print(A_ETA4, azi4, ETA_4, a4, b)
                  etas.append(ETA_4)

         #else:
         #        value = 0
         #        etas.append(value)

         if xn[j-1] >= xe and x5 <= xn[j-1] < x6:
                  if xe >= x5 and once ==0:
                     nn4 = 0
                     dd1 = (math.sqrt((xn[j - 1] - xe) ** 2 + (yn[j - 1] - ye) ** 2 + (zn[j - 1] - ze) ** 2))
                     ETA_Measured_Interval_Data_tp = (math.sqrt((xn[j - 1] - xe) ** 2 + (yn[j - 1] - ye) ** 2 + (zn[j - 1] - ze) ** 2)) / speed
                     once = 1
                     #print("enter 5")

                  d = math.sqrt((xn[j] - xn[j - start]) ** 2 + (yn[j] - yn[j - start]) ** 2 + (zn[j] - zn[j - start]) ** 2)  # distance between points (nodes). This create segments of the interested roude
                  ETA_Interval_from_d = float(d) / speed  # time interval which the vehicles drives in the specific segment
                  distance.append(d)
                  ETA_Measured_Interval_Data.append(ETA_Interval_from_d)
                  dd1 = d + dd1
                  #print("Area 5", dd1)
                  nn5 = len(ETA_Measured_Interval_Data)
                  ETA_predicted = A * ETA_tp + B * U * d  # Prediction Step
                  P_p = A * P_tp * A + Q  # The state covariance of previous step
                  KG = P_p * H / (P_p + R)  # Klaman gain which tells how much the predictions should be corrected on time step k
                  ETA_Measured1 = ETA_Interval_from_d + ETA_Measured_Interval_Data_tp  # Considering every segment data to have measured time arrival
                  ETA_update = ETA_predicted + KG * (ETA_Measured1 - H * ETA_predicted)  # Update Step
                  P_update = (1 - KG * H) * P_p

                  ETA_tp = ETA_update
                  P_tp = P_update
                  ETA_Measured_Interval_Data_tp = ETA_Measured1

                  ETA_t.append(ETA_update)  # adding result to the existing list for ETA
                  P.append(P_tp)  # adding result to the existing list for covariance P
                  ETA_Measured.append(ETA_Measured1)  # adding result to the existing list for ETA_Measured
                  d_t1.append(dd1)

                  Dis5 = d_t1[nn4]
                  ETA_5 = ETA_t[nn4]
                  #print(A_ETA5, azi5, ETA_5, a5, b)
                  etas.append(ETA_5)

         #else:
         #        value = 0
         #        etas.append(value)

         if xn[j-1] >= xe and x6 <= xn[j-1]:
                  if xe >= x6 and once ==0:
                     nn5 = 0
                     dd1 = (math.sqrt((xn[j - 1] - xe) ** 2 + (yn[j - 1] - ye) ** 2 + (zn[j - 1] - ze) ** 2))
                     ETA_Measured_Interval_Data_tp = (math.sqrt((xn[j - 1] - xe) ** 2 + (yn[j - 1] - ye) ** 2 + (zn[j - 1] - ze) ** 2)) / speed
                     once = 1
                     #print("enter 5")

                  d = math.sqrt((xn[j] - xn[j - start]) ** 2 + (yn[j] - yn[j - start]) ** 2 + (zn[j] - zn[j - start]) ** 2)  # distance between points (nodes). This create segments of the interested roude
                  ETA_Interval_from_d = float(d) / speed  # time interval which the vehicles drives in the specific segment
                  distance.append(d)
                  ETA_Measured_Interval_Data.append(ETA_Interval_from_d)
                  dd1 = d + dd1
                  #print("Area 6", dd1)
                  nn6 = len(ETA_Measured_Interval_Data)
                  ETA_predicted = A * ETA_tp + B * U * d  # Prediction Step
                  P_p = A * P_tp * A + Q  # The state covariance of previous step
                  KG = P_p * H / (P_p + R)  # Klaman gain which tells how much the predictions should be corrected on time step k
                  ETA_Measured1 = ETA_Interval_from_d + ETA_Measured_Interval_Data_tp  # Considering every segment data to have measured time arrival
                  ETA_update = ETA_predicted + KG * (ETA_Measured1 - H * ETA_predicted)  # Update Step
                  P_update = (1 - KG * H) * P_p

                  ETA_tp = ETA_update
                  P_tp = P_update
                  ETA_Measured_Interval_Data_tp = ETA_Measured1

                  ETA_t.append(ETA_update)  # adding result to the existing list for ETA
                  P.append(P_tp)  # adding result to the existing list for covariance P
                  ETA_Measured.append(ETA_Measured1)  # adding result to the existing list for ETA_Measured
                  d_t1.append(dd1)

                  Dis6 = d_t1[nn5]
                  ETA_6 = ETA_t[nn5]
                  #print(A_ETA6, azi6, ETA_6, a5, b)
                  etas.append(ETA_6)

     etas = list(filter(lambda num: num != 0, etas))
     etas = list(dict.fromkeys(etas)) #remove duplicates
     if (len(etas)!=6):
       diff = 6-len(etas)
       for i in range(0, diff):
         value = 0
         etas.append(value)
     etas.sort() #sort from lowest to highest
     etas = list(np.around(np.array(etas),2))
     for i in range(0, len(etas)):
       if etas[i]<1 and etas[i]!=0:
         etas[i] = 1
     print(etas)
     #etas = [ETA_0, ETA_1, ETA_2, ETA_3, ETA_4, ETA_5]
     #areas = [Dis0, Dis1, Dis2, Dis3, Dis4, Dis5]

     area1 = [46.9917970, 11.4989080]
     area2 = [46.9969320, 11.5030600]
     area3 = [47.0022330, 11.5070870]
     area4 = [47.0083850, 11.5085370]
     area5 = [47.0143620, 11.5077130]
     area6 = [47.0198840, 11.5050900]

     eta_json  = {"data":[{"emv_id": id, "area_id": 1,"eta": etas[0],"area_latitude": area1[0], "area_longitude": area1[1]},{"emv_id": id, "area_id":2,"eta":etas[1],"area_latitude": area2[0], "area_longitude": area2[1]},{"emv_id": id, "area_id": 3,"eta": etas[2], "area_latitude": area3[0], "area_longitude": area3[1]},{"emv_id": id, "area_id": 4,"eta": etas[3],"area_latitude": area4[0], "area_longitude": area4[1]},{"emv_id": id, "area_id": 5,"eta": etas[4],"area_latitude": area5[0], "area_longitude": area5[1]},{"emv_id": id, "area_id": 6,"eta": etas[5],"area_latitude": area6[0], "area_longitude": area6[1]}]}

     #print(ETA_0, ETA_1, ETA_2, ETA_3, ETA_4, ETA_5 )
     #print(Dis0, Dis1, Dis2, Dis3, Dis4, Dis5)

     speed_json  = {"speed": speed}
     location = {"longitude": lon_e, "latitude": lat_e}
     #r2 = requests.put("http://localhost:5000/api/v1/state/location", json=location)
     #r1 = requests.put("http://localhost:5000/api/v1/state/speed", json=speed_json)
     #r3 = requests.put("http://localhost:5000/api/v1/state/emvid", json=emvID)
     #r4 = requests.put("http://localhost:5000/api/v1/state/destination", json=destination)
     r5 = requests.put("http://localhost:5000/api/v1/eta", json=eta_json)
     #print(location)
     #print(speed)
     #print(destination)
     #print(eta_json)




