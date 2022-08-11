#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 15 10:42:33 2021

@author: kapil
"""

import mysql.connector
import flask
from flask import request,jsonify
import numpy as np
import datetime
# from datetime import datetime
app = flask.Flask(__name__)

hostname = 'localhost'
username = 'kapil'
password = 'kapil@123'
database_name = "PM_WANI"

err_code = None
err_msg = None

def access_response(err_code,err_msg):
    access_res = {'status':{"err_code": err_code,
                          "err_msg": err_msg}}
    return access_res

mob = None
mac_address = None
ipv4_address = None
ipv6_address1 = None
storeId = None
ipv6_address2 = None
publicIP = None
Status = None

def check_response(mob,mac_address,ipv4_address,ipv6_address1,ipv6_address2,storeId,publicIP):
    check = {"number": mob,
             "mac_address": mac_address,
             "ipv4_address" : ipv4_address,
             "ipv6_address1" : ipv6_address1,
             "ipv6_address2" : ipv6_address2,
             "storeId" : storeId,
             "PublicIP" : publicIP,
             "status" : Status}
    return check


# mac_address = '3c:a9:f4:53:1a:58'
# ipv4_address = "10.10.16.99"

@app.route('/v1/accessinternet', methods=['POST'])

def InternetAccess():
    mob = request.form.get('mn', type = int)
    mac_address = request.form.get('mac', type = str)
    ipv4_address = request.form.get('ipv4', type = str)
    ipv6_address1 = request.form.get('ipv6_add1', type = str)
    ipv6_address2 = request.form.get('ipv6_add2', type = str)
    storeId = request.form.get('storeId', type = str)
    PublicIP = request.form.get('publicIP', type = str)

    
    if mob is None or not mac_address or not ipv4_address or not ipv6_address1 or not ipv6_address2 or not storeId or not PublicIP:
        err_code = 1
    else:
        err_code = 0
    if mob is None:
        err_msg = "Missing Mobile number credentials"
    elif not mac_address:
        err_msg = "Missing mac_address credentials"
    elif not ipv4_address:
        err_msg = "Missing ipv4_address credentials"
    elif not ipv6_address1:
        err_msg = "Missing ipv6_address1 credentials"
    elif not ipv6_address2:
        err_msg = "Missing ipv6_address2 credentials"
    elif not storeId:
        err_msg = "Missing storeId credentials"
    elif not PublicIP:
        err_msg = "Missing PublicIP credentials"
    else:
        err_msg = "Success"
    if err_code == 0:
        mydb = mysql.connector.connect(host = hostname,user = username,
                                   passwd = password,database = database_name)
        mycursor = mydb.cursor()    
        number_list = ("select mobile_number,Login_Time from Connection_Details")
        mycursor.execute(number_list)
        fetch = mycursor.fetchall()
        mob_list = np.array(fetch)    
        if mob in mob_list[:,0]:
                i, j = np.where(mob_list == mob)
                log_time = mob_list[i,j+1]
                stop_time = datetime.datetime.now().replace(microsecond=0)
                time_diff = (stop_time - log_time[0]).total_seconds()
                if time_diff > 30:
                    update_status = ('''UPDATE Connection_Details SET Status = 'Inactive'
                                     where mobile_number = ''' + str(mob) )
                    mycursor.execute(update_status)
                    mydb.commit()
                status_list = ('''SELECT Status from Connection_Details''')
                mycursor.execute(status_list)
                fetch_msg = mycursor.fetchall()
                status_msg = np.array(fetch_msg)
                active_msg = status_msg[i][0][0]
                if active_msg == "Active":
                    err_msg = "You are already Active"
                elif active_msg == "Inactive":
                    err_msg = "You will be connected in 30 seconds"
                err_code = 1    
        else:
            mydb = mysql.connector.connect(host = hostname,user = username,
                                   passwd = password,database = database_name)
            mycursor = mydb.cursor()
            Status = "Active"
            sql = ('''insert into Connection_Details (mobile_number,mac,ipv4_addr,
                   ipv6_add1,ipv6_add2,store_Id,PublicIP,Status) 
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s)''')
            vals = [mob, mac_address,ipv4_address,ipv6_address1,ipv6_address2,storeId,PublicIP,Status]
            mycursor.execute(sql,vals)
            mydb.commit()
        
        
        
    response = access_response(err_code,err_msg)
    check = check_response(mob,mac_address,ipv4_address,ipv6_address1,ipv6_address2,
                           storeId,PublicIP)
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug = True)



