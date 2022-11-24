from dialogMatrix import *
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5 import Qt, QtCore, QtGui
from Modules.Matrix.MatrixData import MatrixData
from Modules.Dictionary.DMatrix import *
import Modules.ManageFiles.ManageFiles
from functools import partial
import Modules.Matrix.createMatrix

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
        self.win, Modules.Matrix.createMatrix.allNewMatrix.vectorCoefficientPDE, self.posMatrix))
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
         for x in range(Modules.Matrix.createMatrix.allNewMatrix.n):
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
        for x in range(Modules.Matrix.createMatrix.allNewMatrix.n):
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

        
