# -*- coding: utf-8 -*-
"""
Created on Wed Oct 15 14:52:29 2014

@author: Dan
"""

# Ajuste simple sin desfasaje todavia. Hay que corren en angulo con
# respecto a la norma seleccionada para los ejes del robot.
import numpy as np
# Parámetros de Ajuste
global fitm2, fitm3, fitm4
directory='/Users/Dan/Documents/Python Scripts/VideosCalibracion/'
a2,b2,c2=np.load(directory+'m2_valCalib.npy')
a3,b3,c3=np.load(directory+'m3_valCalib.npy')
a4,b4,c4=np.load(directory+'m4_valCalib.npy')

def fixM1(pos1):
    fixPos1=pos1+90 # ajustado a norma cartesiana. Revisar angulos intermedios q no sean 0, +/-80
    return fixPos1
    
def fixM2(pos2):
    #fixPos2=pos2-40     # ajustar como curva xq en los extremos la diferencia es menor
	
    #fixPos2=0.002*pos2**2-1.209*pos2+132.893	#using this rn
	#fixPos2=a2*pos2**2+b2*pos2+c2
    #fixPos2=fixPos2.astype(int)
    #fixPos2=int(fixPos2)
	
    fixPos2=a2*pos2**2+b2*pos2+c2
	
    return fixPos2
    
def fixM3(pos3):    
    #fixPos3=0.004*pos3**2-0.802*pos3+-4.463

    fixPos3=a3*pos3**2+b3*pos3+c3
    #fixPos3=fixPos3.astype(int)
    #fixPos3=int(fixPos3)

    # Coeficientes calculados con la función polyfit (Matlab) y datos experimentales.
    return fixPos3

def fixM4(pos4):

    #fixPos4=-0.00107*pos4**2+0.87103*pos4+117.261-10

    fixPos4=a4*pos4**2+b4*pos4+c4-5
	
    #fixPos4=int(fixPos4)
    #fixPos4=fixPos4.astype(int)
    #fixPos4=pos4
    return fixPos4

def fixM5(pos5):
    fixPos5=0.0005*pos5**2+0.9468*pos5+88.0947+10
    #fixPos5=fixPos5.astype(int)
    #fixPos5=int(fixPos5)

    # Coeficientes calculados con la función polyfit (Matlab) y datos experimentales.
    return fixPos5
    
    
def limiteM1(m1):
    if m1<-80 or m1>80:
        print 'Angulo m1 excede limites fisicos. Ingrese otro'
        return 1
    else:
        return 0
        
def limiteM2(m2):
    if m2<40 or m2>140:
        print 'Angulo m2 excede limites fisicos. Ingrese otro'
        return 1
    else:
        return 0
        
def limiteM3(m3):
    if m3>0 or m3<-110:
        print 'Angulo m3 excede limites fisicos. Ingrese otro'
        return 1
    else:
        return 0
        
def limiteM4(m4):
    if m4<-110 or m4>-5:
        print 'Angulo m4 excede limites fisicos. Ingrese otro'
        return 1
    else:
        return 0
        
def limiteM5(m5):
    if m5<-90 or m5>30:
        print 'Angulo m5 excede limites fisicos. Ingrese otro'
        return 1
    else:
        return 0
        