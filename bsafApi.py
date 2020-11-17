import flask 
from flask import Flask, render_template, redirect, url_for, request, jsonify
import sqlite3
import requests
import json
from multiprocessing import Process
import sys
import subprocess
from subprocess import check_output
#import bsaf_main


app = flask.Flask(__name__)
app.config["DEBUG"] = True

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


@app.route('/', methods=['GET'])
def home():
    conn = sqlite3.connect('domainAdb.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()

    current_state = cur.execute('SELECT * FROM state;').fetchall()
    speed = current_state[0]["speed"]
    location_latitude = current_state[0]["location_latitude"]
    location_longitude = current_state[0]["location_longitude"]
    destination_latitude = current_state[0]["destination_latitude"]
    destination_longitude = current_state[0]["destination_longitude"]

    current_eta = cur.execute('SELECT * FROM eta;').fetchall()
    eta_1 = current_eta[0]["eta"]
    eta_2 = current_eta[1]["eta"]
    eta_3 = current_eta[2]["eta"]
    eta_4 = current_eta[3]["eta"]
    eta_5 = current_eta[4]["eta"]
    eta_6 = current_eta[5]["eta"]

    #latitude1 = current_eta[0]["area_latitude"]
    #latitude2 = current_eta[1]["area_latitude"]
    #latitude3 = current_eta[2]["area_latitude"]
    #latitude4 = current_eta[3]["area_latitude"]
    #latitude5 = current_eta[4]["area_latitude"]
    #latitude6 = current_eta[5]["area_latitude"]

    #longitude1 = current_eta[0]["area_longitude"]
    #longitude2 = current_eta[1]["area_longitude"]
    #longitude3 = current_eta[2]["area_longitude"]
    #longitude4 = current_eta[3]["area_longitude"]
    #longitude5 = current_eta[4]["area_longitude"]
    #longitude6 = current_eta[5]["area_longitude"]


    return render_template('test1.html', speed_input = speed, location_latitude_input = location_latitude, location_longitude_input = location_longitude, destination_latitude_input = destination_latitude, destination_longitude_input = destination_longitude, eta1_input = eta_1, eta2_input = eta_2, eta3_input = eta_3, eta4_input = eta_4, eta5_input = eta_5, eta6_input = eta_6)


@app.route('/map', methods=['GET'])
def map():
    return render_template('map.html')

@app.route('/api/v1/state', methods=['GET'])
def state():
    conn = sqlite3.connect('domainAdb.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    current_state = cur.execute('SELECT * FROM state;').fetchall()

    return jsonify(current_state)

@app.route('/api/v1/eta', methods=['GET'])
def eta_state():
    conn = sqlite3.connect('domainAdb.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    current_state = cur.execute('SELECT * FROM eta;').fetchall()

    return jsonify(current_state)


#gets node, decision on placement
@app.route('/api/v1/state/speed', methods=['GET'])
def speed():

    conn = sqlite3.connect('domainAdb.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()

    current_state = cur.execute('SELECT * FROM state;').fetchall()
    speed = current_state[0]["speed"]
    dataset = {"speed":speed}

    return dataset

@app.route('/api/v1/state/speed', methods=['PUT'])
def update_speed():
    data = request.json
    query = "SELECT * FROM state WHERE"
    speed = data["speed"]

    conn = sqlite3.connect('domainAdb.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()

    sql = "UPDATE state SET speed = ? WHERE emvID = ?"
    val = (speed, 1)

    cur.execute(sql,val)
    conn.commit()

    current_state = cur.execute('SELECT * FROM state;').fetchall()
    #r = requests.put("http://195.37.154.72:31135/api/v1/state/speed", json=data)
    #r = requests.put("http://193.190.127.252:5000/api/v1/state/speed", json=data)

    return jsonify(current_state)


@app.route('/api/v1/state/location', methods=['GET'])
def location():

    conn = sqlite3.connect('domainAdb.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()

    current_state = cur.execute('SELECT * FROM state;').fetchall()
    longitude = current_state[0]["location_longitude"]
    latitude = current_state[0]["location_latitude"]
    dataset = {"longitude": longitude, "latitude": latitude}

    return dataset

@app.route('/api/v1/state/location', methods=['PUT'])
def update_location():
    data = request.json
    query = "SELECT * FROM state WHERE"
    longitude = data["longitude"]
    latitude = data["latitude"]

    conn = sqlite3.connect('domainAdb.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()

    sql = "UPDATE state SET location_longitude = ? WHERE emvID = ?"
    val = (longitude, 1)

    cur.execute(sql,val)
    conn.commit()

    sql = "UPDATE state SET location_latitude = ? WHERE emvID = ?"
    val = (latitude, 1)

    cur.execute(sql,val)
    conn.commit()
    
    current_state = cur.execute('SELECT * FROM state;').fetchall()
    #r = requests.put("http://195.37.154.72:31135/api/v1/state/location", json=data)
    #r = requests.put("http://193.190.127.252:5000/api/v1/state/location", json=data)

    return jsonify(current_state)

@app.route('/api/v1/state/destination', methods=['GET'])
def destination():

    conn = sqlite3.connect('domainAdb.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()

    current_state = cur.execute('SELECT * FROM state;').fetchall()
    longitude = current_state[0]["destination_longitude"]
    latitude = current_state[0]["destination_latitude"]
    dataset = {"longitude": longitude, "latitude": latitude}

    return dataset

@app.route('/api/v1/state/destination', methods=['PUT'])
def update_destination():
    data = request.json
    query = "SELECT * FROM state WHERE"
    longitude = data["longitude"]
    latitude = data["latitude"]

    conn = sqlite3.connect('domainAdb.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()

    sql = "UPDATE state SET destination_longitude = ? WHERE emvID = ?"
    val = (longitude, 1)

    cur.execute(sql,val)
    conn.commit()

    sql = "UPDATE state SET destination_latitude = ? WHERE emvID = ?"
    val = (latitude, 1)

    cur.execute(sql,val)
    conn.commit()
    
    current_state = cur.execute('SELECT * FROM state;').fetchall()

    #r = requests.put("http://195.37.154.72:31135/api/v1/state/destination", json=data)
    #r = requests.put("http://193.190.127.252:500/api/v1/state/destination", json=data)

    return jsonify(current_state)

@app.route('/api/v1/eta', methods=['PUT'])
def update_eta():
    data = request.json
    query = "SELECT * FROM eta WHERE"
    #etas = [data["data"][0]["eta"],eta_json["data"][1]["eta"],eta_json["data"][2]["eta"],eta_json["data"][3]["eta"],eta_json["data"][4]["eta"],eta_json["data"][5]["eta"]]
    #dissemination_areas = [data["data"][0]["dissemination_area"],data["data"][1]["dissemination_area"],data["data"][2]["dissemination_area"],data["data"][3]["dissemination_area"],data["data"][4]["dissemination_area"],data["data"][5]["dissemination_area"]]

    conn = sqlite3.connect('domainAdb.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()

    sql = "UPDATE eta SET eta = ? WHERE id = ?"
    val = (data["data"][0]["eta"], 1)

    cur.execute(sql,val)
    conn.commit()

    sql = "UPDATE eta SET area_latitude = ? WHERE id = ?"
    val = (data["data"][0]["area_latitude"], 1)

    cur.execute(sql,val)
    conn.commit()

    sql = "UPDATE eta SET area_longitude = ? WHERE id = ?"
    val = (data["data"][0]["area_longitude"], 1)

    cur.execute(sql,val)
    conn.commit()

    sql = "UPDATE eta SET eta = ? WHERE id = ?"
    val = (data["data"][1]["eta"], 2)

    cur.execute(sql,val)
    conn.commit()

    sql = "UPDATE eta SET area_latitude = ? WHERE id = ?"
    val = (data["data"][1]["area_latitude"], 2)

    cur.execute(sql,val)
    conn.commit()

    sql = "UPDATE eta SET area_longitude = ? WHERE id = ?"
    val = (data["data"][1]["area_longitude"], 2)

    cur.execute(sql,val)
    conn.commit()

    sql = "UPDATE eta SET eta = ? WHERE id = ?"
    val = (data["data"][2]["eta"], 3)

    cur.execute(sql,val)
    conn.commit()

    sql = "UPDATE eta SET area_latitude = ? WHERE id = ?"
    val = (data["data"][2]["area_latitude"], 3)


    cur.execute(sql,val)
    conn.commit()

    sql = "UPDATE eta SET area_longitude = ? WHERE id = ?"
    val = (data["data"][2]["area_longitude"], 3)


    cur.execute(sql,val)
    conn.commit()

    sql = "UPDATE eta SET eta = ? WHERE id = ?"
    val = (data["data"][3]["eta"], 4)

    cur.execute(sql,val)
    conn.commit()

    sql = "UPDATE eta SET area_latitude = ? WHERE id = ?"
    val = (data["data"][3]["area_latitude"], 4)


    cur.execute(sql,val)
    conn.commit()

    sql = "UPDATE eta SET area_longitude = ? WHERE id = ?"
    val = (data["data"][3]["area_longitude"], 4)


    cur.execute(sql,val)
    conn.commit()

    sql = "UPDATE eta SET eta = ? WHERE id = ?"
    val = (data["data"][4]["eta"], 5)

    cur.execute(sql,val)
    conn.commit()

    sql = "UPDATE eta SET area_latitude = ? WHERE id = ?"
    val = (data["data"][4]["area_latitude"], 5)


    cur.execute(sql,val)
    conn.commit()

    sql = "UPDATE eta SET area_longitude = ? WHERE id = ?"
    val = (data["data"][4]["area_longitude"], 5)


    cur.execute(sql,val)
    conn.commit()

    sql = "UPDATE eta SET eta = ? WHERE id = ?"
    val = (data["data"][5]["eta"], 6)

    cur.execute(sql,val)
    conn.commit()

    sql = "UPDATE eta SET area_latitude = ? WHERE id = ?"
    val = (data["data"][5]["area_latitude"], 6)


    cur.execute(sql,val)
    conn.commit()

    sql = "UPDATE eta SET area_longitude = ? WHERE id = ?"
    val = (data["data"][5]["area_longitude"], 6)


    cur.execute(sql,val)
    conn.commit()
    
    current_state = cur.execute('SELECT * FROM eta;').fetchall()
    #r = requests.put("http://195.37.154.72:31135/api/v1/eta", json=data)
    #r = requests.put("http://193.190.127.252:5000/api/v1/eta", json=data)

    return jsonify(current_state)


app.run(host= '0.0.0.0')








                         
