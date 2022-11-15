import sys
from functools import partial

import numpy as np
from PyQt5 import Qt, QtCore, QtGui
from PyQt5.QtWidgets import QDialog, QMessageBox

import Modules.ManageFiles.ManageFiles
from dialogMatrix import *
from Modules.Dictionary.DFiles import *
from Modules.Dictionary.DMatrix import *
from Modules.Matrix.MatrixData import *


class allNewMatrix():
        matrixCoefficientPDE = None
        vectorCoefficientPDE = None
        matrixItemsActivated = None
        n = 1
        domains = 0
        
        def __init__(self):
         pass  

        def getMatrixCoefficient(self):
            return self.matrixCoefficientPDE
        
        def setMatrixCoefficient(self, matrix):
            self.matrixCoefficientPDE = matrix

        def getVectorCoefficient(self):
            return self.vectorCoefficientPDE

        def setVectorCoefficient(self, vector):
            self.vectorCoefficientPDE = vector

        def getMatrixDimensionNumber(self):
            return self.n

        def setMatrixDimensionNumber(self, n):
            self.n = n

        def getMatrixDomains(self):
            return domains

        def setMatrixDomains(self, domains):
            self.domains = domains

        def setDomainItemsActivated(self, items):
            self.matrixItemsActivated = items
            
        def changeMatrixDimensions(self, n, canvas, win):
            self.dMatrix = dialogMatrix(n)
            self.dVector = dialogVector(n)
            numberDomains = canvas.getSolids()
            initialValues["noVariables"] = n

            allNewMatrix.domains = len(numberDomains)
            allNewMatrix.n = win.modelwizard.getVariables()

            allNewMatrix.matrixCoefficientPDE = np.empty([allNewMatrix.domains, 8, 
            allNewMatrix.n, allNewMatrix.n], dtype= 'U256')
            allNewMatrix.vectorCoefficientPDE = np.empty([allNewMatrix.domains, 2,1,
            allNewMatrix.n], dtype= 'U256')
            allNewMatrix.matrixItemsActivated = np.empty([allNewMatrix.domains, 8], 
            dtype='U256')
            
            print("Matrices de Coefficients PDE")
            print(allNewMatrix.matrixCoefficientPDE)

        def changeDimensionMatrix3D(self, canvas):
            numberDomains = canvas.getSolids()
            print("Numero de dominios")
            print(len(numberDomains))
            print("Dimension de la matriz nxn")
            print(allNewMatrix.n)
            print(self.n)
            updatedMatrix = np.resize(self.matrixCoefficientPDE, (len(numberDomains), 
            8, allNewMatrix.n, allNewMatrix.n))
            updatedVector = np.resize(self.vectorCoefficientPDE, (len(numberDomains), 
            2, 1, allNewMatrix.n))
            updatedItemsMatrix = np.resize(self.matrixItemsActivated,
            (len(numberDomains), 8))
            allNewMatrix.matrixCoefficientPDE = updatedMatrix
            allNewMatrix.vectorCoefficientPDE = updatedVector
            allNewMatrix.matrixItemsActivated = updatedItemsMatrix
        

#Clase para Crear la matrix de N dimensiones y darle las funciones para insertar, editar y eliminar datos en cada coordenada
class dialogMatrix(QDialog):
    def __init__(self, n):
        QDialog.__init__(self)
        self.ui = Ui_Matrix()
        self.ui.setupUi(self)
        self.setWindowTitle('Matriz ' + str(n) + 'x' + str(n))
        self.setMinimumSize(QtCore.QSize(500,500))
        self.setMaximumSize(QtCore.QSize(1000,700))
        self.setWindowFlags(QtCore.Qt.Popup)
        
        #Mandar a llamar la función n veces para poder crear la matriz
            #Rows
        for x in range(0, n):
            #Columns
            for y in range(0, n):
                self.createMatrix(x, y)

    def getEditorWindow(self):
        return self.editorWindow

    #Función que genera la matriz de n dimensiones con sus caracteristicas
    def createMatrix(self, row, column):
        self.lineEdit = QtWidgets.QLineEdit(self.ui.scrollAreaWidgetContents)
        self.lineEdit.setMinimumSize(QtCore.QSize(70, 70))
        self.lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit.setObjectName("lineEdit" + str(row + 1) + "X" + str(column + 1) + "Y")
        self.lineEdit.setEnabled(False)
        self.ui.gridLayout.addWidget(self.lineEdit, row, column, 1, 1, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.ui.scrollArea.setWidget(self.ui.scrollAreaWidgetContents)
        self.ui.verticalLayout.addWidget(self.ui.scrollArea)

    #Función para mandar a llamar otra función que inserte los datos en una coordenada específico, además de marcar su casilla
    def marklineEdit(self, comb, comb1, n, arraylEdit, pos, diffusionComb, window):
        for x in range(0, n):
            for y in range(0, n):
                self.cell = self.findChild(QtWidgets.QLineEdit, "lineEdit" + str(x + 1) + "X" + str(y + 1) + "Y")
                self.cell.setStyleSheet("")
                self.namecell = self.cell.objectName()
                if self.namecell == ("lineEdit" + str(comb.currentIndex() + 1) + "X" + str(comb1.currentIndex() + 1) + "Y"):
                    self.cell.clear()
                    if pos == 1:
                        if diffusionComb.currentIndex() == 0:
                         MatrixData.setDiffusionMatrixSingleData(self, x, y, diffusionComb, arraylEdit, allNewMatrix.matrixCoefficientPDE[domains["domain"]][0])
                        else:
                         MatrixData.setDiffusionMatrixMultipleData(self, x, y, diffusionComb, arraylEdit, allNewMatrix.matrixCoefficientPDE[domains["domain"]][0])
                    if pos == 2:
                      MatrixData.setMatrixSingleData(self, x, y, arraylEdit[1][0], allNewMatrix.matrixCoefficientPDE[domains["domain"]][1])
                    if pos == 4:
                      MatrixData.setMatrixSingleData(self, x, y, arraylEdit[3][0], allNewMatrix.matrixCoefficientPDE[domains["domain"]][2])
                    if pos == 5:
                      MatrixData.setMatrixSingleData(self, x, y, arraylEdit[4][0], allNewMatrix.matrixCoefficientPDE[domains["domain"]][3])
                    if pos == 6:
                      MatrixData.setMatrixDoubleData(self, x, y, arraylEdit[5][0], arraylEdit[5][1], allNewMatrix.matrixCoefficientPDE[domains["domain"]][4])
                    if pos == 7:
                      MatrixData.setMatrixDoubleData(self, x, y, arraylEdit[6][0], arraylEdit[6][1], allNewMatrix.matrixCoefficientPDE[domains["domain"]][5])
        Modules.ManageFiles.ManageFiles.FileData.checkUpdateFile(window)


  

    def showMeDiffusion(self, matrix, arrayComb):
        self.clearMatrix()
        for x in range(allNewMatrix.n):
            for y in range(allNewMatrix.n):
                self.cell = self.findChild(QtWidgets.QLineEdit, "lineEdit" + str(x + 1) + "X" + str(y + 1) + "Y")
                if matrix[x][y] == "None" or matrix[x][y] == '':
                 self.cell.clear()
                else:
                 MatrixData.pullAndFormatDiffusionCell(self, x, y,  matrix)
        self.showdialog(self.findChild(QtWidgets.QLineEdit, "lineEdit" + (str(arrayComb[0].currentIndex() + 1) + "X" + (str(arrayComb[1].currentIndex() + 1)) + "Y")))

                 
     #Función para limpiar la casilla especifica e insertarle los datos
    def insertMatrix(self, matrix):
        self.clearMatrix()
        for x in range(allNewMatrix.n):
            for y in range(allNewMatrix.n):
                self.cell = self.findChild(QtWidgets.QLineEdit, "lineEdit" + str(x + 1) + "X" + str(y + 1) + "Y")
                if matrix[x][y] != "None":
                 self.cell.insert(matrix[x][y])
                else:
                 self.cell.clear()

    #Función para mandar a llamar otra función que muestre la matriz de la sección seleccionada por el usuario
    def showMe(self, matrix, arrayComb):
        self.clearMatrix()
        for x in range(allNewMatrix.n):
            for y in range(allNewMatrix.n):
                self.cell = self.findChild(QtWidgets.QLineEdit, "lineEdit" + str(x + 1) + "X" + str(y + 1) + "Y")
                if matrix[x][y] != "None":
                 MatrixData.pullAndFormatCell(self, x, y, matrix)
                else:
                 self.cell.clear()
        self.showdialog(self.findChild(QtWidgets.QLineEdit, "lineEdit" + (str(arrayComb[0].currentIndex() + 1) + "X" + (str(arrayComb[1].currentIndex() + 1)) + "Y")))

    #Función que muestra una matriz
    def showdialog(self, cell):
        QtCore.QTimer.singleShot(0, partial(self.ui.scrollArea.ensureWidgetVisible, cell))
        cell.setStyleSheet("color : blue")
        self.show()

    #Función para limpiar todas los QLineEdit de la matrix a mostrar
    def clearMatrix(self):
        for row in range(allNewMatrix.n):
            for column in range(allNewMatrix.n):
             self.cell = self.findChild(QtWidgets.QLineEdit, "lineEdit" + str(row + 1) + "X" + str(column + 1) + "Y")
             self.cell.setStyleSheet("")
             self.cell.setFixedSize(QtCore.QSize(70, 70))
             self.cell.clear()  
    #Función para limpiar los datos de la matrix almacenada
    def clearMatrixData(self, matrix):
        dialog = QMessageBox.question(self, 'Importante', '¿Seguro que quieres reiniciar la matriz? Todos los datos se perderán', QMessageBox.Cancel | QMessageBox.Yes)
        if dialog == QMessageBox.Yes:
         matrix.fill('')
         Modules.ManageFiles.ManageFiles.FileData.checkUpdateFile(self)
        else:
            print("Operación Cancelada")


#Clase para Crear el vector de N dimensiones y darle las funciones para insertar, editar y eliminar datos en cada coordenada
class dialogVector(QDialog):
    def __init__(self, n):
        QDialog.__init__(self)
        self.ui = Ui_Matrix()
        self.ui.setupUi(self)
        self.setWindowTitle('Vector ' + str(n))
        self.setWindowFlags(QtCore.Qt.Popup)
        #Rows
        for x in range(0, n):
            #Columns
                self.createVector(x)

    #Función que genera el vector de n dimensiones con sus caracteristicas
    def createVector(self, row):
        self.lineEdit = QtWidgets.QLineEdit(self.ui.scrollAreaWidgetContents)
        self.lineEdit.setMinimumSize(QtCore.QSize(70, 70))
        self.lineEdit.setMaximumSize(QtCore.QSize(70, 70))
        self.lineEdit.setObjectName("lineEdit" + str(row + 1) + "X" + "1Y")
        self.lineEdit.setEnabled(False)
        self.ui.gridLayout.addWidget(self.lineEdit, row, 0, 1, 1, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.ui.scrollArea.setWidget(self.ui.scrollAreaWidgetContents)
        self.ui.verticalLayout.addWidget(self.ui.scrollArea)

    #Función para mandar a llamar otra función que inserte los datos en una coordenada específico, además de marcar su casilla
    def marklineEdit(self, comb, n, arraylEdit, pos, window):
        for x in range(0, n):
            self.cell = self.findChild(QtWidgets.QLineEdit, "lineEdit" + str(x + 1) + "X" + "1Y")
            self.cell.setStyleSheet("")
            self.namecell = self.cell.objectName()

            if self.namecell == ("lineEdit" + str(comb.currentIndex() + 1) + "X" + "1Y"):
                    self.cell.setStyleSheet("QLineEdit { background-color: yellow}")
                    self.cell.clear()

                    if pos == 3:
                     MatrixData.setVectorSingleData(self, x, arraylEdit[2][0], allNewMatrix.vectorCoefficientPDE[domains["domain"]][0][0])
                    if pos == 8:
                     MatrixData.setVectorDoubleData(self, x, arraylEdit[7][0], arraylEdit[7][1], allNewMatrix.vectorCoefficientPDE[domains["domain"]][1][0])
        Modules.ManageFiles.ManageFiles.FileData.checkUpdateFile(window)
        

     #Función para limpiar la casilla especifica e insertarle los datos
    def insertVector(self, matrix):
        self.clearVector()
        for x in range(allNewMatrix.n):
                self.cell = self.findChild(QtWidgets.QLineEdit, "lineEdit" + str(x + 1) + "X" + "1Y")
                if matrix[x] != "None":
                 self.cell.insert(matrix[x])
                else:
                 self.cell.clear()

    #Función para mandar a llamar otra función que muestre el vector de la sección seleccionada por el usuario
    def showMe(self, matrix, arrayComb):
        self.clearVector()
        for x in range(allNewMatrix.n):
                self.cell = self.findChild(QtWidgets.QLineEdit, "lineEdit" + str(x + 1) + "X" + "1Y")
                if matrix[x] != "None":
                 MatrixData.pullAndFormatVector(self, x, matrix)
                else:
                 self.cell.clear()
        self.showdialog(self.findChild(QtWidgets.QLineEdit, "lineEdit" + (str(arrayComb[0].currentIndex() + 1) + "X" + "1Y")))

    #Función que muestra un vector
    def showdialog(self, cell):
        QtCore.QTimer.singleShot(0, partial(self.ui.scrollArea.ensureWidgetVisible, cell))
        cell.setStyleSheet("color : blue")
        self.show()

    #Función para limpiar todas las casillas del vector
    def clearVector(self):
        for row in range(allNewMatrix.n):
             self.cell = self.findChild(QtWidgets.QLineEdit, "lineEdit" + str(row + 1) + "X" + "1Y")
             self.cell.setStyleSheet("")
             self.cell.clear()


#Clase para definir la dimension de las matrices encargadas de guardar la información en la memoria del programa
#Estas matrices sirven como un intermediario para intercambiar información entre el programa y los archivos EXCEL
class Matrix():
 def newMatrix(self, canvas):
    dialog = QMessageBox.question(self, 'Importante', '¿Seguro que quieres cambiar el numero de variables dependientes? Harán cambios en todas las matrices', QMessageBox.Cancel | QMessageBox.Yes)
    if dialog == QMessageBox.Yes:
     #try:
        #Cambiar las dimensiones de las matrices
        n = int(self.inputDepedentVarial.text())
        if n == '':
            n = 1
        allNewMatrix.changeMatrixDimensions(self, n, canvas, self)
        #Actualizar los combobox segun el numero de variables dependientes
        MatrixData.updateCombobox(self, n)
        #Decirle al programa el archivo Excel fue editado
        Modules.ManageFiles.ManageFiles.FileData.checkUpdateFile(self)

        self.btnModelWizardApply.setEnabled(False)
     #except Exception:
            #QMessageBox.warning(self, "Important message", "Solo puede ingresar valores numericos")
            #return
    else:
        print("Operacion Cancelada")

 def resetMatrix(self):
    dialog = QMessageBox.question(self, 'Importante', '¿Seguro que quieres reiniciar el numero de variables dependientes? Esto reiniciará todas las matrices', QMessageBox.Cancel | QMessageBox.Yes)
    if dialog == QMessageBox.Yes:
        #Cambiar las dimensiones de las matrices
        n = 1
        allNewMatrix.changeMatrixDimensions(self, n)
        #Cambiar el lineEdit de las variables iniciales
        Matrix.currentInitialVariable(self)
        #Actualizar el combobox según el numero de variables dependientes
        MatrixData.updateCombobox(self, n)
        #Decirle al programa que el archivo Excel fue editado
        Modules.ManageFiles.ManageFiles.FileData.checkUpdateFile(self)
    else:
        print("Operacion Cancelada")

 def currentInitialVariable(self, allnewmatrix):
        noVar = "{}".format(allnewmatrix.n)
        self.inputDepedentVarial.setText(noVar)

