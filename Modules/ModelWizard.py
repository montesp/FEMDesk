from Modules.Tabs import *
from PyQt5.QtGui import QBrush
from PyQt5.QtCore import Qt
import Modules.Matrix
from Modules.Dictionary.DModelWizard import *
#from dialogMatrix import Matrix

class ModelWizard:
    def hideInitialTabs(tabs, tabMenu):
        Tabs.hideElementsTab(tabs, tabMenu)

    flagHeatTransferSolids = False
    flagHeatTransferFluids = False
    flagCoefficientPDE = False
    flagModelWizardActivated = False

    def currentTreeItem(self, item, indexTree):
        if item.text(indexTree) == "Heat Transfer in Solids":
            item.setForeground(0, QBrush(Qt.blue))
            anotheritem = self.treeModelWizard.itemBelow(item)
            anotheritem.setForeground(0, QBrush(Qt.black))

            myFlags["ModelWizardMode"] = "Solids"
            ModelWizard.flagModelWizardActivated = False

        if item.text(indexTree) == "Heat Transfer in Fluids":
            item.setForeground(0, QBrush(Qt.blue))
            anotheritem = self.treeModelWizard.itemAbove(item)
            anotheritem.setForeground(0, QBrush(Qt.black))

            myFlags["ModelWizardMode"] = "Fluids"
            ModelWizard.flagModelWizardActivated = False
            
        if item.text(indexTree) == "Coefficient form PDE":
            item.setForeground(0, QBrush(Qt.blue))

            myFlags["ModelWizardMode"] = "PDE"
            ModelWizard.flagModelWizardActivated = False

        


    def currentTreeWidgetConfiguration(self, tabs, tabMenu):
    
        if ModelWizard.flagModelWizardActivated == True:
            Modules.Matrix.Matrix.newMatrix(self)
        else:
         if myFlags["ModelWizardMode"] == "Solids":
            Tabs.hideElementsTab(tabs, tabMenu)
            Tabs.addTabElement(tabs, tabMenu)
            Tabs.hideElementTab(5, tabMenu)
            Tabs.hideElementTab(5, tabMenu)
            self.tboxMaterialsConditions.removeItem(2)


         if myFlags["ModelWizardMode"] == "Fluids":
            Tabs.hideElementsTab(tabs, tabMenu)
            Tabs.addTabElement(tabs, tabMenu)
            Tabs.hideElementTab(5, tabMenu)
            Tabs.hideElementTab(5, tabMenu)
            print(self.tboxMaterialsConditions.count())
            if self.tboxMaterialsConditions.count() == 3:
                self.tboxMaterialsConditions.insertItem(2, self.heatConvection, "Heat Convection")
           
            
         if myFlags["ModelWizardMode"] == "PDE":
            Tabs.hideElementsTab(tabs, tabMenu)
            Tabs.addTabElement(tabs, tabMenu)
            Tabs.hideElementTab(1, tabMenu)
            Tabs.hideElementTab(2, tabMenu)
            Tabs.hideElementTab(5, tabMenu)
            self.inputDepedentVarial.setEnabled(True)
            self.btnModelWizardReset.setEnabled(True)
            ModelWizard.flagModelWizardActivated = True
           
            


    

    

