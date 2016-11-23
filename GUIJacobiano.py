# -*- coding: utf-8 -*-
"""
Created on Fri Aug 07 12:33:51 2015

@author: Dan
"""

import numpy as np
from CinematicaInversa import*
from array import*
from numpy import arange
from math import*
from CinematicaDirecta import*

# Calculo de Trayectoria
#L1=7; L2=13; L3=10; L4=7;

def JacobGUI(L1,L2,L3,L4,mOld,Xm,Ym,Zm,vel):
    #dt=0.025;   #paso de tiempo
    #Tper=2;     #tiempo en completar recorrido
    #Nt=Tper/dt;
    #print str(mOld)
    # Adapto los valores de la ultima posicion conicida
    q1=mOld[0]/180.*math.pi
    q2=mOld[1]/180.*math.pi
    q3=mOld[2]/180.*math.pi
    q4=mOld[3]/180.*math.pi
    q5=mOld[4]/180.*math.pi
    
    # Obtengo la posicion espacial
    T=cinematicaDir(q1,q2,q3,q4,q5,L1,L2,L3,L4)
    Tn=T[0:3,3]
    #print str(Tn)
    
    
    
    Q=np.zeros(shape=(5,1))
    
    Q=np.matrix([q1,q2,q3,q4+math.pi/2,q5]);
    
    xini=np.matrix([Tn[0],Tn[1],Tn[2],0,0]).T;
    
    x=np.zeros(shape=(5,1))
    
    x[:,0]=xini.T;
    #amp=5;
    #Kp=5;
    Kp=vel
    
    #x=np.zeros(shape=(5,int(Nt)))
    xd=np.zeros(shape=(5,1))
    vel=np.zeros(shape=(5,1))
    #t=np.zeros((int(Nt)-1))
    error=np.zeros(shape=(5,1))
    
    
        
    #t[n]=n*dt+dt;
    #####
      
    xd[1]=xini[1]+Ym;
    xd[2]=xini[2]+Zm;
    xd[0]=xini[0]+Xm;
    
    xd[3]=0;
    xd[4]=0;
    
    #####    
    error=xd-x;
    #print str(Q)
    # Actualizacion del Jacobiano
    q1=Q[0,0];
    q2=Q[0,1];
    q3=Q[0,2];
    q4=Q[0,3];
    q5=Q[0,4];
    
    J0_s=np.matrix(([-sin(q1)*(L3*cos(q2 + q3) + L2*cos(q2) + L4*sin(q2 + q3 + q4)), -cos(q1)*(L3*sin(q2 + q3) + L2*sin(q2) - L4*cos(q2 + q3 + q4)),-cos(q1)*(L3*sin(q2 + q3) - L4*cos(q2 + q3 + q4)),L4*cos(q2 + q3 + q4)*cos(q1), 0],
         [cos(q1)*(L3*cos(q2 + q3) + L2*cos(q2) + L4*sin(q2 + q3 + q4)), -sin(q1)*(L3*sin(q2 + q3) + L2*sin(q2) - L4*cos(q2 + q3 + q4)), -sin(q1)*(L3*sin(q2 + q3) - L4*cos(q2 + q3 + q4)), L4*cos(q2 + q3 + q4)*sin(q1), 0],
          [0,L3*cos(q2 + q3) + L2*cos(q2) + L4*sin(q2 + q3 + q4),L3*cos(q2 + q3) + L4*sin(q2 + q3 + q4),L4*sin(q2 + q3 + q4), 0],
          [0,-1,-1,-1,0], [0,0,0,0,1]));
    #####
    invJ0=J0_s.I;
    #%%
    vel=Kp*error;
    Q=Q+np.dot(invJ0,vel).T
    #%%
    q1=Q[0,0];
    q2=Q[0,1];
    q3=Q[0,2];
    q4=Q[0,3];
    q5=Q[0,4];
    
    x[0] =cos(q1)*(L3*cos(q2 + q3) + L2*cos(q2) + L4*sin(q2 + q3 + q4));
    x[1] =math.sin(q1)*(L3*math.cos(q2 + q3) + L2*math.cos(q2) + L4*math.sin(q2 + q3 + q4));
    x[2] =L1 + L3*sin(q2 + q3) + L2*sin(q2) - L4*cos(q2 + q3 + q4);
    x[3]=0;
    x[4]=0;
#    print (str(x[0])+' '+str(x[1])+' '+str(x[2]))
    #Qout=np.zeros(shape=(5,1))
#    Qout[0]=Q[0,0]*180/pi
#    Qout[1]=Q[0,1]*180/pi
#    Qout[2]=Q[0,2]*180/pi
#    Qout[3]=(Q[0,3]-math.pi/2)*180/pi
#    Qout[4]=Q[0,4]*180/pi

    m1=Q[0,0]*180/pi
    m2=Q[0,1]*180/pi
    m3=Q[0,2]*180/pi
    m4=(Q[0,3]-math.pi/2)*180/pi
    m5=Q[0,4]*180/pi    
    #print str(Qout)
    return [m1,m2,m3,m4,m5]