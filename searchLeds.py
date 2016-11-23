# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 15:39:35 2015

@author: Dan
"""
import numpy as np
import cv2
from matplotlib import pyplot as plt
import matplotlib.image as mpimg
import time
from datetime import datetime
from scipy import misc

def searchLeds(cap):
    di='/Users/Dan/Documents/Python Scripts/VideosLoop/Procesados/'
    ts=str(datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H-%M-%S'))

    newName=di+'ColorMarked_'+ts+'.avi'    
    
    w=640
    h=480
    my_dpi=100
    video = cv2.VideoWriter(newName,-1, 10,(w,h))
                            
    Cx_r=[]
    Cy_r=[]
    Cx_g=[]
    Cy_g=[]
    Cx_y=[]
    Cy_y=[]
    k=0
    
    while (1):
        ret, frame = cap.read()
        
        #_, frame = cap.read()
        #_, frame = cap.read()
        #_, frame = cap.read()
        if ret==True:
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            
            kernel = np.ones((5,5),np.float32)/25
            kernel=np.ones((3,3))/9
            #kernel=np.array([[1,4,7,4,1],[4,16,26,16,4],[7,26,41,26,7],[4,16,26,16,4],[1,4,7,4,1]])/273
            
            frame1= cv2.filter2D(frame,-1,kernel)
            frame1= cv2.filter2D(frame1,-1,kernel)
            frame1= cv2.filter2D(frame1,-1,kernel)
            
            # Convert BGR to HSV
            hsv = cv2.cvtColor(frame1, cv2.COLOR_BGR2HSV)
            
            #MASCARAS        
            # Los valores se obtienen en base a las ROI de RegionOfInterestValues.py
            
            # Define range of RED color in HSV       
            lower_red = np.array([100,160,160])
            upper_red = np.array([120,255,250])
            # Threshold the HSV image to get only red colors
            mask_r = cv2.inRange(hsv, lower_red, upper_red)
            
            # Define range of MAGENTA color in HSV       
            lower_magenta = np.array([126,70,60])
            upper_magenta = np.array([145,95,140])
            
            # Threshold the HSV image to get only magenta colors
            mask_m = cv2.inRange(hsv, lower_magenta, upper_magenta)
            
            # Define range of bgreen color in HSV
            lower_green = np.array([60,120,120])
            upper_green = np.array([90,230,250]) #v75
            #        
            #        # Threshold the HSV image to get only blue colors
            mask_g = cv2.inRange(hsv, lower_green, upper_green)
                            
            # Define range of yellow color in HSV
            lower_yellow1 = np.array([20,10,240])
            upper_yellow1 = np.array([50,75,250])
            
            #        # Threshold the HSV image to get only blue colors
            #mask_y = cv2.inRange(hsv, lower_yellow, upper_yellow)
            mask_y1 = cv2.inRange(hsv, lower_yellow1, upper_yellow1)
            
            mask_y=mask_y1
            
            # Mascara combinada
            mask=mask_r+mask_g+mask_y+mask_m
            
            
            #Analisis de color Rojo
            kernel = np.ones((5,5),np.uint8)
            erosion_r = cv2.erode(mask_r,kernel,iterations = 1)
            #plt.imshow(erosion)
            dilation_r = cv2.dilate(erosion_r,kernel,iterations = 1)
            
            # Bitwise-AND mask and original image
            res_r = cv2.bitwise_and(frame,frame, mask= dilation_r)
            
            
            contours_r,hierarchy_r = cv2.findContours(mask_r,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
            
            # finding contour with maximum area and store it as best_cnt
            max_area = 0
            for cnt in contours_r:
                area = cv2.contourArea(cnt)
                if area > max_area:
                    max_area = area
                    best_cnt = cnt
            
            # finding centroids of best_cnt and draw a circle there
            M = cv2.moments(best_cnt)  
            cx_r,cy_r = int(M['m10']/M['m00']), int(M['m01']/M['m00'])
            
            Cx_r.append(cx_r)
            Cy_r.append(cy_r)
            
            #Analisis de color Magenta
            kernel = np.ones((5,5),np.uint8)
            erosion_m = cv2.erode(mask_m,kernel,iterations = 1)
            #plt.imshow(erosion)
            dilation_m = cv2.dilate(erosion_m,kernel,iterations = 1)
            
            # Bitwise-AND mask and original image
            res_m = cv2.bitwise_and(frame,frame, mask= dilation_m)
            
            
            contours_m,hierarchy_m = cv2.findContours(mask_m,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
            
            # finding contour with maximum area and store it as best_cnt
            max_area = 0
            for cnt in contours_m:
                area = cv2.contourArea(cnt)
                if area > max_area:
                    max_area = area
                    best_cnt = cnt
            
            # finding centroids of best_cnt and draw a circle there
            M = cv2.moments(best_cnt)  
            cx_m,cy_m = int(M['m10']/M['m00']), int(M['m01']/M['m00'])
            
            
            
            #Analisis de color Verde
            kernel = np.ones((5,5),np.uint8)
            erosion_g = cv2.erode(mask_g,kernel,iterations = 1)
            #plt.imshow(erosion)
            dilation_g = cv2.dilate(erosion_g,kernel,iterations = 1)
            
            # Bitwise-AND mask and original image
            res_g = cv2.bitwise_and(frame,frame, mask= mask_g)
            
            
            contours_g,hierarchy_g = cv2.findContours(mask_g,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
            
            # finding contour with maximum area and store it as best_cnt
            max_area = 0
            for cnt in contours_g:
                area = cv2.contourArea(cnt)
                if area > max_area:
                    max_area = area
                    best_cnt = cnt
            
            # finding centroids of best_cnt and draw a circle there
            M = cv2.moments(best_cnt)  
            cx_g,cy_g = int(M['m10']/M['m00']), int(M['m01']/M['m00'])
            
            Cx_g.append(cx_g)
            Cy_g.append(cy_g)
            
            
            #Analisis de color Amarillo
            kernel = np.ones((5,5),np.uint8)
            erosion_y = cv2.erode(mask_y,kernel,iterations = 1)
            #plt.imshow(erosion)
            dilation_y = cv2.dilate(erosion_y,kernel,iterations = 1)
            
            # Bitwise-AND mask and original image
            res_y = cv2.bitwise_and(frame,frame, mask= mask_y)
            
            
            contours_y,hierarchy_y = cv2.findContours(mask_y,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
            
            # finding contour with maximum area and store it as best_cnt
            max_area = 0
            for cnt in contours_y:
                area = cv2.contourArea(cnt)
                if area > max_area:
                    max_area = area
                    best_cnt = cnt
            
            # finding centroids of best_cnt and draw a circle there
            M = cv2.moments(best_cnt)  
            cx_y,cy_y = int(M['m10']/M['m00']), int(M['m01']/M['m00'])
            
            Cx_y.append(cx_y)
            Cy_y.append(cy_y)
            
            
            
            # Grafico y guardo video
            #plt.scatter(Cx[k],Cy[k],c='r', s=100)
            plt.figure(figsize=(w/my_dpi, h/my_dpi), dpi=my_dpi)
            plt.plot(cx_r, cy_r,color='r', marker='o', linestyle='None',markersize=6)
            #plt.plot(cx_m, cy_m,color='m', marker='o', linestyle='None',markersize=6)
            plt.plot(cx_g, cy_g,color='g', marker='o', linestyle='None',markersize=6)
            plt.plot(cx_y, cy_y,color='c', marker='o', linestyle='None',markersize=6)
            fig=plt.imshow(frame)
            
            fig.axes.get_xaxis().set_visible(False)
            fig.axes.get_yaxis().set_visible(False)
            
            plt.savefig(di+'temp_img.png', bbox_inches='tight', pad_inches = 0,dpi=my_dpi)
            #plt.cla()
        
            img = cv2.imread(di+"temp_img.png")
            video.write(img)
            #time.sleep(0.5)     #para que de tiempo de cerrar la imagen
            plt.cla()
        else:
            break
       
    cap.release()
    video.release()