#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 10 11:02:26 2021

@author: kapil
"""
import mysql.connector
import flask
from flask import request,jsonify
import numpy as np

app = flask.Flask(__name__)

err_code = None
err_msg = None

mobile_num= None
refId = None
OTP = None

hostname = 'localhost'
username = 'kapil'
password = 'kapil@123'
database_name = "PM_WANI"

def check_response(mobile_num,refId,OTP):
    check = {"number": mobile_num,
             "refId": refId,
             "otp" : OTP}
    return check
    
def check_null_values(mobile_num,refId,OTP):
    err_code = None
    err_msg = ""
    if mobile_num == None:
        err_msg = "Missing mobile number field"
        err_code = 1
    elif refId == None:
        err_msg = "Missing refId field"
        err_code = 1
    elif OTP == None:
        err_msg = "Missing OTP field"
        err_code = 1
    else:
        err_code = 0
        err_msg = "Successfull"
    return err_code, err_msg
        
    

def otp_Verify_response(err_code,err_msg):
    otp_response = {'status':{"err_code": err_code,
                          "err_msg": err_msg}}
    return otp_response
    

@app.route('/v1/otpVerification', methods=['POST'])

def otpAuthentication():
    try :
        mobile_num = request.form.get('mn', type = int)
        refId = request.form.get('refId', type = int)
        OTP = request.form.get('otp', type = int)
        print(OTP)
        check = check_response(mobile_num,refId,OTP)
        err_code, err_msg = check_null_values(mobile_num,refId,OTP)
        otp_response = otp_Verify_response(err_code,err_msg)
        if err_code == 0:
            
            mydb = mysql.connector.connect(host = hostname,user = username,
                                       passwd = password,database = database_name)
            mycursor = mydb.cursor()
            sql = ("select mob_no,OTPrefId, GeneratedOTP from User_Info")
            mycursor.execute(sql)
            fetch = mycursor.fetchall()
            mob_list = np.array(fetch)
            
            
            i, j = np.where(mob_list == mobile_num)
            if mob_list[i,j+1] == refId and mob_list[i,j+2] == OTP:
                err_msg = "OTP Verified Successfully"
                err_code = 0
                print(err_code, err_msg)
            else:
                err_msg = "Incorrect OTP "
                err_code = 1
                
            otp_response = otp_Verify_response(err_code,err_msg)
        
            return jsonify(otp_response)
        
        else:
            
            return jsonify(otp_response)
        
    
    except Exception as e:
        return jsonify(e)

if __name__ == '__main__':
    app.run(debug = True)