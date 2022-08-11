#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 13:54:16 2021

@author: kapil
"""

import mysql.connector
import flask
from flask import request,jsonify
import numpy as np
# from datetime import datetime
app = flask.Flask(__name__)

hostname = 'localhost'
username = 'kapil'
password = 'kapil@123'
database_name = "PM_WANI"

err_code = None
err_msg = None
customer_plan = None

def remaining_data_response(err_code,err_msg,customer_plan):
    remaining_plan_response = {'status':{"err_code": err_code,
                          "err_msg": err_msg},
                'body': customer_plan }
    return remaining_plan_response


@app.route('/v1/remainingdata', methods=['POST'])

def InternetAccess():
    mobile_number = request.form.get('mn', type = int)
    print(mobile_number)
    # mobile_number = 9911583381
    if not mobile_number:
        err_code = 1
        err_msg = "Missing mobile number credentials"
        customer_plan = None
    else:
        mydb = mysql.connector.connect(host = hostname,user = username,
                                       passwd = password,database = database_name)
        mycursor = mydb.cursor()
        
        ##get data from tables User_Info
        sql = ("select mobile_number from Customer_Plan_Details")
        mycursor.execute(sql)
        fetch = mycursor.fetchall()
        mob_list = np.array(fetch)
        if str(mobile_number) in mob_list:
        
            fetch_customer_plan_details = ('''select Plan_ID,Plan_Name,
                                  Validity,Data,Amount,Remaining_data
                                  from Customer_Plan_Details
                                  where mobile_number = ''' + str(mobile_number))
            mycursor.execute(fetch_customer_plan_details)
            fetch = mycursor.fetchall()
            customer_plan_list = np.array(fetch)
            num_rows = customer_plan_list.shape[0]
            if num_rows == 0:
                err_code = 1
                err_msg = "Records Not Found"
            else :
                customer_plan = []
                j = 0
                i = 0
                plans = {"planid" : customer_plan_list[i][j],
                            "plan_name" : customer_plan_list[i][j+1],
                            "plan_Validity" : customer_plan_list[i][j+2],
                            "plan_Data" : customer_plan_list[i][j+3],
                            "plan_Price" : customer_plan_list[i][j+4],
                            "Remaining_data":customer_plan_list[i][j+5]}
                customer_plan.append(plans)
                    
                err_msg = "Success"
                err_code = 0
        else:
            err_code = 1
            err_msg = "Data Not Found"
            customer_plan = None
    response = remaining_data_response(err_code,err_msg,customer_plan)
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug = True)
    
# a = None
# if not a:
#     print("Yes")