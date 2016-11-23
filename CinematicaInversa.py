# -*- coding: utf-8 -*-
"""
Created on Wed Oct 01 15:02:13 2014

@author: Dan
"""
import math

def cinInv(qpitch,qroll,x,y,z,L1,L2,L3,L4):

    qyaw=math.atan2(y,x);
    q5=qroll;
    q1=qyaw;
    qpitch1=-qpitch
    
    # Resolucion
    Xprima=math.sqrt(x**2+y**2);
    
    Afx=math.cos(-qpitch1)*L4;
    LadoB=Xprima-Afx;
    Afy=math.sin(-qpitch1)*L4;
    LadoA=z-Afy-L1;
    
    Hipot=math.sqrt(LadoA**2+LadoB**2);
    if Hipot<=(L2+L3): 
        Alfa=math.atan2(LadoA,LadoB);
        Beta=(math.acos((L2**2-L3**2+Hipot**2)/(2*L2*Hipot)));
        
        q2=Alfa+Beta;           # Angulo Primer Link
        
        Gamma=(math.acos((L2**2+L3**2-Hipot**2)/(2*L2*L3)));  # Aplica teorema del coseno
        q3=math.pi-Gamma;    
        q3=-q3;                 # Angulo Segundo Link
        q4=-(qpitch1+q2+q3);     # Angulo Tercer Link
        return [q1,q2,q3,q4,q5,0]       # 6to es flag de status

    else:
        print 'Fuera de Area de Trabajo'
        return [0,0,0,0,0,1]
