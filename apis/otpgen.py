#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  9 15:44:15 2021

@author: kapil
"""


# import random as r
# function for otp generation
# def otpgen():
#     import random as r
#     otp=""
#     otprefid=""
#     for i in range(4):
#         otp+=str(r.randint(1,9))
#         otprefid+= str(r.randint(1,9))
#     print ("Your One Time Password is ")
#     print (otp)
#     print ("Your refId is ")
#     print (otprefid)
#     return otp,otprefid
# generated_otp,generated_refId = otpgen()

def generateOTP_refId():
    import random as r
    generate_otp = r.randint(1000,10000)
    otp_refId = r.randint(100,999)
    return generate_otp,otp_refId