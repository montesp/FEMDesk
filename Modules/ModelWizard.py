from Modules.Tabs import *
from PyQt5.QtGui import QBrush
from PyQt5.QtCore import Qt

class ModelWizard:
    def hideInitialTabs(tabs, tabMenu):
        Tabs.hideElementsTab(tabs, tabMenu)

    flagHeatTransferSolids = False
    flagHeatTransferFluids = False
    flagCoefficientPDE = False

    def currentTreeItem(self, item, indexTree):
        if item.text(indexTree) == "Heat Transfer in Solids":
            item.setForeground(0, QBrush(Qt.blue))
            anotheritem = self.treeModelWizard.itemBelow(item)
            anotheritem.setForeground(0, QBrush(Qt.black))
            ModelWizard.flagSolid = True
            ModelWizard.flagFluid = False

        if item.text(indexTree) == "Heat Transfer in Fluids":
            item.setForeground(0, QBrush(Qt.blue))
            anotheritem = self.treeModelWizard.itemAbove(item)
            anotheritem.setForeground(0, QBrush(Qt.black))
            ModelWizard.flagSolid = False
            ModelWizard.flagFluid = True
            
        if item.text(indexTree) == "Coefficient form PDE":
            item.setForeground(0, QBrush(Qt.blue))
            ModelWizard.flagCoefficientPDE = True


    def currentTreeWidgetConfiguration(self, tabs, tabMenu):
        if ModelWizard.flagSolid == True and ModelWizard.flagCoefficientPDE == True:
            Tabs.addTabElement(tabs, tabMenu)
            Tabs.hideElementTab(1, tabMenu)
            self.cmbGeneralStudie.show()
            self.lblGeneralStudie.show()
            self.tboxModelWizard.show()


    

    

