from Modules.Tabs import *
from PyQt5.QtGui import QBrush
from PyQt5.QtCore import Qt
import Modules.Matrix
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

            ModelWizard.flagHeatTransferSolids= True
            ModelWizard.flagHeatTransferFluids = False
            ModelWizard.flagCoefficientPDE = False
            ModelWizard.flagModelWizardActivated = False

        if item.text(indexTree) == "Heat Transfer in Fluids":
            item.setForeground(0, QBrush(Qt.blue))
            anotheritem = self.treeModelWizard.itemAbove(item)
            anotheritem.setForeground(0, QBrush(Qt.black))

            ModelWizard.flagHeatTransferSolids = False
            ModelWizard.flagHeatTransferFluids = True
            ModelWizard.flagCoefficientPDE = False
            ModelWizard.flagModelWizardActivated = False
            
        if item.text(indexTree) == "Coefficient form PDE":
            item.setForeground(0, QBrush(Qt.blue))

            ModelWizard.flagHeatTransferSolids = False
            ModelWizard.flagHeatTransferFluids = False
            ModelWizard.flagCoefficientPDE = True
            ModelWizard.flagModelWizardActivated = False



    def currentTreeWidgetConfiguration(self, tabs, tabMenu):
        if ModelWizard.flagModelWizardActivated == True:
            Modules.Matrix.Matrix.newMatrix(self)
        else:
         if ModelWizard.flagHeatTransferSolids == True:
            Tabs.hideElementsTab(tabs, tabMenu)
            Tabs.addTabElement(tabs, tabMenu)
            Tabs.hideElementTab(5, tabMenu)
            Tabs.hideElementTab(5, tabMenu)
            self.tboxMaterialsConditions.removeItem(2)

         if ModelWizard.flagHeatTransferFluids == True:
            Tabs.hideElementsTab(tabs, tabMenu)
            Tabs.addTabElement(tabs, tabMenu)
            Tabs.hideElementTab(5, tabMenu)
            Tabs.hideElementTab(5, tabMenu)
            print(self.tboxMaterialsConditions.count())
            if self.tboxMaterialsConditions.count() == 3:
                self.tboxMaterialsConditions.insertItem(2, self.heatConvection, "Heat Convection")


         if ModelWizard.flagCoefficientPDE == True:
            Tabs.hideElementsTab(tabs, tabMenu)
            Tabs.addTabElement(tabs, tabMenu)
            Tabs.hideElementTab(1, tabMenu)
            Tabs.hideElementTab(2, tabMenu)
            Tabs.hideElementTab(5, tabMenu)
            self.inputDepedentVarial.setEnabled(True)
            self.btnModelWizardReset.setEnabled(True)
            ModelWizard.flagModelWizardActivated == True



