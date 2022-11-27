# -*- coding: utf-8 -*-
"""
Created on Wed May 11 19:47:03 2022

@author: alberto.diaz
"""

import os
import re
import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse import csc_matrix
from scipy.sparse.linalg import spsolve
# import lectura_malla

import Modules.Postprocesing.CF_y_Valoresiniciales as CF_y_Valoresiniciales
#from lectura_malla import lectura_malla_COMSOL


import Modules.Postprocesing.Acondiciona_sistema as Acondiciona_sistema
import Modules.Postprocesing.Solvers as Solvers
from Modules.Postprocesing.Derivadas_Tri1 import flujo_y_derivs

def resolverEq(nodos, elemBor, tablaCon, dataPost):
    fisica=0 
    # print("DATA POST")
    # print(dataPost)
    # fisica es 0 si transferencia de calor
    # fisica es 1 si caso general
        
    s=1 # número de funciones incógnita
    if fisica==0:
        s=1 

    tiposolver=11
    # tiposolver es 0 si estacionario
    # tiposolver es 1* si transiente con coeficientes de ecua dif independientes de t,
    #               *=0 si A!=0 y B!=0
    #               *=1 si A=0 y B!=0
    #               *=2 si A!=0 y B=0
    # tiposolver es 2 si transiente con coeficientes de ecua dif dependientes de t,

    # mallado = lectura_malla.lectura_malla_COMSOL(); #Carlos
    mallado = [nodos, elemBor, tablaCon]
    # condiciones de frontera
    CF , acond_CF = CF_y_Valoresiniciales.asignayanalizaCF(s,mallado,dataPost)  #Carlos
    if tiposolver!=0:
        Vectini=CF_y_Valoresiniciales.valores_ini(s,mallado)
        tiempos=0.01*np.array(list(range(0,100)),dtype=np.float64) #Carlos
        

    ######################
    #Resolución
    ######################

    #Caso estacionario

    #listaDOF=Acondiciona_sistema.componentes_CFdesp(s,mallado,CF)
    #milista=Acondiciona_sistema.lista_DOF_Dirichlet_y_valor(s,mallado,CF)

    if tiposolver==0:  
        Sistema=Acondiciona_sistema.sistema_estac(s,mallado,CF,acond_CF)
        U , R = Solvers.resuelve_sistema_estac(s,mallado,CF,Sistema,acond_CF)
        del Sistema
        qx, qy, Ux, Uy = flujo_y_derivs(mallado, s, U, 0)
        np.savetxt("U.txt", U)
        np.savetxt("Ux.txt", Ux)
        np.savetxt("Uy.txt", Uy)   
        np.savetxt("qx.txt", qx)
        np.savetxt("qy.txt", qy)   
        

    if tiposolver==11:    
        Sistema = Acondiciona_sistema.sistema_trans1_B(s,mallado,CF,acond_CF)
        Solvers.resuelve_sistema_trans1_B(s,mallado,CF,Sistema,acond_CF,tiempos,Vectini)
        del Sistema
        # qx, qy, Ux, Uy = flujo_y_derivs(mallado, s, U, t)
        
    #Ecua_dif.EQ_a(0,0,0,s)

