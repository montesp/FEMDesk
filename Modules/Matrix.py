import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QVBoxLayout, QLabel, QGridLayout, QMessageBox, QDialog
from PyQt5 import QtCore
from dialogMatrix import *
import EF
from interfaz import Ui_Interfaz


class allNewMatrix():
        diffusionM = np.empty([1,1], dtype= 'U256')
        absorptionM = np.empty([1,1], dtype='U256')
        sourceM = np.empty(1, dtype='U256')
        massM = np.empty([1,1], dtype='U256')
        damMassM = np.empty([1,1], dtype='U256')
        cFluxM = np.empty([1,1], dtype='U256')
        convectionM = np.empty([1,1], dtype='U256')
        cSourceM = np.empty(1, dtype='U256')
    

class dialogMatrix(QDialog):
    def __init__(self, n):
        QDialog.__init__(self)
        self.ui = Ui_Matrix()
        self.ui.setupUi(self)
        self.setWindowTitle('Matriz')
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
                #print(self.namecell)
                if self.namecell == ("lineEdit" + str(comb.currentIndex() + 1) + "X" + str(comb1.currentIndex() + 1) + "Y"):
                    self.cell.setStyleSheet("QLineEdit { background-color: yellow}")
                    self.cell.clear()

                    if pos == 1:
                        if diffusionComb.currentIndex() == 0:
                            self.cell.insert(arraylEdit[0][0].text())
                            allNewMatrix.diffusionM[x,y] = arraylEdit[0][0].text()
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
                                print(allNewMatrix.diffusionM)
                                print("")
                    if pos == 2:
                        self.cell.insert(arraylEdit[1][0].text())
                        allNewMatrix.absorptionM[x,y] = arraylEdit[1][0].text()
                        print(allNewMatrix.absorptionM)
                    if pos == 4:
                        self.cell.insert(arraylEdit[3][0].text())
                        allNewMatrix.massM[x,y] = arraylEdit[3][0].text()
                        print(allNewMatrix.massM)
                    if pos == 5:
                        self.cell.insert(arraylEdit[4][0].text())
                        allNewMatrix.damMassM[x,y] = arraylEdit[4][0].text()
                        print(allNewMatrix.damMassM)
                    if pos == 6:
                        ar = []
                        self.cell.insert(arraylEdit[5][0].text() + ",")
                        self.cell.insert(arraylEdit[5][1].text())
                        ar.append(arraylEdit[5][0].text())
                        ar.append(arraylEdit[5][1].text())
                        allNewMatrix.cFluxM[x,y] = str(ar)
                        print(allNewMatrix.cFluxM)
                    if pos == 7:
                        ar = []
                        self.cell.insert(arraylEdit[6][0].text() + ",")
                        self.cell.insert(arraylEdit[6][1].text())
                        ar.append(arraylEdit[6][0].text())
                        ar.append(arraylEdit[6][1].text())
                        allNewMatrix.convectionM[x,y] = str(ar)
                        print(allNewMatrix.convectionM)
        self.showdialog()
        

    def showdialog(self):
        self.show()

    def createMatrix(self, row, column):
        self.lineEdit = QtWidgets.QLineEdit(self.ui.scrollAreaWidgetContents)
        self.lineEdit.setMinimumSize(QtCore.QSize(70, 70))
        self.lineEdit.setMaximumSize(QtCore.QSize(70, 70))
        self.lineEdit.setObjectName("lineEdit" + str(row + 1) + "X" + str(column + 1) + "Y")
        self.ui.gridLayout.addWidget(self.lineEdit, row, column, 1, 1, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.ui.scrollArea.setWidget(self.ui.scrollAreaWidgetContents)
        self.ui.verticalLayout.addWidget(self.ui.scrollArea)
        print(self.lineEdit.objectName())
    

class dialogVector(QDialog):
    def __init__(self, n):
        QDialog.__init__(self)
        self.ui = Ui_Matrix()
        self.ui.setupUi(self)
        self.setWindowTitle('Vector')
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
                        print(allNewMatrix.sourceM)
                    if pos == 8:
                        ar = []
                        self.cell.insert(arraylEdit[7][0].text() + ",")
                        self.cell.insert(arraylEdit[7][1].text())
                        ar.append(arraylEdit[7][0].text())
                        ar.append(arraylEdit[7][1].text())
                        allNewMatrix.cSourceM[x] = str(ar)
                        print(allNewMatrix.cSourceM)
        self.showdialog()


    def showdialog(self):
        self.show()
        
    def createVector(self, row):
        self.lineEdit = QtWidgets.QLineEdit(self.ui.scrollAreaWidgetContents)
        self.lineEdit.setMinimumSize(QtCore.QSize(70, 70))
        self.lineEdit.setMaximumSize(QtCore.QSize(70, 70))
        self.lineEdit.setObjectName("lineEdit" + str(row + 1) + "X" + "1Y")
        self.ui.gridLayout.addWidget(self.lineEdit, row, 0, 1, 1, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.ui.scrollArea.setWidget(self.ui.scrollAreaWidgetContents)
        self.ui.verticalLayout.addWidget(self.ui.scrollArea)
        print(self.lineEdit.objectName())





class Matrix():
 def newMatrix(self):
    dialog = QMessageBox.question(self, 'Importante', '¿Seguro que quieres cambiar el numero de variables dependientes? Harán cambios en todas las matrices', QMessageBox.Cancel | QMessageBox.Yes)
    if dialog == QMessageBox.Yes:    
        n = int(self.inputDepedentVarial.text())
        self.dMatrix = dialogMatrix(n)
        self.dVector = dialogVector(n)
        allNewMatrix.diffusionM = np.empty([n,n], dtype='U256')
        allNewMatrix.absorptionM = np.empty([n,n], dtype='U256')
        allNewMatrix.sourceM = np.empty(n, dtype='U256')
        allNewMatrix.massM = np.empty([n,n], dtype='U256')
        allNewMatrix.damMassM = np.empty([n,n], dtype='U256')
        allNewMatrix.cFluxM = np.empty([n,n], dtype='U256')
        allNewMatrix.convectionM = np.empty([n,n], dtype='U256')
        allNewMatrix.cSourceM = np.empty(n, dtype='U256')
        print(allNewMatrix.diffusionM)
        print("")
        print(allNewMatrix.sourceM)

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
 
class Matrix1X1(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Matriz')

        mainLayout = QGridLayout()

        self.lEdit11 = QLineEdit(objectName = "lEdit11M11")
        self.lEdit11.setFixedSize(70,70)
        self.lEdit11.setAlignment(QtCore.Qt.AlignCenter)
        self.lEdit11.setEnabled(False)
        mainLayout.addWidget(self.lEdit11)

        self.setLayout(mainLayout)


class Matrix2X2(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Matriz')

        mainLayout = QGridLayout()

        self.lEdit11 = QLineEdit(objectName = "lEdit11M22")
        self.lEdit11.setFixedSize(70,70)
        self.lEdit11.setAlignment(QtCore.Qt.AlignCenter)
        self.lEdit11.setEnabled(False)

        self.lEdit12 = QLineEdit(objectName = "lEdit12M22")
        self.lEdit12.setFixedSize(70,70)
        self.lEdit12.setAlignment(QtCore.Qt.AlignCenter)
        self.lEdit12.setEnabled(False)

        self.lEdit21 = QLineEdit(objectName = "lEdit21M22")
        self.lEdit21.setFixedSize(70,70)
        self.lEdit21.setAlignment(QtCore.Qt.AlignCenter)
        self.lEdit21.setEnabled(False)

        self.lEdit22 = QLineEdit(objectName = "lEdit22M22")
        self.lEdit22.setFixedSize(70,70)
        self.lEdit22.setAlignment(QtCore.Qt.AlignCenter)
        self.lEdit22.setEnabled(False)

       

        

        mainLayout.addWidget(self.lEdit11)
        mainLayout.addWidget(self.lEdit12, 0 , 1)
        mainLayout.addWidget(self.lEdit21, 1 , 0)
        mainLayout.addWidget(self.lEdit22, 1 , 1)

        self.setLayout(mainLayout)

class Matrix3X3(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Matriz')

        mainLayout = QGridLayout()

        self.lEdit11 = QLineEdit(objectName = "lEdit11M33")
        self.lEdit11.setFixedSize(70,70)
        self.lEdit11.setAlignment(QtCore.Qt.AlignCenter)
        self.lEdit11.setEnabled(False)

        self.lEdit12 = QLineEdit(objectName = "lEdit12M33")
        self.lEdit12.setFixedSize(70,70)
        self.lEdit12.setAlignment(QtCore.Qt.AlignCenter)
        self.lEdit12.setEnabled(False)

        self.lEdit13 = QLineEdit(objectName = "lEdit13M33")
        self.lEdit13.setFixedSize(70,70)
        self.lEdit13.setAlignment(QtCore.Qt.AlignCenter)
        self.lEdit13.setEnabled(False)

        self.lEdit21 = QLineEdit(objectName = "lEdit21M33")
        self.lEdit21.setFixedSize(70,70)
        self.lEdit21.setAlignment(QtCore.Qt.AlignCenter)
        self.lEdit21.setEnabled(False)

        self.lEdit22 = QLineEdit(objectName = "lEdit22M33")
        self.lEdit22.setFixedSize(70,70)
        self.lEdit22.setAlignment(QtCore.Qt.AlignCenter)
        self.lEdit22.setEnabled(False)

        self.lEdit23 = QLineEdit(objectName = "lEdit23M33")
        self.lEdit23.setFixedSize(70,70)
        self.lEdit23.setAlignment(QtCore.Qt.AlignCenter)
        self.lEdit23.setEnabled(False)

        self.lEdit31 = QLineEdit(objectName = "lEdit31M33")
        self.lEdit31.setFixedSize(70,70)
        self.lEdit31.setAlignment(QtCore.Qt.AlignCenter)
        self.lEdit31.setEnabled(False)

        self.lEdit32 = QLineEdit(objectName = "lEdit32M33")
        self.lEdit32.setFixedSize(70,70)
        self.lEdit32.setAlignment(QtCore.Qt.AlignCenter)
        self.lEdit32.setEnabled(False)

        self.lEdit33 = QLineEdit(objectName = "lEdit33M33")
        self.lEdit33.setFixedSize(70,70)
        self.lEdit33.setAlignment(QtCore.Qt.AlignCenter)
        self.lEdit33.setEnabled(False)

        mainLayout.addWidget(self.lEdit11)
        mainLayout.addWidget(self.lEdit12, 0 , 1)
        mainLayout.addWidget(self.lEdit13, 0 , 2)
        mainLayout.addWidget(self.lEdit21, 1 , 0)
        mainLayout.addWidget(self.lEdit22, 1 , 1)
        mainLayout.addWidget(self.lEdit23, 1 , 2)
        mainLayout.addWidget(self.lEdit31, 2 , 0)
        mainLayout.addWidget(self.lEdit32, 2 , 1)
        mainLayout.addWidget(self.lEdit33, 2 , 2)
        self.setLayout(mainLayout)

class Matrix2X1(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Matriz')

        mainLayout = QGridLayout()

        self.lEdit11 = QLineEdit(objectName = "lEdit11M21")
        self.lEdit11.setFixedSize(70,70)
        self.lEdit11.setAlignment(QtCore.Qt.AlignCenter)
        self.lEdit11.setEnabled(False)

        self.lEdit21 = QLineEdit(objectName = "lEdit21M21")
        self.lEdit21.setFixedSize(70,70)
        self.lEdit21.setAlignment(QtCore.Qt.AlignCenter)
        self.lEdit21.setEnabled(False)

        mainLayout.addWidget(self.lEdit11)
        mainLayout.addWidget(self.lEdit21, 1, 0)

        self.setLayout(mainLayout)

class Matrix3X1(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Matriz')

        mainLayout = QGridLayout()

        self.lEdit11 = QLineEdit(objectName = "lEdit11M31")
        self.lEdit11.setFixedSize(70,70)
        self.lEdit11.setAlignment(QtCore.Qt.AlignCenter)
        self.lEdit11.setEnabled(False)

        self.lEdit21 = QLineEdit(objectName = "lEdit21M31")
        self.lEdit21.setFixedSize(70,70)
        self.lEdit21.setAlignment(QtCore.Qt.AlignCenter)
        self.lEdit21.setEnabled(False)

        self.lEdit31 = QLineEdit(objectName = "lEdit31M31")
        self.lEdit31.setFixedSize(70,70)
        self.lEdit31.setAlignment(QtCore.Qt.AlignCenter)
        self.lEdit31.setEnabled(False)
        mainLayout.addWidget(self.lEdit11)
        mainLayout.addWidget(self.lEdit21, 1, 0)
        mainLayout.addWidget(self.lEdit31, 2, 0)

        self.setLayout(mainLayout)

        


