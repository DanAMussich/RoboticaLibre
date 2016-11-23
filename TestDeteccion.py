# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 15:27:55 2015

@author: Dan
"""

import numpy as np
import cv2
from matplotlib import pyplot as plt
import matplotlib.image as mpimg
import time
from datetime import datetime
from scipy import misc



def deteccion(cap,m,path):
    #ts=str(datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H-%M-%S'))

    #video  = cv2.VideoWriter(di+'TestColorMarked'+ts+'.avi', -1, 10.0, (640, 480))
    dire='/Users/Dan/Documents/Python Scripts/Camera Calibration/'
    roi=np.load(dire+'roi1.npy')


    x,y,w,h = roi
    
    my_dpi=100
    
    Cx_r=[]
    Cy_r=[]
    Cx_g=[]
    Cy_g=[]
    Cx_c=[]
    Cy_c=[]
    k=0
    n=0
    while (1):
        ret, frame = cap.read()
        if ret==True:
            frame = frame[y:y+h, x:x+w]

            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            
            kernel = np.ones((5,5),np.float32)/25
            kernel=np.ones((3,3))/9
            #kernel=np.array([[1,4,7,4,1],[4,16,26,16,4],[7,26,41,26,7],[4,16,26,16,4],[1,4,7,4,1]])/273
            
            frame1= cv2.filter2D(frame,-1,kernel)
            frame1= cv2.filter2D(frame1,-1,kernel)
            frame1= cv2.filter2D(frame1,-1,kernel)
            
            #Create Region Masks
            if n==0:
                imgr=frame1
                imgg=frame1
                imgc=frame1
                n=n+1
            else:
                imgr=regionMask(h,w,cxr,cyr,frame1)   
                imgg=regionMask(h,w,cxg,cyg,frame1)
                imgc=regionMask(h,w,cxc,cyc,frame1)          
            
            # Convert BGR to HSV
            hsv = cv2.cvtColor(frame1, cv2.COLOR_BGR2HSV)
            
            #MASCARAS        
            # Los valores se obtienen en base a las ROI de RegionOfInterestValues.py
            
            # Define range of RED color in HSV       
            lower_red = np.array([90,120,120])
            upper_red = np.array([120,255,255])
            # Threshold the HSV image to get only red colors
            mask_r = cv2.inRange(hsv, lower_red, upper_red)
            
            # Define range of bgreen color in HSV
            lower_green = np.array([70,120,120])
            upper_green = np.array([85,255,255]) #v75
            #        
            #        # Threshold the HSV image to get only blue colors
            mask_g = cv2.inRange(hsv, lower_green, upper_green)
                            
            # Define range of cyan color in HSV
            lower_cyan = np.array([10,10,130])
            upper_cyan = np.array([40,230,250])
            
            #        # Threshold the HSV image to get only blue colors
            #mask_y = cv2.inRange(hsv, lower_yellow, upper_yellow)
            mask_c = cv2.inRange(hsv, lower_cyan, upper_cyan)
                                    
            
            #Analisis de color Rojo            
            cx_r,cy_r=detec(mask_r)
            Cx_r.append(cx_r)
            Cy_r.append(cy_r)
            cxr=cx_r
            cyr=cy_r

            
        
            #Analisis de color Verde
            cx_g,cy_g=detec(mask_g)
            
            Cx_g.append(cx_g)
            Cy_g.append(cy_g)
            cxg=cx_g
            cyg=cy_g
                       
            #Analisis de color Amarillo                       
            cx_c,cy_c=detec(mask_c)
            
            Cx_c.append(cx_c)
            Cy_c.append(cy_c)
            cxc=cx_c
            cyc=cy_c
            
            
            
            
            # Grafico y guardo video
            #plt.scatter(Cx[k],Cy[k],c='r', s=100)
            plt.figure(figsize=(w/my_dpi, h/my_dpi), dpi=my_dpi)
            plt.plot(cx_r, cy_r,color='r', marker='o', linestyle='None',markersize=6)
            plt.plot(cx_g, cy_g,color='g', marker='o', linestyle='None',markersize=6)
            plt.plot(cx_c, cy_c,color='c', marker='o', linestyle='None',markersize=6)
            fig=plt.imshow(frame)
            plt.imshow(frame)
            fig.axes.get_xaxis().set_visible(False)
            fig.axes.get_yaxis().set_visible(False)
            
            plt.savefig(path+str(m)+'_'+str(k)+'_'+'_marked.png', bbox_inches='tight', pad_inches = 0,dpi=my_dpi)
            plt.cla()
            plt.close()

            k=k+1
        else:
            break
    #video.release()
    return[Cx_r,Cy_r,Cx_g,Cy_g,Cx_c,Cy_c]

#cap.release()

def detec(mask):
    contours_y,hierarchy_y = cv2.findContours(mask,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    
    # finding contour with maximum area and store it as best_cnt
    max_area = 0
    for cnt in contours_y:
        area = cv2.contourArea(cnt)
        if area > max_area:
            max_area = area
            best_cnt = cnt
            flag=1

        # finding centroids of best_cnt and draw a circle there
    M = cv2.moments(best_cnt)  
    cx,cy = int(M['m10']/M['m00']), int(M['m01']/M['m00'])

    
    return[cx,cy]

    
def regionMask(h,w,cx,cy,frame):
    p_r=np.zeros([h,w],dtype=np.uint8)

    for i in range(h):
        for j in range(w):
            #Circulo: 281**2+395**2=5**2
            if ((j-cx)**2+(i-cy)**2)<=20**2:
                p_r[i,j]=255
                
    img = cv2.bitwise_and(frame,frame,mask = p_r) 
    
    return img