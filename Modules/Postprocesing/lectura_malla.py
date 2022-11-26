# -*- coding: utf-8 -*-

import os
import numpy as np
import re

def lectura_malla_COMSOL():    
    ruta=os.getcwd(); 
    with open(ruta+'\\mallado.MPHTXT') as f:
        lines = f.readlines()

    i=0
    while lines[i] != '# Mesh vertex coordinates\n': 
        i=i+1

    i=i+1


    # lectura de coordenadas de nodos
    row = re.findall(r"[-+]?\d*\.\d+|\d+", lines[i])
    puntosc = np.array([float(row[0]) , float(row[1])])
    i=i+1
    while lines[i] != '\n':    
        row = re.findall(r"[-+]?\d*\.\d+|\d+", lines[i])
        row = [float(row[0]) , float(row[1])]
        puntosc = np.vstack([puntosc,row])    
        i=i+1
        
    while lines[i] != '2 # number of vertices per element\n':
        i=i+1
    i=i+3


    # lectura de nodos por elemento en bordes
    row = [int(j) for j in lines[i].split() if j.isdigit()]
    infi = np.array([row[0] , row[1]])
    i=i+1
    while lines[i] != '\n' :
        row = [int(j) for j in lines[i].split() if j.isdigit()]
        infi = np.vstack([infi,row])
        i=i+1
        

    while lines[i] != '# Geometric entity indices\n' :
        i=i+1
    i=i+1
    dominio = 0
    row = [int(j) for j in lines[i].split() if j.isdigit()]
    iini=i
    elemborde = np.empty((len(infi),4), dtype=int)
    elemborde[0][0]= infi[0][0] 
    elemborde[0][1]= infi[0][1]
    elemborde[0][2]= dominio
    elemborde[0][3]= row[0]

    i=i+1
    while lines[i] != '\n' :
        row = [int(j) for j in lines[i].split() if j.isdigit()]
        elemborde[i-iini][0]= infi[i-iini][0] 
        elemborde[i-iini][1]= infi[i-iini][1]
        elemborde[i-iini][2]= dominio
        elemborde[i-iini][3]= row[0]
        i=i+1
        
        
    #Tabla de conectividad
    while lines[i] != '# Elements\n' :
        i=i+1
    i=i+1
    dominio = 0
    row = [int(j) for j in lines[i].split() if j.isdigit()]
    tri = np.array([row[0] , row[1], row[2], dominio])
    i=i+1
    while lines[i] != '\n' :
        row = [int(j) for j in lines[i].split() if j.isdigit()]
        row.append(dominio)
        tri = np.vstack([tri,row])
        i=i+1
    
    f.close()
    return [puntosc,elemborde,tri]




# def lectura_malla_COMSOL():    
#     ruta=os.getcwd(); 
#     with open(ruta+'\\mallado.MPHTXT') as f:
#         lines = f.readlines()
    
#     i=0
#     while lines[i] != '# Mesh vertex coordinates\n': 
#         i=i+1
    
#     i=i+1
    
    
#     # lectura de coordenadas de nodos
#     row = re.findall(r"[-+]?\d*\.\d+|\d+", lines[i])
#     puntosc = np.array([float(row[0]) , float(row[1])])
#     i=i+1
#     while lines[i] != '\n':    
#         row = re.findall(r"[-+]?\d*\.\d+|\d+", lines[i])
#         row = [float(row[0]) , float(row[1])]
#         puntosc = np.vstack([puntosc,row])    
#         i=i+1
        
#     while lines[i] != '2 # number of vertices per element\n':
#         i=i+1
#     i=i+3
    
    
#     # lectura de nodos por elemento en bordes
#     row = [int(j) for j in lines[i].split() if j.isdigit()]
#     infi = np.array([row[0] , row[1]])
#     i=i+1
#     while lines[i] != '\n' :
#         row = [int(j) for j in lines[i].split() if j.isdigit()]
#         infi = np.vstack([infi,row])
#         i=i+1
        
    
#     while lines[i] != '# Geometric entity indices\n' :
#         i=i+1
#     i=i+1
#     row = [int(j) for j in lines[i].split() if j.isdigit()]
#     numbor = row
#     i=i+1
#     while lines[i] != '\n' :
#         row = [int(j) for j in lines[i].split() if j.isdigit()]
#         numbor.append(row[0])
#         i=i+1
        
        
#     #Tabla de conectividad
#     while lines[i] != '# Elements\n' :
#         i=i+1
#     i=i+1
#     row = [int(j) for j in lines[i].split() if j.isdigit()]
#     tri = np.array([row[0] , row[1], row[2]])
#     i=i+1
#     while lines[i] != '\n' :
#         row = [int(j) for j in lines[i].split() if j.isdigit()]
#         tri = np.vstack([tri,row])
#         i=i+1
    
#     return [puntosc,numbor,tri]


# def perteneceborde(i,j):  #pertenece el nodo i al borde j?
#     [Nodos,numbor,tri]=lectura_malla_COMSOL()
#     indices = []
#     for i in range(len(a_list)):
#     Loop over indices of elements in `a_list`
    
#        if a_list[i] == 1:
#           indices.append(i)
    
#     print(indices)    
        


# function valor=perteneceborde(i,j) //pertenece el nodo i al borde j?


# [r]=find(numbor==j);
# valor=0;
# for k=1:size(r,2)
#     l=length(find(infi(r(k),:)==i))
#     if l>0
#         valor=1;
#     end 
# end
# endfunction
     




    


