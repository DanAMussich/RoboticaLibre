# -*- coding: utf-8 -*-
"""
Created on Fri Oct 03 15:29:56 2014

@author: Dan
"""

# Prueba de programa principal

#%% Seteo de variables

inclLibrerias()

#%% Parametros de trabajo

sleepTime=0.025
status=0
poseDefined==0

#%%
if status==0:
    ser=startSerial(9600,10,sleepTime)


if status==1:
    if poseDefined==0:
        cinematicaDir()
        posDefined=1

if status==2:
    if poseDefined==0:
        [q1,q2,q3,q4,q5]=cinInv(qpitch,qroll,x,y,z,L1,L2,L3,L4)
        posDefined=1

if poseDefined==1:
    m1=calcTrayectoria(puntos[1],tiempoEP)
    m2=calcTrayectoria(puntos[2],tiempoEP)
    m3=calcTrayectoria(puntos[3],tiempoEP)
    m4=calcTrayectoria(puntos[4],tiempoEP)
    m5=calcTrayectoria(puntos[5],tiempoEP)
    m6=calcTrayectoria(puntos[6],tiempoEP)
    

if status==3:
    if posedDefined==1:
        transmSerie(m1,m2,m3,m4,m5,m6,slp,ser)
        poseDefined=0
    
if status==4:
    goToZero(lastPos)

if status==5:
    closeSerial()