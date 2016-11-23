# -*- coding: utf-8 -*-
"""
Created on Mon Jun 08 15:29:40 2015

@author: Dan
"""

import cv2
import glob
import numpy
from searchLeds import*
from TestDeteccion import*
from matplotlib import pyplot as plt
from calcAngulos import*
from matplotlib.pyplot import *


directory='/Users/Dan/Documents/Python Scripts/VideosCalibracion/'
path='/Users/Dan/Documents/Python Scripts/VideosCalibracion/Images/'
videos = glob.glob(directory+'*.avi')
variables= glob.glob(directory+'*.npy')


k=0
m=0
l1t=[]
l2t=[]
l3t=[]

for m in range(len(videos)):
#for m in range(1):
    
    cap = cv2.VideoCapture(videos[m])
    #ret, frame = cap.read()
    [Cx_r,Cy_r,Cx_g,Cy_g,Cx_c,Cy_c]=deteccion(cap,m,path)
    cap.release()
    
    [m2,m3,m4,l1,l2,l3]=calcAngulos(Cx_r,Cy_r,Cx_g,Cy_g,Cx_c,Cy_c)
    
    l1t.extend(l1)
    l2t.extend(l2)
    l3t.extend(l3)
    
    if m==0:
        m2ang=m2
    if m==1:
        m3ang=m3
    if m==2:
        m4ang=m4
    
    
m2v=np.load(variables[0])
m3v=np.load(variables[2])
m4v=np.load(variables[4])
    
    
    
fitm2=numpy.polyfit(m2ang, m2v, 2)
fitm3=numpy.polyfit(m3ang, m3v, 2)
fitm4=numpy.polyfit(m4ang, m4v, 2)

np.save(directory+'m2_valCalib',fitm2)
np.save(directory+'m3_valCalib',fitm3)
np.save(directory+'m4_valCalib',fitm4)




l2=numpy.polyfit(range(len(l1t)),l1t,0)    
l3=numpy.polyfit(range(len(l2t)),l2t,0)
l4=numpy.polyfit(range(len(l3t)),l3t,0)


polynomial = numpy.poly1d(fitm2)
xs1 = range(int(min(m2ang)),int(max(m2ang)))
ys1 = polynomial(xs1)

polynomial = numpy.poly1d(fitm3)
xs2 = range(int(min(m3ang)),int(max(m3ang)))
ys2 = polynomial(xs2)

polynomial = numpy.poly1d(fitm4)
xs3 = range(int(min(m4ang)),int(max(m4ang)))
ys3 = polynomial(xs3)



plt.figure(1)
plt.plot(m2ang,m2v,'o')
plt.plot(xs1,ys1)
plt.xlabel('Angulo')
plt.ylabel('Valor Servo')
plt.legend(['m2 Transm.','m2 Ajustado.'],bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
           ncol=2, mode="expand", borderaxespad=0.) 
plt.savefig(directory+'Graficos de Ajuste/'+'m2_Ajustado.png', bbox_inches='tight', pad_inches = 0)

plt.figure(2)
plt.plot(m3ang,m3v,'o')
plt.plot(xs2,ys2)
plt.xlabel('Angulo')
plt.ylabel('Valor Servo')
plt.legend(['m3 Transm.','m3 Ajustado.'],bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
           ncol=2, mode="expand", borderaxespad=0.) 
plt.savefig(directory+'Graficos de Ajuste/'+'m3_Ajustado.png', bbox_inches='tight', pad_inches = 0)

plt.figure(3)
plt.plot(m4ang,m4v,'o')
plt.plot(xs3,ys3)
plt.xlabel('Angulo')
plt.ylabel('Valor Servo')
plt.legend(['m4 Transm.','m4 Ajustado.'],bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
           ncol=2, mode="expand", borderaxespad=0.) 
plt.savefig(directory+'Graficos de Ajuste/'+'m4_Ajustado.png', bbox_inches='tight', pad_inches = 0)


