
import enum
from tkinter import dialog
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QBrush, QColor

from Modules.Dictionary.DMatrix import *
import Modules.ManageFiles.ManageFiles


class CoefficientsPDE():
    def currentCoefficentSelection(win):
        index = win.cmbCoefficientSelection.currentIndex()
        text = win.cmbCoefficientSelection.itemText(index)

        if text == "All domains":
            win.lWDomainsPDE.setDisabled(True)
            canvas = win.canvas
            solids = canvas.getSolids()
            paint = QBrush(QColor(255,0,0,50))

            if solids:
                # Componentes del tool box
                win.btnMaterialApply.setEnabled(True)
                win.btnMaterialsReset.setEnabled(True)
                win.btnMaterialsHelp.setEnabled(True)
                win.lblMaterial.show()
                win.cmbMaterial.show()
                win.tboxMaterialsConditions.show()
                win.lblFigureSelected.setText("All domains")

            for item in solids:
                item.setBrush(paint)

        else:
            win.lWDomainsPDE.setDisabled(False)
            canvas = win.canvas
            solids = canvas.getSolids()
            paint = QBrush(QColor(0,0,0,50))
            
            # win.btnMaterialApply.setEnabled(False)
            # win.btnMaterialsReset.setEnabled(False)
            # win.btnMaterialsHelp.setEnabled(False)
            # win.lblMaterial.hide()
            # win.cmbMaterial.hide()
            # win.tboxMaterialsConditions.hide()
            # win.lblFigureSelected.setText("")


            for item in solids:
                item.setBrush(paint)


    def currentDomainSelected(win, element):
        index = int(element.currentRow())
        win.lblFigureSelected.setText("Figura " + str(index + 1))

        # Obtiene la figuras que son solidas
        solids = win.canvas.getSolids()
        paint = QBrush(QColor(255,0,0,50))

        # Pinta todos los poligonos para resetear todos los valores
        for item in solids:
            item.setBrush(QBrush(QColor(0, 0, 0, 50)))
        # Pinta la figura seleccionada
        solids[index].setBrush(paint)
        # Ya tienes el indice con el index y tienes los dominions con los solids
        # Sigue aqui 



    def CheckCoefficient(ar):
        CoefficientArray = []
    
        for index, item in enumerate(ar):
            if ar[index].isChecked() == True:
                CoefficientArray.append(index + 1)
        if len(CoefficientArray) != 0:
         noItemsCoeffM["noItems"] = len(CoefficientArray)
         noItemsCoeffM["items"] = CoefficientArray
        else:
         noItemsCoeffM["noItems"] = 0
         noItemsCoeffM["items"] = [0]
        return CoefficientArray


    def clearCoefficientTbox(self,section, arrayCoeff, arrayCheck):
        for i in range(section.count()):
            section.removeItem(1)

        section.insertItem(100, arrayCoeff[9], arrayCheck[9])

    def currentCoefficientForM(self,section, check, arrayCoeff, arrayCheck):
        position = 1
        for i in range(section.count()):
            section.removeItem(1)

        section.insertItem(100, arrayCoeff[9], arrayCheck[9])

        Modules.ManageFiles.ManageFiles.FileData.checkUpdateFile(self)

        for i in check:
            if(i != 0):
                section.insertItem(position, arrayCoeff[i], arrayCheck[i])
                position+=1
        
        Modules.ManageFiles.ManageFiles.FileData.checkUpdateFile(self)

    def currentDiffusionCoef(self, comb, ar):
        for i, item in enumerate(ar):
            ar[i].clear()
            ar[i].setEnabled(False)

        if comb.currentIndex() == 0:
            diffusionMatrix["inputMode"] = 0
            ar[0].setEnabled(True)
        elif comb.currentIndex() == 1:
            diffusionMatrix["inputMode"] = 1
            ar[1].setEnabled(True)
            ar[4].setEnabled(True)
            ar[2].insert("0")
            ar[3].insert("0")
        elif comb.currentIndex() == 2:
            diffusionMatrix["inputMode"] = 2
            ar[1].setEnabled(True)
            ar[2].setEnabled(True)
            ar[4].setEnabled(True)
        elif comb.currentIndex() == 3:
            diffusionMatrix["inputMode"] = 3
            ar[1].setEnabled(True)
            ar[2].setEnabled(True)
            ar[3].setEnabled(True)
            ar[4].setEnabled(True)

    def currentTextSimmetry(self, comb, ar):
        if comb.currentIndex() == 2:
            ar[3].clear()
            ar[3].insert(ar[2].text())

            
    
    