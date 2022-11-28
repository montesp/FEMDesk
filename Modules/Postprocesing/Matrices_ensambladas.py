# -*- coding: utf-8 -*-
"""
Created on Thu Oct  6 13:34:47 2022

@author: alberto.diaz
"""
from scipy.sparse import dok_matrix
import numpy as np
import Modules.Postprocesing.Matrices_elementales as Matrices_elementales
from scipy.sparse import csc_matrix
from scipy.sparse import csr_matrix


def matrices_transiente_AB(t,s,mallado,CF):
    Nodos=mallado[0]
    Conectividad=mallado[2]
    matrizA=dok_matrix((s*len(Nodos), s*len(Nodos)), dtype=np.float64)
    matrizB=dok_matrix((s*len(Nodos), s*len(Nodos)), dtype=np.float64)
    matrizK=dok_matrix((s*len(Nodos), s*len(Nodos)), dtype=np.float64)
    vectorF=dok_matrix((s*len(Nodos), 1), dtype=np.float64)
    for i in range(len(Conectividad)):
        r1=Conectividad[i][0] #1er nodo del elemento i
        r2=Conectividad[i][1] #2o nodo del elemento i
        r3=Conectividad[i][2] #3er nodo del elemento i
        x1=Nodos[r1][0] #abscisas de estos nodos
        x2=Nodos[r2][0]
        x3=Nodos[r3][0]
        y1=Nodos[r1][1] #ordenadas de estos nodos
        y2=Nodos[r2][1]
        y3=Nodos[r3][1]
        
        x=[x1,x2,x3]
        y=[y1,y2,y3]
        
        
        detJ=(x2-x1)*(y3-y1)-(x3-x1)*(y2-y1);
        A_elem = Matrices_elementales.Ai_elemental(x, y, t, detJ, s , Conectividad[i,3])
        B_elem = Matrices_elementales.Bi_elemental(x, y, t, detJ, s , Conectividad[i,3])
        K_elem = Matrices_elementales.Ci_elemental(x, y, t, detJ, s , Conectividad[i,3])
        K_elem = K_elem + Matrices_elementales.di_elemental(x,y,t,s , Conectividad[i,3])
        K_elem = K_elem + Matrices_elementales.gi_elemental(x,y,t,s , Conectividad[i,3])
        K_elem = K_elem + Matrices_elementales.hi_elemental(x,y,t,detJ,s , Conectividad[i,3])
        F_elem = Matrices_elementales.Fi_elemental_dominio(x, y, t, detJ, s , Conectividad[i,3])
        for j in range(s):
            vectorF[r1*s+j , 0] = vectorF[r1*s+j , 0]+F_elem[j][0]
            vectorF[r2*s+j , 0] = vectorF[r2*s+j , 0]+F_elem[j+s][0]
            vectorF[r3*s+j , 0] = vectorF[r3*s+j , 0]+F_elem[j+2*s][0]
            for k in range(s):
                matrizA[r1*s+j , r1*s+k] = matrizA[r1*s+j , r1*s+k]+A_elem[j][k]
                matrizA[r1*s+j , r2*s+k] = matrizA[r1*s+j , r2*s+k]+A_elem[j][k+s]
                matrizA[r1*s+j , r3*s+k] = matrizA[r1*s+j , r3*s+k]+A_elem[j][k+2*s]
                matrizA[r2*s+j , r1*s+k] = matrizA[r2*s+j , r1*s+k]+A_elem[j+s][k]
                matrizA[r2*s+j , r2*s+k] = matrizA[r2*s+j , r2*s+k]+A_elem[j+s][k+s]
                matrizA[r2*s+j , r3*s+k] = matrizA[r2*s+j , r3*s+k]+A_elem[j+s][k+2*s]
                matrizA[r3*s+j , r1*s+k] = matrizA[r3*s+j , r1*s+k]+A_elem[j+2*s][k]
                matrizA[r3*s+j , r2*s+k] = matrizA[r3*s+j , r2*s+k]+A_elem[j+2*s][k+s]
                matrizA[r3*s+j , r3*s+k] = matrizA[r3*s+j , r3*s+k]+A_elem[j+2*s][k+2*s]
                matrizB[r1*s+j , r1*s+k] = matrizB[r1*s+j , r1*s+k]+B_elem[j][k]
                matrizB[r1*s+j , r2*s+k] = matrizB[r1*s+j , r2*s+k]+B_elem[j][k+s]
                matrizB[r1*s+j , r3*s+k] = matrizB[r1*s+j , r3*s+k]+B_elem[j][k+2*s]
                matrizB[r2*s+j , r1*s+k] = matrizB[r2*s+j , r1*s+k]+B_elem[j+s][k]
                matrizB[r2*s+j , r2*s+k] = matrizB[r2*s+j , r2*s+k]+B_elem[j+s][k+s]
                matrizB[r2*s+j , r3*s+k] = matrizB[r2*s+j , r3*s+k]+B_elem[j+s][k+2*s]
                matrizB[r3*s+j , r1*s+k] = matrizB[r3*s+j , r1*s+k]+B_elem[j+2*s][k]
                matrizB[r3*s+j , r2*s+k] = matrizB[r3*s+j , r2*s+k]+B_elem[j+2*s][k+s]
                matrizB[r3*s+j , r3*s+k] = matrizB[r3*s+j , r3*s+k]+B_elem[j+2*s][k+2*s]
                matrizK[r1*s+j , r1*s+k] = matrizK[r1*s+j , r1*s+k]+K_elem[j][k]
                matrizK[r1*s+j , r2*s+k] = matrizK[r1*s+j , r2*s+k]+K_elem[j][k+s]
                matrizK[r1*s+j , r3*s+k] = matrizK[r1*s+j , r3*s+k]+K_elem[j][k+2*s]
                matrizK[r2*s+j , r1*s+k] = matrizK[r2*s+j , r1*s+k]+K_elem[j+s][k]
                matrizK[r2*s+j , r2*s+k] = matrizK[r2*s+j , r2*s+k]+K_elem[j+s][k+s]
                matrizK[r2*s+j , r3*s+k] = matrizK[r2*s+j , r3*s+k]+K_elem[j+s][k+2*s]
                matrizK[r3*s+j , r1*s+k] = matrizK[r3*s+j , r1*s+k]+K_elem[j+2*s][k]
                matrizK[r3*s+j , r2*s+k] = matrizK[r3*s+j , r2*s+k]+K_elem[j+2*s][k+s]
                matrizK[r3*s+j , r3*s+k] = matrizK[r3*s+j , r3*s+k]+K_elem[j+2*s][k+2*s]
                
    vectorF=vectorF_conCFflujo(vectorF,s,mallado,CF)
    matrizK=matrizK_conCFflujo(matrizK,s,mallado,CF)
    # matrizA=csr_matrix(matrizA)
    # matrizB=csr_matrix(matrizB)
    # matrizK=csr_matrix(matrizK)
    
    matrizA=csc_matrix(matrizA)
    matrizB=csc_matrix(matrizB)
    matrizK=csc_matrix(matrizK)
    vectorF=csr_matrix(vectorF)
    
    return [vectorF,matrizK,matrizA,matrizB]


def matrices_transiente_A(t,s,mallado,CF):
    Nodos=mallado[0]
    Conectividad=mallado[2]
    matrizA=dok_matrix((s*len(Nodos), s*len(Nodos)), dtype=np.float64)
    matrizK=dok_matrix((s*len(Nodos), s*len(Nodos)), dtype=np.float64)
    vectorF=dok_matrix((s*len(Nodos), 1), dtype=np.float64)
    for i in range(len(Conectividad)):
        r1=Conectividad[i][0] #1er nodo del elemento i
        r2=Conectividad[i][1] #2o nodo del elemento i
        r3=Conectividad[i][2] #3er nodo del elemento i
        x1=Nodos[r1][0] #abscisas de estos nodos
        x2=Nodos[r2][0]
        x3=Nodos[r3][0]
        y1=Nodos[r1][1] #ordenadas de estos nodos
        y2=Nodos[r2][1]
        y3=Nodos[r3][1]
        
        x=[x1,x2,x3]
        y=[y1,y2,y3]
        
        detJ=(x2-x1)*(y3-y1)-(x3-x1)*(y2-y1);
        A_elem = Matrices_elementales.Ai_elemental(x, y, t, detJ, s , Conectividad[i,3])
        K_elem = Matrices_elementales.Ci_elemental(x, y, t, detJ, s , Conectividad[i,3])
        K_elem = K_elem + Matrices_elementales.di_elemental(x,y,t,s , Conectividad[i,3])
        K_elem = K_elem + Matrices_elementales.gi_elemental(x,y,t,s , Conectividad[i,3])
        K_elem = K_elem + Matrices_elementales.hi_elemental(x,y,t,detJ,s , Conectividad[i,3])
        F_elem = Matrices_elementales.Fi_elemental_dominio(x, y, t, detJ, s , Conectividad[i,3])
        for j in range(s):
            vectorF[r1*s+j , 0] = vectorF[r1*s+j , 0]+F_elem[j][0]
            vectorF[r2*s+j , 0] = vectorF[r2*s+j , 0]+F_elem[j+s][0]
            vectorF[r3*s+j , 0] = vectorF[r3*s+j , 0]+F_elem[j+2*s][0]
            for k in range(s):
                matrizA[r1*s+j , r1*s+k] = matrizA[r1*s+j , r1*s+k]+A_elem[j][k]
                matrizA[r1*s+j , r2*s+k] = matrizA[r1*s+j , r2*s+k]+A_elem[j][k+s]
                matrizA[r1*s+j , r3*s+k] = matrizA[r1*s+j , r3*s+k]+A_elem[j][k+2*s]
                matrizA[r2*s+j , r1*s+k] = matrizA[r2*s+j , r1*s+k]+A_elem[j+s][k]
                matrizA[r2*s+j , r2*s+k] = matrizA[r2*s+j , r2*s+k]+A_elem[j+s][k+s]
                matrizA[r2*s+j , r3*s+k] = matrizA[r2*s+j , r3*s+k]+A_elem[j+s][k+2*s]
                matrizA[r3*s+j , r1*s+k] = matrizA[r3*s+j , r1*s+k]+A_elem[j+2*s][k]
                matrizA[r3*s+j , r2*s+k] = matrizA[r3*s+j , r2*s+k]+A_elem[j+2*s][k+s]
                matrizA[r3*s+j , r3*s+k] = matrizA[r3*s+j , r3*s+k]+A_elem[j+2*s][k+2*s]
                matrizK[r1*s+j , r1*s+k] = matrizK[r1*s+j , r1*s+k]+K_elem[j][k]
                matrizK[r1*s+j , r2*s+k] = matrizK[r1*s+j , r2*s+k]+K_elem[j][k+s]
                matrizK[r1*s+j , r3*s+k] = matrizK[r1*s+j , r3*s+k]+K_elem[j][k+2*s]
                matrizK[r2*s+j , r1*s+k] = matrizK[r2*s+j , r1*s+k]+K_elem[j+s][k]
                matrizK[r2*s+j , r2*s+k] = matrizK[r2*s+j , r2*s+k]+K_elem[j+s][k+s]
                matrizK[r2*s+j , r3*s+k] = matrizK[r2*s+j , r3*s+k]+K_elem[j+s][k+2*s]
                matrizK[r3*s+j , r1*s+k] = matrizK[r3*s+j , r1*s+k]+K_elem[j+2*s][k]
                matrizK[r3*s+j , r2*s+k] = matrizK[r3*s+j , r2*s+k]+K_elem[j+2*s][k+s]
                matrizK[r3*s+j , r3*s+k] = matrizK[r3*s+j , r3*s+k]+K_elem[j+2*s][k+2*s]
       
    # matrizA=csr_matrix(matrizA)
    # matrizB=csr_matrix(matrizB)
    # matrizK=csr_matrix(matrizK)
    vectorF=vectorF_conCFflujo(vectorF,s,mallado,CF)
    matrizK=matrizK_conCFflujo(matrizK,s,mallado,CF)
    
    matrizA=csc_matrix(matrizA)
    matrizK=csc_matrix(matrizK)
    vectorF=csr_matrix(vectorF)
    
    return [vectorF,matrizK,matrizA]


def matrices_transiente_B(t,s,mallado,CF):
    Nodos=mallado[0]
    Conectividad=mallado[2]
    matrizB=dok_matrix((s*len(Nodos), s*len(Nodos)), dtype=np.float64)
    matrizK=dok_matrix((s*len(Nodos), s*len(Nodos)), dtype=np.float64)
    vectorF=dok_matrix((s*len(Nodos), 1), dtype=np.float64)
    for i in range(len(Conectividad)):
        r1=Conectividad[i][0] #1er nodo del elemento i
        r2=Conectividad[i][1] #2o nodo del elemento i
        r3=Conectividad[i][2] #3er nodo del elemento i
        x1=Nodos[r1][0] #abscisas de estos nodos
        x2=Nodos[r2][0]
        x3=Nodos[r3][0]
        y1=Nodos[r1][1] #ordenadas de estos nodos
        y2=Nodos[r2][1]
        y3=Nodos[r3][1]
        
        x=[x1,x2,x3]
        y=[y1,y2,y3]
        
        detJ=(x2-x1)*(y3-y1)-(x3-x1)*(y2-y1);
        B_elem = Matrices_elementales.Bi_elemental(x, y, t, detJ, s , Conectividad[i,3])
        K_elem = Matrices_elementales.Ci_elemental(x, y, t, detJ, s , Conectividad[i,3])
        K_elem = K_elem + Matrices_elementales.di_elemental(x,y,t,s , Conectividad[i,3])
        K_elem = K_elem + Matrices_elementales.gi_elemental(x,y,t,s , Conectividad[i,3])
        K_elem = K_elem + Matrices_elementales.hi_elemental(x,y,t,detJ,s , Conectividad[i,3])
        F_elem = Matrices_elementales.Fi_elemental_dominio(x, y, t, detJ, s , Conectividad[i,3])
        for j in range(s):
            vectorF[r1*s+j , 0] = vectorF[r1*s+j , 0]+F_elem[j][0]
            vectorF[r2*s+j , 0] = vectorF[r2*s+j , 0]+F_elem[j+s][0]
            vectorF[r3*s+j , 0] = vectorF[r3*s+j , 0]+F_elem[j+2*s][0]
            for k in range(s):
                matrizB[r1*s+j , r1*s+k] = matrizB[r1*s+j , r1*s+k]+B_elem[j][k]
                matrizB[r1*s+j , r2*s+k] = matrizB[r1*s+j , r2*s+k]+B_elem[j][k+s]
                matrizB[r1*s+j , r3*s+k] = matrizB[r1*s+j , r3*s+k]+B_elem[j][k+2*s]
                matrizB[r2*s+j , r1*s+k] = matrizB[r2*s+j , r1*s+k]+B_elem[j+s][k]
                matrizB[r2*s+j , r2*s+k] = matrizB[r2*s+j , r2*s+k]+B_elem[j+s][k+s]
                matrizB[r2*s+j , r3*s+k] = matrizB[r2*s+j , r3*s+k]+B_elem[j+s][k+2*s]
                matrizB[r3*s+j , r1*s+k] = matrizB[r3*s+j , r1*s+k]+B_elem[j+2*s][k]
                matrizB[r3*s+j , r2*s+k] = matrizB[r3*s+j , r2*s+k]+B_elem[j+2*s][k+s]
                matrizB[r3*s+j , r3*s+k] = matrizB[r3*s+j , r3*s+k]+B_elem[j+2*s][k+2*s]
                matrizK[r1*s+j , r1*s+k] = matrizK[r1*s+j , r1*s+k]+K_elem[j][k]
                matrizK[r1*s+j , r2*s+k] = matrizK[r1*s+j , r2*s+k]+K_elem[j][k+s]
                matrizK[r1*s+j , r3*s+k] = matrizK[r1*s+j , r3*s+k]+K_elem[j][k+2*s]
                matrizK[r2*s+j , r1*s+k] = matrizK[r2*s+j , r1*s+k]+K_elem[j+s][k]
                matrizK[r2*s+j , r2*s+k] = matrizK[r2*s+j , r2*s+k]+K_elem[j+s][k+s]
                matrizK[r2*s+j , r3*s+k] = matrizK[r2*s+j , r3*s+k]+K_elem[j+s][k+2*s]
                matrizK[r3*s+j , r1*s+k] = matrizK[r3*s+j , r1*s+k]+K_elem[j+2*s][k]
                matrizK[r3*s+j , r2*s+k] = matrizK[r3*s+j , r2*s+k]+K_elem[j+2*s][k+s]
                matrizK[r3*s+j , r3*s+k] = matrizK[r3*s+j , r3*s+k]+K_elem[j+2*s][k+2*s]
       
    # matrizA=csr_matrix(matrizA)
    # matrizB=csr_matrix(matrizB)
    # matrizK=csr_matrix(matrizK)
    vectorF=vectorF_conCFflujo(vectorF,s,mallado,CF)
    matrizK=matrizK_conCFflujo(matrizK,s,mallado,CF)
    
    matrizB=csc_matrix(matrizB)
    matrizK=csc_matrix(matrizK)
    vectorF=csr_matrix(vectorF)
    
    return [vectorF,matrizK,matrizB]


def matrices_estacionario(s,mallado,CF, heatConvection):
    Nodos=mallado[0]
    Conectividad=mallado[2]    
    matrizK=dok_matrix((s*len(Nodos), s*len(Nodos)), dtype=np.float64)
    vectorF=dok_matrix((s*len(Nodos), 1), dtype=np.float64)
    t=0
    for i in range(len(Conectividad)):
        r1=Conectividad[i][0] #1er nodo del elemento i
        r2=Conectividad[i][1] #2o nodo del elemento i
        r3=Conectividad[i][2] #3er nodo del elemento i
        x1=Nodos[r1][0] #abscisas de estos nodos
        x2=Nodos[r2][0]
        x3=Nodos[r3][0]
        y1=Nodos[r1][1] #ordenadas de estos nodos
        y2=Nodos[r2][1]
        y3=Nodos[r3][1]
        
        x=[x1,x2,x3]
        y=[y1,y2,y3]
        
        detJ=(x2-x1)*(y3-y1)-(x3-x1)*(y2-y1);        
        K_elem = Matrices_elementales.Ci_elemental(x, y, t, detJ, s , Conectividad[i,3], heatConvection)
        K_elem = K_elem + Matrices_elementales.di_elemental(x,y,t,s , Conectividad[i,3])
        K_elem = K_elem + Matrices_elementales.gi_elemental(x,y,t,s , Conectividad[i,3])
        K_elem = K_elem + Matrices_elementales.hi_elemental(x,y,t,detJ,s , Conectividad[i,3])
        F_elem = Matrices_elementales.Fi_elemental_dominio(x, y, t, detJ, s , Conectividad[i,3])
        for j in range(s):
            vectorF[r1*s+j , 0] = vectorF[r1*s+j , 0]+F_elem[j][0]
            vectorF[r2*s+j , 0] = vectorF[r2*s+j , 0]+F_elem[j+s][0]
            vectorF[r3*s+j , 0] = vectorF[r3*s+j , 0]+F_elem[j+2*s][0]
            for k in range(s):
                matrizK[r1*s+j , r1*s+k] = matrizK[r1*s+j , r1*s+k]+K_elem[j][k]
                matrizK[r1*s+j , r2*s+k] = matrizK[r1*s+j , r2*s+k]+K_elem[j][k+s]
                matrizK[r1*s+j , r3*s+k] = matrizK[r1*s+j , r3*s+k]+K_elem[j][k+2*s]
                matrizK[r2*s+j , r1*s+k] = matrizK[r2*s+j , r1*s+k]+K_elem[j+s][k]
                matrizK[r2*s+j , r2*s+k] = matrizK[r2*s+j , r2*s+k]+K_elem[j+s][k+s]
                matrizK[r2*s+j , r3*s+k] = matrizK[r2*s+j , r3*s+k]+K_elem[j+s][k+2*s]
                matrizK[r3*s+j , r1*s+k] = matrizK[r3*s+j , r1*s+k]+K_elem[j+2*s][k]
                matrizK[r3*s+j , r2*s+k] = matrizK[r3*s+j , r2*s+k]+K_elem[j+2*s][k+s]
                matrizK[r3*s+j , r3*s+k] = matrizK[r3*s+j , r3*s+k]+K_elem[j+2*s][k+2*s]
       
    # matrizA=csr_matrix(matrizA)
    # matrizB=csr_matrix(matrizB)
    # matrizK=csr_matrix(matrizK)
    vectorF=vectorF_conCFflujo(vectorF,s,mallado,CF)
    matrizK=matrizK_conCFflujo(matrizK,s,mallado,CF)
    
    matrizK=csc_matrix(matrizK)
    vectorF=csr_matrix(vectorF)

    return [vectorF,matrizK]     

def vectorF_conCFflujo(vectorF,s,mallado,CF):
    for i in range(len(mallado[1])):
        Nodo1 = mallado[1][i][0]
        Nodo2 = mallado[1][i][1]
        dominio = mallado[1][i][2]
        borde = mallado[1][i][3]
        
        vectflujodato1=np.zeros(s)
        vectflujodato2=np.zeros(s)
        for j in range(s):
            if CF[0][borde][j]: #CF[0] contiene el tipo de CF, True si sobre flujo
                vectflujodato1[j]=CF[1][borde][j]  #CF[1] contiene el valor de CF
                vectflujodato2[j]=CF[1][borde][j]
        
        x1 = mallado[0][Nodo1][0]
        x2 = mallado[0][Nodo2][0]
        y1 = mallado[0][Nodo1][1]
        y2 = mallado[0][Nodo2][1]
        longitud=pow(pow(x1-x2,2)+pow(y1-y2,2),0.5)        
        
        vectCF1 = -longitud/6*(2*vectflujodato1+vectflujodato2)
        vectCF2 = -longitud/6*(vectflujodato1+2*vectflujodato2)
        
        for j in range(s):
            vectorF[Nodo1*s+j , 0] = vectorF[Nodo1*s+j , 0] + vectCF1[j]
            vectorF[Nodo2*s+j , 0] = vectorF[Nodo2*s+j , 0] + vectCF2[j]
            
    return vectorF

def matrizK_conCFflujo(matrizK,s,mallado,CF):
    indicesnonulos=np.nonzero(CF[2])
    listafilasnonulo=list(set(list(indicesnonulos[0])))
    if list(listafilasnonulo): #en caso de que haya bordes con absorción
        # listabordes=[]
        # for i in range(listafilasnonulo):
        #     listabordes+=[math.floor(listafilasnonulo[i]/s)]
        # listabordes=list(set(listabordes))
        
        for i in range(len(mallado[1])): #i es el numero de elemento de borde
            Nodo1 = mallado[1][i][0]
            Nodo2 = mallado[1][i][1]
            dominio = mallado[1][i][2]
            borde = mallado[1][i][3] #éste es el número de borde
            
            x1 = mallado[0][Nodo1][0]
            x2 = mallado[0][Nodo2][0]
            y1 = mallado[0][Nodo1][1]
            y2 = mallado[0][Nodo2][1]
            longitud=pow(pow(x1-x2,2)+pow(y1-y2,2),0.5)                    
            matrizbeta=longitud*CF[2][(borde*s):(borde*s+s),:] #es una matriz s*s
            
            for j in range(s):
                for k in range(s):
                    matrizK[Nodo1*s+j , Nodo1*s+k ]+=1/3*matrizbeta[j,k]
                    matrizK[Nodo1*s+j , Nodo2*s+k ]+=1/6*matrizbeta[j,k]
                    matrizK[Nodo2*s+j , Nodo1*s+k ]+=1/6*matrizbeta[j,k]
                    matrizK[Nodo2*s+j , Nodo2*s+k ]+=1/3*matrizbeta[j,k]
            # matrizK[(Nodo1*s):(Nodo1*s+s) , (Nodo1*s):(Nodo1*s+s) ]+=1/3*matrizbeta
            # matrizK[(Nodo1*s):(Nodo1*s+s) , (Nodo2*s):(Nodo2*s+s) ]+=1/6*matrizbeta
            # matrizK[(Nodo2*s):(Nodo2*s+s) , (Nodo1*s):(Nodo1*s+s) ]+=1/6*matrizbeta
            # matrizK[(Nodo2*s):(Nodo2*s+s) , (Nodo2*s):(Nodo2*s+s) ]+=1/3*matrizbeta
        
    return matrizK