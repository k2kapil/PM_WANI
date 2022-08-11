#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 12 12:55:02 2021

@author: kapil
"""

import flask
from flask import request,jsonify
import numpy as np
import mysql.connector


app = flask.Flask(__name__)

hostname = 'localhost'
username = 'kapil'
password = 'kapil@123'
database_name = "PM_WANI"

mob  = None
err_code = None
err_msg = None
bbnl_avail_networks = None

def response(err_code,err_msg,bbnl_avail_networks):
    res = {'status':{"err_code": err_code,
                          "err_msg": err_msg},
                'body': bbnl_avail_networks}
    return res

@app.route('/v1/getValidAccessPoints', methods=['POST'])

def userdetails():
    Av_wifi = (request.form.getlist('aw'))
    # Av_wifi = (request.form.get('aw'))

    # Av_wifi = [
    #     "[bbnl,fofi,Augur]"
    # ]
    mob = request.form.get('mn', type = int)
    print(Av_wifi)
    print(mob)
    # check = {"av":Av_wifi}
    # return jsonify(check)
    Av_wifi1 = Av_wifi[0].replace('[','',1)
    Av_wifi_list = Av_wifi1.replace(']','')
    Av_wifi = Av_wifi_list.split(',')
    # eval(Av_wifi[0])
    print(Av_wifi)
    mydb = mysql.connector.connect(host = hostname,user = username,
                           passwd = password,database = database_name)
    mycursor = mydb.cursor()

    ##get data from tables User_Info
    sql = ("select Service_Providers from BBNL_Services")
    mycursor.execute(sql)
    fetch = mycursor.fetchall()
    bbnl_network = np.array(fetch)
    bbnl_avail_networks = []
    for i in range(0,len(Av_wifi)):
        if Av_wifi[i] in bbnl_network:
            bbnl_avail_networks.append(Av_wifi[i])
            err_code = 0
            err_msg = "Success"
        else:
            err_code = 1
            err_msg = "Not Available"
            
    if len(bbnl_avail_networks) == 0:
        bbnl_avail_networks = None
    avail_wifi_resp = response(err_code,err_msg,bbnl_avail_networks)
    return jsonify(avail_wifi_resp)

if __name__ == '__main__':
    app.run(debug = True)