
from PyQt5.QtWidgets import QMessageBox
from Modules.Dictionary.DMatrix import *
from PyQt5 import QtGui, QtCore



class MatrixData():
    def updateCombobox(self, n):
        #Actualizar el combobox según el numero de variables dependientes
        for index, item in enumerate(self.CoefficientCheckBoxArray):
                for j, item in enumerate(self.arrayCmbRowColumns[index]):
                        self.arrayCmbRowColumns[index][j].clear()

                for j, item in enumerate(self.arrayCmbRowColumns[index]):
                    for i in range(1, n + 1):
                        self.arrayCmbRowColumns[index][j].addItem(str(i))
        self.cmbInitialValues.clear()

        for i in range(1, n + 1):
            self.cmbInitialValues.addItem("u" + str(i))

    def setDiffusionMatrixSingleData(self, x, y, diffusionComb, lineEdit, matrix):
     #try:
        ar = []
        ar.append(float(lineEdit[0][0].text()))
        ar.append(float(lineEdit[0][0].text()))
        ar.append(float(lineEdit[0][0].text()))
        ar.append(float(lineEdit[0][0].text()))
        ar.append(diffusionComb.currentIndex())
        matrix[x,y] = str(ar)
        print(matrix)
        self.insertMatrix(matrix)
     #except Exception:
        #QMessageBox.warning(self, "Important message", "Solo puede ingresar valores numericos")
        #return
    
    def setDiffusionMatrixMultipleData(self, x, y, diffusionComb, lineEdit, matrix):
     try:
        ar = []
        ar.append(float(lineEdit[0][1].text()))
        ar.append(float(lineEdit[0][2].text()))
        ar.append(float(lineEdit[0][3].text()))
        ar.append(float(lineEdit[0][4].text()))
        ar.append(diffusionComb.currentIndex())
        matrix[x,y] = str(ar)
        print(matrix)
        self.insertMatrix(matrix)
     except Exception:
        QMessageBox.warning(self, "Important message", "Solo puede ingresar valores numericos")
        return

    def setMatrixSingleData(self, x, y, lineEdit, matrix):
     try:
        data = float(lineEdit.text())
        matrix[x,y] = data
        self.insertMatrix(matrix)
     except Exception:
        QMessageBox.warning(self, "Important message", "Solo puede ingresar valores numericos")
        return

    def setMatrixDoubleData(self, x, y, lineEdit, lineEdit2, matrix):
     try:
        ar = []
        ar.append(float(lineEdit.text()))
        ar.append(float(lineEdit2.text()))
        matrix[x,y] = str(ar)
        self.insertMatrix(matrix)
     except Exception:
        QMessageBox.warning(self, "Important message", "Solo puede ingresar valores numericos")
        return

    def setVectorSingleData(self, x, lineEdit, matrix):
     try:
        self.cell.insert(float(lineEdit.text()))
        matrix[x] = lineEdit.text()
        self.insertVector(matrix)
     except Exception:
        QMessageBox.warning(self, "Important message", "Solo puede ingresar valores numericos")
        return

    def setVectorDoubleData(self, x, lineEdit, lineEdit2, matrix):
     try:
        ar = []
        ar.append(float(lineEdit.text()))
        ar.append(float(lineEdit2.text()))
        self.cell.insert(str(ar))
        matrix[x] = str(ar)
        self.insertVector(matrix)
     except Exception:
        QMessageBox.warning(self, "Important message", "Solo puede ingresar valores numericos")
        return

    def pullAndFormatDiffusionCell(self, x, y, matrix):
        arrMatrix = matrix[x][y]
        arrMatrix = arrMatrix.replace(" ","")
        arrMatrix = arrMatrix.strip('[]')
        arrMatrix = arrMatrix.split(',')
        floatMatrix = ['{0:g}'.format(float(i))  for i in arrMatrix]
        floatMatrix = floatMatrix[:-1]
        self.cell.insert(str(floatMatrix))

        text = self.cell.text()
        fm = QtGui.QFontMetrics(self.cell.font())
        pixelsWide = fm.width(text)
        self.cell.setFixedSize(QtCore.QSize(pixelsWide + 12, 70))

    def pullAndFormatCell(self, x, y, matrix):
      self.cell.insert(matrix[x][y])
      text = self.cell.text()
      fm = QtGui.QFontMetrics(self.cell.font())
      pixelsWide = fm.width(text)
      self.cell.setFixedSize(QtCore.QSize(pixelsWide + 12, 70))