#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  2 13:28:45 2021

@author: kapil
"""

import mysql.connector
import flask
from flask import request,jsonify
import numpy as np
from username_mobileNo_validation import mob_number_validation
from otpgen import generateOTP_refId
# from datetime import datetime
app = flask.Flask(__name__)
### enter into sql
hostname = 'localhost'
username = 'kapil'
password = 'kapil@123'
database_name = "PM_WANI"
# mydb = mysql.connector.connect(host = hostname,user = username,passwd = password)
# mycursor = mydb.cursor()
# mycursor.execute("CREATE DATABASE " + database_name ) 
# mycursor.execute("show databases")
# # check database
# for i in mycursor:
#     print(i)

results = []

err_code = 404
err_msg = None
otprefId = None
def response(err_code,err_msg,otprefId):
    res = {'status':{"err_code": err_code,
                          "err_msg": err_msg},
                'body': otprefId}
    return res
    
    

@app.route('/v1/userdetails', methods=['GET','POST'])

def userdetails():
    user = request.form.get('user', type = str)
    mob = request.form.get('mn', type = int)
    print(user)
    print(mob)
    numb = None
    try:
        err_code_mob,err_msg_mob,numb = mob_number_validation(mob)
    except:
        err_code_mob,err_msg_mob = mob_number_validation(mob)
        
    err_code = err_code_mob
    err_msg = err_msg_mob
    mob = numb
    refId = None
    resp = response(err_code, err_msg, refId)
    if mob:
        
        mydb = mysql.connector.connect(host = hostname,user = username,
                               passwd = password,database = database_name)
        mycursor = mydb.cursor()
    
        ##get data from tables User_Info
        sql = ("select mob_no from User_Info")
        mycursor.execute(sql)
        fetch = mycursor.fetchall()
        mob_list = np.array(fetch)
        if mob in mob_list:
            print("Existing user")
            err_msg = "Existing user"
            err_code = 1
            
        else:
            otp,refId = generateOTP_refId()
            otprefId = {'otprefid': refId}
            #insert values
            # now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            sql = ("insert into User_Info (name,mob_no,OTPrefId,GeneratedOTP) VALUES(%s, %s, %s, %s)")
            vals = [user, mob,refId,otp]
            mycursor.execute(sql,vals)
            mydb.commit()   
        resp = response(err_code, err_msg, otprefId)
        return jsonify(resp)
    
    else:
        return jsonify(resp)
    
if __name__ == '__main__':
    app.run(debug = True)