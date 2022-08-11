#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 17 18:37:55 2021

@author: kapil
"""

import mysql.connector
import flask
from flask import jsonify
import numpy as np
# from datetime import datetime
app = flask.Flask(__name__)

hostname = 'localhost'
username = 'kapil'
password = 'kapil@123'
database_name = "PM_WANI"

err_code = None
err_msg = None
plan_Details = None

def plan_list_response(err_code,err_msg,plan_Details):
    plans_response = {'status':{"err_code": err_code,
                          "err_msg": err_msg},
                'body': plan_Details }
    return plans_response


@app.route('/v1/planslist', methods=['GET'])

def InternetAccess():
    mydb = mysql.connector.connect(host = hostname,user = username,
                                   passwd = password,database = database_name)
    mycursor = mydb.cursor()    
    fetch_plan_details = ("select Plan_ID,Plan_Name,Validity,Data,Amount from Plans_List")
    mycursor.execute(fetch_plan_details)
    fetch = mycursor.fetchall()
    plan_list = np.array(fetch)
    
    if plan_list.size == 0:
        err_code = 1
        err_msg = "Data not available"
    else:
        plan_Details = []
        for i in range(0,len(plan_list)):
            j = 0
            plans = {"planid" : plan_list[i][j],
                    "plan_name" : plan_list[i][j+1],
                    "plan_Validity" : plan_list[i][j+2],
                    "plan_Data" : plan_list[i][j+3],
                    "plan_Price" : plan_list[i][j+4]}
            plan_Details.append(plans)
        
        err_msg = "Success"
        err_code = 0
    response = plan_list_response(err_code,err_msg,plan_Details)
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug = True)