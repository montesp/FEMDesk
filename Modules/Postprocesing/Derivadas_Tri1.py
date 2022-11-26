# -*- coding: utf-8 -*-
"""
Created on Tue Oct 18 11:02:44 2022

@author: alberto.diaz
"""
import numpy as np
from scipy.sparse import dok_matrix
import Ecua_dif


def crea_PGyderivporelemento(mallado,s,U):
    
    tabla_gauss=dok_matrix((len(mallado[2]), 2), dtype=np.float64) # tabla con coordenadas de centros de elementos
    tabla_dUdx=np.empty((len(mallado[2]),s), dtype=np.float64) # tabla con derivadas de las componentes respecto a x en cada elemento
    tabla_dUdy=np.empty((len(mallado[2]),s), dtype=np.float64) # tabla con derivadas de las componentes respecto a y en cada elemento
    
    for i in range(len(mallado[2])): #i es el numero de elemento
        nodo1=mallado[2][i,0]
        nodo2=mallado[2][i,1]
        nodo3=mallado[2][i,2]
        x1=mallado[0][nodo1,0]
        x2=mallado[0][nodo2,0]
        x3=mallado[0][nodo3,0]
        y1=mallado[0][nodo1,1]
        y2=mallado[0][nodo2,1]
        y3=mallado[0][nodo3,1]
        tabla_gauss[i,0]=(x1+x2+x3)/3
        tabla_gauss[i,1]=(y1+y2+y3)/3
        
        Pi21=(y2 - y3)/(x1*y2 - x2*y1 - x1*y3 + x3*y1 + x2*y3 - x3*y2)
        Pi22=-(y1 - y3)/(x1*y2 - x2*y1 - x1*y3 + x3*y1 + x2*y3 - x3*y2)
        Pi23=(y1 - y2)/(x1*y2 - x2*y1 - x1*y3 + x3*y1 + x2*y3 - x3*y2)
        Pi31=-(x2 - x3)/(x1*y2 - x2*y1 - x1*y3 + x3*y1 + x2*y3 - x3*y2)
        Pi32=(x1 - x3)/(x1*y2 - x2*y1 - x1*y3 + x3*y1 + x2*y3 - x3*y2)
        Pi33=-(x1 - x2)/(x1*y2 - x2*y1 - x1*y3 + x3*y1 + x2*y3 - x3*y2)
        
        for j in range(s):
            tabla_dUdx[i][j]=Pi21*U[nodo1*s+j]
            tabla_dUdx[i][j]=tabla_dUdx[i][j]+Pi22*U[nodo2*s+j]
            tabla_dUdx[i][j]=tabla_dUdx[i][j]+Pi23*U[nodo3*s+j]
            tabla_dUdy[i][j]=Pi31*U[nodo1*s+j]
            tabla_dUdy[i][j]=tabla_dUdy[i][j]+Pi32*U[nodo2*s+j]
            tabla_dUdy[i][j]=tabla_dUdy[i][j]+Pi33*U[nodo3*s+j]
    
    return [tabla_gauss , tabla_dUdx , tabla_dUdy]  
          

def crea_tabla_parches(mallado,s,U):
    get_indexes = lambda x, xs: [i for (y, i) in zip(xs, range(len(xs))) if x == y] 
    nodel=dok_matrix((len(mallado[0]), len(mallado[2])+1), dtype=int)
    parcheesp1=dok_matrix((len(mallado[0]), 2), dtype=int)
    parcheesp2=dok_matrix((len(mallado[0]), 3), dtype=int)
    
    for i in range(len(mallado[0])):
        listaelem = get_indexes(i,mallado[2][:,0])
        listaelem = listaelem + get_indexes(i,mallado[2][:,1])
        listaelem = listaelem + get_indexes(i,mallado[2][:,2])
        nodel[i,0] = len(listaelem) #1a columna: numero de elementos a los que pertenece el nodo
        for j in range(len(listaelem)):
            nodel[i,j+1]=listaelem[j] #siguientes columnas: elementos a los que pertenece el nodo                    
    
    listanodos1=get_indexes(1,nodel[:,0]) # nodos que no son centro de parche, solo un elemento lo toca
    listanodos2=get_indexes(2,nodel[:,0]) # nodos que no son centro de parche, solo dos elementos lo tocan
    
    for i in listanodos1:
        elem=nodel[i,1] #único elemento que toca al nodo
        nodos=[mallado[2][elem,0],mallado[2][elem,1],mallado[2][elem,2]]
        nodos.remove(i)
        parcheesp1[i,0],parcheesp1[i,1] =nodos #nodos que conectan al nodo i
        
    for i in listanodos2:
        elem=nodel[i,1] #primer elemento que toca al nodo
        nodos1=[mallado[2][elem,0],mallado[2][elem,1],mallado[2][elem,2]]
        nodos1.remove(i)
        elem=nodel[i,2] #segundo elemento que toca al nodo
        nodos2=[mallado[2][elem,0],mallado[2][elem,1],mallado[2][elem,2]]
        nodos2.remove(i)
        nodos=nodos1+nodos2
        nodos=list(set(nodos)) 
        parcheesp2[i,0],parcheesp2[i,1],parcheesp2[i,2] =nodos #nodos que conectan al nodo i
        
    return [nodel , parcheesp1, parcheesp2]

    
def derivadas(mallado,s,U):    
    get_indexes = lambda x, xs: [i for (y, i) in zip(xs, range(len(xs))) if x == y]     
    tabla_gauss , tabla_dUdx , tabla_dUdy = crea_PGyderivporelemento(mallado,s,U)
    
    nodel,parcheesp1,parcheesp2 = crea_tabla_parches(mallado,s,U)
    listanodos1=get_indexes(1,nodel[:,0]) # nodos que no son centro de parche, solo un elemento lo toca
    listanodos2=get_indexes(2,nodel[:,0]) # nodos que no son centro de parche, solo dos elementos lo tocan
    repeticiones1=dok_matrix((len(mallado[0]), 1), dtype=int)
    repeticiones2=dok_matrix((len(mallado[0]), 1), dtype=int)
    Ux = np.zeros( (s*len(mallado[0])) )
    Uy = np.zeros( (s*len(mallado[0])) )
    IA=np.zeros( (3, 3) )
    
    for i in range(len(mallado[0])):
        if nodel[i,0]>2:
            A11, A12, A13, A22, A23, F , = [0,0,0,0,0,0]
            Bx=np.zeros( (3, s) )
            By=np.zeros( (3, s) )
            for k in range(nodel[i,0]):
                elem=nodel[i,k+1]
                xk=tabla_gauss[elem,0]
                yk=tabla_gauss[elem,1]
                A11=A11+xk*xk
                A12=A12+xk*yk
                A13=A13+xk
                A22=A22+yk*yk
                A23=A23+yk
                F=F+abs(xk)+abs(yk)
                Bx[0,:]=Bx[0,:]+xk*tabla_dUdx[elem,:]
                Bx[1,:]=Bx[1,:]+yk*tabla_dUdx[elem,:]
                Bx[2,:]=Bx[2,:]+tabla_dUdx[elem,:]
                By[0,:]=By[0,:]+xk*tabla_dUdy[elem,:]
                By[1,:]=By[1,:]+yk*tabla_dUdy[elem,:]
                By[2,:]=By[2,:]+tabla_dUdy[elem,:]
                    
            A21=A12
            A31=A13*F
            A32=A23*F
            A33=nodel[i,0]*F
            Bx[2,:]=Bx[2,:]*F
            By[2,:]=By[2,:]*F
            
            IA[0,0]=A22*A33 - A23*A32
            IA[0,1]=A13*A32 - A12*A33
            IA[0,2]=A12*A23 - A13*A22
            IA[1,0]=A23*A31 - A21*A33
            IA[1,1]=A11*A33 - A13*A31
            IA[1,2]=A13*A21 - A11*A23
            IA[2,0]=A21*A32 - A22*A31
            IA[2,1]=A12*A31 - A11*A32
            IA[2,2]=A11*A22 - A12*A21
            Det=1/(A11*A22*A33 - A11*A23*A32 - A12*A21*A33 + A12*A23*A31 + A13*A21*A32 - A13*A22*A31)
            IA=Det*IA;
            
            # numero de veces que es corregido el valor en nodos que no son cebtro de parche
            listaparche2 = get_indexes(i,parcheesp2[:,0]) #lista de nodos que conectan con solo tres nodos, uno de ellos es i
            listaparche2 = listaparche2+get_indexes(i,parcheesp2[:,1])
            listaparche2 = listaparche2+get_indexes(i,parcheesp2[:,2])            
            listaparche1 = get_indexes(i,parcheesp1[:,0]) #lista de nodos que conectan con solo dos nodos, uno de ellos es i
            listaparche1 = listaparche1+get_indexes(i,parcheesp1[:,1])
            for k in listaparche2:
                repeticiones2[k,0]=repeticiones2[k,0]+1
            for k in listaparche1:
                repeticiones1[k,0]=repeticiones1[k,0]+1
             
            #calculo de derivadas en nodo i y nodos que no son centro de parche contiguos
            for j in range(s):
                vx=np.array([Bx[0,j],Bx[1,j],Bx[2,j]])
                ajx,bjx,cjx=IA@vx
                Ux[i*s+j]=ajx*mallado[0][i,0]+bjx*mallado[0][i,1]+cjx
                vy=np.array([By[0,j],By[1,j],By[2,j]])
                ajy,bjy,cjy=IA@vy
                Uy[i*s+j]=ajy*mallado[0][i,0]+bjy*mallado[0][i,1]+cjy
                 
                #caso particular de nodos que no son centro de parche
                for k in listaparche2: 
                    Ux[k*s+j]=Ux[k*s+j]+ajx*mallado[0][k,0]+bjx*mallado[0][k,1]+cjx
                    Uy[k*s+j]=Uy[k*s+j]+ajy*mallado[0][k,0]+bjy*mallado[0][k,1]+cjy
                        
                for k in listaparche1:
                    Ux[k*s+j]=Ux[k*s+j]+ajx*mallado[0][k,0]+bjx*mallado[0][k,1]+cjx
                    Uy[k*s+j]=Uy[k*s+j]+ajy*mallado[0][k,0]+bjy*mallado[0][k,1]+cjy                    
    
    #caso particular de nodos que no son centro de parche
    for i in listanodos2: 
        if repeticiones2[i,0]>0:
            for j in range(s):
                Ux[i*s+j]=Ux[i*s+j]/repeticiones2[i,0]
                Uy[i*s+j]=Uy[i*s+j]/repeticiones2[i,0]
        else:
            elem1=nodel[i,1]
            elem2=nodel[i,2]
            for j in range(s):
                Ux[i*s+j]=(tabla_dUdx[elem1,j]+tabla_dUdx[elem2,j])/2
                Uy[i*s+j]=(tabla_dUdy[elem1,j]+tabla_dUdy[elem2,j])/2
                
    for i in listanodos1:
        if repeticiones1[i,0]>0:
            for j in range(s):
                Ux[i*s+j]=Ux[i*s+j]/repeticiones1[i,0]
                Uy[i*s+j]=Uy[i*s+j]/repeticiones1[i,0]
        else:
            elem1=nodel[i,1]
            for j in range(s):
                Ux[i*s+j]=tabla_dUdx[elem1,j]
                Uy[i*s+j]=tabla_dUdy[elem1,j]
    
    return [Ux , Uy]


def flujo_y_derivs(mallado,s,U,t):   
    get_indexes = lambda x, xs: [i for (y, i) in zip(xs, range(len(xs))) if x == y]     
    
    Ux, Uy = derivadas(mallado, s, U)
    
    qx = np.zeros( (s*len(mallado[0])) )
    qy = np.zeros( (s*len(mallado[0])) )
    
    #calculo de flujo
    for i in range(len(mallado[0])):
        x=mallado[0][i,0]
        y=mallado[0][i,1]
                
        listaelem = get_indexes(i,mallado[2][:,0])
        listaelem = listaelem + get_indexes(i,mallado[2][:,1])
        listaelem = listaelem + get_indexes(i,mallado[2][:,2])
        
        dominio=mallado[2][listaelem[0],3]
        
        c11=Ecua_dif.EQ_c11(x,y,t,s,dominio)
        c12=Ecua_dif.EQ_c12(x,y,t,s,dominio)
        c21=Ecua_dif.EQ_c21(x,y,t,s,dominio)
        c22=Ecua_dif.EQ_c22(x,y,t,s,dominio)
        d1=Ecua_dif.EQ_d1(x,y,t,s,dominio)
        d2=Ecua_dif.EQ_d2(x,y,t,s,dominio)
        e1=Ecua_dif.EQ_e1(x,y,t,s,dominio)
        e2=Ecua_dif.EQ_e2(x,y,t,s,dominio)
        
        qx[(i*s):(i*s+s)]=-c11@Ux[(i*s):(i*s+s)]-c12@Uy[(i*s):(i*s+s)]-d1@U[(i*s):(i*s+s)]+e1
        qy[(i*s):(i*s+s)]=-c21@Ux[(i*s):(i*s+s)]-c22@Uy[(i*s):(i*s+s)]-d2@U[(i*s):(i*s+s)]+e2
        
            
    return [qx , qy , Ux , Uy]
            
    
 