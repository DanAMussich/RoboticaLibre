# -*- coding: utf-8 -*-
"""
Created on Fri Oct 03 15:27:40 2014

@author: Dan
"""

import serial

def closeSerial(ser):
    ser.close()
    return