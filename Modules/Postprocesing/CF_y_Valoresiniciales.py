# -*- coding: utf-8 -*-
"""
Created on Wed Oct 12 10:28:16 2022

@author: alberto.diaz
"""
import numpy as np
from scipy.sparse import dok_matrix
from scipy.sparse import csr_matrix
from scipy import sparse
from Modules.Postprocesing.Postprocessing import *

# ConditionsCF = []


def creacionCF(s,mallado, datos=None):
    # newValues = DataPost.getCoefficent()
    datosA = datos[0]
    # numbordes=max(mallado[1][:,3])+1
    numbordes = len(datosA[0])

    tipoCF = datosA[0]
    tipoCF = [[val] for val in tipoCF]
    print("tipo cf")
    print(tipoCF)
    #Carlos
    #inicializado con CF sobre flujo, todo en True
    #En valor CF, las primeras s columnas son el flujo entrante, las otras s son términos de absorción de pared
    valorCF=datosA[1]
    valorCF=[[val] for val in valorCF]
    print("valor cf")
    print(valorCF)
    #inicializado con cero flujo, cero absorción de pared
    matrizbeta = datosA[2]
    matrizbeta = [[val] for val in matrizbeta]
    print("Matriz beta")
    print(matrizbeta)
    # matrizbeta=dok_matrix((numbordes*s, s), dtype=np.float64) #Carlos pendiente
    #absorción, inicializada cero absorción de pared
    # se lee por paquetes de s filas, las primeras s filas son para el primer borde
    
    # particularidad borde 0 bloqueado
    # for i in range(s):
    #     tipoCF[0][i]=False
    #     valorCF[0][i]=0
    
    # particularidad borde 3 bloqueado algunas componentes
    # tipoCF[3][0]=False
    # valorCF[3][0]=1
    
    #particularidad borde 2 flujo entrante
    # valorCF[2][0]=1000
    
    #particularidad borde 3 flujo entrante
    # valorCF[3][0]=1000
    
    #particularidad borde 2 conveccion
    # valorCF[2][0]=100 #temp aire*h
    # matrizbeta[2,0]=1  #h
    #en caso gral, valorCF es g  y matrizbeta es q
    #se cambia de signo porque se captura flujo entrante
    
    for k in range(numbordes):
        for i in range(s):
            if tipoCF[k][i]:
                valorCF[k][i]=-valorCF[k][i]                
    
    return [tipoCF,valorCF,matrizbeta]


def valores_ini(s,mallado): 
    Nodos=mallado[0]
    vectorini=np.zeros( (s*len(Nodos),1) , dtype=np.float64)#Carlos
    print("Valores iniciales")
    print(vectorini)
    return(vectorini)


def lista_DOF_Dirichlet_y_valor(s,mallado,CF):
    get_indexes = lambda x, xs: [i for (y, i) in zip(xs, range(len(xs))) if x == y] 
    lista_bordes_CFDirichlet = []
    for i in range(len(CF[0])): #len(CF[0]) es el numero de bordes
        if not min(CF[0][i]): # se impone Dirichlet en alguna componente de u en ese borde
            lista_bordes_CFDirichlet.append(i)
            
    lista_elem_Dirichlet=[] #construye la lista de elementos que tienen CF de Dirichlet en alguna componente
    for i in lista_bordes_CFDirichlet:
        listaelemborde = get_indexes(i,mallado[1][:,3])
        lista_elem_Dirichlet=lista_elem_Dirichlet+listaelemborde
    lista_elem_Dirichlet.sort()
   
    mallado_borde_Dirichlet=np.empty((len(lista_elem_Dirichlet),4),dtype=int)
    count=0
    lista_nodos_CFDirichlet = []
    lista_DOF_Dirichlet = []
    lista_valorCF_Dirichlet = []
    for i in lista_elem_Dirichlet:
        for j in range(4):
            mallado_borde_Dirichlet[count][j]=mallado[1][i,j]
        lista_nodos_CFDirichlet = lista_nodos_CFDirichlet+[mallado_borde_Dirichlet[count][0],mallado_borde_Dirichlet[count][1]]
        for j in range(s):
            if not CF[0][mallado[1][i,3]][j]:
                lista_DOF_Dirichlet = lista_DOF_Dirichlet + [mallado[1][i,0]*s+j , mallado[1][i,1]*s+j]
                lista_valorCF_Dirichlet = lista_valorCF_Dirichlet + [ CF[1][mallado[1][i,3]][j] , CF[1][mallado[1][i,3]][j] ]
        count=count+1
            
    lista_DOF_repetidos = [idx for idx, item in enumerate(lista_DOF_Dirichlet) if item in lista_DOF_Dirichlet[:idx]]
    for i in lista_DOF_repetidos:
        lista_DOF_Dirichlet[i]=-1  # se pone -1 si es un repetido
    
    lista_DOF=[]  ## en esta rutina se guardan solo los no repetidos
    lista_valor=[]  
    for i in range(len(lista_DOF_Dirichlet)):
        if lista_DOF_Dirichlet[i]!=-1:
            lista_DOF=lista_DOF+[lista_DOF_Dirichlet[i]]
            lista_valor=lista_valor+[lista_valorCF_Dirichlet[i]]            
            
    
    # ordena lista_DOF y acomoda lista_valor segun ese orden
    n=len(lista_DOF)
    for i in range(n-1):        
        minimo=min(lista_DOF[i:n])  
        num=lista_DOF.index(minimo)
        respaldo=lista_DOF[i]
        lista_DOF[i]=lista_DOF[num]
        lista_DOF[num]=respaldo
        respaldo=lista_valor[i]
        lista_valor[i]=lista_valor[num]
        lista_valor[num]=respaldo
       
    lista_DOF_Dirichlet = lista_DOF   
    del lista_DOF
    lista_valor=sparse.csr_matrix(np.array(lista_valor)) 
    lista_valorCF_Dirichlet=lista_valor
    del lista_valor
        
    lista_DOF_sin_Dirichlet=list(range(len(mallado[0])*s))
    for i in lista_DOF_Dirichlet:
        lista_DOF_sin_Dirichlet.remove(i)
        
    lista_valorCF_Dirichlet=csr_matrix.transpose(lista_valorCF_Dirichlet)
    
    return [lista_valorCF_Dirichlet , lista_DOF_Dirichlet , lista_DOF_sin_Dirichlet]


def asignayanalizaCF(s,mallado, datos=None):
    CF=creacionCF(s,mallado, datos)
    acond_CF=lista_DOF_Dirichlet_y_valor(s,mallado,CF)
    
    return [CF , acond_CF]




    