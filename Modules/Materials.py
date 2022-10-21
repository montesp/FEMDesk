from operator import index
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

    def currentDomains(self, lwDomains, canvas, tboxMaterialsConditions, cmbMaterial, lblMaterial, tableDomainsMaterials):
        solids = canvas.getSolids()

        if lwDomains.count() != 0:
            lwDomains.clear()
        else:
            tboxMaterialsConditions.hide()
            cmbMaterial.hide()
            lblMaterial.hide()
       
        rowCount = tableDomainsMaterials.rowCount()
        for i in range(rowCount):
            tableDomainsMaterials.removeRow(i)

        if len(solids) != 0:
                for indexPoly in range(len(solids)):
                    tableDomainsMaterials.insertRow(rowCount)
                    text = 'figura ' + str(indexPoly + 1)
                    lwDomains.addItem(text)
                    tableDomainsMaterials.setItem(indexPoly, 0, QTableWidgetItem(text))
                    tableDomainsMaterials.setItem(indexPoly, 1, QTableWidgetItem("No selected"))
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
        if cmbMaterial.currentText() == 'User defined':
            mainWin.heatConductionSolid.setFocus(True)
            mainWin.tboxMaterialsConditions.setItemEnabled(0, True)
            mainWin.tboxMaterialsConditions.setItemEnabled(1, True)
            mainWin.tboxMaterialsConditions.setItemEnabled(2, True)
            mainWin.tboxMaterialsConditions.setItemEnabled(3, False)
        else: 

            # here
            mainWin.tableDomains.setItem(0, 1, QTableWidgetItem(  str(mainWin.materialsDataBase[mainWin.cmbMaterial.currentIndex()-1][2]))) # Thermal conductivity
            mainWin.tableDomains.setItem(1, 1, QTableWidgetItem(str(mainWin.materialsDataBase[mainWin.cmbMaterial.currentIndex()-1][7]))) #Heat Capacity
            mainWin.tableDomains.setItem(2, 1, QTableWidgetItem(str(mainWin.materialsDataBase[mainWin.cmbMaterial.currentIndex()-1][8]))) #Density

            if mainWin.materialsDataBase[mainWin.cmbMaterial.currentIndex()-1][6] == 0:  #isotropic
                print('iso')
            elif mainWin.materialsDataBase[mainWin.cmbMaterial.currentIndex()-1][6] == 1 : #diagonal  
                print('diag')
            elif mainWin.materialsDataBase[mainWin.cmbMaterial.currentIndex()-1][6] == 2 : #symmetric   
                print('syme')
            elif mainWin.materialsDataBase[mainWin.cmbMaterial.currentIndex()-1][6] == 3 : #full
                print('full')


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
        else: # Material selected
            thermalConductiviy = [] # Thermal conductivity
            heatCapacity = str(win.materialsDataBase[win.cmbMaterial.currentIndex()-1][7]) #Heat Capacity
            density = str(win.materialsDataBase[win.cmbMaterial.currentIndex()-1][8]) #Density
            
            if win.cmbNameMaterials.currentIndex() != -1 :
                if win.materialsDataBase[win.cmbNameMaterials.currentIndex()][6] == 0:  #isotropic
                    thermalConductiviy.append(str(win.materialsDataBase[win.cmbMaterial.currentIndex()-1][2]))
                elif win.materialsDataBase[win.cmbNameMaterials.currentIndex()][6] == 1 : #diagonal 
                    thermalConductiviy.append(str(win.materialsDataBase[win.cmbMaterial.currentIndex()-1][2]))
                    thermalConductiviy.append(0)
                    thermalConductiviy.append(0)
                    thermalConductiviy.append(str(win.materialsDataBase[win.cmbMaterial.currentIndex()-1][5]))
                elif win.materialsDataBase[win.cmbNameMaterials.currentIndex()][6] == 2 : #symmetric
                    thermalConductiviy.append(str(win.materialsDataBase[win.cmbMaterial.currentIndex()-1][2]))
                    thermalConductiviy.append(str(win.materialsDataBase[win.cmbMaterial.currentIndex()-1][3]))
                    thermalConductiviy.append(str(win.materialsDataBase[win.cmbMaterial.currentIndex()-1][4]))
                    thermalConductiviy.append(str(win.materialsDataBase[win.cmbMaterial.currentIndex()-1][5]))
                elif win.materialsDataBase[win.cmbNameMaterials.currentIndex()][6] == 3 : #full
                    thermalConductiviy.append(str(win.materialsDataBase[win.cmbMaterial.currentIndex()-1][2]))
                    thermalConductiviy.append(str(win.materialsDataBase[win.cmbMaterial.currentIndex()-1][3]))
                    thermalConductiviy.append(str(win.materialsDataBase[win.cmbMaterial.currentIndex()-1][4]))
                    thermalConductiviy.append(str(win.materialsDataBase[win.cmbMaterial.currentIndex()-1][5]))
    def add(self, mainWin):
        rowCount = mainWin.tableDomainsMaterials.rowCount()
        mainWin.tableDomainsMaterials.insertRow(rowCount)
        



        mainWin.tableDomainsMaterials.clear()


        if rowCount != 0:
            mainWin.tableDomainsMaterials.setItem(rowCount, 0, QTableWidgetItem(1)) 
            mainWin.tableDomainsMaterials.setItem(rowCount, 1, QTableWidgetItem("No selected"))
        else:
            mainWin.tableDomainsMaterials.setItem(0, 0, QTableWidgetItem(str(self.figure)))
            mainWin.tableDomainsMaterials.setItem(0, 1, QTableWidgetItem("No selected"))

        


