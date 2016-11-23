# -*- coding: utf-8 -*-
"""
Created on Fri Jun 05 18:17:55 2015

@author: Dan
"""

from menuOptions import*
#from menuOptions import preTrayectoria
#import menuOptions
from transmSerie import*
from fixM import*
import time
import matplotlib.pyplot as plt
import cv2


#%%
def autoCalib(L1,L2,L3,L4,mOld1,slp,ser,step,m6):

    dire='/Users/Dan/Documents/Python Scripts/Camera Calibration/'
    
    mtx=np.load(dire+'matrix1.npy')
    dist=np.load(dire+'dist1.npy')
    newcameramtx=np.load(dire+'newcameramtx1.npy')



    m1=fixM1(0)
    m2=10
    m3=0  
    m4=20
    m5=fixM2(0)
    m6=80    
    
    m2v=[]
    m3v=[]
    m4v=[]    
    
    timeStep=1
    step=2


    newName='0'+'.avi'
    directory='/Users/Dan/Documents/Python Scripts/VideosCalibracion/'
    fvid=directory+newName
        

    
    #Posiciones de calibracion

    m2p=[50,65,80]
    m2p4=[15]
    m3p=[55,40,10]
    m3p4=[100]
    m4p=[100,75,50]
    m4p1=[100]
    i=0
    transmSerie([m1],[m2],[m3p[i]],[m4p[i]],[m5],[m6],slp,ser)
    time.sleep(5)    
    
    camera = cv2.VideoCapture(0)
    video  = cv2.VideoWriter(fvid, 1, 10.0, (640, 480));    
    
    while i<3:   
        # Voy a posición del proximo
        transmSerie([m1],[m2],[m3p[i]],[m4p[i]],[m5],[m6],slp,ser)
        time.sleep(5)

        k=0
        while k<2:    
            while m2<=110:
                m2v.append(m2)
                
                transmSerieA([m1],[m2],[m3p[i]],[m4p[i]],[m5],[m6],slp,ser)
                m2=m2+5
                time.sleep(2)
                f,img = camera.read()   #flush el frame viejo
                f,img = camera.read()   #adquiero frame actual
                
                dst = cv2.undistort(img, mtx, dist, None, newcameramtx)
        
                video.write(dst)
                time.sleep(2)
            mOld1=[m1,m2,m3p[i],m4p[i],m5]    
            m2=10
            k=k+1
            mNew=[m1,m2,m3p[i],m4p[i],m5]
            [m1t,m2t,m3t,m4t,m5t]=preTrayectoria(L1,L2,L3,L4,mOld1,mNew,step,slp)
            transmSerie(m1t,m2t,m3t,m4t,m5t,[m6]*len(m1t),slp,ser)
            time.sleep(5)    
            
        i=i+1
  
    video.release()   
    camera.release()

    #transmSerieA([m1],[m2p[0]],15,[m4p[0]],[m5],[m6],slp,ser)    #para evitar el juego del brazo incialmente

    newName='1'+'.avi'
    fvid=directory+newName
    camera = cv2.VideoCapture(0)
    video  = cv2.VideoWriter(fvid, 1, 10.0, (640, 480));
    i=0
    while i<3:   
        # Voy a posición del proximo    
        transmSerieA([m1],[m2p[i]],[m3],[m4p[i]],[m5],[m6],slp,ser)
        time.sleep(2)
        k=0
        while k<2:
            while m3<=110:
                m3v.append(m3)
                transmSerieA([m1],[m2p[i]],[m3],[m4p[i]],[m5],[m6],slp,ser)
                m3=m3+5
                time.sleep(2)
                f,img = camera.read()   #flush el frame viejo
                f,img = camera.read()   #adquiero frame actual
            
                dst = cv2.undistort(img, mtx, dist, None, newcameramtx)
        
                video.write(dst)
                time.sleep(2)
            mOld1=[m1,m2p[i],m3,m4p[i],m5]
            m3=0
            k=k+1
            mNew=[m1,m2p[i],m3,m4p[i],m5]
            [m1t,m2t,m3t,m4t,m5t]=preTrayectoria(L1,L2,L3,L4,mOld1,mNew,step,slp)
            transmSerie(m1t,m2t,m3t,m4t,m5t,[m6]*len(m1t),slp,ser)
            time.sleep(2)    
            
        i=i+1       
    video.release()   
    camera.release()

    newName='2'+'.avi'
    fvid=directory+newName
    camera = cv2.VideoCapture(0)
    video  = cv2.VideoWriter(fvid, 1, 10.0, (640, 480));
    
    i=0
    #while i<3: 
        # Voy a posición del proximo
    transmSerieA([m1],[m2p4[i]],[m3p4[i]],[m4],[m5],[m6],slp,ser)
    time.sleep(2)
    k=0
    while k<6:    
        while m4<=100:
            m4v.append(m4)
            transmSerieA([m1],[m2p4[i]],[m3p4[i]],[m4],[m5],[m6],slp,ser)
            m4=m4+5
            time.sleep(2)
            f,img = camera.read()   #flush el frame viejo
            f,img = camera.read()   #adquiero frame actual
        
            dst = cv2.undistort(img, mtx, dist, None, newcameramtx)
    
            video.write(dst)
            time.sleep(2)
        mOld1=[m1,m2p4[i],m3p4[i],m4,m5]
        m4=10
        k=k+1
        mNew=[m1,m2p4[i],m3p4[i],m4,m5]
        [m1t,m2t,m3t,m4t,m5t]=preTrayectoria(L1,L2,L3,L4,mOld1,mNew,step,slp)
        transmSerie(m1t,m2t,m3t,m4t,m5t,[m6]*len(m1t),slp,ser)
        time.sleep(2) 
        #i=i+1
        
    video.release()    
    camera.release()

    
    np.save(directory+'m2_motor',m2v)
    np.save(directory+'m3_motor',m3v)
    np.save(directory+'m4_motor',m4v)

    
    return [m2v,m3v,m4v]