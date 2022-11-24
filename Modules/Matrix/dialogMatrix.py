from dialogMatrix import *
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5 import Qt, QtCore, QtGui
from Modules.Matrix.MatrixData import MatrixData
from Modules.Dictionary.DMatrix import *
import Modules.ManageFiles.ManageFiles
from functools import partial
import Modules.Matrix.createMatrix

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
        self.win, Modules.Matrix.createMatrix.allNewMatrix.matrixCoefficientPDE, self.posMatrix))
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
                         Modules.Matrix.createMatrix.allNewMatrix.matrixCoefficientPDE[domains["domain"]][0], 
                         Modules.Matrix.createMatrix.allNewMatrix.matrixCoefficientPDE)
                        else:
                         MatrixData.setDiffusionMatrixMultipleData(self, x, y, diffusionComb, arraylEdit, 
                         Modules.Matrix.createMatrix.allNewMatrix.matrixCoefficientPDE[domains["domain"]][0], 
                         Modules.Matrix.createMatrix.allNewMatrix.matrixCoefficientPDE)
                    if pos == 2:
                      MatrixData.setMatrixSingleData(self, x, y, arraylEdit[1][0], 
                      Modules.Matrix.createMatrix.allNewMatrix.matrixCoefficientPDE[domains["domain"]][1], 
                      Modules.Matrix.createMatrix.allNewMatrix.matrixCoefficientPDE, 2)
                    if pos == 4:
                      MatrixData.setMatrixSingleData(self, x, y, arraylEdit[3][0], 
                      Modules.Matrix.createMatrix.allNewMatrix.matrixCoefficientPDE[domains["domain"]][2], 
                      Modules.Matrix.createMatrix.allNewMatrix.matrixCoefficientPDE, 3)
                    if pos == 5:
                      MatrixData.setMatrixSingleData(self, x, y, arraylEdit[4][0], 
                      Modules.Matrix.createMatrix.allNewMatrix.matrixCoefficientPDE[domains["domain"]][3], 
                      Modules.Matrix.createMatrix.allNewMatrix.matrixCoefficientPDE, 4)
                    if pos == 6:
                      MatrixData.setMatrixDoubleData(self, x, y, arraylEdit[5][0], arraylEdit[5][1], 
                      Modules.Matrix.createMatrix.allNewMatrix.matrixCoefficientPDE[domains["domain"]][4], 
                      Modules.Matrix.createMatrix.allNewMatrix.matrixCoefficientPDE, 6)
                    if pos == 7:
                      MatrixData.setMatrixDoubleData(self, x, y, arraylEdit[6][0], arraylEdit[6][1], 
                      Modules.Matrix.createMatrix.allNewMatrix.matrixCoefficientPDE[domains["domain"]][5], 
                      Modules.Matrix.createMatrix.allNewMatrix.matrixCoefficientPDE, 7)
        Modules.ManageFiles.ManageFiles.FileData.checkUpdateFile(window)

    def fillMatrix(self, matrix, win, allMatrix, pos):
         for x in range(Modules.Matrix.createMatrix.allNewMatrix.n):
            for y in range(Modules.Matrix.createMatrix.allNewMatrix.n):
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
                        elif pos == 4:
                            for i in range(MatrixData.domains):
                                allMatrix[i][2][x][y] = str(float(self.cell.text()))
                        elif pos == 5:
                            for i in range(MatrixData.domains):
                                allMatrix[i][3][x][y] = str(float(self.cell.text()))
                    
                 except Exception:
                    QMessageBox.warning(self, "Important message", "You can only enter numeric values")
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
        for x in range(Modules.Matrix.createMatrix.allNewMatrix.n):
            for y in range(Modules.Matrix.createMatrix.allNewMatrix.n):
                self.cell = self.findChild(QtWidgets.QLineEdit, "lineEdit" + str(x + 1) + "X" + str(y + 1) + "Y")
                self.cell.setEnabled(True)
                if matrix[x][y] == "None" or matrix[x][y] == '':
                 self.cell.clear()
                else:
                 MatrixData.pullAndFormatCell(self, x, y,  matrix)
        self.showdialogEdit()

    def showMeDiffusion(self, matrix, arrayComb):
        self.setWindowFlags(QtCore.Qt.Popup)
        self.btnAccept.hide()
        self.btnCancel.hide()
        self.clearMatrix()
        for x in range(Modules.Matrix.createMatrix.allNewMatrix.n):
            for y in range(Modules.Matrix.createMatrix.allNewMatrix.n):
                self.cell = self.findChild(QtWidgets.QLineEdit, "lineEdit" + str(x + 1) + "X" + str(y + 1) + "Y")
                self.cell.setEnabled(False)
                if matrix[x][y] == "None" or matrix[x][y] == '':
                 self.cell.clear()
                else:
                        MatrixData.pullAndFormatDiffusionCell(self, x, y, matrix)
        self.showdialogPreview(self.findChild(QtWidgets.QLineEdit, "lineEdit" + (str(arrayComb[0].currentIndex() + 1) + "X" + (str(arrayComb[1].currentIndex() + 1)) + "Y")))

                 
     #Función para limpiar la casilla especifica e insertarle los datos
    def insertMatrix(self, matrix):
        self.clearMatrix()
        for x in range(Modules.Matrix.createMatrix.allNewMatrix.n):
            for y in range(Modules.Matrix.createMatrix.allNewMatrix.n):
                self.cell = self.findChild(QtWidgets.QLineEdit, "lineEdit" + str(x + 1) + "X" + str(y + 1) + "Y")
                if matrix[x][y] != "None":
                 self.cell.insert(matrix[x][y])
                else:
                 self.cell.clear()

    #Función para mandar a llamar otra función que muestre la matriz de la sección seleccionada por el usuario
    def showMe(self, matrix, arrayComb, pos):
        self.setWindowFlags(QtCore.Qt.Popup)
        self.btnAccept.hide()
        self.btnCancel.hide()
        self.clearMatrix()
        for x in range(Modules.Matrix.createMatrix.allNewMatrix.n):
            for y in range(Modules.Matrix.createMatrix.allNewMatrix.n):
                self.cell = self.findChild(QtWidgets.QLineEdit, "lineEdit" + str(x + 1) + "X" + str(y + 1) + "Y")
                self.cell.setEnabled(False)
                if matrix[x][y] == "None" or matrix[x][y] == '':
                    self.cell.clear()
                else:
                    if pos == 6 or pos == 7:
                        MatrixData.pullAndFormatDoubleCell(self, x, y, matrix)
                    else:
                        MatrixData.pullAndFormatCell(self, x, y, matrix)
        self.showdialogPreview(self.findChild(QtWidgets.QLineEdit, "lineEdit" + (str(arrayComb[0].currentIndex() + 1) + "X" + (str(arrayComb[1].currentIndex() + 1)) + "Y")))


    def showdialogEdit(self):
        self.show()

    #Función que muestra una matriz
    def showdialogPreview(self, cell):
        QtCore.QTimer.singleShot(0, partial(self.ui.scrollArea.ensureWidgetVisible, cell))
        cell.setStyleSheet("color : blue")
        self.show()

    #Función para limpiar todas los QLineEdit de la matrix a mostrar
    def clearMatrix(self):
        for row in range(Modules.Matrix.createMatrix.allNewMatrix.n):
            for column in range(Modules.Matrix.createMatrix.allNewMatrix.n):
             self.cell = self.findChild(QtWidgets.QLineEdit, "lineEdit" + str(row + 1) + "X" + str(column + 1) + "Y")
             self.cell.setStyleSheet("")
             self.cell.setFixedSize(QtCore.QSize(70, 70))
             self.cell.clear()  
    #Función para limpiar los datos de la matrix almacenada
    def clearMatrixData(self, matrix):
        dialog = QMessageBox.question(self, 'Important', 'Are you sure you want to reset the array? All data will be lost', QMessageBox.Cancel | QMessageBox.Yes)
        if dialog == QMessageBox.Yes:
         matrix.fill('')
         Modules.ManageFiles.ManageFiles.FileData.checkUpdateFile(self)
        else:
            print("Operation Canceled")
