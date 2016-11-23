# -*- coding: utf-8 -*-
"""
Created on Wed Oct 01 17:49:06 2014

@author: Dan
"""
import math
import numpy
from numpy import arange
from array import*
#import matplotlib.pyplot as plt
import pylab
from pylab import plot

#tiempoEP=1
#puntos=[80,120]
#step=0.025

    #Defino parametros del ejercicio
def calcTrayectoria(puntos,tiempoEP,step):    
    
    theta=puntos;
        
    t=tiempoEP;    #tiempo entre segmentos
        
    #Establezco parametros de tiempo y vectores para almacenar los valores:
    paso=step; 
    N=t/paso;                
    th=t/2.               #puntos por segmento    
    #tiempo=arange(0,(len(theta)-1)*N,paso);    #tiempo total
    tiempo=arange(0,t*(len(theta)-1),paso);     #tiempo total
    
    #defino vectores necesarios
    length=int((len(theta)-1)*N)    #largo total
    lengthS=int(length/(len(theta)-1))
    posT=numpy.array(range(length))
    #pos1=numpy.array(range(lengthS))
    pos1=[0]*int(N)
    vel1=numpy.array(range(lengthS))
    acel1=numpy.array(range(lengthS))
    posTot=numpy.array(range(length))
        
    # Primer for permite el calculo de trayectorias entre más de un punto    
    for k in arange (0,len(theta)-1):
        #k=0        
        theta_pp=6.*abs(theta[k+1]-theta[k])/t**2
        tb=t/2.-math.sqrt(theta_pp**2*t**2-4*theta_pp*abs(theta[k+1]-theta[k]))/(2*theta_pp);

        theta_h=(theta[k+1]+theta[k])/2.;
        theta_b=theta[k]+1./2*math.copysign(1,theta[k+1]-theta[k])*theta_pp*tb**2;
        
        i=0;
        r=0;
        length1=int(math.floor(tb/paso))
        
        for i in arange (0,length1):
            pos1[i]=(theta[k]+1./2*math.copysign(1,theta[k+1]-theta[k])*theta_pp*r**2);
            vel1[i]=(theta_pp*r);
            acel1[i]=theta_pp;
            r=r+paso;
            
        r=0;
        length2=int(math.floor(tb/paso+1))-1    #-1 porque los for no llegan al ultimo valor
        length3=int(math.floor(N-tb/paso))
        
        for i in arange (length2,length3):
            r=r+paso;
            pos1[i]=(theta_h-theta_b)/(th-tb)*r+pos1[int(math.floor(tb/paso)-1)];
            vel1[i]=(theta_h-theta_b)/(th-tb);
            acel1[i]=0;
            
        length4=int(math.floor((N-tb/paso)+1)-1)
        r=tb;
        for i in arange (length4,int(N)):   
            pos1[i]=theta[k+1]-1./2*math.copysign(1,theta[k+1]-theta[k])*theta_pp*r**2;  #invertir el orden de r
            vel1[i]=theta_pp*r;     #signo invertido porque el calculo se realiza a la inversa
            acel1[i]=-theta_pp;
            r=r-paso;
        
        if k==0:
            n=k*len(pos1)
        if k>0:
            n=k*len(pos1)
        l=0
        last=(k+1)*len(pos1)
        
        for m in range(n,last):
            posT[m]=pos1[l];
            l=l+1
    
    #posTot=pos[0,:]
    #posTRound=numpy.round(posT)
    posTRound=(posT)
    #plt.plot(tiempo,posTRound)
    
#plot(tiempo,posTRound)
#pylab.xlabel('Tiempo')
#pylab.ylabel('Angulo')
#pylab.show() 

    #pylab.ylabel('Ángulo')
    #pylab.title('My First Plot')

    return posTRound
