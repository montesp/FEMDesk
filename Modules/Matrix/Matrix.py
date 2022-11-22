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
from Modules.Dictionary.DModelWizard import *



class dialogTableMatrix(QDialog):
    def __init__(self, n):
        QDialog.__init__(self)
        self.ui = Ui_Matrix()
        self.ui.setupUi(self)
        self.setWindowTitle('Matriz ' + str(n) + 'x' + str(n))
        self.setMinimumSize(QtCore.QSize(600,600))
        self.setMaximumSize(QtCore.QSize(1000,700))
        self.buttonsLayout = self.ui.horizontalLayout_3
        self.btnAccept = self.ui.btnAccept
        self.btnCancel = self.ui.btnCancel
        self.defaultWindowFlag = self.windowFlags()
        self.currentMatrix = None
        self.posMatrix = None
        self.win = None

        for x in range(0, n):
            #Columns
            for y in range(0, n):
                self.createMatrix(x, y)

        self.btnAccept.clicked.connect(lambda: self.fillMatrix(self.currentMatrix, 
        self.win, allNewMatrix.matrixCoefficientPDE, self.posMatrix))
        self.btnCancel.clicked.connect(lambda: self.close())

    #Función que genera la matriz de n dimensiones con sus caracteristicas
    def createMatrix(self, row, column):
        self.table = QtWidgets.QTableWidget(self.ui.scrollAreaWidgetContents)
        self.table.setMinimumHeight(40)
        self.table.setMaximumHeight(75)
        self.table.setMinimumWidth(162)
        self.table.setMaximumWidth(162)
        self.table.setRowCount(1)
        self.table.setColumnCount(2)
        self.table.setItem(0,0, QtWidgets.QTableWidgetItem('alpha X'))
        self.table.setItem(0,1, QtWidgets.QTableWidgetItem('alpha Y'))
        self.table.item(0,0).setText('')
        self.table.item(0,1).setText('')
        self.table.setHorizontalHeaderLabels(['alpha X', 'alpha Y'])
        self.table.setColumnWidth(0, 80)
        self.table.setColumnWidth(1, 80)
        self.table.setRowHeight(0, 35)
        self.table.verticalHeader().hide()
        self.table.setObjectName("table" + str(row + 1) + "X" + str(column + 1) + "Y")
        self.ui.gridLayout.addWidget(self.table, row, column, 1, 1, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.ui.scrollArea.setWidget(self.ui.scrollAreaWidgetContents)
        self.ui.verticalLayout.addWidget(self.ui.scrollArea)
    

    def fillMatrix(self, matrix, win, allMatrix, pos):
         for x in range(allNewMatrix.n):
            for y in range(allNewMatrix.n):
                self.cell = self.findChild(QtWidgets.QTableWidget, "table" + str(x + 1) + "X" + str(y + 1) + "Y")
                if self.cell.itemAt(0,0).text() == '' or self.cell.itemAt(0,1).text() == '':
                 matrix[x][y] = ''
                else:
                 try:
                    arTable = []
                    arTable.append(float(self.cell.item(0,0).text()))
                    arTable.append(float(self.cell.item(0,1).text()))
                    if MatrixData.flagAllDomains == False:
                        matrix[x][y] = str(arTable)
                    else:
                        if pos == 6:
                            for i in range(MatrixData.domains):
                                allMatrix[i][4][x][y] = str(arTable)
                        elif pos == 7:
                            for i in range(MatrixData.domains):
                                allMatrix[i][5][x][y] = str(arTable)
                 except Exception:
                    QMessageBox.warning(self, "Important message", "Solo puede ingresar valores numericos")
                    return
         print(allMatrix)
         Modules.ManageFiles.ManageFiles.Update.currentData(win, pos)
         self.close()

    def editMatrix(self, matrix, win, pos):
        self.setWindowFlags(self.defaultWindowFlag)
        self.win = win
        self.btnAccept.show()
        self.btnCancel.show()
        self.posMatrix = pos
        self.currentMatrix = matrix
        for x in range(allNewMatrix.n):
            for y in range(allNewMatrix.n):
                self.cell = self.findChild(QtWidgets.QTableWidget, "table" + str(x + 1) + "X" + str(y + 1) + "Y")
                self.cell.setItem(0,0, QtWidgets.QTableWidgetItem('00'))
                self.cell.setItem(0,1, QtWidgets.QTableWidgetItem('01'))
                if matrix[x][y] == "None" or matrix[x][y] == '':
                 self.cell.item(0,0).setText('')
                 self.cell.item(0,1).setText('')
                else:
                 MatrixData.pullAndFormatTableCellMatrix(self, x, y,  matrix)
        self.showDialog()


    def showDialog(self):
        self.show()

class dialogTableVector(QDialog):
    def __init__(self, n):
        QDialog.__init__(self)
        self.ui = Ui_Matrix()
        self.ui.setupUi(self)
        self.setWindowTitle('Vector ' + str(n))
        self.setMinimumSize(QtCore.QSize(600,600))
        self.setMaximumSize(QtCore.QSize(1000,700))
        self.buttonsLayout = self.ui.horizontalLayout_3
        self.btnAccept = self.ui.btnAccept
        self.btnCancel = self.ui.btnCancel
        self.defaultWindowFlag = self.windowFlags()
        self.currentMatrix = None
        self.posMatrix = None
        self.win = None
        #Rows
        for x in range(0, n):
            #Columns
                self.createVector(x)

        self.btnAccept.clicked.connect(lambda: self.fillVector(self.currentMatrix, 
        self.win, allNewMatrix.vectorCoefficientPDE, self.posMatrix))
        self.btnCancel.clicked.connect(lambda: self.close())

    #Función que genera el vector de n dimensiones con sus caracteristicas
    def createVector(self, row):
        self.table = QtWidgets.QTableWidget(self.ui.scrollAreaWidgetContents)
        self.table.setMinimumHeight(40)
        self.table.setMaximumHeight(75)
        self.table.setMinimumWidth(182)
        self.table.setMaximumWidth(182)
        self.table.setRowCount(1)
        self.table.setColumnCount(2)
        self.table.setItem(0,0, QtWidgets.QTableWidgetItem('00'))
        self.table.setItem(0,1, QtWidgets.QTableWidgetItem('01'))
        self.table.item(0,0).setText('')
        self.table.item(0,1).setText('')
        self.table.setHorizontalHeaderLabels(['gamma X', 'gamma Y'])
        self.table.setColumnWidth(0, 90)
        self.table.setColumnWidth(1, 90)
        self.table.setRowHeight(0, 35)
        self.table.verticalHeader().hide()
        self.table.setObjectName("table" + str(row + 1) + "X" + "1Y")
        self.ui.gridLayout.addWidget(self.table, row, 0, 1, 1, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.ui.scrollArea.setWidget(self.ui.scrollAreaWidgetContents)
        self.ui.verticalLayout.addWidget(self.ui.scrollArea)

    def fillVector(self, matrix, win, allMatrix, pos):
         for x in range(allNewMatrix.n):
                self.cell = self.findChild(QtWidgets.QTableWidget, "table" + str(x + 1) + "X" + "1Y")
                if self.cell.itemAt(0,0).text() == '' or self.cell.itemAt(0,1).text() == '':
                 matrix[x] = ''
                else:
                 try:
                    arTable = []
                    arTable.append(float(self.cell.item(0,0).text()))
                    arTable.append(float(self.cell.item(0,1).text()))
                    if MatrixData.flagAllDomains == False:
                        matrix[x] = str(arTable)
                    else:
                        for i in range(MatrixData.domains):
                            allMatrix[i][1][0][x] = str(arTable)
                 except Exception:
                    QMessageBox.warning(self, "Important message", "Solo puede ingresar valores numericos")
                    return
         print(allMatrix)
         Modules.ManageFiles.ManageFiles.Update.currentData(win, pos)
         self.close()

    def editVector(self, matrix, win, pos):
        self.setWindowFlags(self.defaultWindowFlag)
        self.win = win
        self.btnAccept.show()
        self.btnCancel.show()
        self.posMatrix = pos
        self.currentMatrix = matrix
        for x in range(allNewMatrix.n):
                self.cell = self.findChild(QtWidgets.QTableWidget, "table" + str(x + 1) + "X" + "1Y")
                self.cell.setItem(0,0, QtWidgets.QTableWidgetItem('00'))
                self.cell.setItem(0,1, QtWidgets.QTableWidgetItem('01'))
                if matrix[x] == "None" or matrix[x] == '':
                 self.cell.item(0,0).setText('')
                 self.cell.item(0,1).setText('')
                else:
                 MatrixData.pullAndFormatTableCellVector(self, x,  matrix)
        self.showDialog()

    def showDialog(self):
        self.show()
class allNewMatrix():
        matrixCoefficientPDE = None
        vectorCoefficientPDE = None
        matrixItemsActivated = None
        n = 1
        domains = 0
        
        def __init__(self):
         pass  
            
        def changeMatrixDimensions(self, n, canvas, win):
            self.dMatrix = dialogMatrix(n)
            self.dVector = dialogVector(n)
            self.dTableMatrix = dialogTableMatrix(n)
            self.dTableVector = dialogTableVector(n)
            numberDomains = canvas.getSolids()
            initialValues["noVariables"] = n

            allNewMatrix.domains = len(numberDomains)
            MatrixData.domains = len(numberDomains)
            allNewMatrix.n = win.modelwizard.getVariables()
            print("Dominios desde el allnewmatrix")
            print(allNewMatrix.domains)
            allNewMatrix.matrixCoefficientPDE = np.empty([allNewMatrix.domains, 6, 
            allNewMatrix.n, allNewMatrix.n], dtype= 'U256')
            allNewMatrix.vectorCoefficientPDE = np.empty([allNewMatrix.domains, 2,1,
            allNewMatrix.n], dtype= 'U256')
            allNewMatrix.matrixItemsActivated = np.empty([allNewMatrix.domains, 8], 
            dtype='U256')
            
            print("Matrices de Coefficients PDE")
            print(allNewMatrix.matrixCoefficientPDE)

        def addDimensionMatrix3D(self, canvas):
            numberDomains = canvas.getSolids()
            allNewMatrix.domains = len(numberDomains)
            MatrixData.domains = len(numberDomains)
            updatedMatrix = np.resize(self.matrixCoefficientPDE, (len(numberDomains), 
            6, allNewMatrix.n, allNewMatrix.n))
            updatedVector = np.resize(self.vectorCoefficientPDE, (len(numberDomains), 
            2, 1, allNewMatrix.n))
            updatedItemsMatrix = np.resize(self.matrixItemsActivated,
            (len(numberDomains), 8))

            #Limpíar los datos que pudieron ser copiados de las otras dimensiones
            for i in range(len(updatedMatrix[len(numberDomains) - 1])):
                updatedMatrix[len(numberDomains) - 1][i].fill('')

            for i in range(len(updatedVector[len(numberDomains) - 1])):
                updatedVector[len(numberDomains) - 1][i].fill('')
        
            for i in range(len(updatedItemsMatrix[len(numberDomains) - 1])):
                updatedItemsMatrix[len(numberDomains) - 1][i] = ''

            print(updatedMatrix)
            allNewMatrix.matrixCoefficientPDE = updatedMatrix
            allNewMatrix.vectorCoefficientPDE = updatedVector
            allNewMatrix.matrixItemsActivated = updatedItemsMatrix

        def removeDimensionMatrix3D(self, solids, poly):
            if myFlags["ModelWizardMode"] == "Coefficient form PDE":
                print(solids.index(poly))
                print("Dimension de la matriz nxn")
                print(allNewMatrix.n)
                print(self.n)
                updatedMatrix = np.reshape(self.matrixCoefficientPDE, (len(solids), 
                8, allNewMatrix.n, allNewMatrix.n))
                updatedVector = np.reshape(self.vectorCoefficientPDE, (len(solids), 
                2, 1, allNewMatrix.n))
                updatedItemsMatrix = np.reshape(self.matrixItemsActivated, (len(solids), 8))

                updatedMatrix = np.delete(self.matrixCoefficientPDE, solids.index(poly), 0)
                updatedVector = np.delete(self.vectorCoefficientPDE, solids.index(poly), 0)
                updatedItemsMatrix = np.delete(self.matrixItemsActivated, solids.index(poly), 0)

                print("Matrix con fila borrada")
                print(updatedMatrix)
                print("Vector con fila borrada")
                print(updatedVector)

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
        self.buttonsLayout = self.ui.horizontalLayout_3
        self.btnAccept = self.ui.btnAccept
        self.btnCancel = self.ui.btnCancel
        self.defaultWindowFlag = self.windowFlags()
        self.currentMatrix = None
        self.labelsReferences = []
        self.posMatrix = None
        self.win = None
        #self.setWindowFlags(QtCore.Qt.Popup)
        
        #Mandar a llamar la función n veces para poder crear la matriz
            #Rows
        for x in range(0, n):
            #Columns
            for y in range(0, n):
                self.createMatrix(x, y)

        self.btnAccept.clicked.connect(lambda: self.fillMatrix(self.currentMatrix, 
        self.win, allNewMatrix.matrixCoefficientPDE, self.posMatrix))
        self.btnCancel.clicked.connect(lambda: self.close())

    def getEditorWindow(self):
        return self.editorWindow

    #Función que genera la matriz de n dimensiones con sus caracteristicas
    def createMatrix(self, row, column):
        self.lineEdit = QtWidgets.QLineEdit(self.ui.scrollAreaWidgetContents)
        self.lineEdit.setMinimumSize(QtCore.QSize(70, 70))
        self.lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit.setObjectName("lineEdit" + str(row + 1) + "X" + str(column + 1) + "Y")
        self.labelsReferences.append(self.lineEdit)
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
                         MatrixData.setDiffusionMatrixSingleData(self, x, y, diffusionComb, arraylEdit, 
                         allNewMatrix.matrixCoefficientPDE[domains["domain"]][0], allNewMatrix.matrixCoefficientPDE)
                        else:
                         MatrixData.setDiffusionMatrixMultipleData(self, x, y, diffusionComb, arraylEdit, 
                         allNewMatrix.matrixCoefficientPDE[domains["domain"]][0], allNewMatrix.matrixCoefficientPDE)
                    if pos == 2:
                      MatrixData.setMatrixSingleData(self, x, y, arraylEdit[1][0], 
                      allNewMatrix.matrixCoefficientPDE[domains["domain"]][1], allNewMatrix.matrixCoefficientPDE, 2)
                    if pos == 4:
                      MatrixData.setMatrixSingleData(self, x, y, arraylEdit[3][0], 
                      allNewMatrix.matrixCoefficientPDE[domains["domain"]][2], allNewMatrix.matrixCoefficientPDE, 3)
                    if pos == 5:
                      MatrixData.setMatrixSingleData(self, x, y, arraylEdit[4][0], 
                      allNewMatrix.matrixCoefficientPDE[domains["domain"]][3], allNewMatrix.matrixCoefficientPDE, 4)
                    if pos == 6:
                      MatrixData.setMatrixDoubleData(self, x, y, arraylEdit[5][0], arraylEdit[5][1], 
                      allNewMatrix.matrixCoefficientPDE[domains["domain"]][4], allNewMatrix.matrixCoefficientPDE, 6)
                    if pos == 7:
                      MatrixData.setMatrixDoubleData(self, x, y, arraylEdit[6][0], arraylEdit[6][1], 
                      allNewMatrix.matrixCoefficientPDE[domains["domain"]][5], allNewMatrix.matrixCoefficientPDE, 7)
        Modules.ManageFiles.ManageFiles.FileData.checkUpdateFile(window)

    def fillMatrix(self, matrix, win, allMatrix, pos):
         for x in range(allNewMatrix.n):
            for y in range(allNewMatrix.n):
                self.cell = self.findChild(QtWidgets.QLineEdit, "lineEdit" + str(x + 1) + "X" + str(y + 1) + "Y")
                self.cell.setEnabled(True)
                if self.cell.text() == None or self.cell.text() == '':
                 matrix[x][y] = ''
                else:
                 try:
                    if MatrixData.flagAllDomains == False:
                        matrix[x][y] = str(float(self.cell.text()))
                    else:
                        if pos == 2:
                            for i in range(MatrixData.domains):
                                allMatrix[i][1][x][y] = str(float(self.cell.text()))
                        elif pos == 3:
                            for i in range(MatrixData.domains):
                                allMatrix[i][2][x][y] = str(float(self.cell.text()))
                        elif pos == 4:
                            for i in range(MatrixData.domains):
                                allMatrix[i][3][x][y] = str(float(self.cell.text()))
                    
                 except Exception:
                    QMessageBox.warning(self, "Important message", "Solo puede ingresar valores numericos")
                    return
         print(allMatrix)
         Modules.ManageFiles.ManageFiles.Update.currentData(win, pos)
         self.close()
       
    def editMatrix(self, matrix, arrayComb, win, pos):
        self.setWindowFlags(self.defaultWindowFlag)
        self.btnAccept.show()
        self.btnCancel.show()
        self.win = win
        self.posMatrix = pos
        self.currentMatrix = matrix
        self.clearMatrix()
        for x in range(allNewMatrix.n):
            for y in range(allNewMatrix.n):
                self.cell = self.findChild(QtWidgets.QLineEdit, "lineEdit" + str(x + 1) + "X" + str(y + 1) + "Y")
                self.cell.setEnabled(True)
                if matrix[x][y] == "None" or matrix[x][y] == '':
                 self.cell.clear()
                else:
                 MatrixData.pullAndFormatCell(self, x, y,  matrix)
        self.showdialog(self.findChild(QtWidgets.QLineEdit, "lineEdit" + (str(arrayComb[0].currentIndex() + 1) + "X" + (str(arrayComb[1].currentIndex() + 1)) + "Y")))

    def showMeDiffusion(self, matrix, arrayComb):
        self.setWindowFlags(QtCore.Qt.Popup)
        self.btnAccept.hide()
        self.btnCancel.hide()
        self
        self.clearMatrix()
        for x in range(allNewMatrix.n):
            for y in range(allNewMatrix.n):
                self.cell = self.findChild(QtWidgets.QLineEdit, "lineEdit" + str(x + 1) + "X" + str(y + 1) + "Y")
                self.cell.setEnabled(False)
                if matrix[x][y] == "None" or matrix[x][y] == '':
                 self.cell.clear()
                else:
                 MatrixData.pullAndFormatCell(self, x, y,  matrix)
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
        self.setWindowFlags(QtCore.Qt.Popup)
        self.btnAccept.hide()
        self.btnCancel.hide()
        self.clearMatrix()
        for x in range(allNewMatrix.n):
            for y in range(allNewMatrix.n):
                self.cell = self.findChild(QtWidgets.QLineEdit, "lineEdit" + str(x + 1) + "X" + str(y + 1) + "Y")
                self.cell.setEnabled(False)
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
        self.buttonsLayout = self.ui.horizontalLayout_3
        self.btnAccept = self.ui.btnAccept
        self.btnCancel = self.ui.btnCancel
        self.defaultWindowFlag = self.windowFlags()
        self.currentMatrix = None
        self.labelsReferences = []
        self.posMatrix = None
        self.win = None
        #Rows
        for x in range(0, n):
            #Columns
                self.createVector(x)

        self.btnAccept.clicked.connect(lambda: self.fillVector(self.currentMatrix, 
        self.win, allNewMatrix.vectorCoefficientPDE, self.posMatrix))
        self.btnCancel.clicked.connect(lambda: self.close())

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

    def fillVector(self, matrix, win, allMatrix, pos):
         for x in range(allNewMatrix.n):
                self.cell = self.findChild(QtWidgets.QLineEdit, "lineEdit" + str(x + 1) + "X" + "1Y")
                if self.cell.text() == '':
                 matrix[x] = ''
                else:
                 try:
                    if MatrixData.flagAllDomains == False:
                        matrix[x] = str(float(self.cell.text()))
                    else:
                        for i in range(MatrixData.domains):
                            allMatrix[i][0][0][x] = str(float(self.cell.text()))
                 except Exception:
                    QMessageBox.warning(self, "Important message", "Solo puede ingresar valores numericos")
                    return
         print(allMatrix)
         Modules.ManageFiles.ManageFiles.Update.currentData(win, pos)
         self.close()

    def editVector(self, matrix, win, pos):
        self.setWindowFlags(self.defaultWindowFlag)
        self.win = win
        self.btnAccept.show()
        self.btnCancel.show()
        self.posMatrix = pos
        self.currentMatrix = matrix
        self.clearVector()
        for x in range(allNewMatrix.n):
                self.cell = self.findChild(QtWidgets.QLineEdit, "lineEdit" + str(x + 1) + "X" + "1Y")
                self.cell.setEnabled(True)
                if matrix[x] == "None" or matrix[x] == '':
                 self.cell.setText('')
                 self.cell.setText('')
                else:
                 MatrixData.pullAndFormatVector(self, x,  matrix)
        self.showDialog()

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
                     MatrixData.setVectorSingleData(self, x, arraylEdit[2][0], 
                     allNewMatrix.vectorCoefficientPDE[domains["domain"]][0][0], allNewMatrix.vectorCoefficientPDE)
                    if pos == 8:
                     MatrixData.setVectorDoubleData(self, x, arraylEdit[7][0], arraylEdit[7][1], 
                     allNewMatrix.vectorCoefficientPDE[domains["domain"]][1][0], allNewMatrix.vectorCoefficientPDE)
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
        self.setWindowFlags(QtCore.Qt.Popup)
        self.btnAccept.hide()
        self.btnCancel.hide()
        self.clearVector()
        for x in range(allNewMatrix.n):
                self.cell = self.findChild(QtWidgets.QLineEdit, "lineEdit" + str(x + 1) + "X" + "1Y")
                self.cell.setEnabled(False)
                if matrix[x] != "None":
                 MatrixData.pullAndFormatVector(self, x, matrix)
                else:
                 self.cell.clear()
        self.showdialog(self.findChild(QtWidgets.QLineEdit, "lineEdit" + (str(arrayComb[0].currentIndex() + 1) + "X" + "1Y")))

    def showDialog(self):
        self.show()

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

