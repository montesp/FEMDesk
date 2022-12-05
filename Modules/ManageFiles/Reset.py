from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush

import Modules.ModelWizard
from Modules.Dictionary.DFiles import *
from Modules.Dictionary.DMatrix import *
from Modules.Dictionary.DModelWizard import *


class Reset():
    def resetItemsCoefficientPDE(self):
        #Ocultar todos los items del ToolBox Coefficients PDE y dejar solo el item Initial Values
        for i in range(1, self.CoefficentForM.count()):
            self.CoefficentForM.setItemEnabled(i, False)

        for i, item in enumerate(self.CoefficientCheckBoxArray):
                self.CoefficientCheckBoxArray[i - 1].setChecked(False)
 
    def resetCoordinatesPDE(self):
        #Resetear todos los combobox de las secciones y dejarles solo el valor de 1
        for i, item in enumerate(self.arrayCmbRowColumns):
         for j, item in enumerate(self.arrayCmbRowColumns[i]):
                        self.arrayCmbRowColumns[i][j].clear()
                        self.arrayCmbRowColumns[i][j].addItem("1")

        #Limpiar todos los lineEdits de cada seccion
        for i, item in enumerate(self.arraylEditsCoefficientsPDE):
         for j, item in enumerate(self.arraylEditsCoefficientsPDE[i]):
                        self.arraylEditsCoefficientsPDE[i][j].setText("")
        
        #Resetear el combobox de Initial Values
        self.cmbInitialValues.clear()
        self.cmbInitialValues.addItem("u1")

    def resetItemsConfig(self):
        #Resetear el modo de input del diffusion matrix a 1 (isotrópico)
        diffusionMatrix["inputMode"] = 0
        self.cmbDiffusionCoef.setCurrentIndex(diffusionMatrix["inputMode"])
        noItemsCoeffM["noItems"] = 0
        noItemsCoeffM["items"] = 0
        initialValues["noVariables"] = 1
        self.inputDepedentVarial.setText(str(initialValues["noVariables"]))

    def resetUpdateFile(self):
         #Eliminar la dirección del archivo excel actual del QLabel
        self.lblDirectory.setText("")
        self.actionSaves.setEnabled(False)
        self.actionSave_As.setEnabled(False)
        self.actionClose.setEnabled(False)

        fileIndicator["*"] = ""
        #Eliminar la dirección del archivo excel en la memoria de la variable
        directory["dir"] = ""

    def resetModelWizard(self):
        #Resetear la configuracion del ModelWizard
        myFlags["ModelWizardMode"] = "None"
        self.itemSpace[0].setExpanded(False)
        self.item2D[0].setExpanded(False)
        self.itemPhysics[0].setExpanded(False)
        self.itemHeat[0].setExpanded(False)
        self.itemMath[0].setExpanded(False)
        self.itemFluids[0].setForeground(0, QBrush(Qt.black))
        self.itemPDE[0].setForeground(0, QBrush(Qt.black))
        self.itemSolids[0].setForeground(0, QBrush(Qt.black))
        Modules.ModelWizard.ModelWizard.flagModelWizardActivated = False
        Modules.Tabs.Tabs.hideElementsTab(self.tabs, self.tabWidgetMenu)
 
    def removeModelWizard(self):
        myFlags["ModelWizardMode"] = "None"
        Modules.ModelWizard.ModelWizard.flagModelWizardActivated = False
        Modules.Tabs.Tabs.hideElementsTab(self.tabs, self.tabWidgetMenu)

    def resetMaterials(self, material):
        material.__dataFigures = []
        self.lblFigureSelected.setText("")

    def resetConditions(self, conditions):
        conditions.sidesData = []
        self.lWBoundarys.clear()

    def resetFigures(self, canvas):
        tempList = []
        for poly in canvas.polyList:
            tempList.append(poly)
        for poly in tempList:
            canvas.deletePolygon(poly)