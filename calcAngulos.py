# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 17:15:24 2015

@author: Dan
"""

import math

def calcAngulos(Cx_r,Cy_r,Cx_g,Cy_g,Cx_c,Cy_c):

    #w=len(frame)
    w=640
    h=480
    # Defino centro de las coordenadas nuevas    
#    centro_x=Cx_c[0]
#    centro_y=w-Cy_c[0]   #para invertir los valores verticales.
    
    centro_x=301
    centro_y=h-379    
    
    m2=[]
    m3=[]
    m4=[]
    l1=[]
    l2=[]
    l3=[]
    cy_rc=[]
    cy_gc=[]
    cy_cc=[]
    for k in range(len(Cx_r)):
        
        cx_r=Cx_r[k]
        cy_r=h-Cy_r[k]
        
        cx_g=Cx_g[k]
        cy_g=h-Cy_g[k]
        
        cx_c=Cx_c[k]
        cy_c=h-Cy_c[k]    
        
        v1_x=cx_r-centro_x
        v1_y=cy_r-centro_y
        
        v2_x=cx_g-cx_r
        v2_y=cy_g-cy_r
        
        v3_x=cx_c-cx_g    
        v3_y=cy_c-cy_g    
        
        m2.append((math.atan2(v1_y,v1_x))*180/math.pi)
        
        m3.append((math.atan2(v2_y,v2_x)-math.atan2(v1_y,v1_x))*180/math.pi)
        
        m4.append((math.atan2(v3_y,v3_x)-math.atan2(v2_y,v2_x))*180/math.pi)
        
        # Medidas para verificar que no varie la geometria
        
        l1.append(math.sqrt(v1_x**2+v1_y**2))
        l2.append(math.sqrt(v2_x**2+v2_y**2))
        l3.append(math.sqrt(v3_x**2+v3_y**2))
        
        cy_rc.append(cy_r)
        cy_gc.append(cy_g)
        cy_cc.append(cy_c)

    return[m2,m3,m4,l1,l2,l3,cy_rc,cy_gc,cy_cc]