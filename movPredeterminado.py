# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 17:07:50 2015

@author: Dan
"""

from menuOptions import*
import time

def movPredeterminado(mOld,m6,slp,timeStep,ser,L1,L2,L3,L4):
    
    mNew=[-45,120,-45,-45,0]
    
    # Angulos pre-ajuste a servo
    [m1,m2,m3,m4,m5]=preTrayectoria(L1,L2,L3,L4,mOld,mNew,timeStep,slp) 
    
    [m1New,m2New,m3New,m4New,m5New,m1p,m2p,m3p,m4p,m5p]=ajustesVariables(m1,m2,m3,m4,m5)        
    
    t=transmSerie(m1p,m2p,m3p,m4p,m5p,[m6]*int(timeStep/slp),slp,ser)
    
    time.sleep(1)
    
    m1Old=m1New
    m2Old=m2New
    m3Old=m3New
    m4Old=m4New
    m5Old=m5New
    mOld=[m1Old,m2Old,m3Old,m4Old,m5Old]
    
    #Claw change
    
    time.sleep(0.5)
    
    mNew=[0,140,-90,-90,0]
    
    [m1,m2,m3,m4,m5]=preTrayectoria(L1,L2,L3,L4,mOld,mNew,timeStep,slp) 
    
    [m1New,m2New,m3New,m4New,m5New,m1p,m2p,m3p,m4p,m5p]=ajustesVariables(m1,m2,m3,m4,m5)        
    
    t=transmSerie(m1p,m2p,m3p,m4p,m5p,[m6]*int(timeStep/slp),slp,ser)
    
    time.sleep(1)
    
    m1Old=m1New
    m2Old=m2New
    m3Old=m3New
    m4Old=m4New
    m5Old=m5New
    mOld=[m1Old,m2Old,m3Old,m4Old,m5Old]
    
    return[m1Old,m2Old,m3Old,m4Old,m5Old,mOld,m1p,m2p,m3p,m4p,m5p,m1,m2,m3,m4,m5]