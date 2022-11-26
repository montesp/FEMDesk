# -*- codingww utf-8 -*-
"""
Created on Thu Oct  6 17f   25*       57 2022

@author: alberto.diaz
"""
import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse import dok_matrix

import Modules.Postprocesing.Matrices_ensambladas as Matrices_ensambladas

def delete_row_csr(mat, i): #works only for CSR format    
    n = mat.indptr[i+1] - mat.indptr[i]
    if n > 0:
        mat.data[mat.indptr[i]:-n] = mat.data[mat.indptr[i+1]:]
        mat.data = mat.data[:-n]
        mat.indices[mat.indptr[i]:-n] = mat.indices[mat.indptr[i+1]:]
        mat.indices = mat.indices[:-n]
    mat.indptr[i:-1] = mat.indptr[i+1:]
    mat.indptr[i:] -= n
    mat.indptr = mat.indptr[:-1]
    mat._shape = (mat._shape[0]-1, mat._shape[1])


def sistema_estac(s,mallado,CF,acond_CF):    
    F , K = Matrices_ensambladas.matrices_estacionario(s,mallado,CF)

    lista_valorCF_Dirichlet , lista_DOF_Dirichlet , lista_DOF_sin_Dirichlet=acond_CF
    
    Kc=K[:,lista_DOF_Dirichlet]
    K=K[:,lista_DOF_sin_Dirichlet] # en lugar de Ki debe ser K
    K=csr_matrix(K)
    Kc=csr_matrix(Kc)
    
    Kii= dok_matrix((len(lista_DOF_Dirichlet), len(lista_DOF_sin_Dirichlet)), dtype=np.float64)    
    
    for i in range(len(lista_DOF_Dirichlet)): #corregir 
        Kii[i,:]=K[lista_DOF_Dirichlet[i]-i,:]
        delete_row_csr(K, lista_DOF_Dirichlet[i]-i)
    #K es Kic         
    
    Kci= dok_matrix((len(lista_DOF_Dirichlet), len(lista_DOF_Dirichlet)), dtype=np.float64)        
    Fi= dok_matrix((len(lista_DOF_Dirichlet), 1),dtype = np.float64)
    for i in range(len(lista_DOF_Dirichlet)):
        Kci[i,:]=Kc[lista_DOF_Dirichlet[i]-i,:]
        delete_row_csr(Kc, lista_DOF_Dirichlet[i]-i)
        Fi[i,:]=F[lista_DOF_Dirichlet[i]-i,:]
        delete_row_csr(F, lista_DOF_Dirichlet[i]-i)
    #Kc es Kcc, F es Fc
      
    return [F,Fi,K,Kii,Kc,Kci]
    
    
def sistema_trans1_B(s,mallado,CF,acond_CF):   
    F , K , B = Matrices_ensambladas.matrices_transiente_B(0,s,mallado,CF)    
    
    lista_valorCF_Dirichlet , lista_DOF_Dirichlet , lista_DOF_sin_Dirichlet=acond_CF
    
    Kc=K[:,lista_DOF_Dirichlet]
    K=K[:,lista_DOF_sin_Dirichlet] # en lugar de Ki debe ser K
    K=csr_matrix(K)
    Kc=csr_matrix(Kc)
    
    Bc=B[:,lista_DOF_Dirichlet]
    B=B[:,lista_DOF_sin_Dirichlet] # en lugar de Ki debe ser K
    B=csr_matrix(B)
    Bc=csr_matrix(Bc)
        
    Kii= dok_matrix((len(lista_DOF_Dirichlet), len(lista_DOF_sin_Dirichlet)), dtype=np.float64)    
    Bii= dok_matrix((len(lista_DOF_Dirichlet), len(lista_DOF_sin_Dirichlet)), dtype=np.float64)    
        
    for i in range(len(lista_DOF_Dirichlet)): #corregir 
        Kii[i,:]=K[lista_DOF_Dirichlet[i]-i,:]
        delete_row_csr(K, lista_DOF_Dirichlet[i]-i)
        Bii[i,:]=B[lista_DOF_Dirichlet[i]-i,:]
        delete_row_csr(B, lista_DOF_Dirichlet[i]-i)       
    
    Kci= dok_matrix((len(lista_DOF_Dirichlet), len(lista_DOF_Dirichlet)), dtype=np.float64)        
    Bci= dok_matrix((len(lista_DOF_Dirichlet), len(lista_DOF_Dirichlet)), dtype=np.float64)        
    Fi= dok_matrix((len(lista_DOF_Dirichlet), 1),dtype = np.float64)
    for i in range(len(lista_DOF_Dirichlet)):
        Kci[i,:]=Kc[lista_DOF_Dirichlet[i]-i,:]        
        delete_row_csr(Kc, lista_DOF_Dirichlet[i]-i)
        Bci[i,:]=Bc[lista_DOF_Dirichlet[i]-i,:]
        delete_row_csr(Bc, lista_DOF_Dirichlet[i]-i)
        Fi[i,:]=F[lista_DOF_Dirichlet[i]-i,:]
        delete_row_csr(F, lista_DOF_Dirichlet[i]-i)
      
    return [F,Fi,K,Kii,Kc,Kci,B,Bii,Bc,Bci]
    
    

