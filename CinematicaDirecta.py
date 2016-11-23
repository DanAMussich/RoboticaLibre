# -*- coding: utf-8 -*-
"""
Created on Tue Sep 30 14:44:28 2014

@author: Dan
""" 
import numpy
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from pylab import *
import sympy
from sympy import symbols
import math
#%% Prametros Físicos del Robot
def cinematicaDir(q1,q2,q3,q4,q5,L1,L2,L3,L4):
    #L1=7
    #L2=13
    #L3=10
    #L4=3.5

#% Cinematica: Valores Finales

    #q4=0
    #%
    q1=q1*math.pi/180;
    q2=q2*math.pi/180;
    q3=q3*math.pi/180;
    q4=q4*math.pi/180+math.pi/2;
    q5=q5*math.pi/180;
#%  Calculo Matrices Tramas

    T0=numpy.matrix(eye(4))
    T1=numpy.matrix([[math.cos(q1), -math.sin(q1), 0, 0],
                     [math.sin(q1), math.cos(q1), 0, 0],
                     [0, 0, 1, L1],
                     [0, 0, 0, 1]])
    
    T1_0=T0*T1;
    
    T2_pos=numpy.matrix([[1, 0, 0, 0],
                         [0, 0, -1, 0],
                         [0, 1, 0, 0],
                         [0, 0, 0, 1]])
    
    T2=matrix([[math.cos(q2), -math.sin(q2), 0, 0],
        [math.sin(q2), math.cos(q2), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]])
    
    T2_0=T1_0*T2_pos*T2;
    
    T3=matrix([[math.cos(q3), -math.sin(q3), 0, L2],
        [math.sin(q3), math.cos(q3), 0, 0,],
        [0, 0, 1, 0],
        [0, 0, 0, 1]])
    
    T3_0=T2_0*T3;
    
    T4=matrix([[math.cos(q4), -math.sin(q4), 0, L3],
        [math.sin(q4), math.cos(q4), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]])
    
    T4_0=T3_0*T4;
    
    T5_pos=matrix([[1, 0, 0, 0], [0, 0, -1, 0], [0, 1, 0, 0], [0, 0, 0, 1]]);
    T5=matrix([[math.cos(q5), -math.sin(q5), 0, 0],
        [math.sin(q5), math.cos(q5), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]]);
    
    
    T5_0=T4_0*T5_pos*T5;
    
    #TH=matrix([[0, 0, 1, 0], [0, -1, 0, 0], [1, 0, 0, L4], [0, 0, 0, 1]]);
    TH=matrix([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, L4],[ 0, 0, 0, 1]])
    TH_0=T5_0*TH;
    #print 'CI Calculada'
   

    #%% Grafico
    
    PosX=[T0[0,3],T1_0[0,3],T2_0[0,3],T3_0[0,3],T4_0[0,3],T5_0[0,3],TH_0[0,3]]
    PosY=[T0[1,3],T1_0[1,3],T2_0[1,3],T3_0[1,3],T4_0[1,3],T5_0[1,3],TH_0[1,3]]
    PosZ=[T0[2,3],T1_0[2,3],T2_0[2,3],T3_0[2,3],T4_0[2,3],T5_0[2,3],TH_0[2,3]]
#    fig = plt.figure()
    
    #ax = fig.add_subplot(111, projection='3d')
    
#    plot(PosX,PosZ)
    #ax.plot([min(PosX),min(PosY)],[max(PosX),max(PosY)],color='gray')
#    plt.show()
#    print str(T2_0)
#    print str(TH_0)    
    
    return TH_0

