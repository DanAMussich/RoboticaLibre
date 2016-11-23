# -*- coding: utf-8 -*-
"""
Created on Wed Apr 08 14:16:51 2015

@author: Dan
"""

from menuOptions import*
#from menuOptions import preTrayectoria
#import menuOptions
from transmSerie import*
from fixM import*
import time
import matplotlib.pyplot as plt



#%%
def loopPosiciones(L1,L2,L3,L4,mOld1,slp,ser,step,m6):

    m1=0
    #m2=[140,106,73,40]
    m2=[130,100,70,40]
    m3=[-90,-60,-30,0]    
    #m4=[-90,-43,4,50]
    m4=[-100,-60,-35,0]
    m5=0
    #m6=80    
    
    timeStep=1
    step=2
    #Posicion de Arranque
    mNew=[m1,m2[0],m3[0],m4[0],m5]
    
    [m1t,m2t,m3t,m4t,m5t]=preTrayectoria(L1,L2,L3,L4,mOld1,mNew,step,slp)
    
    [m1New,m2New,m3New,m4New,m5New,m1p,m2p,m3p,m4p,m5p]=ajustesVariables(m1t,m2t,m3t,m4t,m5t)        
                    
    #Transmito
     
    #transmSerie(m1p,m2p,m3p,m4p,m5p,[m6]*int(step/slp),slp,ser)
      
    time.sleep(1)
         
    mOld=[m1,m2[0],m3[0],m4[0],m5]
    m2v=[]
    m3v=[]
    m4v=[]
    
    m2s=[]
    m3s=[]
    m4s=[]
    
    while timeStep<=1:
        for k in range(0,3):
            for l in range(0,3):
                for m in range(0,3):
                             
                    
                    mNew=[m1,m2[k+1],m3[l+1],m4[m+1],m5]
                    
                    [m1t,m2t,m3t,m4t,m5t]=preTrayectoria(L1,L2,L3,L4,mOld,mNew,timeStep,slp)
                    [m1Newp,m2Newp,m3Newp,m4Newp,m5Newp,m1p,m2p,m3p,m4p,m5p]=ajustesVariables(m1t,m2t,m3t,m4t,m5t)        
    
                    m2v.extend(m2t)            
                    m3v.extend(m3t)            
                    m4v.extend(m4t) 
                    
#                    dirStringVar='/Users/Dan/Documents/Python Scripts/VideosLoopVariables/'
#                    
#                    np.save(dirStringVar+str(timeStep)+'_Step_'+str(k)+str(l)+str(m)+'_m2',m2t)
#                    np.save(dirStringVar+str(timeStep)+'_Step_'+str(k)+str(l)+str(m)+'_m3',m3t)
#                    np.save(dirStringVar+str(timeStep)+'_Step_'+str(k)+str(l)+str(m)+'_m4',m4t)

                    m2s.extend(m2p)            
                    m3s.extend(m3p)            
                    m4s.extend(m4p)                  
                    
                    # Transmito y Grabo
                    #t=transmSerie(m1p,m2p,m3p,m4p,m5p,[m6]*int(timeStep/slp),slp,ser)
                    

                    dirString='/Users/Dan/Documents/Python Scripts/VideosLoopDay/'
                    newName=str(timeStep)+'_Step_'+str(k)+str(l)+str(m)
                
                    [t,s,t_extra,s_extra,st,di]=transmSerieVid(m1p,m2p,m3p,m4p,m5p,[m6]*int(timeStep/slp),slp,ser,dirString,newName)
#                    saveLog(t,s,t_extra,s_extra,st,di,[m1]*int(timeStep/slp),m2t,m3t,m4t,[m5]*int(timeStep/slp),m6)
                    saveLog2(m2t,m3t,m4t,t,t_extra,timeStep,k,l,m,s,s_extra)
                    
                    saveLog(t,s,t_extra,s_extra,st,dirString,m1t,m2t,m3t,m4t,m5t,m6)
                    #np.save(dirStringVar+str(timeStep)+'_Step_'+str(k)+str(l)+str(m)+'_time',s)                    
                                        
                    time.sleep(1)
                    
                    mOld=[m1,m2[k+1],m3[l+1],m4[m+1],m5]
                    
                    # Defino posicion a volver para proxima iteración de grabación
                    mNew[0]=m1
                    mNew[4]=m5
                    
                    #Condiciones de M4
                    if m==2:
                        mNew[3]=m4[0]                                                               
                    elif m<2:
                        mNew[3]=m4[m+1]           
                    
                    #Condiciones de M3
                    if l==2 & m==2:
                        mNew[2]=m3[0]
                    elif m==2:
                        mNew[2]=m3[l+1]
                    else:
                        mNew[2]=m3[l]
                    
                    #Condiciones de M2
                    if k==2 & l==2 & m==2:
                        mNew[1]=m2[0]  
                    elif l==2 & m==2:
                        mNew[1]=m2[k+1]
                    else:
                        mNew[1]=m2[k]
                    
                    [m1_0,m2_0,m3_0,m4_0,m5_0]=preTrayectoria(L1,L2,L3,L4,mOld,mNew,timeStep,slp)
                    [m1Newp,m2Newp,m3Newp,m4Newp,m5Newp,m1p0,m2p0,m3p0,m4p0,m5p0]=ajustesVariables(m1_0,m2_0,m3_0,m4_0,m5_0)        
                    
                    
                    # Transmito SIN Grabar
                    transmSerie(m1p0,m2p0,m3p0,m4p0,m5p0,[m6]*int(timeStep/slp),slp,ser)
                    time.sleep(1)
                    
                    mOld[0]=m1
                    mOld[1]=mNew[1]
                    mOld[2]=mNew[2]
                    mOld[3]=mNew[3]       
                    mOld[4]=m5
                    
                    m2v.extend(m2_0)            
                    m3v.extend(m3_0)            
                    m4v.extend(m4_0)    
                    
                    m2s.extend(m2p0)            
                    m3s.extend(m3p0)            
                    m4s.extend(m4p0)
         
        timeStep=timeStep*2 

    #Vuelvo a Posicion Inicial antes de volver al programa principal          
    [m1t,m2t,m3t,m4t,m5t]=preTrayectoria(L1,L2,L3,L4,mOld1,mNew,step,slp)
    
    [m1New,m2New,m3New,m4New,m5New,m1p,m2p,m3p,m4p,m5p]=ajustesVariables(m1t,m2t,m3t,m4t,m5t)        
  
    #Transmito
    
    transmSerie(m1p,m2p,m3p,m4p,m5p,[m6]*int(timeStep/slp),slp,ser)    
    
    #Grafico trayectorias reales y en valores de servo
    figure(1)
    plt.plot(m2v)
    #figure(2)
    plt.plot(m3v)
    #figure(3)
    plt.plot(m4v)    
    
    plt.legend(['m2','m3','m4'], 'upper center', bbox_to_anchor=(0.5, -0.05),
                fancybox=True, shadow=True, ncol=5)      
    plt.show()

            
    figure(2)
    plt.plot(m2s)
    #figure(2)
    plt.plot(m3s)
    #figure(3)
    plt.plot(m4s)    
    
    plt.legend(['m2','m3','m4'], 'upper center', bbox_to_anchor=(0.5, -0.05),
                fancybox=True, shadow=True, ncol=5)  
    plt.show()            
    
    return [m2v,m3v,m4v]
        

#def saveLog(t,s,t_extra,s_extra,st,di,m1,m2,m3,m4,m5,m6):
#
#    td=[]
#    td.append(0)
#    f=open(di+'StatusTransmision_'+st+'.txt','w')
#    f2=open(di+'StatusTransmision_Simple_'+st+'.txt','w')
#
#    for i in range(len(t)-1):
#        td.append(t[i+1]-t[i])  
#        f.write(str(round(td[i],3))+' segundos. \n'+ str(round(t[i],3)) +'\nPosición: M1: %s; M2:%s; M3:%s; M4:%s; M5:%s; M6:%s.\n\n'%(m1[i],m2[i],m3[i],m4[i],m5[i],m6))
#    k=0
#    i=0
#    while i<=(len(s)-1):                                
#        f2.write(str(s[i])+' '+str(t[k]-t[0])+' %s %s %s %s %s %s.\n\n'%(m1[k],m2[k],m3[k],m4[k],m5[k],m6))
#        i=i+1                    
#        k=k+4
#    i=0    
#    while i<=(len(s_extra)-1):    
#        f2.write(str(s_extra[i])+' '+str(t_extra[i]-t[0])+' %s %s %s %s %s %s.\n\n'%(m1[-1],m2[-1],m3[-1],m4[-1],m5[-1],m6))
#        i=i+1
#
#    f.write('Tiempo máximo de transmisión: '+str(round(max(td),3))+' segundos.\n') 
#    f.write('Tiempo total: '+str(sum(td))+' segundos.')
#    f.close()
#    f2.close()      
    
    
def saveLog2(m2,m3,m4,t,t_extra,timeStep,k,l,m,s,s_extra):
    
    dirStringVar='/Users/Dan/Documents/Python Scripts/VideosLoopDayVariables/'
                    
    m2v=[]
    m3v=[]                
    m4v=[]
    td=[]
    
    #t.append(t_extra)
    
    n=0
    i=0
    while i<=(len(s)-1):                                
        #f2.write(str(s[i])+' '+str(t[k]-t[0])+' %s %s %s %s %s %s.\n\n'%(m1[k],m2[k],m3[k],m4[k],m5[k],m6))
        m2v.append(m2[n])  
        m3v.append(m3[n])
        m4v.append(m4[n])
        td.append(t[n]-t[0])
        
        i=i+1                    
        n=n+4  
     
    m2v.extend([m2v[-1]]*len(s_extra))
    m3v.extend([m3v[-1]]*len(s_extra))
    m4v.extend([m4v[-1]]*len(s_extra))
                 
    np.save(dirStringVar+str(timeStep)+'_Step_'+str(k)+str(l)+str(m)+'_m2',m2v)
    np.save(dirStringVar+str(timeStep)+'_Step_'+str(k)+str(l)+str(m)+'_m3',m3v)
    np.save(dirStringVar+str(timeStep)+'_Step_'+str(k)+str(l)+str(m)+'_m4',m4v)

    td_e=[]
    #td_e.append(0)                    
    for i in range(len(t_extra)):
        td_e.append(t_extra[i]-t[0])  
                    
    td.extend(td_e)
    np.save(dirStringVar+str(timeStep)+'_Step_'+str(k)+str(l)+str(m)+'_time',td)
