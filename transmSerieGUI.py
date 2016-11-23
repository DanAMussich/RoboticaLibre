# -*- coding: utf-8 -*-
"""
Created on Mon Aug 03 13:42:02 2015

@author: Dan
"""

import time
import numpy as np
import serial
from datetime import datetime
import time
import os
import timeit

def transmSerie(m1,m2,m3,m4,m5,m6,slp,ser):
    t=[]

    t.append(timeit.default_timer())
    for i in range(len(m1)):
        string=("ARDU;A%s;B%s;C%s;D%s;E%s;F%s;X" %(int(m1[i]),int(m2[i]),int(m3[i]),int(m4[i]),int(m5[i]),int(m6[i])))
        ser.write(string)
        t.append(timeit.default_timer())
        time.sleep(slp)
    
    return t 
    
    
    
#exclusivo para jacobiano
def transmSerieJ(m1,m2,m3,m4,m5,m6,slp,ser):
    t=[]

    t.append(timeit.default_timer())
    
    
    string=("ARDU;A%s;B%s;C%s;D%s;E%s;F%s;X" %(int(m1),int(m2),int(m3),int(m4),int(m5),int(m6)))
    ser.write(string)
    t.append(timeit.default_timer())
    #time.sleep(slp)
     
    return t      