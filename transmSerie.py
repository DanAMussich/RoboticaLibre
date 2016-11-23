# -*- coding: utf-8 -*-
"""
Created on Fri Oct 03 15:23:52 2014

@author: Dan
"""

import time
import numpy as np
import serial
from datetime import datetime
import time
import os
import timeit
import cv2

def transmSerie(m1,m2,m3,m4,m5,m6,slp,ser):
    t=[]

    t.append(timeit.default_timer())
    for i in range(len(m1)):
        string=("ARDU;A%s;B%s;C%s;D%s;E%s;F%s;X" %(int(m1[i]),int(m2[i]),int(m3[i]),int(m4[i]),int(m5[i]),int(m6[i])))
        ser.write(string)
        t.append(timeit.default_timer())
        time.sleep(slp)
     
    return t

#exclusivo para la autocalibracion
def transmSerieA(m1,m2,m3,m4,m5,m6,slp,ser):
    t=[]

    t.append(timeit.default_timer())
    for i in range(len(m1)):
        string=("ARDU;A%s;B%s;C%s;D%s;E%s;F%s;X" %(m1[i],m2[i],m3[i],m4[i],m5[i],m6[i]))
        ser.write(string)
        t.append(timeit.default_timer())
        time.sleep(slp)
     
    return t  
        

def transmSerieVid(m1,m2,m3,m4,m5,m6,slp,ser,dirString,newName):
    dir='/Users/Dan/Documents/Python Scripts/Camera Calibration/'
    #dir=dirString    
    
    mtx=np.load(dir+'matrix1.npy')
    dist=np.load(dir+'dist1.npy')
    newcameramtx=np.load(dir+'newcameramtx1.npy')
    #roi=np.load(dir+'roi1.npy')
    
    #ts=str(datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H-%M-%S'))
    newName=newName+'.avi'
    directory='/Users/Dan/Documents/Python Scripts/Videos/'
    fvid=dirString+newName
    
    #x,y,w,h = roi
    
    camera = cv2.VideoCapture(0)
    video  = cv2.VideoWriter(fvid, 1, 10.0, (640, 480));
    
    
    
    t=[]
    t_extra=[]
    img2=[]
    s=[]
    s_extra=[]
    t.append(timeit.default_timer())
    for i in range(len(m1)):
        string=("ARDU;A%s;B%s;C%s;D%s;E%s;F%s;X" %(int(m1[i]),int(m2[i]),int(m3[i]),int(m4[i]),int(m5[i]),int(m6[i])))
        ser.write(string)
        t.append(timeit.default_timer())
        if i %4==0:
            f,img = camera.read()
            img2.append(img)
            s.append(i/4)
        time.sleep(slp)
    k=0    
    while k<10:
        t_extra.append(timeit.default_timer())
        s_extra.append((i+1)/4+k)
        f,img = camera.read()
        img2.append(img)
        k=k+1
    k=0
    while k<(len(m1)/4+10):
        dst = cv2.undistort(img2[k], mtx, dist, None, newcameramtx)
        #dst = dst[y:y+h, x:x+w]    

        video.write(dst)
        k=k+1
        
    video.release()   
    camera.release()   

    return [t,s,t_extra,s_extra,newName,directory]