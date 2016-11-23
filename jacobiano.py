# -*- coding: utf-8 -*-
"""
Created on Tue Feb 03 16:03:20 2015

@author: Dan
"""
import numpy as np
from CinematicaInversa import*
from array import*
from numpy import arange
from math import*

# Calculo de Trayectoria
#L1=7; L2=13; L3=10; L4=7;

def Jacobiano(L1,L2,L3,L4):

    dt=0.025;   #paso de tiempo
    Tper=2;     #tiempo en completar recorrido
    Nt=Tper/dt;
    
    [q1,q2,q3,q4,q5,status]=cinInv(0,0,15,0,24,L1,L2,L3,L4);
    
    Q=np.zeros(shape=(5,int(Nt)))
    
    Q[:,0]=np.matrix([q1,q2,q3,q4+math.pi/2,q5]);
    
    xini=np.matrix([15,0,24,0,0]).T;
    
    x=np.zeros(shape=(5,int(Nt)))
    
    x[:,0]=xini.T;
    amp=5;
    Kp=5;
    
    #x=np.zeros(shape=(5,int(Nt)))
    xd=np.zeros(shape=(5,int(Nt)-1))
    vel=np.zeros(shape=(5,int(Nt)))
    t=np.zeros((int(Nt)-1))
    error=np.zeros(shape=(5,int(Nt)-1))
    
    for n in arange (0,int(Nt)-1):
        
        t[n]=n*dt+dt;
    #####
      
        xd[1,n]=xini[1]+amp*cos((2*math.pi*t[n])/Tper);
        xd[2,n]=xini[2]+amp*sin((2*math.pi*t[n])/Tper);
        
        xd[0,:]=xini[0];
        xd[3,:]=0;
        xd[4,:]=0;
    
    #####    
        error[:,n]=xd[:,n]-x[:,n];
        
        # Actualizacion del Jacobiano
        q1=Q[0,n];q2=Q[1,n];q3=Q[2,n];q4=Q[3,n];q5=Q[4,n];
        
        J0_s=np.matrix(([-sin(q1)*(L3*cos(q2 + q3) + L2*cos(q2) + L4*sin(q2 + q3 + q4)), -cos(q1)*(L3*sin(q2 + q3) + L2*sin(q2) - L4*cos(q2 + q3 + q4)),-cos(q1)*(L3*sin(q2 + q3) - L4*cos(q2 + q3 + q4)),L4*cos(q2 + q3 + q4)*cos(q1), 0],
             [cos(q1)*(L3*cos(q2 + q3) + L2*cos(q2) + L4*sin(q2 + q3 + q4)), -sin(q1)*(L3*sin(q2 + q3) + L2*sin(q2) - L4*cos(q2 + q3 + q4)), -sin(q1)*(L3*sin(q2 + q3) - L4*cos(q2 + q3 + q4)), L4*cos(q2 + q3 + q4)*sin(q1), 0],
              [0,L3*cos(q2 + q3) + L2*cos(q2) + L4*sin(q2 + q3 + q4),L3*cos(q2 + q3) + L4*sin(q2 + q3 + q4),L4*sin(q2 + q3 + q4), 0],
              [0,-1,-1,-1,0], [0,0,0,0,1]));
    #####
        invJ0=J0_s.I;
        
        vel[:,n]=Kp*error[:,n];
        #Q[:,n+1]=Q[:,n]+invJ0*(vel[:,n].T*dt);
        Q[:,n+1]=Q[:,n]+np.dot(invJ0,vel[:,n]*dt)
        
        q1=Q[0,n+1];
        q2=Q[1,n+1];
        q3=Q[2,n+1];
        q4=Q[3,n+1];
        q5=Q[4,n+1];
        
        x[0,n+1] =cos(q1)*(L3*cos(q2 + q3) + L2*cos(q2) + L4*sin(q2 + q3 + q4));
        x[1,n+1] =math.sin(q1)*(L3*math.cos(q2 + q3) + L2*math.cos(q2) + L4*math.sin(q2 + q3 + q4));
        x[2,n+1] =L1 + L3*sin(q2 + q3) + L2*sin(q2) - L4*cos(q2 + q3 + q4);
        x[3,n+1]=0;
        x[4,n+1]=0;
    
    return [Q[0,:],Q[1,:],Q[2,:],(Q[3,:]-math.pi/2),Q[4,:]]