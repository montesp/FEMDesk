
import enum
from tkinter import dialog

import numpy as np
from PyQt5.QtGui import QBrush, QColor
from PyQt5.QtWidgets import QMessageBox

import Modules.ManageFiles.ManageFiles
from Modules.Dictionary.DMatrix import *
from Modules.ManageFiles.Reset import *
from Modules.Matrix.Matrix import allNewMatrix
from Modules.Matrix.MatrixData import MatrixData


class CoefficientsPDE():
    flagAllDomains = False
    def __init__(self):
        self.__allMatrixCoefficentsPDE = None

    def currentCoefficentSelection(self, win):
        index = win.cmbCoefficientSelection.currentIndex()
        text = win.cmbCoefficientSelection.itemText(index)

        if text == "All domains":
            win.lWDomainsPDE.setDisabled(True)
            canvas = win.canvas
            solids = canvas.getSolids()
            paint = QBrush(QColor(255,0,0,50))

            win.CoefficentForM.show()
            win.lblFigureSelected.setText("All domains")


            for item in solids:
                item.setBrush(paint)

            win.lWDomainsPDE.setEnabled(False)

        else:
            win.lWDomainsPDE.setDisabled(False)
            canvas = win.canvas
            solids = canvas.getSolids()
            paint = QBrush(QColor(0,0,0,50))

            win.CoefficentForM.hide()
            win.lblFigureSelected.setText("")


            for item in solids:
                item.setBrush(paint)

            win.lWDomainsPDE.setEnabled(True)

    def currentItemDomainPDESelected(self, win):
        win.CoefficentForM.show()

    def changeDomainConfigurationCoefficientPDE(self, win):
        Reset.resetItemsCoefficientPDE(win)

        #Limpiar todos los lineEdits de cada seccion
        for i, item in enumerate(win.arraylEditsCoefficientsPDE):
         for j, item in enumerate(win.arraylEditsCoefficientsPDE[i]):
                        win.arraylEditsCoefficientsPDE[i][j].setText("")

        for i in allNewMatrix.matrixItemsActivated[domains["domain"]]:
            if i == '':
                pass
            else:
                Modules.ManageFiles.ManageFiles.Update.currentData(win, int(i))
                win.CoefficientCheckBoxArray[int(i) - 1].setChecked(True)
                win.CoefficentForM.setItemEnabled(int(i), True)

    def selectAllDomains(self):
        if self.cmbCoefficientSelection.currentIndex() == 0:
            CoefficientsPDE.flagAllDomains = False
            MatrixData.flagAllDomains = False
        else:
            CoefficientsPDE.flagAllDomains = True
            MatrixData.flagAllDomains = True

    def currentDomainSelected(self, win, element):
        index = int(element.currentRow())
        win.lblFigureSelected.setText("Figura " + str(index + 1))
        domains["domain"] = index
        # Obtiene la figuras que son solidas
        solids = win.canvas.getSolids()
        paint = QBrush(QColor(255,0,0,50))

        # Pinta todos los poligonos para resetear todos los valores
        for item in solids:
            item.setBrush(QBrush(QColor(0, 0, 0, 50)))
        # Pinta la figura seleccionada
        solids[index].setBrush(paint)

        #Cambiar los datos de coefficient pde según el dominio seleccionado
        self.changeDomainConfigurationCoefficientPDE(win)
        win.CoefficentForM.setItemEnabled(9, True)


    
    def CheckCoefficient(self, ar):
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

        print("Dominios")
        print(allNewMatrix.domains)
        if CoefficientsPDE.flagAllDomains == False:
            #Vaciar elementos del dominio en cuestion
            for i in range(len(allNewMatrix.matrixItemsActivated[domains["domain"]])):
                allNewMatrix.matrixItemsActivated[domains["domain"]][i] = ''
            #Insertar nuevos valores
            for i, item in enumerate(CoefficientArray):
                allNewMatrix.matrixItemsActivated[domains["domain"]][i] = str(item) 
        else:
            for index in range(allNewMatrix.domains):
                #Vaciar elementos del dominio en cuestion
                for i in range(len(allNewMatrix.matrixItemsActivated[index])):
                    allNewMatrix.matrixItemsActivated[index][i] = ''
                #Insertar nuevos valores
                for i, item in enumerate(CoefficientArray):
                    allNewMatrix.matrixItemsActivated[index][i] = str(item)
            
        print("Matriz de items activados")
        print(allNewMatrix.matrixItemsActivated)

        self.matrixCoefficents = allNewMatrix
        return CoefficientArray


    def clearCoefficientTbox(self, section, arrayCoeff, arrayCheck):
        for i in range(section.count()):
            if i != 0 and i != 9:
                section.setItemEnabled(i, False)


    def currentCoefficientForM(self, section, check, arrayCoeff, arrayCheck):
        position = 1
        for i in range(section.count()):
            if i != 0 and i != 9:
                section.setItemEnabled(i, False)

        # section.insertItem(100, arrayCoeff[9], arrayCheck[9])

        Modules.ManageFiles.ManageFiles.FileData.checkUpdateFile(self)

        # print(check)
        for i in check:
            section.setItemEnabled(i, True)

        #     if(i != 0):
        #         section.insertItem(position, arrayCoeff[i], arrayCheck[i])
        #         position+=1
        
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


    def showMatrixInfo(self):
        print(self.__allMatrixCoefficentsPDE)