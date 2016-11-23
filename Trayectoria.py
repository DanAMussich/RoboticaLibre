# -*- coding: utf-8 -*-
"""
Created on Wed Oct 01 17:00:49 2014

@author: Dan
"""
from numpy import arange
import math
import matplotlib.pyplot as plt

#global pos

def trayectoria(puntos,tiempoEP):

    pos=0
    pos1=0
    vel1=0
    acel1=0
    posTot=0
    #Defino parametros del ejercicio
    
    theta=puntos;
    
    t=tiempoEP;    #tiempo entre segmentos
    
    #Establezco parametros de tiempo y vectores para almacenar los valores:
    paso=0.025; 
    N=t/paso;                               #puntos por segmento    
    tiempo=arange(1,(len(theta)-1)*N,paso);    #tiempo total
    
    th=t/2;
    for k in range (1,len(theta)-1):
        
        theta_pp=100;
        tb=t/2-math.sqrt(theta_pp**2*t**2-4*theta_pp*abs(theta[k+1]-theta[k]))/(2*theta_pp);
        #tb_1=tb;
        theta_h=(theta[k+1]+theta[k])/2;
        theta_b=theta[k]+1/2*math.sign(theta[k+1]-theta[k])*theta_pp*tb**2;
    
        i=0;
        r=0;
        for i in range (1,math.floor(tb/paso)):
            pos1[i]=theta[k]+1/2*math.sign(theta[k+1]-theta[k])*theta_pp*r**2;
            vel1[i]=theta_pp*r;
            acel1[i]=theta_pp;
            r=r+paso;
        
    
        r=0;
        for i in range (math.floor(tb/paso+1),math.floor(N-tb/paso)):
            r=r+paso;
            pos1[i]=(theta_h-theta_b)/(th-tb)*r+pos1[math.floor(tb/paso)];
            vel1[i]=(theta_h-theta_b)/(th-tb);
            acel1[i]=0;
        
    
        r=tb;
        for i in range (math.floor((N-tb/paso)+1),N):   
            pos1[i]=theta[k+1]-1/2*math.sign(theta[k+1]-theta[k])*theta_pp*(r)**2;  #invertir el orden de r
            vel1[i]=theta_pp*r;     #signo invertido porque el calculo se realiza a la inversa
            acel1[i]=-theta_pp;
            r=r-paso;
        
        pos[k,:]=pos1;              #almaceno cada segmento en filas
    
    
    posTot=pos[0,:];
    
    # Loop para realinear las filas con segmentos en una función continua
    for h in range (1,len(theta)-1):
        l=len(posTot);               #variable auxiliar
        for m in range (1,len[pos]):
            posTot[l+m]=pos[h,m];
        
    
    
    #figure(1)
    plt.plot(tiempo,posTot);
    
    #plot(tiempo,round(posTot),'r');
    #ylim([(min(posTot)-5), (max(posTot)+5)])
    
    return posTot