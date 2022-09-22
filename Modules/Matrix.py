import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QVBoxLayout, QLabel, QGridLayout, QMessageBox, QDialog
from PyQt5 import QtCore
from dialogMatrix import *
import EF
from interfaz import Ui_Interfaz
from Modules.Dictionary.DMatrix import *


class allNewMatrix():
        diffusionM = np.empty([1,1], dtype= 'U256')
        absorptionM = np.empty([1,1], dtype='U256')
        sourceM = np.empty(1, dtype='U256')
        massM = np.empty([1,1], dtype='U256')
        damMassM = np.empty([1,1], dtype='U256')
        cFluxM = np.empty([1,1], dtype='U256')
        convectionM = np.empty([1,1], dtype='U256')
        cSourceM = np.empty(1, dtype='U256')
        n = 1
    

class dialogMatrix(QDialog):
    def __init__(self, n):
        QDialog.__init__(self)
        self.ui = Ui_Matrix()
        self.ui.setupUi(self)
        self.setWindowTitle('Matriz ' + str(n) + 'x' + str(n))
        #Rows
        for x in range(0, n):
            #Columns
            for y in range(0, n):
                self.createMatrix(x, y)


    def marklineEdit(self, comb, comb1, n, arraylEdit, pos, diffusionComb):
        for x in range(0, n):
            for y in range(0, n):
                self.cell = self.findChild(QtWidgets.QLineEdit, "lineEdit" + str(x + 1) + "X" + str(y + 1) + "Y")
                self.cell.setStyleSheet("")
                self.namecell = self.cell.objectName()
                if self.namecell == ("lineEdit" + str(comb.currentIndex() + 1) + "X" + str(comb1.currentIndex() + 1) + "Y"):
                    self.cell.clear()

                    if pos == 1:
                        if diffusionComb.currentIndex() == 0:
                            self.cell.insert(arraylEdit[0][0].text())
                            allNewMatrix.diffusionM[x,y] = arraylEdit[0][0].text()
                            self.insertMatrix(allNewMatrix.diffusionM)
                            print(allNewMatrix.diffusionM)
                            print("") 
                        else: 
                                ar = []
                                self.cell.insert(arraylEdit[0][1].text() + ",")
                                self.cell.insert(arraylEdit[0][2].text() + ",")
                                self.cell.insert(arraylEdit[0][3].text() + ",")
                                self.cell.insert(arraylEdit[0][4].text())
                                ar.append(arraylEdit[0][1].text())
                                ar.append(arraylEdit[0][2].text())
                                ar.append(arraylEdit[0][3].text())
                                ar.append(arraylEdit[0][4].text())
                                allNewMatrix.diffusionM[x,y] = str(ar)
                                self.insertMatrix(allNewMatrix.diffusionM)
                                print(allNewMatrix.diffusionM)
                                print("")
                    if pos == 2:
                        self.cell.insert(arraylEdit[1][0].text())
                        allNewMatrix.absorptionM[x,y] = arraylEdit[1][0].text()
                        self.insertMatrix(allNewMatrix.absorptionM)
                        print(allNewMatrix.absorptionM)
                    if pos == 4:
                        self.cell.insert(arraylEdit[3][0].text())
                        allNewMatrix.massM[x,y] = arraylEdit[3][0].text()
                        self.insertMatrix(allNewMatrix.massM)
                        print(allNewMatrix.massM)
                    if pos == 5:
                        self.cell.insert(arraylEdit[4][0].text())
                        allNewMatrix.damMassM[x,y] = arraylEdit[4][0].text()
                        self.insertMatrix(allNewMatrix.damMassM)
                        print(allNewMatrix.damMassM)
                    if pos == 6:
                        ar = []
                        self.cell.insert(arraylEdit[5][0].text() + ",")
                        self.cell.insert(arraylEdit[5][1].text())
                        ar.append(arraylEdit[5][0].text())
                        ar.append(arraylEdit[5][1].text())
                        allNewMatrix.cFluxM[x,y] = str(ar)
                        self.insertMatrix(allNewMatrix.cFluxM)
                        print(allNewMatrix.cFluxM)
                    if pos == 7:
                        ar = []
                        self.cell.insert(arraylEdit[6][0].text() + ",")
                        self.cell.insert(arraylEdit[6][1].text())
                        ar.append(arraylEdit[6][0].text())
                        ar.append(arraylEdit[6][1].text())
                        allNewMatrix.convectionM[x,y] = str(ar)
                        self.insertMatrix(allNewMatrix.convectionM)
                        print(allNewMatrix.convectionM)   
        QMessageBox.information(self, "Important message", "Información insertada con éxito")
        

    def showMe(self, matrix):
        self.clearMatrix()
        for x in range(allNewMatrix.n):
            for y in range(allNewMatrix.n):
                self.cell = self.findChild(QtWidgets.QLineEdit, "lineEdit" + str(x + 1) + "X" + str(y + 1) + "Y")
                if matrix[x][y] != "None":
                 self.cell.insert(matrix[x][y])
                else: 
                 self.cell.clear()
        self.showdialog()

    def insertMatrix(self, matrix):
        self.clearMatrix()
        for x in range(allNewMatrix.n):
            for y in range(allNewMatrix.n):
                self.cell = self.findChild(QtWidgets.QLineEdit, "lineEdit" + str(x + 1) + "X" + str(y + 1) + "Y")
                if matrix[x][y] != "None":
                 self.cell.insert(matrix[x][y])
                else: 
                 self.cell.clear()


    def showdialog(self):
        self.show()

    def createMatrix(self, row, column):
        self.lineEdit = QtWidgets.QLineEdit(self.ui.scrollAreaWidgetContents)
        self.lineEdit.setMinimumSize(QtCore.QSize(70, 70))
        self.lineEdit.setMaximumSize(QtCore.QSize(70, 70))
        self.lineEdit.setObjectName("lineEdit" + str(row + 1) + "X" + str(column + 1) + "Y")
        self.lineEdit.setEnabled(False)
        self.ui.gridLayout.addWidget(self.lineEdit, row, column, 1, 1, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.ui.scrollArea.setWidget(self.ui.scrollAreaWidgetContents)
        self.ui.verticalLayout.addWidget(self.ui.scrollArea)
        print(self.lineEdit.objectName())

    def clearMatrix(self):
        for row in range(allNewMatrix.n):
            for column in range(allNewMatrix.n):
             self.cell = self.findChild(QtWidgets.QLineEdit, "lineEdit" + str(row + 1) + "X" + str(column + 1) + "Y")
             self.cell.setStyleSheet("")
             self.cell.clear()

class dialogVector(QDialog):
    def __init__(self, n):
        QDialog.__init__(self)
        self.ui = Ui_Matrix()
        self.ui.setupUi(self)
        self.setWindowTitle('Vector ' + str(n))
        #Rows
        for x in range(0, n):
            #Columns
                self.createVector(x)

    def marklineEdit(self, comb, n, arraylEdit, pos):
        for x in range(0, n):
            self.cell = self.findChild(QtWidgets.QLineEdit, "lineEdit" + str(x + 1) + "X" + "1Y")
            self.cell.setStyleSheet("")
            self.namecell = self.cell.objectName()

            if self.namecell == ("lineEdit" + str(comb.currentIndex() + 1) + "X" + "1Y"):
                    self.cell.setStyleSheet("QLineEdit { background-color: yellow}")
                    self.cell.clear()

                    if pos == 3:
                        self.cell.insert(arraylEdit[2][0].text())
                        allNewMatrix.sourceM[x] = arraylEdit[2][0].text()
                        self.insertVector(allNewMatrix.sourceM)
                        print(allNewMatrix.sourceM)
                    if pos == 8:
                        ar = []
                        self.cell.insert(arraylEdit[7][0].text() + ",")
                        self.cell.insert(arraylEdit[7][1].text())
                        ar.append(arraylEdit[7][0].text())
                        ar.append(arraylEdit[7][1].text())
                        allNewMatrix.cSourceM[x] = str(ar)
                        self.insertVector(allNewMatrix.cSourceM)
                        print(allNewMatrix.cSourceM)
        self.showdialog()


    def showdialog(self):
        self.show()

    def showMe(self, matrix):
        self.clearVector()
        for x in range(allNewMatrix.n):
                self.cell = self.findChild(QtWidgets.QLineEdit, "lineEdit" + str(x + 1) + "X" + "1Y")
                if matrix[x] != "None":
                 self.cell.insert(matrix[x])
                else: 
                 self.cell.clear()
        self.showdialog()

    def insertVector(self, matrix):
        self.clearVector()
        for x in range(allNewMatrix.n):
                self.cell = self.findChild(QtWidgets.QLineEdit, "lineEdit" + str(x + 1) + "X" + "1Y")
                if matrix[x] != "None":
                 self.cell.insert(matrix[x])
                else: 
                 self.cell.clear()
        
    def createVector(self, row):
        self.lineEdit = QtWidgets.QLineEdit(self.ui.scrollAreaWidgetContents)
        self.lineEdit.setMinimumSize(QtCore.QSize(70, 70))
        self.lineEdit.setMaximumSize(QtCore.QSize(70, 70))
        self.lineEdit.setObjectName("lineEdit" + str(row + 1) + "X" + "1Y")
        self.lineEdit.setEnabled(False)
        self.ui.gridLayout.addWidget(self.lineEdit, row, 0, 1, 1, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.ui.scrollArea.setWidget(self.ui.scrollAreaWidgetContents)
        self.ui.verticalLayout.addWidget(self.ui.scrollArea)
        print(self.lineEdit.objectName())


    def clearVector(self):
        for row in range(allNewMatrix.n):
             self.cell = self.findChild(QtWidgets.QLineEdit, "lineEdit" + str(row + 1) + "X" + "1Y")
             self.cell.setStyleSheet("")
             self.cell.clear()



class Matrix():
 def newMatrix(self):
    dialog = QMessageBox.question(self, 'Importante', '¿Seguro que quieres cambiar el numero de variables dependientes? Harán cambios en todas las matrices', QMessageBox.Cancel | QMessageBox.Yes)
    if dialog == QMessageBox.Yes:    
        n = int(self.inputDepedentVarial.text())
        if n == '':
            n = 1
        self.dMatrix = dialogMatrix(n)
        self.dVector = dialogVector(n)
        initialValues["noVariables"] = n
        allNewMatrix.diffusionM = np.empty([n,n], dtype='U256')
        allNewMatrix.absorptionM = np.empty([n,n], dtype='U256')
        allNewMatrix.sourceM = np.empty(n, dtype='U256')
        allNewMatrix.massM = np.empty([n,n], dtype='U256')
        allNewMatrix.damMassM = np.empty([n,n], dtype='U256')
        allNewMatrix.cFluxM = np.empty([n,n], dtype='U256')
        allNewMatrix.convectionM = np.empty([n,n], dtype='U256')
        allNewMatrix.cSourceM = np.empty(n, dtype='U256')
        allNewMatrix.n = n
        print("Imprimir matriz diffusion")
        print(allNewMatrix.diffusionM)
        print("Imprimir matriz absorption")
        print(allNewMatrix.absorptionM)
        
        #Actualizar Combobox de cada seccion
        for index, item in enumerate(self.CoefficientCheckBoxArray):
                for j, item in enumerate(self.arrayCmbRowColumns[index]):
                        self.arrayCmbRowColumns[index][j].clear()

                for j, item in enumerate(self.arrayCmbRowColumns[index]):
                    for i in range(1, n + 1):
                        self.arrayCmbRowColumns[index][j].addItem(str(i))
        self.cmbInitialValues.clear()

        for i in range(1, n + 1):
            self.cmbInitialValues.addItem("u" + str(i))

    else:
        print("Operacion Cancelada")
 
