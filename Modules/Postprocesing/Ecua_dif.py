# -*- coding: utf-8 -*-
"""
Created on Wed May 11 14:51:39 2022

@author: alberto.diaz
"""
import numpy as np
#global s

from Modules.Postprocesing.PostprocessingData import *

def EQ_a(x,y,t,s,dominio):
    resp=np.zeros( (s, s) ,dtype=np.float64)
    if dominio == 0:
        for i in range(0,s):
            resp[i][i]=0
    return(resp)

def EQ_b(x,y,t,s,dominio): #Carlos
    resp=np.zeros( (s, s) ,dtype=np.float64)
    if dominio == 0:
        for i in range(0,s): # en caso de transf de calor es rho*Cp
            resp[i][i]=0.01
    return(resp)

def EQ_c11(x,y,t,s,dominio): #Carlos
    resp=np.zeros( (s, s) ,dtype=np.float64)
    if dominio == 0:
        for i in range(0,s): # en caso de transf de calor es K11 (si isotropico K11=k)
            resp[i][i]=1
    return(resp)

def EQ_c12(x,y,t,s,dominio): #Carlos
    resp=np.zeros( (s, s) ,dtype=np.float64)
    if dominio == 0:
        for i in range(0,s): # en caso de transf de calor es K12 (si isotropico K12=0)
            resp[i][i]=0
    return(resp)

def EQ_c21(x,y,t,s,dominio): #Carlos
    resp=np.zeros( (s, s),dtype=np.float64 )
    if dominio == 0:
        for i in range(0,s): # en caso de transf de calor es K21 (si isotropico K21=0)
            resp[i][i]=0
    return(resp)

def EQ_c22(x,y,t,s,dominio): #Carlos
    resp=np.zeros( (s, s),dtype=np.float64 )
    if dominio == 0:
        for i in range(0,s): # en caso de transf de calor es K22 (si isotropico K22=k)
            resp[i][i]=1
    return(resp)

def EQ_d1(x,y,t,s,dominio):
    resp=np.zeros( (s, s),dtype=np.float64 )
    if dominio == 0:
        for i in range(0,s):
            resp[i][i]=0
    return(resp)

def EQ_d2(x,y,t,s,dominio):
    resp=np.zeros( (s, s) ,dtype=np.float64)
    if dominio == 0:
        for i in range(0,s):
            resp[i][i]=0
    return(resp)


def EQ_e1(x,y,t,s,dominio):
    resp=np.zeros((s, 1),dtype=np.float64)
    return(resp)

def EQ_e2(x,y,t,s,dominio):
    resp=np.zeros((s, 1),dtype=np.float64)
    return(resp)

def EQ_g1(x,y,t,s,dominio):
    resp=np.zeros( (s, s),dtype=np.float64 )
    for i in range(0,s):
        resp[i][i]=0
    return(resp)

def EQ_g2(x,y,t,s,dominio):
    resp=np.zeros( (s, s),dtype=np.float64 )
    for i in range(0,s):
        resp[i][i]=0
    return(resp)

def EQ_h(x,y,t,s,dominio):
    resp=np.zeros( (s, s),dtype=np.float64 )
    for i in range(0,s):
        resp[i][i]=0
    return(resp)

def EQ_f(x,y,t,s,dominio):
    resp=np.zeros((s,1),dtype=np.float64)            
    return(resp)