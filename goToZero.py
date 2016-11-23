# -*- coding: utf-8 -*-
"""
Created on Fri Oct 03 15:54:52 2014

@author: Dan
"""

def goToZero(lastPos,cero,slp,ser,tiempoEP):
    cero=[]
    m1=calcTrayectoria([lastPos[1],cero[1]],tiempoEP,slp)
    m2=calcTrayectoria([lastPos[2],cero[2]],tiempoEP,slp)
    m3=calcTrayectoria([lastPos[3],cero[3]],tiempoEP,slp)
    m4=calcTrayectoria([lastPos[4],cero[4]],tiempoEP,slp)
    m5=calcTrayectoria([lastPos[5],cero[5]],tiempoEP,slp)

    transmSerie(m1,m2,m3,m4,m5,m6,slp,ser)
    
    
    return