
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QMessageBox

from Modules.Dictionary.DMatrix import *
import numpy as np

class MatrixData():
    domains = 0
    flagAllDomains = False
    def updateCombobox(self, n):
        #Actualizar el combobox según el numero de variables dependientes
        for index, item in enumerate(self.CoefficientCheckBoxArray):
                for j, item in enumerate(self.arrayCmbRowColumns[index]):
                        self.arrayCmbRowColumns[index][j].clear()

                for j, item in enumerate(self.arrayCmbRowColumns[index]):
                    for i in range(1, n + 1):
                        self.arrayCmbRowColumns[index][j].addItem(str(i))
        self.cmbZeroFlux.clear()
        self.cmbInitialValues.clear()
      
        #Actualizar combobox de Conditions PDE
        for i in range(1, n + 1):
            self.cmbZeroFlux.addItem("u" + str(i))

         #Actualizar Combobox de los valores iniciales
        for i in range(1, n + 1):
            self.cmbInitialValues.addItem("u" + str(i))

    def setDiffusionMatrixSingleData(self, x, y, diffusionComb, lineEdit, matrix, allMatrix):
     try:
        ar = []
        ar.append(float(lineEdit[0][0].text()))
        ar.append(float(lineEdit[0][0].text()))
        ar.append(float(lineEdit[0][0].text()))
        ar.append(float(lineEdit[0][0].text()))
        ar.append(diffusionComb.currentIndex())
        print('dominios desde diffusion matrix')
        print(MatrixData.domains)
        if MatrixData.flagAllDomains == False:
         matrix[x,y] = str(ar)
        else:
         for i in range(MatrixData.domains):
          allMatrix[i][0][x][y] = str(ar)
        print(allMatrix)
        self.insertMatrix(matrix)
        QMessageBox.about(self, "Important message", "Information added successfuly")
     except Exception:
        QMessageBox.warning(self, "Important message", "You can only enter numeric values")
        return
    
    def setDiffusionMatrixMultipleData(self, x, y, diffusionComb, lineEdit, matrix, allMatrix):
     try:
        ar = []
        ar.append(float(lineEdit[0][1].text()))
        ar.append(float(lineEdit[0][2].text()))
        ar.append(float(lineEdit[0][3].text()))
        ar.append(float(lineEdit[0][4].text()))
        ar.append(diffusionComb.currentIndex())
        if MatrixData.flagAllDomains == False:
         matrix[x,y] = str(ar)
         print(matrix)
        else:
         for i in range(MatrixData.domains):
            allMatrix[i][0][x][y] = str(ar)
        print(allMatrix)
        self.insertMatrix(matrix)
        QMessageBox.about(self, "Important message", "Information added successfuly")
     except Exception:
        QMessageBox.warning(self, "Important message", "You can only enter numeric values")
        return

    def setMatrixSingleData(self, x, y, lineEdit, matrix, allMatrix, pos):
     try:
        data = float(lineEdit.text())
        if MatrixData.flagAllDomains == False:
         matrix[x,y] = str(data)
         print(matrix)
        else:
            if pos == 2:
               for i in range(MatrixData.domains):
                  allMatrix[i][1][x][y] = str(data)
            elif pos == 3:
               for i in range(MatrixData.domains):
                  allMatrix[i][2][x][y] = str(data)
            elif pos == 4:
               for i in range(MatrixData.domains):
                  allMatrix[i][3][x][y] = str(data)
        print(allMatrix)
        self.insertMatrix(matrix)
        QMessageBox.about(self, "Important message", "Information added successfuly")
     except Exception:
        QMessageBox.warning(self, "Important message", "You can only enter numeric values")
        return

    def setMatrixDoubleData(self, x, y, lineEdit, lineEdit2, matrix, allMatrix, pos):
     try:
        ar = []
        ar.append(float(lineEdit.text()))
        ar.append(float(lineEdit2.text()))
        if MatrixData.flagAllDomains == False:
         matrix[x,y] = str(ar)
         print(matrix)
        else:
         if pos == 6:
            for i in range(MatrixData.domains):
               allMatrix[i][4][x][y] = str(ar)
         if pos == 7:
            for i in range(MatrixData.domains):
               allMatrix[i][5][x][y] = str(ar)
        print(allMatrix)
        self.insertMatrix(matrix)
        QMessageBox.about(self, "Important message", "Information added successfuly")
     except Exception:
        QMessageBox.warning(self, "Important message", "You can only enter numeric values")
        return

    def setVectorSingleData(self, x, lineEdit, matrix, allMatrix):
     try:
        data = float(lineEdit.text())
        if MatrixData.flagAllDomains == False:
         matrix[x] = data
        else:
         for i in range(MatrixData.domains):
            allMatrix[i][0][0][x] = data
        print(allMatrix)

        self.insertVector(matrix)
   
        QMessageBox.about(self, "Important message", "Information added successfuly")
     except Exception:
        QMessageBox.warning(self, "Important message", "You can only enter numeric values")
        return

    def setVectorDoubleData(self, x, lineEdit, lineEdit2, matrix, allMatrix):
      try:
        ar = []
        ar.append(float(lineEdit.text()))
        ar.append(float(lineEdit2.text()))
        if MatrixData.flagAllDomains == False:
         matrix[x] = str(ar)
         print(matrix)
        else:
         for i in range(MatrixData.domains):
            allMatrix[i][1][0][x] = str(ar)
        print(allMatrix)
        self.insertVector(matrix)
        QMessageBox.about(self, "Important message", "Information added successfuly")
      except Exception:
        QMessageBox.warning(self, "Important message", "You can only enter numeric values")
        return

    def pullAndFormatDiffusionCell(self, x, y, matrix):
        arrMatrix = matrix[x][y]
        arrMatrix = arrMatrix.replace(" ","")
        arrMatrix = arrMatrix.strip('[]')
        arrMatrix = arrMatrix.split(',')
        floatMatrix = [float(i) for i in arrMatrix]
        floatMatrix = [round(i, 2) for i in floatMatrix]
        floatMatrix = floatMatrix[:-1]
        self.cell.insert(str(floatMatrix))

        text = self.cell.text()
        fm = QtGui.QFontMetrics(self.cell.font())
        pixelsWide = fm.width(text)
        self.cell.setFixedSize(QtCore.QSize(pixelsWide + 12, 70))

    def pullAndFormatTableDiffusion(self, x, y, matrix, comb):
      strCell = matrix[x][y]
      strCell = strCell.strip('[]')
      strCell = strCell.split(',')
      self.cell.item(0,0).setText(strCell[0])
      self.cell.item(0,1).setText(strCell[1])
      self.cell.item(1,0).setText(strCell[2])
      self.cell.item(1,1).setText(strCell[3])
      comb.setCurrentIndex(int(strCell[4]))


    def pullAndFormatTableCellMatrix(self, x, y, matrix):
      strCell = matrix[x][y]
      strCell = strCell.strip('[]')
      strCell = strCell.split(',')
      self.cell.item(0,0).setText(strCell[0])
      self.cell.item(0,1).setText(strCell[1])

    def pullAndFormatTableCellVector(self, x, matrix):
      strCell = matrix[x]
      strCell = strCell.strip('[]')
      strCell = strCell.split(',')
      self.cell.item(0,0).setText(strCell[0])
      self.cell.item(0,1).setText(strCell[1])

    def pullAndFormatDoubleCell(self, x, y, matrix):
      floatMatrix = matrix[x][y]
      floatMatrix = floatMatrix.strip('[]')
      floatMatrix = floatMatrix.split(',')
      floatMatrix = [float(i) for i in floatMatrix]
      self.cell.insert(str(floatMatrix))

      text = self.cell.text()
      fm = QtGui.QFontMetrics(self.cell.font())
      pixelsWide = fm.width(text)
      self.cell.setFixedSize(QtCore.QSize(pixelsWide + 12, 70))

    def pullAndFormatCell(self, x, y, matrix):
      floatMatrix = round(float(matrix[x][y]), 2)
      self.cell.insert(str(floatMatrix))

      text = self.cell.text()
      fm = QtGui.QFontMetrics(self.cell.font())
      pixelsWide = fm.width(text)
      self.cell.setFixedSize(QtCore.QSize(pixelsWide + 12, 70))

    def pullAndFormatDoubleVector(self, x, matrix):
      floatMatrix = matrix[x]
      floatMatrix = floatMatrix.strip('[]')
      floatMatrix = floatMatrix.split(',')
      floatMatrix = [float(i) for i in floatMatrix]
      self.cell.insert(str(floatMatrix))

      text = self.cell.text()
      fm = QtGui.QFontMetrics(self.cell.font())
      pixelsWide = fm.width(text)
      self.cell.setFixedSize(QtCore.QSize(pixelsWide + 12, 70))

      

    def pullAndFormatVector(self, x, matrix):
      floatMatrix = round(float(matrix[x]), 2)
      self.cell.insert(str(floatMatrix))
      text = self.cell.text()
      fm = QtGui.QFontMetrics(self.cell.font())
      pixelsWide = fm.width(text)
      self.cell.setFixedSize(QtCore.QSize(pixelsWide + 12, 70))