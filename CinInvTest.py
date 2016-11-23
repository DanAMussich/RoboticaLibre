# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 12:01:26 2015

@author: Dan
"""
import math
from CinematicaDirecta import*
from CinematicaInversa import*

L1=8
L2=13
L3=10
L4=10

x=15
y=0
z=25
qpitch=-0
#qpitch=-qpitch
qroll=0


qyaw=math.atan2(y,x);
q5=qroll;
q1=qyaw;
qpitch1=-qpitch*math.pi/180

# Resolucion
Xprima=math.sqrt(x**2+y**2);

Afx=math.cos(-qpitch1)*L4;
LadoB=Xprima-Afx;
Afy=math.sin(-qpitch1)*L4;
LadoA=z-Afy-L1;

Hipot=math.sqrt(LadoA**2+LadoB**2);

Alfa=math.atan2(LadoA,LadoB);
Beta=(math.acos((L2**2-L3**2+Hipot**2)/(2*L2*Hipot)));

q2=Alfa+Beta;           # Angulo Primer Link

Gamma=(math.acos((L2**2+L3**2-Hipot**2)/(2*L2*L3)));  # Aplica teorema del coseno
q3=math.pi-Gamma;    
q3=-q3;                 # Angulo Segundo Link
q4=-(qpitch1+q2+q3);     # Angulo Tercer Link

T_H=cinematicaDir(q1,q2,q3,q4,q5,L1,L2,L3,L4)
