from dialogMatrix import *
import Modules.Matrix.createMatrix
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5 import Qt, QtCore, QtGui
from Modules.Matrix.MatrixData import MatrixData
from Modules.Dictionary.DMatrix import *
import Modules.ManageFiles.ManageFiles
from functools import partial

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
        self.win, Modules.Matrix.createMatrix.allNewMatrix.vectorCoefficientPDE, self.posMatrix))
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
         for x in range(Modules.Matrix.createMatrix.allNewMatrix.n):
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
                    QMessageBox.warning(self, "Important message", "You can only enter numeric values")
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
        for x in range(Modules.Matrix.createMatrix.allNewMatrix.n):
                self.cell = self.findChild(QtWidgets.QLineEdit, "lineEdit" + str(x + 1) + "X" + "1Y")
                self.cell.setEnabled(True)
                if matrix[x] == "None" or matrix[x] == '':
                 self.cell.setText('')
                 self.cell.setText('')
                else:
                 MatrixData.pullAndFormatVector(self, x,  matrix)
        self.showDialogEdit()

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
                     Modules.Matrix.createMatrix.allNewMatrix.vectorCoefficientPDE[domains["domain"]][0][0], 
                     Modules.Matrix.createMatrix.allNewMatrix.vectorCoefficientPDE)
                    if pos == 8:
                     MatrixData.setVectorDoubleData(self, x, arraylEdit[7][0], arraylEdit[7][1], 
                     Modules.Matrix.createMatrix.allNewMatrix.vectorCoefficientPDE[domains["domain"]][1][0], 
                     Modules.Matrix.createMatrix.allNewMatrix.vectorCoefficientPDE)
        Modules.ManageFiles.ManageFiles.FileData.checkUpdateFile(window)
        

     #Función para limpiar la casilla especifica e insertarle los datos
    def insertVector(self, matrix):
        self.clearVector()
        for x in range(Modules.Matrix.createMatrix.allNewMatrix.n):
                self.cell = self.findChild(QtWidgets.QLineEdit, "lineEdit" + str(x + 1) + "X" + "1Y")
                if matrix[x] != "None":
                 self.cell.insert(matrix[x])
                else:
                 self.cell.clear()

    #Función para mandar a llamar otra función que muestre el vector de la sección seleccionada por el usuario
    def showMe(self, matrix, arrayComb, pos):
        self.setWindowFlags(QtCore.Qt.Popup)
        self.btnAccept.hide()
        self.btnCancel.hide()
        self.clearVector()
        for x in range(Modules.Matrix.createMatrix.allNewMatrix.n):
                self.cell = self.findChild(QtWidgets.QLineEdit, "lineEdit" + str(x + 1) + "X" + "1Y")
                self.cell.setEnabled(False)
                if matrix[x] == "None" or matrix[x] == '':
                    self.cell.clear()
                else:
                    if pos == 8:
                        MatrixData.pullAndFormatDoubleVector(self, x, matrix)
                    else:
                        MatrixData.pullAndFormatVector(self, x, matrix)
        self.showDialogPreview(self.findChild(QtWidgets.QLineEdit, "lineEdit" + (str(arrayComb[0].currentIndex() + 1) + "X" + "1Y")))

    def showDialogEdit(self):
        self.show()

    #Función que muestra un vector
    def showDialogPreview(self, cell):
        QtCore.QTimer.singleShot(0, partial(self.ui.scrollArea.ensureWidgetVisible, cell))
        cell.setStyleSheet("color : blue")
        self.show()

    #Función para limpiar todas las casillas del vector
    def clearVector(self):
        for row in range(Modules.Matrix.createMatrix.allNewMatrix.n):
             self.cell = self.findChild(QtWidgets.QLineEdit, "lineEdit" + str(row + 1) + "X" + "1Y")
             self.cell.setStyleSheet("")
             self.cell.clear()
