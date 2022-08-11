#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  4 15:05:24 2021

@author: kapil
"""

# num = input()    
def number_validation(num):
    if num:
        error = 0
        error_message = "Successfully Registered"
        if len(str(num)) != 10:
            print ({"err": "Invalid Mobile Number"})
            error = 1
            error_message = "Invalid Number"
    else:
        print({"err" : "Enter Mobile Num"})
        error_message = "Enter number"
        error = 2       
    return error,error_message

# err_code,message = number_validation(num)

##User name Validation
# user = input()
def username_validation(user):
    if user:
        error = 0
        error_message = "Successfully Registered"
        print(user)     
    else:
        error = 1
        error_message = "Enter username"

        
    return error,error_message

# err_code,err_msg = username_validation(user)

import re
# def mob_number_validation(num):
#     if num:
#         error = 0
#         error_message = "Successfully Registered"
#         # if re.match(r"^[6789]{1}\d{9}$", num):
#         if (len(str(num)) == 10 and ((str(num)[0]) in ['9','8','7','6'])):
#             print ({"err": "Successfully Registered"})
#             error = 0
#             error_message = "Successfully Registered "
            
#         else:
#             error = 1
#             error_message = "Invalid Mobile Number"
#     else:
#         print({"err" : "Enter Mobile Num"})
#         error_message = "Enter valid number"
#         error = 1       
#     return error,error_message


def Check_Special_characters(string):
    regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
    # Pass the string in search  
    # method of regex object.     
    if(regex.search(string) == None): 
        error = 0
        error_message = "Successfully Registered"
    else:
        error = 1
        error_message = "Special Characters Not Allowed"
    return error, error_message




# num = input()    
def mob_number_validation(num):
    if num:
        error = 0
        error_message = "Successfully Registered"
        # if re.match(r"^[6789]{1}\d{9}$", num):
        if (len(str(num)) == 10 and ((str(num)[0]) in ['9','8','7','6'])):
            print ({"err": "Successfully Registered"})
            error = 0
            error_message = "Successfully Registered "
            
            return error,error_message,num
            
        else:
            error = 1
            error_message = "Invalid Mobile Number"
    else:
        print({"err" : "Missing Mobile Num"})
        error_message = "Missing mobile number credentials"
        error = 1       
    return error,error_message
