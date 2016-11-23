# -*- coding: utf-8 -*-
"""
Created on Thu Oct 23 11:23:30 2014

@author: Dan
"""

#%% Librerias Propias
from CinematicaInversa import*
from CinematicaDirecta import*
from calcTrayectoria import*
from transmSerie import*
from jacobiano import*
from fixM import*
import time

#from TestLoopPosiciones import*
#from movPredeterminado import*
#%% Librerias de Python
import math

#%% Funciones

#%% Funciones de Posición

def movNuevo(L1,L2,L3,L4,timeStep,slp,mOld,posInic,serial,ser,cero,m6):
    
    while(1):
        print """Defina Tipo:
        1. Angulos Manuales
        2. Coordenadas Cartesianas
        3. Volver a Cero
        4. Movimiento Predeterminado
        """
        print "Please Select:"
        selection=raw_input("") 

        if selection=='1':      #Cinematica Directa
            [m1,m2,m3,m4,m5,mNew,TH_0]=menuDos(L1,L2,L3,L4,timeStep,slp,mOld)

            [m1New,m2New,m3New,m4New,m5New,m1p,m2p,m3p,m4p,m5p]=ajustesVariables(m1,m2,m3,m4,m5)        
            
            return [m1New,m2New,m3New,m4New,m5New,m1p,m2p,m3p,m4p,m5p,m1,m2,m3,m4,m5,mOld,posInic]
        
        elif selection=='2':    #Cinematica Inversa
            [m1,m2,m3,m4,m5]=menuUno(L1,L2,L3,L4,timeStep,slp,mOld)
            
            [m1New,m2New,m3New,m4New,m5New,m1p,m2p,m3p,m4p,m5p]=ajustesVariables(m1,m2,m3,m4,m5)                    
             
            return [m1New,m2New,m3New,m4New,m5New,m1p,m2p,m3p,m4p,m5p,m1,m2,m3,m4,m5,mOld,posInic]
        
        elif selection=='3':    #Volver a posicion almacenada en memoria
            if serial==1:
                if posInic==1:
                    [m1Old,m2Old,m3Old,m4Old,m5Old,mOld,m1p,m2p,m3p,m4p,m5p,m1,m2,m3,m4,m5]=retCero(L1,L2,L3,L4,timeStep,slp,mOld,cero,m6,ser)
                    
                    posInic=0
                    return[m1Old,m2Old,m3Old,m4Old,m5Old,m1p,m2p,m3p,m4p,m5p,m1,m2,m3,m4,m5,mOld,posInic]
                else:
                    print "Robot sigue en posición de inicio"
            else:
                print "Conectar Primero"
          
        elif selection=='4':
            if serial==1:
                [m1Old,m2Old,m3Old,m4Old,m5Old,mOld,m1p,m2p,m3p,m4p,m5p,m1,m2,m3,m4,m5]=movPredeterminado(mOld,m6,slp,timeStep,ser,L1,L2,L3,L4,cero)
                posInic=0
                
                return[m1Old,m2Old,m3Old,m4Old,m5Old,m1p,m2p,m3p,m4p,m5p,m1,m2,m3,m4,m5,mOld,posInic]

          
        else:
            print "Opción No Valida!" 
            

def menuUno(L1,L2,L3,L4,timeStep,slp,mOld):
    #Cinematica Inversa
    correct=1    #flag de ingreso de valores aceptables
    while correct==1:
        
        print "Defina Pitch:"
        qpitch=int(input(""))
        print "Defina Roll:"
        qroll=int(input(""))
        print "Defina X:"
        x=int(input(""))
        print "Defina Y:"
        y=int(input(""))
        print "Defina Z:"
        z=int(input(""))
        # ajusto porque fcion necesita radiales
        qpitch=qpitch/180.*math.pi       
        qroll=qroll/180.*math.pi         
    
        [m1New,m2New,m3New,m4New,m5New,status]=cinInv(qpitch,qroll,x,y,z,L1,L2,L3,L4)
        if status==0:   #si la Cinematica Inversa se pudo calcular sin errores
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
                correct=1     
            else:
                correct=0
            
                # Angulos pre-ajuste a servo
                [m1,m2,m3,m4,m5]=preTrayectoria(L1,L2,L3,L4,mOld,mNew,timeStep,slp)
        
                #Grafico        
                plt.plot(m1)
                plt.plot(m2)
                plt.plot(m3)
                plt.plot(m4)
                plt.plot(m5)
                
                plt.legend(['m1', 'm2', 'm3', 'm4','m5'], loc='best')        
                plt.show()            
                
                return [m1,m2,m3,m4,m5]  
        else:
            return [0,0,0,0,0]
        
def menuDos(L1,L2,L3,L4,timeStep,slp,mOld):
    #Cinemática Directa
    correct=1   #flag de ingreso de valores aceptables
    while (correct==1):
        
        print "Defina Angulo 1:"
        m1New=int(input(""))
        print "Defina Angulo 2:"
        m2New=int(input(""))
        print "Defina Angulo 3:"
        m3New=int(input(""))
        print "Defina Angulo 4:"
        m4New=int(input(""))
        print "Defina Angulo 5:"
        m5New=int(input(""))
        
        c1=limiteM1(m1New)
        c2=limiteM2(m2New)
        c3=limiteM3(m3New)
        c4=limiteM4(m4New)
        c5=limiteM5(m5New)
        
        if (c1==1 or c2==1 or c3==1 or c4==1 or c5==1):
            correct=1
        else:
            correct=0
            
        
    TH_0=cinematicaDir(m1New,m2New,m3New,m4New,m5New,L1,L2,L3,L4)
    print "Ingresado" 
    
    mNew=[m1New,m2New,m3New,m4New,m5New]
    
    # Angulos pre-ajuste a servo
    [m1,m2,m3,m4,m5]=preTrayectoria(L1,L2,L3,L4,mOld,mNew,timeStep,slp)    

    #Grafico        
    plt.plot(m1)
    plt.plot(m2)
    plt.plot(m3)
    plt.plot(m4)
    plt.plot(m5)
    
    plt.legend(['m1', 'm2', 'm3', 'm4','m5'], loc='best')        
    plt.show()
        
    return [m1,m2,m3,m4,m5,mNew,TH_0]    
    
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

    return[m1Old,m2Old,m3Old,m4Old,m5Old,mOld,m1p,m2p,m3p,m4p,m5p,m1,m2,m3,m4,m5]     

        
def volverCero(L1,L2,L3,L4,timeStep,slp,mOld,cero):         
        
    TH_0=cinematicaDir(cero[0],cero[1],cero[2],cero[3],cero[4],L1,L2,L3,L4)
    
    mNew=[cero[0],cero[1],cero[2],cero[3],cero[4]]
    
    # Angulos pre-ajuste a servo
    [m1,m2,m3,m4,m5]=preTrayectoria(L1,L2,L3,L4,mOld,mNew,timeStep,slp)    

    #Grafico        
    plt.plot(m1)
    plt.plot(m2)
    plt.plot(m3)
    plt.plot(m4)
    plt.plot(m5)
    
    plt.legend(['m1', 'm2', 'm3', 'm4','m5'], loc='best')        
    plt.show()
    
    # Falta agregar el fix de servos    
    
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
        
        

    
    
def configuracion(SerialPort,Baud,slp,timeStep):

    while (1):    
        print """Configuración:
        1. Puerto Serie (Actual: %s)
        2. Baud Rate (Actual: %s)
        3. Paso (Actual: %s)
        4. Tiempo Entre Puntos (Actual: %s)
        5. Salir
        """ %(SerialPort, Baud,slp, timeStep)
        print "Please Select:"
        
        selection_2=raw_input("") 
        if selection_2== '1':
            print "Nuevo Puerto Serie:"
            SerialPort=int(raw_input(""))
        
        elif selection_2 =='2':
            print "Nuevo Baud Rate:"
            Baud=int(raw_input(""))
            
        elif selection_2 == '3':
            print "Nuevo Paso:"
            slp=int(raw_input(""))
            
        elif selection_2 == '4':
            print "Nuevo Tiempo Entre Puntos:"
            timeStep=int(raw_input(""))
            
        elif selection_2 == '5':
            print "Volviendo al Menú Principal."        
            return [SerialPort,Baud,slp,timeStep]    
            
            
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
    

            
def transmitir(m1p,m2p,m3p,m4p,m5p,m6,slp,ser,timeStep,m1,m2,m3,m4,m5,m1New,m2New,m3New,m4New,m5New):
    while(1):
        print """Desea grabar el movimiento?
        y/n
        """
        print "Please Select:"
        selection=raw_input("") 
        
        if selection=='y':
                dirString='/Users/Dan/Documents/Python Scripts/Videos/'
                ts=str(datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H-%M-%S'))

                newName='CaptureVideo_TEST_'+ts
                
                [t,s,t_extra,s_extra,st,di]=transmSerieVid(m1p,m2p,m3p,m4p,m5p,[m6]*int(timeStep/slp),slp,ser,dirString,newName)
                saveLog(t,s,t_extra,s_extra,st,di,m1,m2,m3,m4,m5,m6)

                # Tras transmitir, paso la coordenada nueva a la vieja
                m1Old=m1New
                m2Old=m2New
                m3Old=m3New
                m4Old=m4New
                m5Old=m5New
                mOld=[m1Old,m2Old,m3Old,m4Old,m5Old]

                return mOld                
                
        elif selection=='n':
            
            t=transmSerie(m1p,m2p,m3p,m4p,m5p,[m6]*int(timeStep/slp),slp,ser)
            td=[]
            td.append(0)
            f=open('/Users/Dan/Documents/Python Scripts/Videos/TiempoTrans_'+str(datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H-%M-%S'))+'.txt','w')
            
            for i in range(len(t)-1):
                td.append(t[i+1]-t[i])  
                f.write(str(round(td[i],3))+' segundos. \n'+ str(round(t[i],3)) +'\nPosición: M1: %s; M2:%s; M3:%s; M4:%s; M5:%s; M6:%s.\n\n'%(m1[i],m2[i],m3[i],m4[i],m5[i],m6))
            f.write('Tiempo máximo de transmisión: '+str(round(max(td),3))+' segundos.\n') 
            f.write('Tiempo total: '+str(sum(td))+' segundos.')
            f.close()
            # Tras transmitir, paso la coordenada nueva a la vieja
            m1Old=m1New
            m2Old=m2New
            m3Old=m3New
            m4Old=m4New
            m5Old=m5New
            mOld=[m1Old,m2Old,m3Old,m4Old,m5Old]
            
            return mOld
            



#def movPredeterminado(mOld,m6,slp,timeStep,ser,L1,L2,L3,L4):
#    
#    mNew=[-45,120,-45,-45,0]    
#    [mOld,m1p,m2p,m3p,m4p,m5p,m1,m2,m3,m4,m5]=movimiento(L1,L2,L3,L4,mOld,mNew,timeStep,slp,ser,m6)
#    
#    #Claw change
#    
#    time.sleep(0.5)
#    
#    mNew=[0,140,-90,-90,0]    
#    [mOld,m1p,m2p,m3p,m4p,m5p,m1,m2,m3,m4,m5]=movimiento(L1,L2,L3,L4,mOld,mNew,timeStep,slp,ser,m6)
#    
#    time.sleep(0.5)
#
#    mNew=[0,90,0,0,0]    
#    [mOld,m1p,m2p,m3p,m4p,m5p,m1,m2,m3,m4,m5]=movimiento(L1,L2,L3,L4,mOld,mNew,timeStep,slp,ser,m6)
#
#    time.sleep(0.5)
#    
#    mNew=[0,140,-90,-90,0]
#    [mOld,m1p,m2p,m3p,m4p,m5p,m1,m2,m3,m4,m5]=movimiento(L1,L2,L3,L4,mOld,mNew,timeStep,slp,ser,m6)
#
#
#    m1Old=mOld[0]
#    m2Old=mOld[1]
#    m3Old=mOld[2]
#    m4Old=mOld[3]
#    m5Old=mOld[4]
#    
#    return[m1Old,m2Old,m3Old,m4Old,m5Old,mOld,m1p,m2p,m3p,m4p,m5p,m1,m2,m3,m4,m5]
    

#Funcion Para Movimientos Genericos
def movimiento(L1,L2,L3,L4,mOld,mNew,timeStep,slp,ser,m6):
    
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
    

    
#def movPredVideo(mOld,m6,slp,timeStep,ser,L1,L2,L3,L4):
#    
#    m1=0
#    m2=[40,73,106,140]
#    m3=[-120,-75,-29,20]    
#    m4=[-100,-47,7,60]
#    m5=0
#    
##    for k<=2:
##        for l<=2:
##            for m<=2:
##                mNew=[m1,m2[]]
#
#
#    m1Old=mOld[0]
#    m2Old=mOld[1]
#    m3Old=mOld[2]
#    m4Old=mOld[3]
#    m5Old=mOld[4]
#    
#    return[m1Old,m2Old,m3Old,m4Old,m5Old,mOld,m1p,m2p,m3p,m4p,m5p,m1,m2,m3,m4,m5]
    
    
#%%    
def saveLog(t,s,t_extra,s_extra,st,di,m1,m2,m3,m4,m5,m6):

    td=[]
    td.append(0)
    f=open(di+'StatusTransmision_'+st+'.txt','w')
    f2=open(di+'StatusTransmision_Simple_'+st+'.txt','w')

    for i in range(len(t)-1):
        td.append(t[i+1]-t[i])  
        f.write(str(round(td[i],3))+' segundos. \n'+ str(round(t[i],3)) +'\nPosición: M1: %s; M2:%s; M3:%s; M4:%s; M5:%s; M6:%s.\n\n'%(m1[i],m2[i],m3[i],m4[i],m5[i],m6))
    k=0
    i=0
    while i<=(len(s)-1):                                
        f2.write(str(s[i])+' '+str(t[k]-t[0])+' %s %s %s %s %s %s.\n\n'%(m1[k],m2[k],m3[k],m4[k],m5[k],m6))
        i=i+1                    
        k=k+4
    i=0    
    while i<=(len(s_extra)-1):    
        f2.write(str(s_extra[i])+' '+str(t_extra[i]-t[0])+' %s %s %s %s %s %s.\n\n'%(m1[-1],m2[-1],m3[-1],m4[-1],m5[-1],m6))
        i=i+1

    f.write('Tiempo máximo de transmisión: '+str(round(max(td),3))+' segundos.\n') 
    f.write('Tiempo total: '+str(sum(td))+' segundos.')
    f.close()
    f2.close()      
    
    
#%% RUTINA MOVIMIENTO DE OBJETO CON CINEMATICA INVERSA
    
def movPredeterminado(mOld,m6,slp,timeStep,ser,L1,L2,L3,L4,cero):
    
    #Posicion arriba de objeto
    qpitch=-90/180.*math.pi       
    qroll=-90/180.*math.pi 
    x=12
    y=0
    z=10
    
    [m1New,m2New,m3New,m4New,m5New,status]=cinInv(qpitch,qroll,x,y,z,L1,L2,L3,L4)

    m1New=m1New/math.pi*180
    m2New=m2New/math.pi*180
    m3New=m3New/math.pi*180
    m4New=m4New/math.pi*180
    m5New=m5New/math.pi*180
    mNew=[m1New,m2New,m3New,m4New,m5New]  
    
    [mOld,m1p,m2p,m3p,m4p,m5p,m1,m2,m3,m4,m5]=movimiento(L1,L2,L3,L4,mOld,mNew,timeStep,slp,ser,m6)
    
    
    #Bajo hacia el objeto
    qpitch=-90/180.*math.pi       
    qroll=-90/180.*math.pi 
    x=12
    y=0
    z=4
    
    [m1New,m2New,m3New,m4New,m5New,status]=cinInv(qpitch,qroll,x,y,z,L1,L2,L3,L4)

    m1New=m1New/math.pi*180
    m2New=m2New/math.pi*180
    m3New=m3New/math.pi*180
    m4New=m4New/math.pi*180
    m5New=m5New/math.pi*180
    mNew=[m1New,m2New,m3New,m4New,m5New]  
    
    [mOld,m1p,m2p,m3p,m4p,m5p,m1,m2,m3,m4,m5]=movimiento(L1,L2,L3,L4,mOld,mNew,timeStep,slp,ser,m6)


    #Cerrar Herramienta
    m6,claw=clawControl(m1[-1],m2[-1],m3[-1],m4[-1],m5[-1],slp,ser,0)
    
    # Levanto Objeto
    qpitch=-90/180.*math.pi       
    qroll=-90/180.*math.pi 
    x=10
    y=0
    z=10
    
    [m1New,m2New,m3New,m4New,m5New,status]=cinInv(qpitch,qroll,x,y,z,L1,L2,L3,L4)

    m1New=m1New/math.pi*180
    m2New=m2New/math.pi*180
    m3New=m3New/math.pi*180
    m4New=m4New/math.pi*180
    m5New=m5New/math.pi*180
    mNew=[m1New,m2New,m3New,m4New,m5New]  
    
    [mOld,m1p,m2p,m3p,m4p,m5p,m1,m2,m3,m4,m5]=movimiento(L1,L2,L3,L4,mOld,mNew,timeStep,slp,ser,m6)
    
    
    #Muevo Objeto a posicion nueva
    qpitch=-90/180.*math.pi       
    qroll=-90/180.*math.pi 
    x=2
    y=10
    z=10
    
    [m1New,m2New,m3New,m4New,m5New,status]=cinInv(qpitch,qroll,x,y,z,L1,L2,L3,L4)

    m1New=m1New/math.pi*180
    m2New=m2New/math.pi*180
    m3New=m3New/math.pi*180
    m4New=m4New/math.pi*180
    m5New=m5New/math.pi*180
    mNew=[m1New,m2New,m3New,m4New,m5New]  
    
    [mOld,m1p,m2p,m3p,m4p,m5p,m1,m2,m3,m4,m5]=movimiento(L1,L2,L3,L4,mOld,mNew,timeStep,slp,ser,m6)

    
    # Bajo Objeto
    qpitch=-90/180.*math.pi       
    qroll=-90/180.*math.pi 
    x=2
    y=10
    z=7
    
    [m1New,m2New,m3New,m4New,m5New,status]=cinInv(qpitch,qroll,x,y,z,L1,L2,L3,L4)

    m1New=m1New/math.pi*180
    m2New=m2New/math.pi*180
    m3New=m3New/math.pi*180
    m4New=m4New/math.pi*180
    m5New=m5New/math.pi*180
    mNew=[m1New,m2New,m3New,m4New,m5New]  
    
    [mOld,m1p,m2p,m3p,m4p,m5p,m1,m2,m3,m4,m5]=movimiento(L1,L2,L3,L4,mOld,mNew,timeStep,slp,ser,m6)


    #Abro Herramienta
    m6,claw=clawControl(m1[-1],m2[-1],m3[-1],m4[-1],m5[-1],slp,ser,1)
    
    
    #Volver a Pos Inicial
    [m1Old,m2Old,m3Old,m4Old,m5Old,mOld,m1p,m2p,m3p,m4p,m5p,m1,m2,m3,m4,m5]=retCero(L1,L2,L3,L4,timeStep,slp,mOld,cero,m6,ser)



    m1Old=mOld[0]
    m2Old=mOld[1]
    m3Old=mOld[2]
    m4Old=mOld[3]
    m5Old=mOld[4]
    
    return[m1Old,m2Old,m3Old,m4Old,m5Old,mOld,m1p,m2p,m3p,m4p,m5p,m1,m2,m3,m4,m5]