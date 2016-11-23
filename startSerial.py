# -*- coding: utf-8 -*-
"""
Created on Fri Oct 03 15:21:48 2014

@author: Dan
"""

#9600 baud, puerto 10, sleep 2

import time
import serial

def startSerial(baud,port,slp):

    ser = serial.Serial()
    ser.baudrate = baud
    ser.port = port
    ser.open()
    ser.isOpen()
    time.sleep(slp)
    
    return ser