# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 13:50:44 2022

@author: alberto.diaz
"""
import numpy as np
import Modules.Postprocesing.Ecua_dif as Ecua_dif


def Ai_elemental(x,y,t,detJ,s,dominio):
#el resultado es una matriz local 3s*3s, el instante valt
#det J es el determinante    
    a_r1=Ecua_dif.EQ_a(x[0],y[0],t,s,dominio)
    a_r2=Ecua_dif.EQ_a(x[1],y[1],t,s,dominio)
    a_r3=Ecua_dif.EQ_a(x[2],y[2],t,s,dominio)
    
    r=np.block([
        [6*a_r1+2*a_r2+2*a_r3 , 2*a_r1+2*a_r2+a_r3 , 2*a_r1+a_r2+2*a_r3],
        [2*a_r1+2*a_r2+a_r3 , 2*a_r1+6*a_r2+2*a_r3 , a_r1+2*a_r2+2*a_r3],
        [2*a_r1+a_r2+2*a_r3 , a_r1+2*a_r2+2*a_r3 , 2*a_r1+2*a_r2+6*a_r3]
        ])
    r=detJ/120*r
    
    return(r)


def Bi_elemental(x,y,t,detJ,s,dominio):
#el resultado es una matriz local 3s*3s, el instante valt
#det J es el determinante    
    b_r1=Ecua_dif.EQ_b(x[0],y[0],t,s,dominio)
    b_r2=Ecua_dif.EQ_b(x[1],y[1],t,s,dominio)
    b_r3=Ecua_dif.EQ_b(x[2],y[2],t,s,dominio)
    
    r=np.block([
        [6*b_r1+2*b_r2+2*b_r3 , 2*b_r1+2*b_r2+b_r3 , 2*b_r1+b_r2+2*b_r3],
        [2*b_r1+2*b_r2+b_r3 , 2*b_r1+6*b_r2+2*b_r3 , b_r1+2*b_r2+2*b_r3],
        [2*b_r1+b_r2+2*b_r3 , b_r1+2*b_r2+2*b_r3 , 2*b_r1+2*b_r2+6*b_r3]
        ])
    
    r=detJ/120*r
    
    return(r)


def Ci_elemental(x,y,t,detJ,s,dominio, heatConvection):
#el resultado es una matriz local 3s*3s, el instante valt
#det J es el determinante    
    c11_r1=Ecua_dif.EQ_c11(x[0],y[0],t,s,dominio, heatConvection[0][0])
    c11_r2=Ecua_dif.EQ_c11(x[1],y[1],t,s,dominio, heatConvection[0][0])
    c11_r3=Ecua_dif.EQ_c11(x[2],y[2],t,s,dominio, heatConvection[0][0])
    
    c12_r1=Ecua_dif.EQ_c12(x[0],y[0],t,s,dominio, heatConvection[0][1])
    c12_r2=Ecua_dif.EQ_c12(x[1],y[1],t,s,dominio, heatConvection[0][1])
    c12_r3=Ecua_dif.EQ_c12(x[2],y[2],t,s,dominio, heatConvection[0][1])
    
    c21_r1=Ecua_dif.EQ_c21(x[0],y[0],t,s,dominio, heatConvection[0][2])
    c21_r2=Ecua_dif.EQ_c21(x[1],y[1],t,s,dominio, heatConvection[0][2])
    c21_r3=Ecua_dif.EQ_c21(x[2],y[2],t,s,dominio, heatConvection[0][2])
    
    c22_r1=Ecua_dif.EQ_c22(x[0],y[0],t,s,dominio, heatConvection[0][3])
    c22_r2=Ecua_dif.EQ_c22(x[1],y[1],t,s,dominio, heatConvection[0][3])
    c22_r3=Ecua_dif.EQ_c22(x[2],y[2],t,s,dominio, heatConvection[0][3])
    
    c11m=c11_r1+c11_r2+c11_r3
    c12m=c12_r1+c12_r2+c12_r3
    c21m=c21_r1+c21_r2+c21_r3
    c22m=c22_r1+c22_r2+c22_r3
    
    r=np.block([
        [pow(y[1]-y[2],2)*c11m , -(y[0]-y[2])*(y[1]-y[2])*c11m , (y[0]-y[1])*(y[1]-y[2])*c11m],
        [-(y[0]-y[2])*(y[1]-y[2])*c11m , pow(y[0]-y[2],2)*c11m , -(y[0]-y[1])*(y[0]-y[2])*c11m],
        [(y[0]-y[1])*(y[1]-y[2])*c11m , -(y[0]-y[1])*(y[0]-y[2])*c11m , pow(y[0]-y[1],2)*c11m]
        ])
      
    r=r+np.block([
        [-(x[1]-x[2])*(y[1]-y[2])*c12m , (x[0]-x[2])*(y[1]-y[2])*c12m , -(x[0]-x[1])*(y[1]-y[2])*c12m],
        [(x[1]-x[2])*(y[0]-y[2])*c12m , -(x[0]-x[2])*(y[0]-y[2])*c12m , (x[0]-x[1])*(y[0]-y[2])*c12m],
        [-(x[1]-x[2])*(y[0]-y[1])*c12m , (x[0]-x[2])*(y[0]-y[1])*c12m , -(x[0]-x[1])*(y[0]-y[1])*c12m]
        ])
      
    r=r+np.block([
        [-(x[1]-x[2])*(y[1]-y[2])*c21m , (x[1]-x[2])*(y[0]-y[2])*c21m , -(x[1]-x[2])*(y[0]-y[1])*c21m],
        [(x[0]-x[2])*(y[1]-y[2])*c21m , -(x[0]-x[2])*(y[0]-y[2])*c21m , (x[0]-x[2])*(y[0]-y[1])*c21m],
        [-(x[0]-x[1])*(y[1]-y[2])*c21m , (x[0]-x[1])*(y[0]-y[2])*c21m , -(x[0]-x[1])*(y[0]-y[1])*c21m]
        ])
       
    r=r+np.block([
        [pow(x[1]-x[2],2)*c22m , -(x[1]-x[2])*(x[0]-x[2])*c22m , (x[1]-x[2])*(x[0]-x[1])*c22m],
        [-(x[0]-x[2])*(x[1]-x[2])*c22m , pow(x[0]-x[2],2)*c22m , -(x[0]-x[2])*(x[0]-x[1])*c22m],
        [(x[0]-x[1])*(x[1]-x[2])*c22m , -(x[0]-x[1])*(x[0]-x[2])*c22m , pow(x[0]-x[1],2)*c22m]
       ])

    r=r/detJ/6
    
    return(r)


def di_elemental(x,y,t,s,dominio):
#el resultado es una matriz local 3s*3s, el instante valt    
    d1_r1=Ecua_dif.EQ_d1(x[0],y[0],t,s,dominio)
    d1_r2=Ecua_dif.EQ_d1(x[1],y[1],t,s,dominio)
    d1_r3=Ecua_dif.EQ_d1(x[2],y[2],t,s,dominio)
    
    d2_r1=Ecua_dif.EQ_d2(x[0],y[0],t,s,dominio)
    d2_r2=Ecua_dif.EQ_d2(x[1],y[1],t,s,dominio)
    d2_r3=Ecua_dif.EQ_d2(x[2],y[2],t,s,dominio)
    
    dcol1=2*d1_r1+d1_r2+d1_r3;
    dcol2=d1_r1+2*d1_r2+d1_r3;
    dcol3=d1_r1+d1_r2+2*d1_r3;
    
    r=np.block([
        [(y[1]-y[2])*dcol1 , (y[1]-y[2])*dcol2 , (y[1]-y[2])*dcol3],
        [(y[2]-y[0])*dcol1 , (y[2]-y[0])*dcol2 , (y[2]-y[0])*dcol3],
        [(y[0]-y[1])*dcol1 , (y[0]-y[1])*dcol2 , (y[0]-y[1])*dcol3]
        ])
        
    dcol1=2*d2_r1+d2_r2+d2_r3;
    dcol2=d2_r1+2*d2_r2+d2_r3;
    dcol3=d2_r1+d2_r2+2*d2_r3;
    
    r=r+np.block([
        [(x[2]-x[1])*dcol1 , (x[2]-x[1])*dcol2 , (x[2]-x[1])*dcol3],
        [(x[0]-x[2])*dcol1 , (x[0]-x[2])*dcol2 , (x[0]-x[2])*dcol3],
        [(x[1]-x[0])*dcol1 , (x[1]-x[0])*dcol2 , (x[1]-x[0])*dcol3]
        ])
    
    r=r/24
    
    return(r)


def gi_elemental(x,y,t,s,dominio):
#el resultado es una matriz local 3s*3s, el instante valt  
    g1_r1=Ecua_dif.EQ_g1(x[0],y[0],t,s,dominio)
    g1_r2=Ecua_dif.EQ_g1(x[1],y[1],t,s,dominio)
    g1_r3=Ecua_dif.EQ_g1(x[2],y[2],t,s,dominio)
    
    g2_r1=Ecua_dif.EQ_g2(x[0],y[0],t,s,dominio)
    g2_r2=Ecua_dif.EQ_g2(x[1],y[1],t,s,dominio)
    g2_r3=Ecua_dif.EQ_g2(x[2],y[2],t,s,dominio)
    
    gfil1=2*g1_r1+g1_r2+g1_r3
    gfil2=g1_r1+2*g1_r2+g1_r3
    gfil3=g1_r1+g1_r2+2*g1_r3

    r=np.block([
        [(y[1]-y[2])*gfil1 , (y[2]-y[0])*gfil1 , (y[0]-y[1])*gfil1],
        [(y[1]-y[2])*gfil2 , (y[2]-y[0])*gfil2 , (y[0]-y[1])*gfil2],
        [(y[1]-y[2])*gfil3 , (y[2]-y[0])*gfil3 , (y[0]-y[1])*gfil3]
        ])
    
    gfil1=2*g2_r1+g2_r2+g2_r3
    gfil2=g2_r1+2*g2_r2+g2_r3
    gfil3=g2_r1+g2_r2+2*g2_r3

    r=r+np.block([
        [(x[2]-x[1])*gfil1 , (x[0]-x[2])*gfil1 , (x[1]-x[0])*gfil1],
        [(x[2]-x[1])*gfil2 , (x[0]-x[2])*gfil2 , (x[1]-x[0])*gfil2],
        [(x[2]-x[1])*gfil3 , (x[0]-x[2])*gfil3 , (x[1]-x[0])*gfil3]
        ])
    
    r=r/24
    
    return(r)


def hi_elemental(x,y,t,detJ,s,dominio):
#el resultado es una matriz local 3s*3s, el instante valt
#det J es el determinante    
    h_r1=Ecua_dif.EQ_h(x[0],y[0],t,s,dominio)
    h_r2=Ecua_dif.EQ_h(x[1],y[1],t,s,dominio)
    h_r3=Ecua_dif.EQ_h(x[2],y[2],t,s,dominio)
    
    r=np.block([
        [6*h_r1+2*h_r2+2*h_r3 , 2*h_r1+2*h_r2+h_r3 , 2*h_r1+h_r2+2*h_r3],
        [2*h_r1+2*h_r2+h_r3 , 2*h_r1+6*h_r2+2*h_r3 , h_r1+2*h_r2+2*h_r3],
        [2*h_r1+h_r2+2*h_r3 , h_r1+2*h_r2+2*h_r3 , 2*h_r1+2*h_r2+6*h_r3]
        ])
    
    r=detJ/120*r
    
    return(r)


def Fi_elemental_dominio(x,y,t,detJ,s,dominio):
#el resultado es una matriz local 3s*3s, el instante valt
#det J es el determinante    
    e1_r1=Ecua_dif.EQ_e1(x[0],y[0],t,s,dominio)
    e1_r2=Ecua_dif.EQ_e1(x[1],y[1],t,s,dominio)
    e1_r3=Ecua_dif.EQ_e1(x[2],y[2],t,s,dominio)
    e2_r1=Ecua_dif.EQ_e2(x[0],y[0],t,s,dominio)
    e2_r2=Ecua_dif.EQ_e2(x[1],y[1],t,s,dominio)
    e2_r3=Ecua_dif.EQ_e2(x[2],y[2],t,s,dominio)
    
    suma1=e1_r1+e1_r2+e1_r3
    r=1/6*np.block([
        [(y[1]-y[2])*suma1], [(y[2]-y[0])*suma1], [(y[0]-y[1])*suma1]
        ])
    suma2=e2_r1+e2_r2+e2_r3
    r=r+1/6*np.block([
        [(x[2]-x[1])*suma2], [(x[0]-x[2])*suma2], [(x[1]-x[0])*suma2]
        ])

    f_r1=Ecua_dif.EQ_f(x[0],y[0],t,s,dominio)
    f_r2=Ecua_dif.EQ_f(x[1],y[1],t,s,dominio)
    f_r3=Ecua_dif.EQ_f(x[2],y[2],t,s,dominio)
    
    r=r+detJ/24*np.block([
        [2*f_r1+f_r2+f_r3] , [f_r1+2*f_r2+f_r3] , [f_r1+f_r2+2*f_r3]
        ])
    
    return(r)