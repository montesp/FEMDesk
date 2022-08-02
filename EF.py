# -*- coding: utf-8 -*-
"""
Created on Wed May 11 13:39:55 2022

@author: ruben.castaneda
"""

# -*- coding: utf-8 -*-
"""
Created on Tue May 10 14:30:09 2022

@author: ruben.castaneda
"""

import os, sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QCloseEvent
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsView, QButtonGroup, QMessageBox
from PyQt5.QtWidgets import QMessageBox
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from Base import *

app = None

class PropertiesData:
    kappa=[]
    rho=[]
    Cp=[]
    def __init__(self):
        self.kappa = [[-1.0,-1.0],[-1.0,-1.0]]
        self.rho = -1.0
        self.Cp = -1.0
       
class EditorWindow(QMainWindow):
    """MainWindow-klass som hanterar vårt huvudfönster"""
    DataProperties = []
    materialsDataBase = []
    conn = []
    statusLibrary = 0 #0 initial value, 1 new material, 2 copyas, 3 changes values 
    def __init__(self):
        super(QMainWindow, self).__init__()
        self.app = app
        root = os.path.dirname(os.path.realpath(__file__))
        loadUi(os.path.join(root, 'Interfaz.ui'), self)
        self.conn = materials()
        self.materialsDataBase = select_all_materials(self.conn)
        self.DataProperties = PropertiesData()

        
        self.btnNewMaterial.clicked.connect(self.click_btnNewMaterial) 
        self.btnSaveMaterial.clicked.connect(self.click_btnSaveMaterial) 
        self.btnResetLibrary.clicked.connect(self.click_btnResetLibrary) 
        self.btnSaveAsMaterial.clicked.connect(self.click_btnSaveAsMaterial)
        self.btnOpenMaterial.clicked.connect(self.click_btnOpenMaterial)
        self.btnDeleteMaterial.clicked.connect(self.click_btnDeleteMaterial)
        
        self.cmbTypeHeatConductionSolid.currentIndexChanged.connect(self.change_cmbTypeHeatConductionSolid)
        self.cmbNameMaterials.currentIndexChanged.connect(self.change_cmbNameMaterials)       
        self.edtTermalConductivityIsotropicProperties.editingFinished.connect(self.exit_edtTermalConductivityIsotropicProperties)
        self.edtTermalConductivityAnisotropicPropertiesA11.editingFinished.connect(self.exit_edtTermalConductivityAnisotropicPropertiesA11)
        self.edtTermalConductivityAnisotropicPropertiesA12.editingFinished.connect(self.exit_edtTermalConductivityAnisotropicPropertiesA12)
        self.edtTermalConductivityAnisotropicPropertiesA21.editingFinished.connect(self.exit_edtTermalConductivityAnisotropicPropertiesA21)
        self.edtTermalConductivityAnisotropicPropertiesA22.editingFinished.connect(self.exit_edtTermalConductivityAnisotropicPropertiesA22)
        self.edtRhoProperties.editingFinished.connect(self.exit_edtRhoProperties)
        self.edtCpProperties.editingFinished.connect(self.exit_edtCpProperties)
        self.addMaterials()
    
    def click_btnDeleteMaterial(self) :
        buttonReply = QMessageBox.question(self, 'Important message', "Are you sure you want to delete the material from the database?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if buttonReply == QMessageBox.Yes:
            delete_task(self.conn, self.materialsDataBase[self.cmbNameMaterials.currentIndex()][0])
            self.materialsDataBase = select_all_materials(self.conn)
            self.btnNewMaterial.setEnabled(True)
            self.btnDeleteMaterial.setEnabled(True)
            self.btnSaveMaterial.setEnabled(False)
            self.btnSaveAsMaterial.setEnabled(True)
            self.btnOpenMaterial.setEnabled(True)
            self.btnResetLibrary.setEnabled(False)
            self.btnHelpLibrary.setEnabled(True)
            self.cmbNameMaterials.setEnabled(True)
            self.edtNameMaterial.setEnabled(False)
            self.edtNameMaterial.setText("")
            self.cmbTypeHeatConductionSolid.setEnabled(False)
            self.cmbTypeHeatConductionSolid.setCurrentIndex (0)
            self.edtTermalConductivityIsotropicProperties.setEnabled(False)
            self.edtTermalConductivityIsotropicProperties.setText("")
            self.edtTermalConductivityAnisotropicPropertiesA11.setEnabled(False)
            self.edtTermalConductivityAnisotropicPropertiesA12.setEnabled(False)
            self.edtTermalConductivityAnisotropicPropertiesA21.setEnabled(False)
            self.edtTermalConductivityAnisotropicPropertiesA22.setEnabled(False)
            self.edtTermalConductivityAnisotropicPropertiesA11.setText("")
            self.edtTermalConductivityAnisotropicPropertiesA12.setText("")
            self.edtTermalConductivityAnisotropicPropertiesA21.setText("")
            self.edtTermalConductivityAnisotropicPropertiesA22.setText("")
            self.edtRhoProperties.setEnabled(False)
            self.edtRhoProperties.setText("")
            self.edtCpProperties.setEnabled(False)
            self.edtCpProperties.setText("")
            self.addMaterials()
            QMessageBox.information(self, "Important message", "Material deleted in the database") 
   
    def click_btnOpenMaterial(self):
        self.btnNewMaterial.setEnabled(False)
        self.btnDeleteMaterial.setEnabled(False)
        self.btnSaveMaterial.setEnabled(True)
        self.btnSaveAsMaterial.setEnabled(False)
        self.btnOpenMaterial.setEnabled(False)
        self.btnResetLibrary.setEnabled(True)
        self.btnHelpLibrary.setEnabled(True)
        self.cmbNameMaterials.setEnabled(False)
        self.edtNameMaterial.setEnabled(False)
        self.edtNameMaterial.setText(self.cmbNameMaterials.currentText())
        self.cmbTypeHeatConductionSolid.setEnabled(True)
        if self.cmbTypeHeatConductionSolid.currentIndex() == 0 : #isotropic
            self.edtTermalConductivityIsotropicProperties.setEnabled(True)
            self.edtTermalConductivityAnisotropicPropertiesA11.setEnabled(False)
            self.edtTermalConductivityAnisotropicPropertiesA12.setEnabled(False)
            self.edtTermalConductivityAnisotropicPropertiesA21.setEnabled(False)
            self.edtTermalConductivityAnisotropicPropertiesA22.setEnabled(False)                  
        elif self.cmbTypeHeatConductionSolid.currentIndex() == 1 : #diagonal
            self.edtTermalConductivityIsotropicProperties.setEnabled(False)
            self.edtTermalConductivityAnisotropicPropertiesA11.setEnabled(True)
            self.edtTermalConductivityAnisotropicPropertiesA12.setEnabled(False)
            self.edtTermalConductivityAnisotropicPropertiesA21.setEnabled(False)
            self.edtTermalConductivityAnisotropicPropertiesA22.setEnabled(True)
        elif self.cmbTypeHeatConductionSolid.currentIndex() == 2 : #symmetric
            self.edtTermalConductivityIsotropicProperties.setEnabled(False)
            self.edtTermalConductivityAnisotropicPropertiesA11.setEnabled(True)
            self.edtTermalConductivityAnisotropicPropertiesA12.setEnabled(True)
            self.edtTermalConductivityAnisotropicPropertiesA21.setEnabled(False)
            self.edtTermalConductivityAnisotropicPropertiesA22.setEnabled(True)
        elif self.cmbTypeHeatConductionSolid.currentIndex() == 3 : #full
            self.edtTermalConductivityIsotropicProperties.setEnabled(True)
            self.edtTermalConductivityAnisotropicPropertiesA11.setEnabled(True)
            self.edtTermalConductivityAnisotropicPropertiesA12.setEnabled(True)
            self.edtTermalConductivityAnisotropicPropertiesA21.setEnabled(True)
            self.edtTermalConductivityAnisotropicPropertiesA22.setEnabled(True)
        self.edtCpProperties.setEnabled(True)
        self.edtRhoProperties.setEnabled(True)         
        self.statusLibrary = 3
        
    def click_btnSaveAsMaterial(self):
        self.btnNewMaterial.setEnabled(False)
        self.btnDeleteMaterial.setEnabled(False)
        self.btnSaveMaterial.setEnabled(True)
        self.btnSaveAsMaterial.setEnabled(False)
        self.btnOpenMaterial.setEnabled(False)
        self.btnResetLibrary.setEnabled(True)
        self.btnHelpLibrary.setEnabled(True)
        self.cmbNameMaterials.setEnabled(False)
        self.edtNameMaterial.setEnabled(True)
        self.edtNameMaterial.setText("Copy"+self.cmbNameMaterials.currentText())
        self.statusLibrary = 2
        
    def click_btnResetLibrary(self):
        self.btnNewMaterial.setEnabled(True)
        self.btnDeleteMaterial.setEnabled(True)
        self.btnSaveMaterial.setEnabled(False)
        self.btnSaveAsMaterial.setEnabled(True)
        self.btnOpenMaterial.setEnabled(True)
        self.btnResetLibrary.setEnabled(False)
        self.btnHelpLibrary.setEnabled(True)
        self.cmbNameMaterials.setEnabled(True)
        self.edtNameMaterial.setEnabled(False)
        self.edtNameMaterial.setText("")
        self.cmbTypeHeatConductionSolid.setEnabled(False)
        self.cmbTypeHeatConductionSolid.setCurrentIndex (0)
        self.edtTermalConductivityIsotropicProperties.setEnabled(False)
        self.edtTermalConductivityIsotropicProperties.setText("")
        self.edtRhoProperties.setEnabled(False)
        self.edtRhoProperties.setText("")
        self.edtCpProperties.setEnabled(False)
        self.edtCpProperties.setText("")
        self.addMaterials()
        
    def click_btnNewMaterial(self):
        self.cmbNameMaterials.setEnabled(False)
        self.edtNameMaterial.setEnabled(True)
        self.edtNameMaterial.setText("Material_Name")
        self.cmbTypeHeatConductionSolid.setEnabled(True)
        self.cmbTypeHeatConductionSolid.setCurrentIndex (0)
        self.edtTermalConductivityIsotropicProperties.setEnabled(True)
        self.edtTermalConductivityIsotropicProperties.setText("")
        self.edtRhoProperties.setEnabled(True)
        self.edtRhoProperties.setText("")
        self.edtCpProperties.setEnabled(True)
        self.edtCpProperties.setText("")
        self.btnNewMaterial.setEnabled(False)
        self.btnSaveMaterial.setEnabled(True)
        self.btnDeleteMaterial.setEnabled(False)
        self.btnSaveAsMaterial.setEnabled(False)
        self.btnOpenMaterial.setEnabled(False)
        self.btnResetLibrary.setEnabled(True)
        self.kappa = [[-1.0,-1.0],[-1.0,-1.0]]
        self.rho = -1.0
        self.Cp = -1.0
        self.statusLibrary = 1
        
    def click_btnSaveMaterial(self):
        reviews = [0,0,0] #review each variable before saving
        reName = 0 #review material name
        
        dato = self.edtNameMaterial.text()
        if not (dato.isspace() or len(dato) == 0):
            mat = select_material(self.conn,dato)
            if len(mat) == 0:
                reName = 1
        
        if self.cmbTypeHeatConductionSolid.currentIndex() == 0 : #isotropic
            if self.DataProperties.kappa[0][0] != -1.0:
                reviews[0] = 1       
        elif self.cmbTypeHeatConductionSolid.currentIndex() == 1 : #diagonal
            if self.DataProperties.kappa[0][0] != -1.0 and self.DataProperties.kappa[1][1] != -1.0 :   
                reviews[0] = 1
        elif self.cmbTypeHeatConductionSolid.currentIndex() == 2 : #symmetric
            if self.DataProperties.kappa[0][0] != -1.0 and self.DataProperties.kappa[0][1] != -1.0 and self.DataProperties.kappa[1][0] != -1.0 and self.DataProperties.kappa[1][1] != -1.0:    
                reviews[0] = 1
        elif self.cmbTypeHeatConductionSolid.currentIndex() == 3 : #full
            if self.DataProperties.kappa[0][0] != -1.0 and self.DataProperties.kappa[0][1] != -1.0 and self.DataProperties.kappa[1][0] != -1.0 and self.DataProperties.kappa[1][1] != -1.0:    
                reviews[0] = 1
        
        if self.DataProperties.rho != -1.0:
            reviews[1] = 1 
            
        if self.DataProperties.Cp != -1.0:
            reviews[2] = 1 
        
        if self.statusLibrary == 1 :
            if sum(reviews) == 3 and reName == 1:
                material = (self.edtNameMaterial.text(),self.DataProperties.kappa[0][0],self.DataProperties.kappa[0][1],self.DataProperties.kappa[1][0],self.DataProperties.kappa[1][1],self.DataProperties.Cp,self.DataProperties.rho,self.cmbTypeHeatConductionSolid.currentIndex())
                add_material(self.conn, material)
                self.materialsDataBase = select_all_materials(self.conn)
                self.btnNewMaterial.setEnabled(True)
                self.btnDeleteMaterial.setEnabled(True)
                self.btnSaveMaterial.setEnabled(False)
                self.btnSaveAsMaterial.setEnabled(True)
                self.btnOpenMaterial.setEnabled(True)
                self.btnResetLibrary.setEnabled(False)
                self.btnHelpLibrary.setEnabled(True)
                self.cmbNameMaterials.setEnabled(True)
                self.edtNameMaterial.setEnabled(False)
                self.edtNameMaterial.setText("")
                self.cmbTypeHeatConductionSolid.setEnabled(False)
                self.cmbTypeHeatConductionSolid.setCurrentIndex (0)
                self.edtTermalConductivityIsotropicProperties.setEnabled(False)
                self.edtTermalConductivityIsotropicProperties.setText("")
                self.edtTermalConductivityAnisotropicPropertiesA11.setEnabled(False)
                self.edtTermalConductivityAnisotropicPropertiesA12.setEnabled(False)
                self.edtTermalConductivityAnisotropicPropertiesA21.setEnabled(False)
                self.edtTermalConductivityAnisotropicPropertiesA22.setEnabled(False)
                self.edtTermalConductivityAnisotropicPropertiesA11.setText("")
                self.edtTermalConductivityAnisotropicPropertiesA12.setText("")
                self.edtTermalConductivityAnisotropicPropertiesA21.setText("")
                self.edtTermalConductivityAnisotropicPropertiesA22.setText("")
                self.edtRhoProperties.setEnabled(False)
                self.edtRhoProperties.setText("")
                self.edtCpProperties.setEnabled(False)
                self.edtCpProperties.setText("")
                self.addMaterials()
                QMessageBox.information(self, "Important message", "Material registered in the database")               
            else:
                QMessageBox.critical(self, "Important message", "Null values ​​exist, please check")
        elif self.statusLibrary == 2:
            if reName == 1:
                material = (self.edtNameMaterial.text(),self.DataProperties.kappa[0][0],self.DataProperties.kappa[0][1],self.DataProperties.kappa[1][0],self.DataProperties.kappa[1][1],self.DataProperties.Cp,self.DataProperties.rho,self.cmbTypeHeatConductionSolid.currentIndex())
                add_material(self.conn, material)
                self.materialsDataBase = select_all_materials(self.conn)
                self.btnNewMaterial.setEnabled(True)
                self.btnDeleteMaterial.setEnabled(True)
                self.btnSaveMaterial.setEnabled(False)
                self.btnSaveAsMaterial.setEnabled(True)
                self.btnOpenMaterial.setEnabled(True)
                self.btnResetLibrary.setEnabled(False)
                self.btnHelpLibrary.setEnabled(True)
                self.cmbNameMaterials.setEnabled(True)
                self.edtNameMaterial.setEnabled(False)
                self.edtNameMaterial.setText("")
                self.cmbTypeHeatConductionSolid.setEnabled(False)
                self.cmbTypeHeatConductionSolid.setCurrentIndex (0)
                self.edtTermalConductivityIsotropicProperties.setEnabled(False)
                self.edtTermalConductivityIsotropicProperties.setText("")
                self.edtTermalConductivityAnisotropicPropertiesA11.setEnabled(False)
                self.edtTermalConductivityAnisotropicPropertiesA12.setEnabled(False)
                self.edtTermalConductivityAnisotropicPropertiesA21.setEnabled(False)
                self.edtTermalConductivityAnisotropicPropertiesA22.setEnabled(False)
                self.edtTermalConductivityAnisotropicPropertiesA11.setText("")
                self.edtTermalConductivityAnisotropicPropertiesA12.setText("")
                self.edtTermalConductivityAnisotropicPropertiesA21.setText("")
                self.edtTermalConductivityAnisotropicPropertiesA22.setText("")
                self.edtRhoProperties.setEnabled(False)
                self.edtRhoProperties.setText("")
                self.edtCpProperties.setEnabled(False)
                self.edtCpProperties.setText("")
                self.addMaterials()
                QMessageBox.information(self, "Important message", "Material registered in the database")               
            else:
                QMessageBox.critical(self, "Important message", "Null values ​​exist, please check")    
        elif self.statusLibrary == 3 :
            if sum(reviews) == 3 :
                display(self.materialsDataBase[self.cmbNameMaterials.currentIndex()][0])
                material = (self.edtNameMaterial.text(),self.DataProperties.kappa[0][0],self.DataProperties.kappa[0][1],self.DataProperties.kappa[1][0],self.DataProperties.kappa[1][1],self.DataProperties.Cp,self.DataProperties.rho,self.cmbTypeHeatConductionSolid.currentIndex(),self.materialsDataBase[self.cmbNameMaterials.currentIndex()][0])
                update_material(self.conn, material)
                self.materialsDataBase = select_all_materials(self.conn)
                self.btnNewMaterial.setEnabled(True)
                self.btnDeleteMaterial.setEnabled(True)
                self.btnSaveMaterial.setEnabled(False)
                self.btnSaveAsMaterial.setEnabled(True)
                self.btnOpenMaterial.setEnabled(True)
                self.btnResetLibrary.setEnabled(False)
                self.btnHelpLibrary.setEnabled(True)
                self.cmbNameMaterials.setEnabled(True)
                self.edtNameMaterial.setEnabled(False)
                self.edtNameMaterial.setText("")
                self.cmbTypeHeatConductionSolid.setEnabled(False)
                self.cmbTypeHeatConductionSolid.setCurrentIndex(0)
                self.edtTermalConductivityIsotropicProperties.setEnabled(False)
                self.edtTermalConductivityIsotropicProperties.setText("")
                self.edtTermalConductivityAnisotropicPropertiesA11.setEnabled(False)
                self.edtTermalConductivityAnisotropicPropertiesA12.setEnabled(False)
                self.edtTermalConductivityAnisotropicPropertiesA21.setEnabled(False)
                self.edtTermalConductivityAnisotropicPropertiesA22.setEnabled(False)
                self.edtTermalConductivityAnisotropicPropertiesA11.setText("")
                self.edtTermalConductivityAnisotropicPropertiesA12.setText("")
                self.edtTermalConductivityAnisotropicPropertiesA21.setText("")
                self.edtTermalConductivityAnisotropicPropertiesA22.setText("")
                self.edtRhoProperties.setEnabled(False)
                self.edtRhoProperties.setText("")
                self.edtCpProperties.setEnabled(False)
                self.edtCpProperties.setText("")
                self.addMaterials()
                QMessageBox.information(self, "Important message", "material registered in the database")               
            else:
                QMessageBox.critical(self, "Important message", "Null values ​​exist, please check")    
        self.statusLibrary = 0
        
    def change_cmbNameMaterials(self) :
        if self.cmbNameMaterials.currentIndex() != -1 :
            if self.materialsDataBase[self.cmbNameMaterials.currentIndex()][6] == 0:  #isotropic
                self.cmbTypeHeatConductionSolid.setCurrentIndex(0)
                self.edtTermalConductivityIsotropicProperties.setText(str(self.materialsDataBase[self.cmbNameMaterials.currentIndex()][2]))  
                self.edtTermalConductivityAnisotropicPropertiesA11.setText("")
                self.edtTermalConductivityAnisotropicPropertiesA12.setText("")
                self.edtTermalConductivityAnisotropicPropertiesA21.setText("")
                self.edtTermalConductivityAnisotropicPropertiesA22.setText("")    
                self.edtCpProperties.setText(str(self.materialsDataBase[self.cmbNameMaterials.currentIndex()][7]))
                self.edtRhoProperties.setText(str(self.materialsDataBase[self.cmbNameMaterials.currentIndex()][8]))
                dato = self.edtTermalConductivityIsotropicProperties.text()
                self.DataProperties.kappa[0][0] = float(dato)
                self.DataProperties.kappa[0][1] = -1.0
                self.DataProperties.kappa[1][0] = -1.0
                self.DataProperties.kappa[1][1] = -1.0
            elif self.materialsDataBase[self.cmbNameMaterials.currentIndex()][6] == 1 : #diagonal  
                self.cmbTypeHeatConductionSolid.setCurrentIndex(1)
                self.edtTermalConductivityIsotropicProperties.setText("")  
                self.edtTermalConductivityAnisotropicPropertiesA11.setText(str(self.materialsDataBase[self.cmbNameMaterials.currentIndex()][2]))
                self.edtTermalConductivityAnisotropicPropertiesA12.setText("0")
                self.edtTermalConductivityAnisotropicPropertiesA21.setText("0")
                self.edtTermalConductivityAnisotropicPropertiesA22.setText(str(self.materialsDataBase[self.cmbNameMaterials.currentIndex()][5]))    
                self.edtCpProperties.setText(str(self.materialsDataBase[self.cmbNameMaterials.currentIndex()][7]))
                self.edtRhoProperties.setText(str(self.materialsDataBase[self.cmbNameMaterials.currentIndex()][8]))
                dato = self.edtTermalConductivityAnisotropicPropertiesA11.text()
                self.DataProperties.kappa[0][0] = float(dato)
                self.DataProperties.kappa[0][1] = 0.0
                self.DataProperties.kappa[1][0] = 0.0
                dato = self.edtTermalConductivityAnisotropicPropertiesA22.text()
                self.DataProperties.kappa[1][1] = float(dato)
            elif self.materialsDataBase[self.cmbNameMaterials.currentIndex()][6] == 2 : #symmetric   
                self.cmbTypeHeatConductionSolid.setCurrentIndex(2)
                self.edtTermalConductivityIsotropicProperties.setText("")  
                self.edtTermalConductivityAnisotropicPropertiesA11.setText(str(self.materialsDataBase[self.cmbNameMaterials.currentIndex()][2]))
                self.edtTermalConductivityAnisotropicPropertiesA12.setText(str(self.materialsDataBase[self.cmbNameMaterials.currentIndex()][3]))
                self.edtTermalConductivityAnisotropicPropertiesA21.setText(str(self.materialsDataBase[self.cmbNameMaterials.currentIndex()][4]))
                self.edtTermalConductivityAnisotropicPropertiesA22.setText(str(self.materialsDataBase[self.cmbNameMaterials.currentIndex()][5]))
                dato = self.edtTermalConductivityAnisotropicPropertiesA11.text()
                self.DataProperties.kappa[0][0] = float(dato)
                dato = self.edtTermalConductivityAnisotropicPropertiesA12.text()
                self.DataProperties.kappa[0][1] = float(dato)
                self.DataProperties.kappa[1][0] = float(dato)
                dato = self.edtTermalConductivityAnisotropicPropertiesA22.text()
                self.DataProperties.kappa[1][1] = float(dato)
            elif self.materialsDataBase[self.cmbNameMaterials.currentIndex()][6] == 3 : #full
                self.cmbTypeHeatConductionSolid.setCurrentIndex(3)
                self.edtTermalConductivityIsotropicProperties.setText("")  
                self.edtTermalConductivityAnisotropicPropertiesA11.setText(str(self.materialsDataBase[self.cmbNameMaterials.currentIndex()][2]))
                self.edtTermalConductivityAnisotropicPropertiesA12.setText(str(self.materialsDataBase[self.cmbNameMaterials.currentIndex()][3]))
                self.edtTermalConductivityAnisotropicPropertiesA21.setText(str(self.materialsDataBase[self.cmbNameMaterials.currentIndex()][4]))
                self.edtTermalConductivityAnisotropicPropertiesA22.setText(str(self.materialsDataBase[self.cmbNameMaterials.currentIndex()][5]))
                dato = self.edtTermalConductivityAnisotropicPropertiesA11.text()
                self.DataProperties.kappa[0][0] = float(dato)
                dato = self.edtTermalConductivityAnisotropicPropertiesA12.text()
                self.DataProperties.kappa[0][1] = float(dato)
                dato = self.edtTermalConductivityAnisotropicPropertiesA21.text()
                self.DataProperties.kappa[1][0] = float(dato)
                dato = self.edtTermalConductivityAnisotropicPropertiesA22.text()
            self.edtCpProperties.setText(str(self.materialsDataBase[self.cmbNameMaterials.currentIndex()][7]))
            self.edtRhoProperties.setText(str(self.materialsDataBase[self.cmbNameMaterials.currentIndex()][8]))
            dato = self.edtRhoProperties.text()
            self.DataProperties.rho = float(dato)
            dato = self.edtCpProperties.text()
            self.DataProperties.Cp = float(dato)
            self.edtTermalConductivityIsotropicProperties.setEnabled(False)
            self.edtTermalConductivityAnisotropicPropertiesA11.setEnabled(False)
            self.edtTermalConductivityAnisotropicPropertiesA12.setEnabled(False)
            self.edtTermalConductivityAnisotropicPropertiesA21.setEnabled(False)
            self.edtTermalConductivityAnisotropicPropertiesA22.setEnabled(False)
            self.edtCpProperties.setEnabled(False)
            self.edtRhoProperties.setEnabled(False)
            
    def change_cmbTypeHeatConductionSolid(self):
        if self.cmbTypeHeatConductionSolid.currentIndex() == 0 : #isotropic
            self.edtTermalConductivityIsotropicProperties.setEnabled(True)
            self.edtTermalConductivityIsotropicProperties.setText("")
            self.edtTermalConductivityAnisotropicPropertiesA11.setEnabled(False)
            self.edtTermalConductivityAnisotropicPropertiesA11.setText("")
            self.edtTermalConductivityAnisotropicPropertiesA12.setEnabled(False)
            self.edtTermalConductivityAnisotropicPropertiesA12.setText("")
            self.edtTermalConductivityAnisotropicPropertiesA21.setEnabled(False)
            self.edtTermalConductivityAnisotropicPropertiesA21.setText("")
            self.edtTermalConductivityAnisotropicPropertiesA22.setEnabled(False)
            self.edtTermalConductivityAnisotropicPropertiesA22.setText("")
        elif self.cmbTypeHeatConductionSolid.currentIndex() == 1 : #diagonal
            self.edtTermalConductivityIsotropicProperties.setEnabled(False)
            self.edtTermalConductivityIsotropicProperties.setText("")
            self.edtTermalConductivityAnisotropicPropertiesA11.setEnabled(True)
            self.edtTermalConductivityAnisotropicPropertiesA11.setText("")
            self.edtTermalConductivityAnisotropicPropertiesA12.setEnabled(False)
            self.edtTermalConductivityAnisotropicPropertiesA12.setText("0")
            self.edtTermalConductivityAnisotropicPropertiesA21.setEnabled(False)
            self.edtTermalConductivityAnisotropicPropertiesA21.setText("0")
            self.edtTermalConductivityAnisotropicPropertiesA22.setEnabled(True)
            self.edtTermalConductivityAnisotropicPropertiesA22.setText("")
        elif self.cmbTypeHeatConductionSolid.currentIndex() == 2 : #symmetric
            self.edtTermalConductivityIsotropicProperties.setEnabled(False)
            self.edtTermalConductivityIsotropicProperties.setText("")
            self.edtTermalConductivityAnisotropicPropertiesA11.setEnabled(True)
            self.edtTermalConductivityAnisotropicPropertiesA11.setText("")
            self.edtTermalConductivityAnisotropicPropertiesA12.setEnabled(True)
            self.edtTermalConductivityAnisotropicPropertiesA12.setText("")
            self.edtTermalConductivityAnisotropicPropertiesA21.setEnabled(False)
            self.edtTermalConductivityAnisotropicPropertiesA21.setText("")
            self.edtTermalConductivityAnisotropicPropertiesA22.setEnabled(True)
            self.edtTermalConductivityAnisotropicPropertiesA22.setText("")
        elif self.cmbTypeHeatConductionSolid.currentIndex() == 3 : #full
            self.edtTermalConductivityIsotropicProperties.setEnabled(False)
            self.edtTermalConductivityIsotropicProperties.setText("")
            self.edtTermalConductivityAnisotropicPropertiesA11.setEnabled(True)
            self.edtTermalConductivityAnisotropicPropertiesA11.setText("")
            self.edtTermalConductivityAnisotropicPropertiesA12.setEnabled(True)
            self.edtTermalConductivityAnisotropicPropertiesA12.setText("")
            self.edtTermalConductivityAnisotropicPropertiesA21.setEnabled(True)
            self.edtTermalConductivityAnisotropicPropertiesA21.setText("")
            self.edtTermalConductivityAnisotropicPropertiesA22.setEnabled(True)
            self.edtTermalConductivityAnisotropicPropertiesA22.setText("")
    
    def exit_edtTermalConductivityIsotropicProperties(self):
        dato = self.edtTermalConductivityIsotropicProperties.text()
        if not (dato.isspace() or len(dato) ==0):
            if float(dato) >= 0:
                self.DataProperties.kappa[0][0] = float(dato)
                self.DataProperties.kappa[0][1] = -1.0
                self.DataProperties.kappa[1][0] = -1.0
                self.DataProperties.kappa[1][1] = -1.0
            else:
                QMessageBox.critical(self, "Important message", "The value must be greater than or equal to zero")
                self.edtTermalConductivityIsotropicProperties.setText("")
        
    def exit_edtTermalConductivityAnisotropicPropertiesA11(self):
        dato = self.edtTermalConductivityAnisotropicPropertiesA11.text()
        if not (dato.isspace() or len(dato) ==0):
            if float(dato) >= 0:
                self.DataProperties.kappa[0][0] = float(dato)
                if self.cmbTypeHeatConductionSolid.currentIndex () == 1 : #diagonal
                    self.DataProperties.kappa[0][1] = 0.0
                    self.DataProperties.kappa[1][0] = 0.0
            else:
                QMessageBox.critical(self, "Important message", "The value must be greater than or equal to zero")
                self.edtTermalConductivityAnisotropicPropertiesA11.setText("")
                    
    def exit_edtTermalConductivityAnisotropicPropertiesA12(self):
        dato = self.edtTermalConductivityAnisotropicPropertiesA12.text()
        if not (dato.isspace() or len(dato) ==0):
            if float(dato) >= 0:
                self.DataProperties.kappa[0][1] = float(dato)
                if self.cmbTypeHeatConductionSolid.currentIndex () == 2 : #symmetric
                    self.DataProperties.kappa[1][0] = float(dato)
                    self.edtTermalConductivityAnisotropicPropertiesA21.setText(dato)
            else:
                QMessageBox.critical(self, "Important message", "The value must be greater than or equal to zero")
                self.edtTermalConductivityAnisotropicPropertiesA12.setText("")
                    
    def exit_edtTermalConductivityAnisotropicPropertiesA21(self):        
        dato = self.edtTermalConductivityAnisotropicPropertiesA21.text()
        if not (dato.isspace() or len(dato) ==0):
            if float(dato) >= 0:
                self.DataProperties.kappa[1][0] = float(dato)
            else:
                QMessageBox.critical(self, "Important message", "The value must be greater than or equal to zero")
                self.edtTermalConductivityAnisotropicPropertiesA21.setText("")
   
    def exit_edtTermalConductivityAnisotropicPropertiesA22(self):
        dato = self.edtTermalConductivityAnisotropicPropertiesA22.text()
        if not (dato.isspace() or len(dato) ==0):
            if float(dato) >= 0:
                self.DataProperties.kappa[1][1] = float(dato)
                if self.cmbTypeHeatConductionSolid.currentIndex () == 1 : #diagonal
                    self.DataProperties.kappa[0][1] = 0.0
                    self.DataProperties.kappa[1][0] = 0.0   
            else:
                QMessageBox.critical(self, "Important message", "The value must be greater than or equal to zero")
                self.edtTermalConductivityAnisotropicPropertiesA22.setText("")
      
    def exit_edtRhoProperties(self):
        dato = self.edtRhoProperties.text()
        if not (dato.isspace() or len(dato) ==0):
            if float(dato) > 0:
                self.DataProperties.rho = float(dato)
            else:
                QMessageBox.critical(self, "Important message", "The value must be greater than zero")
                self.edtRhoProperties.setText("")  
     
    def exit_edtCpProperties(self) :        
        dato = self.edtCpProperties.text()
        if not (dato.isspace() or len(dato) ==0):
            if float(dato) > 0:
                self.DataProperties.Cp = float(dato)
            else:
                QMessageBox.critical(self, "Important message", "The value must be greater than zero")
                self.edtCpProperties.setText("")      
                
    def addMaterials(self) :       
        self.cmbNameMaterials.clear()
        for i in range(len(self.materialsDataBase)):
            self.cmbNameMaterials.addItem(self.materialsDataBase[i][1])
         
def init_app():
    app = QApplication.instance()

    if app is None:
        print("No QApplication instance found. Creating one.")
        # if it does not exist then a QApplication is created
        app = QApplication(sys.argv)
    else:
        print("QApplication instance found.")

    return app

if __name__ == '__main__':
    app = init_app()

    widget = EditorWindow()
    widget.show()
    
    sys.exit(app.exec_())
    