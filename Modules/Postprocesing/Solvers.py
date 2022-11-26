# -*- coding: utf-8 -*-
"""
Created on Mon Oct 17 11:30:56 2022

@author: alberto.diaz
"""
import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import spsolve
from scipy.sparse import dok_matrix
from scipy.sparse.linalg import splu

def resuelve_sistema_estac(s,mallado,CF,Sistema,acond_CF):
    
    #F,Fi,K,Kii,Kc,Kci=Sistema

    lista_valorCF_Dirichlet , lista_DOF_Dirichlet , lista_DOF_sin_Dirichlet=acond_CF
    
    Di=spsolve(Sistema[2],Sistema[0]-Sistema[4]*lista_valorCF_Dirichlet)
    Di=csr_matrix.transpose(csr_matrix(Di))
    Fr=Sistema[3]*Di+Sistema[5]*lista_valorCF_Dirichlet-Sistema[1]
    
    D=np.zeros( (len(mallado[0])*s, 1) )
    for i in range(len(lista_DOF_sin_Dirichlet)):
        D[lista_DOF_sin_Dirichlet[i],0]=Di[i,0]
    for i in range(len(lista_DOF_Dirichlet)):
        D[lista_DOF_Dirichlet[i],0]=lista_valorCF_Dirichlet[i,0]
    
    Freac=dok_matrix((s*len(mallado[0]), 1), dtype=np.float64)
    for i in range(len(lista_DOF_Dirichlet)):
        Freac[lista_DOF_Dirichlet[i],0]=Fr[i,0]
    
    return [D , Freac]


def resuelve_sistema_trans1_B(s,mallado,CF,Sistema,acond_CF,tiempos,Uantes):
    #solo valido para pasos constantes, CF y coefs constantes
    #F,Fi,K,Kii,Kc,Kci,B,Bii,Bc,Bci=Sistema
    
    #guarda resultado ini    
    np.savetxt("U0.txt", Uantes)
    
    
    lista_valorCF_Dirichlet , lista_DOF_Dirichlet , lista_DOF_sin_Dirichlet=acond_CF
    Uantes2=Uantes[lista_DOF_sin_Dirichlet]
    # [h,rk]=lufact(B+deltat/2*K);
    deltat=tiempos[1]-tiempos[0] 
    MAT = splu(Sistema[6]+deltat/2*Sistema[2])
    VecF = Sistema[0]-Sistema[4]*lista_valorCF_Dirichlet
    
        
    for j in range(len(tiempos)-1):           
        Unuevo=MAT.solve(deltat*VecF+(Sistema[6]-deltat/2*Sistema[2])*Uantes2)        
        Uantes2=Unuevo
        for i in range(len(lista_DOF_sin_Dirichlet)):
            Uantes[lista_DOF_sin_Dirichlet[i],0]=Uantes2[i,0]
        for i in range(len(lista_DOF_Dirichlet)):
            Uantes[lista_DOF_Dirichlet[i],0]=lista_valorCF_Dirichlet[i,0]
        
        archivo="U"+str(j+1)+".txt"        
        np.savetxt(archivo, Uantes)
    
