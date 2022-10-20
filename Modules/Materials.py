from Modules.Dictionary.DMatrix import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QColor
from PyQt5.QtWidgets import QTableWidgetItem
class Materials():
    def __init__(self):
        self.figure = None

    def getFigure(self):
        return self.figure
    
    def setFigure(self, figure):
        self.figure = figure

    def currentHeatConduction(self, comb, ar):
        for i, item in enumerate(ar):
            ar[i].clear()
            ar[i].setEnabled(False)

        if comb.currentIndex() == 0:
            diffusionMatrix["inputMode"] = 0
            ar[0].setEnabled(True)
        if comb.currentIndex() == 1:
            diffusionMatrix["inputMode"] = 1
            ar[1].setEnabled(True)
            ar[4].setEnabled(True)
            ar[2].insert("0")
            ar[3].insert("0")
        if comb.currentIndex() == 2:
            diffusionMatrix["inputMode"] = 2
            ar[1].setEnabled(True)
            ar[2].setEnabled(True)
            ar[4].setEnabled(True)
        if comb.currentIndex() == 3:
            diffusionMatrix["inputMode"] = 3
            ar[1].setEnabled(True)
            ar[2].setEnabled(True)
            ar[3].setEnabled(True)
            ar[4].setEnabled(True)

    def currentTextSimmetry(self, comb, ar):
        if comb.currentIndex() == 2:
            ar[3].clear()
            ar[3].insert(ar[1].text())

    def currentDomains(self, lwDomains, canvas, tboxMaterialsConditions, cmbMaterial, lblMaterial):
        solids = canvas.getSolids()

        if lwDomains.count() != 0:
            lwDomains.clear()
        else:
            tboxMaterialsConditions.hide()
            cmbMaterial.hide()
            lblMaterial.hide()

        if len(solids) != 0:
                for indexPoly in range(len(solids)):
                    text = 'figura ' + str(indexPoly + 1)
                    lwDomains.addItem(text)
                tboxMaterialsConditions.show()
                cmbMaterial.show()
                lblMaterial.show()
    
    def selectionType(self,win):
        index = win.cmbSelection.currentIndex()
        text = win.cmbSelection.itemText(index)

        if text == "All domains":
            win.listDomains.setDisabled(True)
        else:
            win.listDomains.setDisabled(False)

    def currentDomainSelected(self, element, canvas):
        index = element.currentRow()
        self.setFigure(index)

        solids = canvas.getSolids()
        paint = QBrush(QColor(255,0,0,50))
        for item in solids:
            item.setBrush(QBrush(QColor(0, 0, 0, 50)))
            
        solids[index].setBrush(paint)

    def currentMaterialSelection(self,cmbMaterial, mainWin):
        # print(cmbMaterial.currentText())
        if cmbMaterial.currentText() == 'User defined':
            mainWin.heatConductionSolid.setFocus(True)
            # mainWin.therModynamicsSolid.close()
            # mainWin.heatConvection.close()
            # mainWin.propertiesFromTheLibrary.close()
            mainWin.tboxMaterialsConditions.setItemEnabled(0, True)
            mainWin.tboxMaterialsConditions.setItemEnabled(1, True)
            mainWin.tboxMaterialsConditions.setItemEnabled(2, True)
            mainWin.tboxMaterialsConditions.setItemEnabled(3, False)
        else: 
            # mainWin.heatConductionSolid.close()
            # mainWin.therModynamicsSolid.close()
            # mainWin.heatConvection.close()
            mainWin.propertiesFromTheLibrary.setFocus(True)
            mainWin.tboxMaterialsConditions.setItemEnabled(0, False)
            mainWin.tboxMaterialsConditions.setItemEnabled(1, False)
            mainWin.tboxMaterialsConditions.setItemEnabled(2, False)
            mainWin.tboxMaterialsConditions.setItemEnabled(3, True)

    def applyMaterialChanges(self, win):
        if win.cmbMaterial.currentText() == "User defined":
            headConductionSelection = win.cmbHeatConduction.currentText()
            if headConductionSelection == "Isotropic":
                inputK = win.inputK.text()
            elif headConductionSelection == "Diagonal":
                inputKD1 = win.inputKD1.text()
                inputKD2 = 0
                inputKD3 = 0
                inputKD4 = win.inputKD4.text()
            elif headConductionSelection == "Symmetric":
                inputKD1 = win.inputKD1.text()
                inputKD2 = win.inputKD2.text()
                inputKD3 = win.inputKD3.text()
                inputKD4 = win.inputKD4.text()
            elif headConductionSelection == "Full":
                inputKD1 = win.inputKD1.text()
                inputKD2 = win.inputKD2.text()
                inputKD3 = win.inputKD3.text()
                inputKD4 = win.inputKD4.text()
            rho = win.inputRho.text()
            cp = win.inputConsantPressure
        else:
            print('material')

            if win.cmbNameMaterials.currentIndex() != -1 :
                if win.materialsDataBase[win.cmbNameMaterials.currentIndex()][6] == 0:  #isotropic
                    pass
                elif win.materialsDataBase[win.cmbNameMaterials.currentIndex()][6] == 1 : #diagonal  
                    pass
                elif win.materialsDataBase[win.cmbNameMaterials.currentIndex()][6] == 2 : #symmetric   
                    pass
                elif win.materialsDataBase[win.cmbNameMaterials.currentIndex()][6] == 3 : #full
                    pass

    def table(self,table):
        table.setItem(0, 1, QTableWidgetItem("Text in column 1"))
        table.setItem(1, 1, QTableWidgetItem("Text in column 2"))
        table.setItem(2, 1, QTableWidgetItem("Text in column 3"))



