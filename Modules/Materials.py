from Modules.Dictionary.DMatrix import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QColor
class Materials():
    def currentHeatConduction(comb, ar):
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

    def currentTextSimmetry(comb, ar):
        if comb.currentIndex() == 2:
            ar[3].clear()
            ar[3].insert(ar[1].text())

    def currentDomains(lwDomains, canvas, tboxMaterialsConditions, cmbMaterial, lblMaterial):
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
    
    def selectionType(win):
        index = win.cmbSelection.currentIndex()
        text = win.cmbSelection.itemText(index)

        if text == "All domains":
            win.listDomains.setDisabled(True)
        else:
            win.listDomains.setDisabled(False)

    def currentDomainSelected(element, canvas):
        index = element.currentRow()
        solids = canvas.getSolids()
        paint = QBrush(QColor(255,0,0,50))
        for item in solids:
            item.setBrush(QBrush(QColor(0, 0, 0, 50)))
            
        solids[index].setBrush(paint)

    def currentMaterialSelection(cmbMaterial, mainWin):
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
