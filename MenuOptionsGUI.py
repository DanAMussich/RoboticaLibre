# -*- coding: utf-8 -*-
"""
Created on Mon Aug 03 13:40:33 2015

@author: Dan
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Oct 23 11:23:30 2014

@author: Dan
"""

#%% Librerias Propias
from CinematicaInversa import*
from CinematicaDirecta import*
from calcTrayectoria import*
from transmSerieGUI import*
from jacobiano import*
from fixM import*
from GUIJacobiano import*
import time

#from TestLoopPosiciones import*
#from movPredeterminado import*
#%% Librerias de Python
import math

import matplotlib.animation as animation
import mpl_toolkits.mplot3d.axes3d as p3

#%% Funciones

#%% Funciones de Posición        

def limites(m1,m2,m3,m4,m5):

    c1=limiteM1(m1)
    c2=limiteM2(m2)
    c3=limiteM3(m3)
    c4=limiteM4(m4)
    c5=limiteM5(m5)
    
    return [c1,c2,c3,c4,c5]
    
    
def preTrayectoria(L1,L2,L3,L4,mOld,mNew,timeStep,slp):
    
    # Verifico que los puntos angulares nuevos no coincidan con los anteriores
    # En caso de coincidencia, genero una lista conteniendo la posición fija,
    # indicando que ese motor no se moverá
    m=[0]*5
    length=int(timeStep/slp)
    
    for k in range(0,5):
        if mOld[k]!=mNew[k]:
            # si la posicion nueva es distinta a la anterior, calculo trayectoria
            m[k]=calcTrayectoria([mOld[k],mNew[k]],timeStep,slp)
        else:
            m[k]=[mNew[k] for i in xrange(length)]
            # Para asegurar que tenga el mismo tipo de variable           
            m[k]=asarray(m[k])
            
    return[m[0],m[1],m[2],m[3],m[4]]


def retCero(L1,L2,L3,L4,timeStep,slp,mOld,cero,m6,ser):

    [m1,m2,m3,m4,m5,mNew,TH_0]=volverCero(L1,L2,L3,L4,timeStep,slp,mOld,cero)
    # Cargo la posicion Cero en Old, para usar como posicion inicial
    # en proximas trayectorias
    m1Old=cero[0]
    m2Old=cero[1]
    m3Old=cero[2]
    m4Old=cero[3]
    m5Old=cero[4]
    
    [m1New,m2New,m3New,m4New,m5New,m1p,m2p,m3p,m4p,m5p]=ajustesVariables(m1,m2,m3,m4,m5)        

    transmSerie(m1p,m2p,m3p,m4p,m5p,[m6]*int(timeStep/slp),slp,ser)
    
    m1Old=m1New
    m2Old=m2New
    m3Old=m3New
    m4Old=m4New
    m5Old=m5New
    mOld=[m1Old,m2Old,m3Old,m4Old,m5Old]   

    return[m1,m2,m3,m4,m5,mOld]     

        
def volverCero(L1,L2,L3,L4,timeStep,slp,mOld,cero):         
        
    TH_0=cinematicaDir(cero[0],cero[1],cero[2],cero[3],cero[4],L1,L2,L3,L4)
    
    mNew=[cero[0],cero[1],cero[2],cero[3],cero[4]]
    
    # Angulos pre-ajuste a servo
    [m1,m2,m3,m4,m5]=preTrayectoria(L1,L2,L3,L4,mOld,mNew,timeStep,slp)    
    
    #return [m1New,m2New,m3New,m4New,m5New,m6New,TH_0]
    return [m1,m2,m3,m4,m5,mNew,TH_0]    


#%% HERRAMIENTA
def clawControl(m1,m2,m3,m4,m5,slp,ser,claw):
    if claw==0:
        m6p=closeClaw(m1,m2,m3,m4,m5,slp,ser)
        m6=120
        claw=1
        return [m6,claw]
    else:
        m6p=openClaw(m1,m2,m3,m4,m5,slp,ser)
        m6=80
        claw=0
        return [m6,claw]
                
                
def closeClaw(m1,m2,m3,m4,m5,slp,ser):  
    # Apertura suave de la herramienta
    puntos=[80,120]
    m6=calcTrayectoria(puntos,0.5,slp)  
    length=int(0.5/slp)    
    m6p=m6.tolist()
    
    # Tomo último valor del resto de los servos para evitar movimientos 

    m1p=[fixM1(m1)]*length
    m2p=[fixM2(m2)]*length
    m3p=[fixM3(m3)]*length
    m4p=[fixM4(m4)]*length
    m5p=[fixM5(m5)]*length 

    transmSerie(m1p,m2p,m3p,m4p,m5p,m6p,slp,ser)
    m6p=[m6p[-1]]*len(m1p)
    
    return[m6p]
       
def openClaw(m1,m2,m3,m4,m5,slp,ser):  
    # Apertura suave de la herramienta
    puntos=[120,80]
    m6=calcTrayectoria(puntos,0.5,slp)   
    length=int(0.5/slp) 
    m6p=m6.tolist()
    
    # Tomo último valor del resto de los servos para evitar movimientos
    m1p=[fixM1(m1)]*length
    m2p=[fixM2(m2)]*length
    m3p=[fixM3(m3)]*length
    m4p=[fixM4(m4)]*length
    m5p=[fixM5(m5)]*length 

    transmSerie(m1p,m2p,m3p,m4p,m5p,m6p,slp,ser)
    
    m6p=[m6p[-1]]*len(m1p)
    return[m6p]

def jacob(L1,L2,L3,L4,mOld,timeStep,slp,ser,m6):
    #Primero calculo la trayectoria del punto actual a donde comienza el circulo
    #que desarrolla el jacobiano
    qpitch=0;qroll=0;x=15;y=0;z=24;
    
    [m1New,m2New,m3New,m4New,m5New,status]=cinInv(qpitch,qroll,x,y,z,L1,L2,L3,L4)
    if status==0:
        m1New=m1New/math.pi*180
        m2New=m2New/math.pi*180
        m3New=m3New/math.pi*180
        m4New=m4New/math.pi*180
        m5New=m5New/math.pi*180
        mNew=[m1New,m2New,m3New,m4New,m5New]
        
        [m1,m2,m3,m4,m5]=preTrayectoria(L1,L2,L3,L4,mOld,mNew,timeStep,slp)
        
        [m1New,m2New,m3New,m4New,m5New,m1p,m2p,m3p,m4p,m5p]=ajustesVariables(m1,m2,m3,m4,m5)             
 
        m1=m1.tolist()
        m2=m2.tolist()
        m3=m3.tolist()
        m4=m4.tolist()
        m5=m5.tolist()
        
        t=transmSerie(m1p,m2p,m3p,m4p,m5p,[m6]*int(len(m1p)),slp,ser)
        
        [m1j,m2j,m3j,m4j,m5j]=Jacobiano(L1,L2,L3,L4)
        
        m1j=(m1j/math.pi*180)
        m2j=(m2j/math.pi*180)
        m3j=(m3j/math.pi*180)
        m4j=(m4j/math.pi*180)
        m5j=(m5j/math.pi*180)

        [m1New,m2New,m3New,m4New,m5New,m1jp,m2jp,m3jp,m4jp,m5jp]=ajustesVariables(m1j,m2j,m3j,m4j,m5j)             
        
        t=transmSerie(m1jp,m2jp,m3jp,m4jp,m5jp,[m6]*int(len(m1p)),slp,ser)        
        
        #Concateno vectores
        #Vector Para Graficar
        m1.extend(m1j)
        m2.extend(m2j)
        m3.extend(m3j)
        m4.extend(m4j)
        m5.extend(m5j)               
        
        # Vectores a Transmitir
        m1p.extend(m1jp)
        m2p.extend(m2jp)
        m3p.extend(m3jp)
        m4p.extend(m4jp)
        m5p.extend(m5jp) 
        
        # Grafico
        plt.plot(m1)
        plt.plot(m2)
        plt.plot(m3)
        plt.plot(m4)
        plt.plot(m5)
        plt.legend(['m1', 'm2', 'm3', 'm4','m5'], loc='best')        
        plt.show()        
        
        return [m1p,m2p,m3p,m4p,m5p,m1,m2,m3,m4,m5]

    else:
        return [0,0,0,0,0]
        
        

    
    
 
            
            
def ajustesVariables(m1,m2,m3,m4,m5):        

    # Ultima posición se almacena en las variables New
    m1New=m1[-1]
    m2New=m2[-1]
    m3New=m3[-1]
    m4New=m4[-1]
    m5New=m5[-1]
    # Ajusto a valores del servo
    m1=fixM1(m1)
    m2=fixM2(m2)
    m3=fixM3(m3)
    m4=fixM4(m4)
    m5=fixM5(m5)   
    # Genero listas para transmitir
    m1p=m1.tolist()
    m2p=m2.tolist()
    m3p=m3.tolist()
    m4p=m4.tolist()
    m5p=m5.tolist()
    
    return [m1New,m2New,m3New,m4New,m5New,m1p,m2p,m3p,m4p,m5p]
    
 
    
    
#%% RUTINA MOVIMIENTO DE OBJETO CON CINEMATICA INVERSA
#Funcion Para Movimientos Genericos
def movimiento(qpitch,qroll,x,y,z,L1,L2,L3,L4,mOld,timeStep,slp,ser,m6):
    
    #Calculo la Cinematica Inversa
    [m1New,m2New,m3New,m4New,m5New,status]=cinInv(qpitch,qroll,x,y,z,L1,L2,L3,L4)
    if status==0:
		#Ajusto resultados a radiales
		m1New=m1New/math.pi*180
		m2New=m2New/math.pi*180
		m3New=m3New/math.pi*180
		m4New=m4New/math.pi*180
		m5New=m5New/math.pi*180
		mNew=[m1New,m2New,m3New,m4New,m5New]
		
		#Verifico límites físicos
		c1=limiteM1(m1New)
		c2=limiteM2(m2New)
		c3=limiteM3(m3New)
		c4=limiteM4(m4New)
		c5=limiteM5(m5New)                        

		if (c1==1 or c2==1 or c3==1 or c4==1 or c5==1):
			print ('Fuera del area de trabajo')
		else:	
			# Angulos pre-ajuste a servo
			[m1,m2,m3,m4,m5]=preTrayectoria(L1,L2,L3,L4,mOld,mNew,timeStep,slp) 
    
			[m1New,m2New,m3New,m4New,m5New,m1p,m2p,m3p,m4p,m5p]=ajustesVariables(m1,m2,m3,m4,m5)        
			
			t=transmSerie(m1p,m2p,m3p,m4p,m5p,[m6]*int(timeStep/slp),slp,ser)
    
    #time.sleep(1)
    
    m1Old=m1New
    m2Old=m2New
    m3Old=m3New
    m4Old=m4New
    m5Old=m5New
    mOld=[m1Old,m2Old,m3Old,m4Old,m5Old]
    
    return [mOld,m1p,m2p,m3p,m4p,m5p,m1,m2,m3,m4,m5]

    
def movPredeterminado(mOld,m6,slp,timeStep,ser,L1,L2,L3,L4,cero):
    
    #Posicion arriba de objeto
    qpitch=-90/180.*math.pi       
    qroll=-90/180.*math.pi 
    x=12.5
    y=0
    z=10
    
    
    [mOld,m1p,m2p,m3p,m4p,m5p,m1,m2,m3,m4,m5]=movimiento(qpitch,qroll,x,y,z,L1,L2,L3,L4,mOld,timeStep,slp,ser,m6)
    
    
    #Bajo hacia el objeto
    qpitch=-90/180.*math.pi       
    qroll=-90/180.*math.pi 
    x=12
    y=0
    z=7

    
    [mOld,m1p,m2p,m3p,m4p,m5p,m1,m2,m3,m4,m5]=movimiento(qpitch,qroll,x,y,z,L1,L2,L3,L4,mOld,0.5,slp,ser,m6)


    #Cerrar Herramienta
    m6,claw=clawControl(m1[-1],m2[-1],m3[-1],m4[-1],m5[-1],slp,ser,0)
    
    # Levanto Objeto
    qpitch=-90/180.*math.pi       
    qroll=-90/180.*math.pi 
    x=10
    y=0
    z=10
 
    
    [mOld,m1p,m2p,m3p,m4p,m5p,m1,m2,m3,m4,m5]=movimiento(qpitch,qroll,x,y,z,L1,L2,L3,L4,mOld,0.5,slp,ser,m6)
    
    
    #Muevo Objeto a posicion nueva
    qpitch=-90/180.*math.pi       
    qroll=-90/180.*math.pi 
    x=2
    y=10
    z=10
 
    
    [mOld,m1p,m2p,m3p,m4p,m5p,m1,m2,m3,m4,m5]=movimiento(qpitch,qroll,x,y,z,L1,L2,L3,L4,mOld,timeStep,slp,ser,m6)

    
    # Bajo Objeto
    qpitch=-90/180.*math.pi       
    qroll=-90/180.*math.pi 
    x=2
    y=10
    z=7

    
    [mOld,m1p,m2p,m3p,m4p,m5p,m1,m2,m3,m4,m5]=movimiento(qpitch,qroll,x,y,z,L1,L2,L3,L4,mOld,0.5,slp,ser,m6)


    #Abro Herramienta
    m6,claw=clawControl(m1[-1],m2[-1],m3[-1],m4[-1],m5[-1],slp,ser,1)
    
    
    #Volver a Pos Inicial
    [m1,m2,m3,m4,m5,mOld]=retCero(L1,L2,L3,L4,timeStep,slp,mOld,cero,m6,ser)



    m1Old=mOld[0]
    m2Old=mOld[1]
    m3Old=mOld[2]
    m4Old=mOld[3]
    m5Old=mOld[4]
    
    return[mOld]
    
    
def readTextMov(mOld,m6,slp,timeStep,ser,L1,L2,L3,L4,cero,text,claw):
    
    positions=numpy.loadtxt('/Users/Dan/Documents/Python Scripts/Custom Scripts/'+text+'.txt')
    
    for i in range(len(positions)):
        qpitch=positions[i,2]/180.*math.pi
        qroll=positions[i,3]/180.*math.pi
        x=positions[i,4]
        y=positions[i,5]
        z=positions[i,6]
        clawChange=positions[i,7]
        timeV=positions[i,0]
        sleepT=positions[i,1]
        
        [mOld,m1p,m2p,m3p,m4p,m5p,m1,m2,m3,m4,m5]=movimiento(qpitch,qroll,x,y,z,L1,L2,L3,L4,mOld,timeV,slp,ser,m6)
        time.sleep(sleepT)
        
        #Abrir/Cerrar Herramienta
        if clawChange!=claw:            
            m6,claw=clawControl(m1[-1],m2[-1],m3[-1],m4[-1],m5[-1],slp,ser,claw)
            #print claw
        #print str(mOld)

            
    # Volver todo a condiciones Iniciales        
    if claw==1:
        m6,claw=clawControl(m1[-1],m2[-1],m3[-1],m4[-1],m5[-1],slp,ser,1)    
    
    #Volver a Pos Inicial
    [m1,m2,m3,m4,m5,mOld1]=retCero(L1,L2,L3,L4,timeStep,slp,mOld,cero,m6,ser)

    mOld[0]=mOld1[0]
    mOld[1]=mOld1[1]
    mOld[2]=mOld1[2]
    mOld[3]=mOld1[3]
    mOld[4]=mOld1[4]
    
    return mOld
	
def cinematicaDirPlot(q1,q2,q3,q4,q5,L1,L2,L3,L4):
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

    return [T0,T1_0,T2_0,T3_0,T4_0,T5_0,TH_0]



