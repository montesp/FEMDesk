from dialogMatrix import *
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5 import Qt, QtCore, QtGui
import Modules.Matrix.createMatrix
from Modules.Matrix.MatrixData import MatrixData
from Modules.Dictionary.DMatrix import *
import Modules.ManageFiles.ManageFiles
from functools import partial

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
        self.win, Modules.Matrix.createMatrix.allNewMatrix.matrixCoefficientPDE, self.posMatrix))
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
         for x in range(Modules.Matrix.createMatrix.allNewMatrix.n):
            for y in range(Modules.Matrix.createMatrix.allNewMatrix.n):
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
                    QMessageBox.warning(self, "Important message", "You can only enter numeric values")
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
        for x in range(Modules.Matrix.createMatrix.allNewMatrix.n):
            for y in range(Modules.Matrix.createMatrix.allNewMatrix.n):
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