# -*- coding: utf-8 -*-
"""
Created on Mon Oct 06 17:46:51 2014

@author: Dan
"""

# Librerias Propias
from calcTrayectoria import*
from startSerial import*
from transmSerie import*
from closeSerial import*
from CinematicaDirecta import*
from CinematicaInversa import*
from menuOptions import*
from fixM import*
from calcAngulos import*
from movPredeterminado import*
from TestLoopPosiciones import*
from AutoCalib import*
#from transmSerieVid import*

#Librerias de Python
import numpy
import matplotlib.pyplot as plt
#from pylab import plot



# Parametros Iniciales, valores en ángulos.
m1Start=0
m2Start=130
m3Start=-90
m4Start=-90

#m4Start=10

m5Start=00
m6Start=80      # Estado Inicial herramienta: ABIERTO, 120: CERRADO

# Defino constante Cero. 
cero=[m1Start,m2Start,m3Start,m4Start,m5Start]
uno=[0,90,-90,-90,0]
# Defino parámetros iniciales en Old para los cálculos iniciales
m1Old=m1Start
m2Old=m2Start
m3Old=m3Start
m4Old=m4Start
m5Old=m5Start
m6Old=m6Start
mOld=[m1Old,m2Old,m3Old,m4Old,m5Old]

m6=m6Start

# Variables de configuración
timeStep=2      #tiempo entre puntos
slp=0.025       #paso de claculo y transmisión
SerialPort=10   #puerto serie usado
Baud=9600       #velocidad de transmisión

# Flags
defined=0       #flag para puntos
serial=0        #flag para conexión
transm=0        #flag de al menos una transmision
claw=0
posInic=0

# Parámetros físicos del robot
L1=8
L2=13
L3=10
L4=10
#%%
menu = {}


while True: 
    
    options=menu.keys()
    options.sort()
    #for entry in range(len(menu)): 
        #print entry, menu[entry]
    print ("""
    1. Definir Movimiento Nuevo
    2. Abrir/Cerrar Herramienta
    3. Conectar/Desconectar Puerto Serie
    4. Configuración
    5. Transmitir
    6. Auto-Calibración
    7. Salir
    """)
    
    print "Ingrese Número de Opción:"
    selection=raw_input("") 
    
    if selection =='1': 
        [m1New,m2New,m3New,m4New,m5New,m1p,m2p,m3p,m4p,m5p,m1,m2,m3,m4,m5,mOld,posInic]=movNuevo(L1,L2,L3,L4,timeStep,slp,mOld,posInic,serial,ser,cero,m6)        
        defined=1       # Flag para indicar que existe una posición definida para
                        # poder transmitir

    
    elif selection == '2': 
        # Abir/Cerrar Herramienta
        if serial==1:
            [m6,claw]=clawControl(mOld[0],mOld[1],mOld[2],mOld[3],mOld[4],slp,ser,claw)
        else:
            print "Conectar Primero"
            
                 
    elif selection == '3':
        if serial==0:
            ser=startSerial(Baud,SerialPort,2)
            print "Puerto Conectado" 
            serial=1
        else:
            closeSerial(ser)
            print "Puerto Cerrado" 
            serial=0

    elif selection == '4':
        # Menu para cambio de parametros
        [SerialPort,Baud,slp,timeStep]=configuracion(SerialPort,Baud,slp,timeStep)
        
    elif selection == '5':
        if serial==1:
            if defined==1:
                mOld=transmitir(m1p,m2p,m3p,m4p,m5p,m6,slp,ser,timeStep,m1,m2,m3,m4,m5,m1New,m2New,m3New,m4New,m5New)
                
                posInic=1
                defined=0
                transm=1
            else:
                print "Definir Movimiento"                            
        else:
            print "Conectar Primero"
            defined=0
        
    elif selection == '7':
        [m1p,m2p,m3p,m4p,m5p,m1j,m2j,m3j,m4j,m5j]=jacob(L1,L2,L3,L4,mOld,timeStep,slp,ser,m6)
        # Ultima posición se almacena en las variables New
        m1New=m1j[-1]
        m2New=m2j[-1]
        m3New=m3j[-1]
        m4New=m4j[-1]
        m5New=m5j[-1]
        posInic=1        
#        defined=1        

    elif selection == '6':
        if serial==1:
            closeSerial(ser)
            serial=0
        print "Adios"
        break

    elif selection == '8':
        m2v,m3v,m4v=loopPosiciones(L1,L2,L3,L4,mOld,slp,ser,timeStep,m6)
        
    elif selection == '9':
        autoCalib(L1,L2,L3,L4,mOld,slp,ser,timeStep,m6)
        
    else: 
        print "Opción No Valida!" 


# Se recomienda correr el comando: 
# %reset -f
# tras salir del programa y antes de iniciarlo nuevamente o correr otro.
# Esto borrara todas las variables del Explorador de Variables, evitando
# posible superposición entre varaibles viejas y nuevas.