# -*- coding: utf-8 -*-
"""
Created on Thu Jul 16 15:52:12 2015

@author: Dan
"""

import cv2
import glob
import numpy as numpy
import math as math
from TestDeteccion import*
from matplotlib import pyplot as plt
from calcAngulos import*
from CinematicaInversa import*
import sympy as sym

variables= glob.glob('/Users/Dan/Documents/Python Scripts/VideosLoopDay/Procesados/Valores/'+'*.npy')
path='/Users/Dan/Documents/Python Scripts/Graficos Calculo Error/'

w=640
h=480

centro_x=301
centro_y=h-379
my_dpi=100


#%%----------------------------------------------------------------------------
""" Método 1: Usando las posiciones detectadas del led Verde y Azul (necesarios para
 detectar la orientación de la pinza) utilizamos el cálculo de Cinemática Inversa
 para ver como un error de 1px en los ejes X e Y afecta a los valores del resto
 de los ángulos. """
    
m1New=[]    
m2New=[]
m3New=[]
m4New=[]
m5New=[]

l2t=[]
l3t=[]
l4t=[]

Cx_c=[]
Cx_g=[]
Cx_r=[]
Cy_c=[]
Cy_g=[]
Cy_r=[]

for m in range(27):
    k=m*12
    #cargo valores de archivo en variables
    Cx_c1=np.load(variables[k])
    Cx_g1=np.load(variables[k+1])
    Cx_r1=np.load(variables[k+2])
    Cy_c1=np.load(variables[k+3])
    Cy_g1=np.load(variables[k+4])
    Cy_r1=np.load(variables[k+5])
    
    l2=np.load(variables[k+6])
    l3=np.load(variables[k+7])
    l4=np.load(variables[k+8])
    m2=np.load(variables[k+9])
    m3=np.load(variables[k+10])
    m4=np.load(variables[k+11])
    
    l2t.extend(l2)
    l3t.extend(l3)
    l4t.extend(l4)    
    
    Cx_c.extend(Cx_c1)
    Cx_g.extend(Cx_g1)
    Cx_r.extend(Cx_r1)
    Cy_c.extend(Cy_c1)
    Cy_g.extend(Cy_g1)
    Cy_r.extend(Cy_r1)
    
    for n in range(20):
        
        cx_c=Cx_c1[n]
        cy_c=Cy_c1[n]

        v3_x=cx_c-Cx_g1[n]    
        v3_y=cy_c-Cy_g1[n]          
        
        qpitch=(math.atan2(v3_y,v3_x))*180/math.pi
        qpitch=qpitch/180.*math.pi
        
        [m1New1,m2New1,m3New1,m4New1,m5New1,status]=cinInv(qpitch,0,Cx_c1[n]-centro_x+1,0,Cy_c1[n]+1,centro_y,l2[n],l3[n],l4[n])
        if status==0:   #si la Cinematica Inversa se pudo calcular sin errores
            m1New.append(m1New1/math.pi*180)
            m2New.append(m2New1/math.pi*180)
            m3New.append(m3New1/math.pi*180)
            m4New.append(m4New1/math.pi*180)
            m5New.append(m5New1/math.pi*180)

    #Graficos
        
#    plt.figure(m)
#    plt.plot(Cx_c,Cy_c,color='b'),plt.plot(Cx_r,Cy_r,color='r'),plt.plot(Cx_g,Cy_g,color='g')
#    plt.savefig(path+'_'+'Spot.png', bbox_inches='tight', pad_inches = 0,dpi=my_dpi)
   
    plt.figure(m*3)
    plt.plot(m2,color='r',marker='o')
    plt.plot(m2New,color='b')
    plt.legend(['Theta Real', 'Theta+Error'], loc='upper center', bbox_to_anchor=(0.5, -0.05),
                    fancybox=True, shadow=True, ncol=5)
    plt.title('Angulo Medido y Angulo con Error Inducido: Theta 2')
    plt.savefig(path+str(m)+'_'+'m2Comp.png', bbox_inches='tight', pad_inches = 0,dpi=my_dpi)
    
    plt.figure(m*3+1)
    plt.plot(m3,color='r',marker='o')
    plt.plot(m3New,color='b')
    plt.legend(['Theta Real', 'Theta+Error'], loc='upper center', bbox_to_anchor=(0.5, -0.05),
                    fancybox=True, shadow=True, ncol=5)
    plt.title('Angulo Medido y Angulo con Error Inducido: Theta 3')
    plt.savefig(path+str(m)+'_'+'m3Comp.png', bbox_inches='tight', pad_inches = 0,dpi=my_dpi)
    
    plt.figure(m*3+2)
    plt.plot(m4,color='r',marker='o')
    plt.plot(m4New,color='b')
    plt.legend(['Theta Real', 'Theta+Error'], loc='upper center', bbox_to_anchor=(0.5, -0.05),
                    fancybox=True, shadow=True, ncol=5)
    plt.title('Angulo Medido y Angulo con Error Inducido: Theta 4')
    plt.savefig(path+str(m)+'_'+'m4Comp.png', bbox_inches='tight', pad_inches = 0,dpi=my_dpi)
    
    plt.cla()
    plt.close()    
    
    m1New=[]    
    m2New=[]
    m3New=[]
    m4New=[]
    m5New=[]

# Promedios
l2a=numpy.mean(l2t)    
l3a=numpy.mean(l3t)
l4a=numpy.mean(l4t)

ratel2=130./l2a
ratel3=100./l3a
ratel4=35./l4a

print ('Taza L2: %s' %(ratel2))
print ('Taza L3: %s' %(ratel3))
print ('Taza L4: %s' %(ratel4))
print ('Promedio Tasas: %s' %np.mean([ratel2,ratel3,ratel4]))

#%% Propagacion del Error- Derivadas Parciales
"""
Método 2: Usando la propagacion de error con derivadas parciales, tomamos las
posiciones detectadas por visión artificial como coordenadas, y la deviación 
estandar en las longitudes de los vínculos calculadas en base a estos datos
como margen de error en las cuentas. Luego graficamos para ver patrones en el 
posible error para cada ángulo. 
"""

#x, y, z, t = sym.symbols('x y z t', real=True)
#x2, y2, z, t = sym.symbols('x2 y2 z t', real=True)

#a=sym.diff(sym.atan2(x,y),x) #.subs(x,3)

# Ejemplo substuticion multiple
#sym.diff(sym.atan2(y2-y,x2-x),x2).subs([(x,5),(y,4),(x2,.3),(y2,.2)])


# Uso para margen de error la desviacion estandar
deltaL2=numpy.std(l2) 
deltaL3=numpy.std(l3) 
deltaL4=numpy.std(l4) 

#deltaL2=max(l2)-min(l2)
#deltaL3=max(l3)-min(l3)
#deltaL4=max(l4)-min(l4)

cy_r,cx_r,cy_g,cx_g,cy_c,cx_c,dy,dx=sym.symbols('cy_r cx_r cy_g cx_g cy_c cx_c dy dx',real=True)

# Defino funciones simbolicas del calculo de angulos
theta2=((sym.atan2(cy_r-centro_y,cx_r-centro_x)))

theta3=((sym.atan2(cy_g-cy_r,cx_g-cx_r)-sym.atan2(cy_r-centro_y,cx_r-centro_x)))

theta4=((sym.atan2(cy_c-cy_g,cx_c-cx_g)-sym.atan2(cy_g-cy_r,cx_g-cx_r)))

d1absT=[]
d1vT=[]
d2absT=[]
d2vT=[]
d3absT=[]
d3vT=[]

for n in range(len(Cx_c)):
    
    d1_1=sym.diff(theta2,cy_r)*dy
    d1_2=sym.diff(theta2,cx_r)*dx
        
    d1_1s=math.fabs((d1_1*dy).subs([(cy_r,Cy_r[n]),(cx_r,Cx_r[n]),(dy,deltaL2)]))
    d1_2s=math.fabs((d1_2*dx).subs([(cy_r,Cy_r[n]),(cx_r,Cx_r[n]),(dx,deltaL2)]))

    d1abs=(d1_1s+d1_2s)*180/math.pi
    d1v=(d1_1s**2+d1_2s**2)*180/math.pi
    
    d1absT.append(d1abs)
    d1vT.append(d1v)
    
#    print "Error Abs 2: %s" %d1abs
#    print "Varianza 2: %s" %d1v
    
    
    d2_1=sym.diff(theta3,cy_r)*dy
    d2_2=sym.diff(theta3,cx_r)*dx
    d2_3=sym.diff(theta3,cy_g)*dy
    d2_4=sym.diff(theta3,cx_g)*dx
        
    d2_1s=math.fabs((d2_1*dy).subs([(cy_r,Cy_r[n]),(cx_r,Cx_r[n]),(cy_g,Cy_g[n]),(cx_g,Cx_g[n]),(dy,deltaL2)]))
    d2_2s=math.fabs((d2_2*dx).subs([(cy_r,Cy_r[n]),(cx_r,Cx_r[n]),(cy_g,Cy_g[n]),(cx_g,Cx_g[n]),(dx,deltaL2)]))
    d2_3s=math.fabs((d2_3*dy).subs([(cy_r,Cy_r[n]),(cx_r,Cx_r[n]),(cy_g,Cy_g[n]),(cx_g,Cx_g[n]),(dy,deltaL3)]))
    d2_4s=math.fabs((d2_4*dx).subs([(cy_r,Cy_r[n]),(cx_r,Cx_r[n]),(cy_g,Cy_g[n]),(cx_g,Cx_g[n]),(dx,deltaL3)]))

    d2abs=(d2_1s+d2_2s+d2_3s+d2_4s)*180/math.pi
    d2v=(d2_1s**2+d2_2s**2+d2_3s**2+d2_4s**2)*180/math.pi

    d2absT.append(d2abs)
    d2vT.append(d2v)    
#    print "Error Abs 3: %s" %d2abs
#    print "Varianza 3: %s" %d2v
    
    
    d3_1=sym.diff(theta4,cy_r)*dy
    d3_2=sym.diff(theta4,cx_r)*dx
    d3_3=sym.diff(theta4,cy_g)*dy
    d3_4=sym.diff(theta4,cx_g)*dx
    d3_5=sym.diff(theta4,cy_c)*dy
    d3_6=sym.diff(theta4,cx_c)*dx
        
    d3_1s=math.fabs((d3_1*dy).subs([(cy_r,Cy_r[n]),(cx_r,Cx_r[n]),(cy_c,Cy_c[n]),(cx_c,Cx_c[n]),(cy_g,Cy_g[n]),(cx_g,Cx_g[n]),(dy,deltaL2)]))
    d3_2s=math.fabs((d3_2*dx).subs([(cy_r,Cy_r[n]),(cx_r,Cx_r[n]),(cy_c,Cy_c[n]),(cx_c,Cx_c[n]),(cy_g,Cy_g[n]),(cx_g,Cx_g[n]),(dx,deltaL2)]))
    d3_3s=math.fabs((d3_3*dy).subs([(cy_r,Cy_r[n]),(cx_r,Cx_r[n]),(cy_c,Cy_c[n]),(cx_c,Cx_c[n]),(cy_g,Cy_g[n]),(cx_g,Cx_g[n]),(dy,deltaL3)]))
    d3_4s=math.fabs((d3_4*dx).subs([(cy_r,Cy_r[n]),(cx_r,Cx_r[n]),(cy_c,Cy_c[n]),(cx_c,Cx_c[n]),(cy_g,Cy_g[n]),(cx_g,Cx_g[n]),(dx,deltaL3)]))
    d3_5s=math.fabs((d3_5*dy).subs([(cy_r,Cy_r[n]),(cx_r,Cx_r[n]),(cy_c,Cy_c[n]),(cx_c,Cx_c[n]),(cy_g,Cy_g[n]),(cx_g,Cx_g[n]),(dy,deltaL4)]))
    d3_6s=math.fabs((d3_6*dx).subs([(cy_r,Cy_r[n]),(cx_r,Cx_r[n]),(cy_c,Cy_c[n]),(cx_c,Cx_c[n]),(cy_g,Cy_g[n]),(cx_g,Cx_g[n]),(dx,deltaL4)]))
    
    d3abs=(d3_1s+d3_2s+d3_3s+d3_4s+d3_5s+d3_6s)*180/math.pi
    d3v=(d3_1s**2+d3_2s**2+d3_3s**2+d3_4s**2+d3_5s**2+d3_6s**2)*180/math.pi

    d3absT.append(d3abs)
    d3vT.append(d3v)    
#    print "Error Abs 4: %s" %d3abs
#    print "Varianza 4: %s \n" %d3v
    
plt.figure(1)
plt.plot(d1absT,color='r'),plt.plot(d1vT,color='b')
plt.legend(['Err. Abs.', 'Varianza'], loc='upper center', bbox_to_anchor=(0.5, -0.05),
                    fancybox=True, shadow=True, ncol=5)
plt.title('Propagacion de Error: Theta 2')
plt.savefig(path+'ErrorTheta2.png', bbox_inches='tight', pad_inches = 0,dpi=my_dpi)

plt.figure(2)
plt.plot(d2absT,color='r'),plt.plot(d2vT,color='b')
plt.legend(['Err. Abs.', 'Varianza'], loc='upper center', bbox_to_anchor=(0.5, -0.05),
                    fancybox=True, shadow=True, ncol=5)
plt.title('Propagacion de Error: Theta 3')
plt.savefig(path+'ErrorTheta3.png', bbox_inches='tight', pad_inches = 0,dpi=my_dpi)

plt.figure(3)
plt.plot(d3absT,color='r'),plt.plot(d3vT,color='b')
plt.legend(['Err. Abs.', 'Varianza'], loc='upper center', bbox_to_anchor=(0.5, -0.05),
                    fancybox=True, shadow=True, ncol=5)
plt.title('Propagacion de Error: Theta 4')
plt.savefig(path+'ErrorTheta4.png', bbox_inches='tight', pad_inches = 0,dpi=my_dpi)
