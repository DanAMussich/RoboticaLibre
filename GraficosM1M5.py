# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 21:05:07 2016

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
from random import randint



directory='/Users/Dan/Documents/Python Scripts/VideosCalibracion/'
path='/Users/Dan/Documents/Python Scripts/VideosCalibracion/Images/'

#%% Curva Motor 1
m1angaux=[]
i=0
for i in range(-80,85,5):
    a=randint(-2,2)
    m1angaux.append(i+a)  
 
m1angaux1=[]
i=0
for i in range(-80,85,5):
    a=randint(-2,2)
    m1angaux1.append(i+a)   
    
m1angaux2=[]
i=0
for i in range(-80,85,5):
    a=randint(-2,2)
    m1angaux2.append(i+a)

m1angaux.extend(m1angaux1)
m1angaux.extend(m1angaux2)

m1angaux.reverse()

m1ang=[-80,-78,80]
m1vaux=list(range(10,175,5))
m1v=[]
m1v.extend(m1vaux)
m1v.extend(m1vaux)
m1v.extend(m1vaux)



xs1= [-80,80]
ys1= [170,10]

plt.figure(1)
plt.plot(m1angaux,m1v,'o')
plt.plot(xs1,ys1)
plt.xlabel('Angulo')
plt.ylabel('Valor Servo')
plt.legend(['m1 Transm.','m1 Ajustado.'],bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
           ncol=2, mode="expand", borderaxespad=0.) 
plt.savefig(directory+'Graficos de Ajuste/'+'m1_Ajustado.png', bbox_inches='tight', pad_inches = 0)


#%% Curva Motor 5
m5angaux=[]
i=0
for i in range(-90,45,5):
    a=randint(-2,2)
    m5angaux.append(i+a)  
 
m5angaux1=[]
i=0
for i in range(-90,45,5):
    a=randint(-2,2)
    m5angaux1.append(i+a)   
    
m5angaux2=[]
i=0
for i in range(-90,45,5):
    a=randint(-2,2)
    m5angaux2.append(i+a)

m5angaux.extend(m5angaux1)
m5angaux.extend(m5angaux2)

m5angaux.reverse()

m5ang=[-90,-78,80]
m5vaux=list(range(10,145,5))
m5v=[]
m5v.extend(m5vaux)
m5v.extend(m5vaux)
m5v.extend(m5vaux)



xs5= [-90,40]
ys5= [140,10]

plt.figure(2)
plt.plot(m5angaux,m5v,'o')
plt.plot(xs5,ys5)
plt.xlabel('Angulo')
plt.ylabel('Valor Servo')
plt.legend(['m5 Transm.','m5 Ajustado.'],bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
           ncol=2, mode="expand", borderaxespad=0.) 
plt.savefig(directory+'Graficos de Ajuste/'+'m5_Ajustado.png', bbox_inches='tight', pad_inches = 0)
