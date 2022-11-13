from PyQt5.QtWidgets import QMessageBox
from Modules.Dictionary.DConditionsPDE import *
from PyQt5 import QtCore
import numpy as np
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPen, QColor

class ConditionsPDEMatrix():

    matrix3D = np.empty([1,1,1], dtype='U256')
    def changeMatrixDimensions(self, n, canvas):
            ConditionsPDEMatrix.matrix3D = np.empty([len(canvas.getEdges()),n, n], dtype='U256')
            print("Matrices de Conditions PDE")
            print(ConditionsPDEMatrix.matrix3D)
            print(len(canvas.getEdges()))
            
       
class ConditionsPDE():
    def createMatrix(self, canvas):
        try:
            n = int(self.inputDepedentVarial.text())
            ConditionsPDEMatrix.changeMatrixDimensions(self, n, canvas)
        except Exception:
             QMessageBox.warning(self, "Important message", "Solo puede ingresar valores numericos")
             return

    def currentElementSelectElementPDE(element, canvas, lblFigureSelected):
        # Obtener el index de la figura
        index = int(element.text())
        # Obtiene el numero de lados
        edges = canvas.getEdges()
        # La linea que esta en el momento --> con esta vas a trabajar
        line = edges[index-1]

        # Colores por defectos de las lineas
        LUBronze = QColor(156, 87, 20)
        defaultColor = QPen(LUBronze)
        defaultColor.setWidth(3)
        # Devuelve todos los colores de la figura
        for elem in edges:
            elem.setPen(defaultColor)
        # El color rojo para guardar 
        paint = QPen(Qt.red)
        paint.setWidth(5)
        # Poner el color en la linea
        line.setPen(paint)
        # Poner el numero de figura en el lbl 
        lblFigureSelected.setText("Lado " + str(index))



    def changeMatrixCoefficient(currentIndexRow, currentIndexColumn, Elements):
        indexDictionary = {
            "00": DC00,
            "01": DC01,
            "02": DC02,
            "10": DC10,
            "11": DC11,
            "12": DC12,
            "20": DC20,
            "21": DC21,
            "22": DC22
        }

        if (currentIndexRow == 0 and currentIndexColumn == 0):
            indexDictionary["00"](Elements)
        elif (currentIndexRow == 0 and currentIndexColumn == 1):
            indexDictionary["01"](Elements)
        elif (currentIndexRow == 0 and currentIndexColumn == 2):
            indexDictionary["02"](Elements)
        elif (currentIndexRow == 1 and currentIndexColumn == 0):
            indexDictionary["10"](Elements)
        elif (currentIndexRow == 1 and currentIndexColumn == 1):
            indexDictionary["11"](Elements)
        elif (currentIndexRow == 1 and currentIndexColumn == 2):
            indexDictionary["12"](Elements)
        elif (currentIndexRow == 2 and currentIndexColumn == 0):
            indexDictionary["20"](Elements)
        elif (currentIndexRow == 2 and currentIndexColumn == 1):
            indexDictionary["21"](Elements)
        elif (currentIndexRow == 2 and currentIndexColumn == 2):
            indexDictionary["22"](Elements)
    
    def activateIndexAlpha(alphaXData, alphaYData, currentIndexRow, currentIndexColumn ):

        indexDictionary = {
            "00": IndexA00,
            "01": IndexA01,
            "02": IndexA02,
            "10": IndexA10,
            "11": IndexA11,
            "12": IndexA12,
            "20": IndexA20,
            "21": IndexA21,
            "22": IndexA22
        }


        if (currentIndexRow == 0 and currentIndexColumn == 1):
            indexDictionary["01"](alphaXData, alphaYData)
        elif (currentIndexRow == 0 and currentIndexColumn == 2):
            indexDictionary["02"](alphaXData, alphaYData)
        elif (currentIndexRow == 1 and currentIndexColumn == 0):
            indexDictionary["10"](alphaXData, alphaYData)
        elif (currentIndexRow == 1 and currentIndexColumn == 1):
            indexDictionary["11"](alphaXData, alphaYData)
        elif (currentIndexRow == 1 and currentIndexColumn == 2):
            indexDictionary["12"](alphaXData, alphaYData)
        elif (currentIndexRow == 2 and currentIndexColumn == 0):
            indexDictionary["20"](alphaXData, alphaYData)
        elif (currentIndexRow == 2 and currentIndexColumn == 1):
            indexDictionary["21"](alphaXData, alphaYData)
        elif (currentIndexRow == 2 and currentIndexColumn == 2):
            indexDictionary["22"](alphaXData, alphaYData)

    # currentRowEdit
    def currentRowEdit(currentIndexRow, diffusionCoefElements):
        if currentIndexRow == 0:
            diffusionCoefElements[1].setEnabled(False)
            diffusionCoefElements[2].setEnabled(False)
        elif currentIndexRow == 1:
            diffusionCoefElements[1].setEnabled(True)
            diffusionCoefElements[2].setEnabled(False)
        elif currentIndexRow == 2:
            diffusionCoefElements[1].setEnabled(True)
            diffusionCoefElements[2].setEnabled(True)

    def disabledRowEdit(dataX, dataY, currentIndexRow):
        if currentIndexRow == 0:
            dataX[1].setEnabled(False)
            dataY[1].setEnabled(False)
            dataX[2].setEnabled(False)
            dataY[2].setEnabled(False)

        elif currentIndexRow == 1:
            dataX[1].setEnabled(True)
            dataY[1].setEnabled(True)
            dataX[2].setEnabled(False)
            dataY[2].setEnabled(False)
        elif currentIndexRow == 2:
            dataX[1].setEnabled(True)
            dataY[1].setEnabled(True)
            dataX[2].setEnabled(True)
            dataY[2].setEnabled(True)

    def turnZeroFlux(self, arrayConditionPDE):
        if self.chkZeroFlux.checkState() == 2:
            self.toolBoxTypeOfCon.setItemEnabled(1, False)
            self.toolBoxTypeOfCon.setItemEnabled(0, False)
            arrayConditionPDE[0].setEnabled(False)
            arrayConditionPDE[1].setEnabled(False)
        else:
            self.toolBoxTypeOfCon.setItemEnabled(1, True)
            self.toolBoxTypeOfCon.setItemEnabled(0, True)
            arrayConditionPDE[0].setEnabled(True)
            arrayConditionPDE[1].setEnabled(True)


    def applyConditionVariable(self, comboboxCondition):
        arrayComboboxText = []
        if comboboxCondition.count() > 0:
            for i in range(comboboxCondition.count()):
             arrayComboboxText.append(int(comboboxCondition.itemText(i).replace('u', '')))
            ConditionsPDE.searchVariableinCombobox(self, 
            comboboxCondition, arrayComboboxText)
        else:
            comboboxCondition.addItem(self.cmbZeroFlux.currentText())

    def searchVariableinCombobox(self, comboboxCondition, arrayComboboxText):
        if int(self.cmbZeroFlux.currentText().replace('u', '')) not in arrayComboboxText:
            updatedCombobox = ConditionsPDE.updateCombobox(self, 
            comboboxCondition, arrayComboboxText)
            ConditionsPDE.putCurrentIndexCondition(self, updatedCombobox)

    def updateCombobox(self, comboboxCondition, arrayComboboxText):
            arrayComboboxText.append(int(self.cmbZeroFlux.currentText().replace('u', '')))
            arrayComboboxText.sort()
            comboboxCondition.clear()
            for i in range(len(arrayComboboxText)):
                comboboxCondition.addItem("u" + str(arrayComboboxText[i]))
            return comboboxCondition

    def putCurrentIndexCondition(self, updatedCombobox):
        index = updatedCombobox.findText(self.cmbZeroFlux.currentText(), QtCore.Qt.MatchFixedString)
        updatedCombobox.setCurrentIndex(index)
