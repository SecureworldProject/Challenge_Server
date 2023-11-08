import flask
from flask import Flask, jsonify, request, abort
from flask_restx import Api, Resource, fields
from functools import wraps
import sqlite3
import sys
import ipaddress
import pygeoip


def check_if_it_in_network(ip,network):
    #network example: 192.168.0.0/24
    return ipaddress.ip_address(ip) in ipaddress.ip_network(network)
def geolocate(ip):
    gi=pygeoip.GeoIP('data/GeoIP.dat')
    try:
        record=gi.record_by_addr(ip)
        latitude=record['latitude']
        longitude=record['longitude']
        return latitude,longitude
    except:
        return None,None

#Returns key based on:
# - If IP is in network
# - IP latitude and longitude
# - Data
def challenge(ip,data):
    key="-"
    if ip!=None:
        result= check_if_it_in_network(ip,"192.168.0.0/24")
        key=key+str(int(result))+"-"
    #generate key based on latitude and longitude
    latitude,longitude=geolocate(ip)
    if(latitude!=None and longitude!=None):
        key=key+str(int(longitude))+"-"+str(int(latitude))+"-"
    if data!=None:
        #Sum of all digits in data. Data is supposed to be an integer
        result=sum(int(digit) for digit in str(int(data)))
        key=key+str(result)
    return ''.join(str(ord(c)) for c in key)



app = Flask(__name__)

api = Api(app, version='1.0', title='Server')
readings_swagger = api.namespace('Readings', description='API for get/set readings')

expected_arguments=["reading_id","ip","data"] #For showing the JSON in GET methods


class Readings(Resource):
    @api.response(200, 'Success')
    @api.response(400, 'Validation Error')
    def get(self):
        try:
            conn = sqlite3.connect('readings.db')
            cursor = conn.cursor()
            all_readings = cursor.execute('SELECT * FROM readings').fetchall()
            results=[]
            for reading in all_readings:
                d=dict(zip(expected_arguments,list(reading)))
                results.append(d)
            return jsonify(results)
        except:
            return "", 400
        finally:
            if conn:
                conn.close()

    @api.response(200, 'Success')
    @api.response(400, 'Validation Error')
    @api.doc(params={'data': 'Data'})
    @api.doc(params={'ip': 'IP'})
    @api.doc(params={'reading_id': 'Reading ID'})
    def post(self):
        reading_id=request.args.get("reading_id")
        ip=request.args.get("ip")
        data=request.args.get("data")
        print([reading_id,ip,data])
        query="INSERT INTO readings VALUES (?,?,?)"
        try:
            conn = sqlite3.connect('readings.db')
            cursor = conn.cursor()
            cursor.execute(query,[reading_id,str(ip),str(data)])
            conn.commit()
            result=challenge(ip,data)
            return result,200
        except:
            return "", 400
        finally:
            if conn:
                conn.close()

class Reading_id(Resource):

    @api.response(200, 'Success')
    @api.response(400, 'Validation Error')
    @api.doc(params={'reading_id': 'Reading ID'})
    def get(self):
        try:
            conn = sqlite3.connect('readings.db')
            cursor = conn.cursor()
            all_readings= cursor.execute('SELECT * FROM readings WHERE reading_id = :id', {"id": format(request.args['reading_id'])})
            results=[]
            for reading in all_readings:
                d=dict(zip(expected_arguments,list(reading)))
                results.append(d)
            return jsonify(results)
        except:
            return "", 400
        finally:
            if conn:
                conn.close()
    


    @api.response(200, 'Success')
    @api.response(400, 'Validation Error')
    @api.doc(params={'reading_id': 'Reading ID'})
    def delete(self):
        try:
            conn = sqlite3.connect('readings.db')
            cursor = conn.cursor()   
            cursor.execute("DELETE FROM readings WHERE reading_id = :id", {"id": format(request.args['reading_id'])})
            conn.commit()
            return 200
        except:
            return "", 400
        finally:
            if conn:
                conn.close()
        

api.add_resource(Readings, '/readings')
api.add_resource(Reading_id, '/reading/id')

if __name__ == '__main__':
    app.run(debug=True)
