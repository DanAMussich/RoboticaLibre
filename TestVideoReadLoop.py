# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 16:58:28 2015

@author: Dan
"""

import cv2
import glob
import numpy
from searchLeds import*
from TestDeteccion import*
from matplotlib import pyplot as plt
from calcAngulos import*


def saveLog3(m,Cx_r,Cy_r,Cx_g,Cy_g,Cx_c,Cy_c,m2v,m3v,m4v,m2,m3,m4,l1,l2,l3):
    

    f=open(dit+str(m)+'_Log_Angulos'+'.txt','w')
    f2=open(dit+str(m)+'_Log_Mediciones'+'.txt','w')

    i=0
    while i<=(len(m2)-1):                                
        f.write(str(i)+' '+' %s %s %s %s %s %s.\n\n'%(m2v[i],m2[i],m3v[i],m3[i],m4v[i],m4[i]))
        i=i+1                    
    i=0    
    while i<=(len(m2)-1):    
        f2.write(str(i)+' '+' %s %s %s %s %s %s %s %s %s.\n\n'%(Cx_r[i],Cy_r[i],Cx_g[i],Cy_g[i],Cx_c[i],Cy_c[i],l1[i],l2[i],l3[i]))
        i=i+1


    f.close()
    f2.close()  




videos = glob.glob('/Users/Dan/Documents/Python Scripts/VideosLoopDay/'+'*.avi')
variables= glob.glob('/Users/Dan/Documents/Python Scripts/VideosLoopDayVariables/'+'*.npy')

path_compare='/Users/Dan/Documents/Python Scripts/VideosLoopDay/Procesados/Comparacion2/'
dim='/Users/Dan/Documents/Python Scripts/VideosLoopDay/Procesados/Medidas/'
dimv='/Users/Dan/Documents/Python Scripts/VideosLoopDay/Procesados/Valores/'
dit='/Users/Dan/Documents/Python Scripts/VideosLoopDay/txt/'
path='/Users/Dan/Documents/Python Scripts/VideosLoopDay/Procesados/'

k=0
m=0
l1t=[]
l2t=[]
l3t=[]
#for m in range(len(videos)):
for m in range(27):
    
    cap = cv2.VideoCapture(videos[m])
    #ret, frame = cap.read()
    [Cx_r,Cy_r,Cx_g,Cy_g,Cx_c,Cy_c]=deteccion(cap,m,path)
    cap.release()
    
    [m2,m3,m4,l1,l2,l3,Cy_r,Cy_g,Cy_c]=calcAngulos(Cx_r,Cy_r,Cx_g,Cy_g,Cx_c,Cy_c)
    
    l1t.extend(l1)
    l2t.extend(l2)
    l3t.extend(l3)
    
    k=m*4
    
    m2v=np.load(variables[k])
    m3v=np.load(variables[k+1])
    m4v=np.load(variables[k+2])
    time=np.load(variables[k+3])
    
    saveLog3(m,Cx_r,Cy_r,Cx_g,Cy_g,Cx_c,Cy_c,m2v,m3v,m4v,m2,m3,m4,l1,l2,l3) 
    
    np.save(dimv+str(m)+'_Cx_r',Cx_r)
    np.save(dimv+str(m)+'_Cy_r',Cy_r)
    np.save(dimv+str(m)+'_Cx_g',Cx_g)
    np.save(dimv+str(m)+'_Cy_g',Cy_g)
    np.save(dimv+str(m)+'_Cx_c',Cx_c)
    np.save(dimv+str(m)+'_Cy_c',Cy_c)
    np.save(dimv+str(m)+'_l2',l1)
    np.save(dimv+str(m)+'_l3',l2)
    np.save(dimv+str(m)+'_l4',l3)
    np.save(dimv+str(m)+'_m2',m2)
    np.save(dimv+str(m)+'_m3',m3)
    np.save(dimv+str(m)+'_m4',m4)
    
    plt.figure(1)
    plt.plot(time,m2,color='r')
    plt.plot(time,m2v,color='b')
    plt.xlabel(u"Tiempo [s]",fontsize=12)
    plt.ylabel(u"Ángulo [grados]",fontsize=12)
    plt.legend(['m2 Calc.','m2 Orig.'], 'upper center', bbox_to_anchor=(0.5, 1.15),
                    fancybox=True, shadow=True, ncol=5) 

    plt.savefig(path_compare+'m2/'+str(m)+'_m2_Comparacion.png', bbox_inches='tight', pad_inches = 0)
    plt.cla()
    plt.close()    
    
    plt.figure(2)
    plt.plot(time,m3,color='r')
    plt.plot(time,m3v,color='b')
    plt.xlabel(u"Tiempo [s]",fontsize=12)
    plt.ylabel(u"Ángulo [grados]",fontsize=12)
    plt.legend(['m3 Calc.','m3 Orig.'], 'upper center', bbox_to_anchor=(0.5, 1.15),
                    fancybox=True, shadow=True, ncol=5) 

    plt.savefig(path_compare+'m3/'+str(m)+'_m3_Comparacion.png', bbox_inches='tight', pad_inches = 0)
    plt.cla()
    plt.close()
    
    plt.figure(3)
    plt.plot(time,m4,color='r')
    plt.plot(time,m4v,color='b')
    plt.xlabel(u"Tiempo [s]",fontsize=12)
    plt.ylabel(u"Ángulo [grados]",fontsize=12)
    plt.legend(['m4 Calc.','m4 Orig.'], 'upper center', bbox_to_anchor=(0.5, 1.15),
                    fancybox=True, shadow=True, ncol=5) 
  
    plt.savefig(path_compare+'m4/'+str(m)+'_m4_Comparacion.png', bbox_inches='tight', pad_inches = 0)
    plt.cla()
    plt.close()
    
    plt.figure(4)
    plt.plot(time,l1,color='r')
    plt.plot(time,l2,color='g')
    plt.plot(time,l3,color='b')
    plt.legend(['L2','L3','L4'], 'upper center', bbox_to_anchor=(0.5, -0.05),
                    fancybox=True, shadow=True, ncol=5) 
    plt.savefig(dim+str(m)+'_medidas.png', bbox_inches='tight', pad_inches = 0)    
    plt.cla()
    plt.close()
    
    





l2=numpy.polyfit(range(len(l1t)),l1t,0)    
l3=numpy.polyfit(range(len(l2t)),l2t,0)
l4=numpy.polyfit(range(len(l3t)),l3t,0)

l2d=numpy.std(l1t)
l3d=numpy.std(l2t)
l4d=numpy.std(l3t)