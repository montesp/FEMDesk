from tkinter import Menu

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush
from PyQt5.QtWidgets import QMessageBox

import Modules.ManageFiles.ManageFiles
#import Modules.Matrix.Matrix
import Modules.SectionTabs.ConditionsPDE
from Modules.Dictionary.DModelWizard import *
from Modules.Tabs import *

#from dialogMatrix import Matrix

class ModelWizard:
    sequence = [0]
    def __init__(self):
        self.flagHeatTransferSolids = False
        self.flagHeatTransferFluids = False
        self.flagCoefficientPDE = False
        self.flagModelWizardActivated = False
        self.variables = 1
        

    def getVariables(self):
        return self.variables

    def setVariables(self, variables):
        self.variables = variables

    def hideInitialTabs(tabs, tabMenu):
        Tabs.hideElementsTab(tabs, tabMenu)
    
    def currentTreeItem(self, item, indexTree, win):
     if item.text(0) == self.itemSolids[0].text(0) or item.text(0) == self.itemFluids[0].text(0) or item.text(0) == self.itemPDE[0].text(0):
      if item.text(0) == myFlags["ModelWizardMode"]:
        return
      else:
        if self.modelwizard.flagModelWizardActivated == True:
            """dialog = QMessageBox.question(self, 'Importante', '¿Seguro que quieres cambiar la configuración del Model Wizard? Todos los cambios se perderán', QMessageBox.Cancel | QMessageBox.Yes)
            if dialog == QMessageBox.Yes:
                #Reseteo
                Modules.ManageFiles.ManageFiles.FileData.resetDataWithoutLoseFile(self)
                self.btnModelWizardApply.setEnabled(True)
                #Cambio de Configuracion
                ModelWizard.selectTreeItem(self,item, indexTree, win)
                ModelWizard.currentTreeWidgetConfiguration(self, self.tabs, self.tabWidgetMenu)
            else:
                return"""
            return
        else: 
            ModelWizard.selectTreeItem(self,item, indexTree, win)
     else:
        return

    def selectTreeItem(self, item, indexTree, win):
        self.cmbGeneralStudie.setEnabled(True)
        self.tboxModelWizard.show()
        if item.text(indexTree) == "Heat Transfer in Solids":
            item.setForeground(0, QBrush(Qt.blue))
            self.itemFluids[0].setForeground(0, QBrush(Qt.black))
            self.itemPDE[0].setForeground(0, QBrush(Qt.black))
            myFlags["ModelWizardMode"] = "Heat Transfer in Solids"
            self.modelwizard.flagModelWizardActivated = False
            self.modelwizard.flagCoefficientPDE = False
            self.inputDepedentVarial.setEnabled(False)
            self.btnModelWizardApply.setEnabled(True)
            win.tboxModelWizard.setEnabled(True)
            win.cmbGeneralStudie.setEnabled(True)
            # win.btnModelWizardReset.setEnabled(True)
            widget = win.tboxMaterialsConditions.widget(2)
            widget.setEnabled(True)

        if item.text(indexTree) == "Heat Transfer in Fluids":
            item.setForeground(0, QBrush(Qt.blue))
            self.itemSolids[0].setForeground(0, QBrush(Qt.black))
            self.itemPDE[0].setForeground(0, QBrush(Qt.black))
            myFlags["ModelWizardMode"] = "Heat Transfer in Fluids"
            self.modelwizard.flagModelWizardActivated = False
            self.modelwizard.flagCoefficientPDE = False
            self.inputDepedentVarial.setEnabled(False)
            win.tboxModelWizard.setEnabled(True)
            win.cmbGeneralStudie.setEnabled(True)
            # win.btnModelWizardReset.setEnabled(True)
            win.btnModelWizardApply.setEnabled(True)
            widget = win.tboxMaterialsConditions.widget(2)
            widget.setEnabled(True)
            
        if item.text(indexTree) == "Coefficient form PDE":
            item.setForeground(0, QBrush(Qt.blue))
            self.itemSolids[0].setForeground(0, QBrush(Qt.black))
            self.itemFluids[0].setForeground(0, QBrush(Qt.black))
            myFlags["ModelWizardMode"] = "Coefficient form PDE"
            self.modelwizard.flagCoefficientPDE = False
            self.modelwizard.flagModelWizardActivated = False
            self.inputDepedentVarial.setEnabled(True)
            win.tboxModelWizard.setEnabled(True)
            win.cmbGeneralStudie.setEnabled(True)
            # win.btnModelWizardReset.setEnabled(True)
            win.btnModelWizardApply.setEnabled(True)
            
        
    def getSigPaso():
        return ModelWizard.sigPaso

    def currentTreeWidgetConfiguration(self, tabs, tabMenu, win):

         """if ModelWizard.flagModelWizardActivated == True:
         #En la seccion Initial Values, cada vez que se presione el boton "Apply", llamar la funcion para establecer el numero de variables dependientes
         #Esto definira las dimensiones de las matrices con la que trabajara el usuario"""
          
         if myFlags["ModelWizardMode"] == "Heat Transfer in Solids":
            Tabs.hideElementsTab(tabs, tabMenu)
            Tabs.addTabElement(tabs, tabMenu)
            Tabs.hideElementTab(2, tabMenu)
            Tabs.hideElementTab(2, tabMenu)
            Tabs.hideElementTab(2, tabMenu)
            Tabs.hideElementTab(2, tabMenu)
            Tabs.hideElementTab(2, tabMenu)
            Tabs.hideElementTab(2, tabMenu)
            win.tboxMaterialsConditions.setItemEnabled(2, False)
            win.heatConvection.setEnabled(False)
            win.cmbGeneralStudie.setEnabled(False)
            win.tboxModelWizard.setEnabled(False)
            win.modelwizard.flagModelWizardActivated = True
            ModelWizard.flagModelWizardActivated = True
            ModelWizard.sigPaso = 1

         if myFlags["ModelWizardMode"] == "Heat Transfer in Fluids":
            Tabs.hideElementsTab(tabs, tabMenu)
            Tabs.addTabElement(tabs, tabMenu)
            Tabs.hideElementTab(2, tabMenu)
            Tabs.hideElementTab(2, tabMenu)
            Tabs.hideElementTab(2, tabMenu)
            Tabs.hideElementTab(2, tabMenu)
            Tabs.hideElementTab(2, tabMenu)
            Tabs.hideElementTab(2, tabMenu)
            win.tboxMaterialsConditions.setItemEnabled(2, True)
            win.heatConvection.setEnabled(False)
            win.tboxModelWizard.setEnabled(False)
            win.cmbGeneralStudie.setEnabled(False)
            win.modelwizard.flagModelWizardActivated = True
            ModelWizard.flagModelWizardActivated = True
            ModelWizard.sigPaso = 1
           
         if myFlags["ModelWizardMode"] == "Coefficient form PDE":
            dialog = QMessageBox.question(self, 'Important', 'Are you sure you want to change the number of dependent variables? They will make changes to all matrices', QMessageBox.Cancel | QMessageBox.Yes)
            if dialog == QMessageBox.Yes:
                try:
                    self.modelwizard.setVariables(int(self.inputDepedentVarial.text()))

                    Modules.Matrix.createMatrix.allNewMatrix.newMatrix(self, win.canvas)
                    Modules.SectionTabs.ConditionsPDE.ConditionsPDE.createMatrix(self, win.canvas) 
                    Tabs.hideElementsTab(tabs, tabMenu)
                    Tabs.addTabElement(tabs, tabMenu)
                    Tabs.hideElementTab(2, tabMenu)
                    Tabs.hideElementTab(2, tabMenu)
                    Tabs.hideElementTab(2, tabMenu)
                    Tabs.hideElementTab(2, tabMenu)
                    Tabs.hideElementTab(2, tabMenu)
                    Tabs.hideElementTab(2, tabMenu)
                    win.cmbGeneralStudie.setEnabled(False)
                    win.tboxModelWizard.setEnabled(False)
                    win.modelwizard.flagModelWizardActivated = True
                    ModelWizard.flagModelWizardActivated = True
                    ModelWizard.sigPaso = 2
                    print("GetVariables desde el model wizard")
                    print(win.modelwizard.getVariables())

                    Modules.ManageFiles.ManageFiles.FileData.checkUpdateFile(self)

                except:
                    QMessageBox.warning(self, "Important message", "You can only enter numeric values")
                    return
            else:
                return
