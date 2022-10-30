from tkinter import Menu
from Modules.Tabs import *
from PyQt5.QtGui import QBrush
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox
import Modules.Matrix
import Modules.ManageFiles
from Modules.Dictionary.DModelWizard import *
#from dialogMatrix import Matrix

class ModelWizard:

    flagHeatTransferSolids = False
    flagHeatTransferFluids = False
    flagCoefficientPDE = False
    flagModelWizardActivated = False
        
    def hideInitialTabs(tabs, tabMenu):
        Tabs.hideElementsTab(tabs, tabMenu)

    flagHeatTransferSolids = False
    flagHeatTransferFluids = False
    flagCoefficientPDE = False
    flagModelWizardActivated = False
    
    def currentTreeItem(self, item, indexTree):
     if item.text(0) == self.itemSolids[0].text(0) or item.text(0) == self.itemFluids[0].text(0) or item.text(0) == self.itemPDE[0].text(0):
      if item.text(0) == myFlags["ModelWizardMode"]:
        return
      else:
        if ModelWizard.flagModelWizardActivated == True:
            dialog = QMessageBox.question(self, 'Importante', '¿Seguro que quieres cambiar la configuración del Model Wizard? Todos los cambios se perderán', QMessageBox.Cancel | QMessageBox.Yes)
            if dialog == QMessageBox.Yes:
                #Reseteo
                Modules.ManageFiles.FileData.resetDataWithoutLoseFile(self)
                #Cambio de Configuracion
                ModelWizard.selectTreeItem(self,item, indexTree)
                ModelWizard.currentTreeWidgetConfiguration(self, self.tabs, self.tabWidgetMenu)
            else:
                return
        else: 
            ModelWizard.selectTreeItem(self,item, indexTree)
     else:
        return

    def selectTreeItem(self, item, indexTree):
        if item.text(indexTree) == "Heat Transfer in Solids":
            item.setForeground(0, QBrush(Qt.blue))
            self.itemFluids[0].setForeground(0, QBrush(Qt.black))
            self.itemPDE[0].setForeground(0, QBrush(Qt.black))
            myFlags["ModelWizardMode"] = "Heat Transfer in Solids"
            ModelWizard.flagModelWizardActivated = False
            ModelWizard.flagCoefficientPDE = False
            self.inputDepedentVarial.setEnabled(False)

        if item.text(indexTree) == "Heat Transfer in Fluids":
            item.setForeground(0, QBrush(Qt.blue))
            self.itemSolids[0].setForeground(0, QBrush(Qt.black))
            self.itemPDE[0].setForeground(0, QBrush(Qt.black))
            myFlags["ModelWizardMode"] = "Heat Transfer in Fluids"
            ModelWizard.flagModelWizardActivated = False
            ModelWizard.flagCoefficientPDE = False
            self.inputDepedentVarial.setEnabled(False)
            
        if item.text(indexTree) == "Coefficient form PDE":
            item.setForeground(0, QBrush(Qt.blue))
            self.itemSolids[0].setForeground(0, QBrush(Qt.black))
            self.itemFluids[0].setForeground(0, QBrush(Qt.black))
            myFlags["ModelWizardMode"] = "Coefficient form PDE"
            ModelWizard.flagCoefficientPDE = False
            ModelWizard.flagModelWizardActivated = False
            self.inputDepedentVarial.setEnabled(True)



    def currentTreeWidgetConfiguration(self, tabs, tabMenu):

        if myFlags["ModelWizardMode"] == "Heat Transfer in Solids":
            Tabs.hideElementsTab(tabs, tabMenu)
            Tabs.addTabElement(tabs, tabMenu)
            Tabs.hideElementTab(5, tabMenu)
            Tabs.hideElementTab(5, tabMenu)
            self.heatConvection.setEnabled(False)
            ModelWizard.flagModelWizardActivated = True

        if myFlags["ModelWizardMode"] == "Heat Transfer in Fluids":
            Tabs.hideElementsTab(tabs, tabMenu)
            Tabs.addTabElement(tabs, tabMenu)
            Tabs.hideElementTab(5, tabMenu)
            Tabs.hideElementTab(5, tabMenu)
            self.heatConvection.setEnabled(True)
            ModelWizard.flagModelWizardActivated = True
           
        if myFlags["ModelWizardMode"] == "Coefficient form PDE":
            Tabs.hideElementsTab(tabs, tabMenu)
            Tabs.addTabElement(tabs, tabMenu)
            Tabs.hideElementTab(1, tabMenu)
            Tabs.hideElementTab(2, tabMenu)
            Tabs.hideElementTab(5, tabMenu)
            #self.inputDepedentVarial.setEnabled(True)
            self.btnModelWizardReset.setEnabled(True)
            ModelWizard.flagModelWizardActivated = True
        
    def selectWizardConfiguration(self, tabs, tabMenu):
        if myFlags["ModelWizardMode"] == "Heat Transfer in Solids":
            Tabs.hideElementsTab(tabs, tabMenu)
            Tabs.addTabElement(tabs, tabMenu)
            Tabs.hideElementTab(5, tabMenu)
            Tabs.hideElementTab(5, tabMenu)
            self.heatConvection.setEnabled(False)
            ModelWizard.flagModelWizardActivated = True

        if myFlags["ModelWizardMode"] == "Heat Transfer in Fluids":
            Tabs.hideElementsTab(tabs, tabMenu)
            Tabs.addTabElement(tabs, tabMenu)
            Tabs.hideElementTab(5, tabMenu)
            Tabs.hideElementTab(5, tabMenu)
            self.heatConvection.setEnabled(True)
            ModelWizard.flagModelWizardActivated = True
           
        if myFlags["ModelWizardMode"] == "Coefficient form PDE":
            Tabs.hideElementsTab(tabs, tabMenu)
            Tabs.addTabElement(tabs, tabMenu)
            Tabs.hideElementTab(1, tabMenu)
            Tabs.hideElementTab(2, tabMenu)
            Tabs.hideElementTab(5, tabMenu)
            #self.inputDepedentVarial.setEnabled(True)
            self.btnModelWizardReset.setEnabled(True)
            ModelWizard.flagCoefficientPDE = True
            ModelWizard.flagModelWizardActivated = True
           
            


    



