from dialogMatrix import *
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5 import Qt, QtCore, QtGui
import Modules.Matrix.createMatrix
from Modules.Matrix.MatrixData import MatrixData
from Modules.Dictionary.DMatrix import *
import Modules.ManageFiles.ManageFiles
from functools import partial

class dialogTableDiffusionMatrix(QDialog):
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
        self.comboboxes = []
        self.tables = []

        for x in range(0, n):
            #Columns
            for y in range(0, n):
                self.createMatrix(x, y)
        
        dialogTableDiffusionMatrix.createSignals(self, self.comboboxes, self.tables)
        dialogTableDiffusionMatrix.updateMatrix(self, self.comboboxes, self.tables)

        self.btnAccept.clicked.connect(lambda: self.fillMatrix(self.currentMatrix, 
        self.win, Modules.Matrix.createMatrix.allNewMatrix.matrixCoefficientPDE, self.posMatrix))
        self.btnCancel.clicked.connect(lambda: self.close())

    #Función que genera la matriz de n dimensiones con sus caracteristicas
    def createMatrix(self, row, column):
        self.vboxlayout = QtWidgets.QVBoxLayout()
        self.combo = QtWidgets.QComboBox()
        self.combo.addItems(['Isotropic', 'Diagonal', 'Symmetric', 'Full'])
        self.combo.setObjectName("combobox" + str(row + 1) + "X" + str(column + 1) + "Y")
        self.table = QtWidgets.QTableWidget()
        self.table.setRowCount(2)
        self.table.setColumnCount(2)
        self.table.setItem(0,0, QtWidgets.QTableWidgetItem(''))
        self.table.setItem(0,1, QtWidgets.QTableWidgetItem(''))
        self.table.setItem(1,0, QtWidgets.QTableWidgetItem(''))
        self.table.setItem(1,1, QtWidgets.QTableWidgetItem(''))
        self.table.setColumnWidth(0, 80)
        self.table.setColumnWidth(1, 80)
        self.table.setRowHeight(0, 35)
        self.table.setRowHeight(1, 35)
        self.table.horizontalHeader().hide()
        self.table.verticalHeader().hide()
        self.table.setObjectName("table" + str(row + 1) + "X" + str(column + 1) + "Y")
        self.table.setFixedHeight(76)
        self.table.setFixedWidth(162)
        self.vboxlayout.addWidget(self.combo)
        self.vboxlayout.addWidget(self.table)
        self.comboboxes.append(self.combo)
        self.tables.append(self.table)
        self.ui.gridLayout.addLayout(self.vboxlayout, row, column, 1, 1, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.ui.scrollArea.setWidget(self.ui.scrollAreaWidgetContents)
        self.ui.verticalLayout.addWidget(self.ui.scrollArea)

    def updateMatrix(self, comboboxes, tables):
        for index, combo in enumerate(comboboxes):
                dialogTableDiffusionMatrix.changeTextSymmetry(self, combo, tables[index])


    def createSignals(self, comboboxes, tables):
        for index, combo in enumerate(comboboxes):
            combo.currentIndexChanged.connect(lambda _, c=combo, t=tables[index]: dialogTableDiffusionMatrix.changeComboConfiguration(self, combo=c, table=t))
            tables[index].itemClicked.connect(lambda _, c=combo, t=tables[index]: dialogTableDiffusionMatrix.changeTextSymmetry(self, combo=c, table=t))
            

    def changeTextSymmetry(self, combo, table):
        if combo.currentIndex() == 2:
            table.item(1,0).setText('')
            table.item(1,0).setText(table.item(0,1).text())
        else:
            return

    def changeComboConfiguration(self, combo, table):
        standardFlags = table.item(0,0).flags()
        if combo.currentIndex() == 0:
            table.item(0,0).setFlags(standardFlags)
            table.item(0,1).setFlags(QtCore.Qt.ItemIsEditable)
            table.item(1,0).setFlags(QtCore.Qt.ItemIsEditable)
            table.item(1,1).setFlags(QtCore.Qt.ItemIsEditable)
            table.item(0,0).setText("")
            table.item(0,1).setText("")
            table.item(1,0).setText("")
            table.item(1,1).setText("")
        elif combo.currentIndex() == 1:
            table.item(0,1).setText("0")
            table.item(1,0).setText("0")
            table.item(0,0).setFlags(standardFlags)
            table.item(1,1).setFlags(standardFlags)
            table.item(0,1).setFlags(QtCore.Qt.ItemIsEditable)
            table.item(1,0).setFlags(QtCore.Qt.ItemIsEditable)
        elif combo.currentIndex() == 2:
            table.item(0,0).setFlags(standardFlags)
            table.item(0,1).setFlags(standardFlags)
            table.item(1,0).setFlags(QtCore.Qt.ItemIsEditable)
            table.item(1,1).setFlags(standardFlags)
            table.item(0,0).setText("")
            table.item(0,1).setText("")
            table.item(1,0).setText("")
            table.item(1,1).setText("")
        elif combo.currentIndex() == 3:
            table.item(0,0).setFlags(standardFlags)
            table.item(0,1).setFlags(standardFlags)
            table.item(1,0).setFlags(standardFlags)
            table.item(1,1).setFlags(standardFlags)
            table.item(0,0).setText("")
            table.item(0,1).setText("")
            table.item(1,0).setText("")
            table.item(1,1).setText("")


    def fillMatrix(self, matrix, win, allMatrix, pos):
         for x in range(Modules.Matrix.createMatrix.allNewMatrix.n):
            for y in range(Modules.Matrix.createMatrix.allNewMatrix.n):
                self.cell = self.findChild(QtWidgets.QTableWidget, "table" + str(x + 1) + "X" + str(y + 1) + "Y")
                self.comboCell = self.findChild(QtWidgets.QComboBox, "combobox" + str(x + 1) + "X" + str(y + 1) + "Y")
                if self.cell.itemAt(0,0).text() == '' or self.cell.itemAt(0,1).text() == '' or self.cell.itemAt(1,0).text() == '' or self.cell.itemAt(1,1).text() == '':
                 matrix[x][y] = ''
                else:
                    try:
                        if self.comboCell.currentIndex() == 0:
                            arTable = []
                            arTable.append(float(self.cell.item(0,0).text()))
                            arTable.append(float(self.cell.item(0,0).text()))
                            arTable.append(float(self.cell.item(0,0).text()))
                            arTable.append(float(self.cell.item(0,0).text()))
                            arTable.append(self.comboCell.currentIndex())
                        else:
                            arTable = []
                            arTable.append(float(self.cell.item(0,0).text()))
                            arTable.append(float(self.cell.item(0,1).text()))
                            arTable.append(float(self.cell.item(1,0).text()))
                            arTable.append(float(self.cell.item(1,1).text()))
                            arTable.append(self.comboCell.currentIndex())

                        if MatrixData.flagAllDomains == False:
                            matrix[x][y] = str(arTable)
                        else:
                                for i in range(MatrixData.domains):
                                    allMatrix[i][0][x][y] = str(arTable)
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
        for x in range(Modules.Matrix.createMatrix.allNewMatrix.n):
            for y in range(Modules.Matrix.createMatrix.allNewMatrix.n):
                self.cell = self.findChild(QtWidgets.QTableWidget, "table" + str(x + 1) + "X" + str(y + 1) + "Y")
                self.comboCell = self.findChild(QtWidgets.QComboBox, "combobox" + str(x + 1) + "X" + str(y + 1) + "Y")
                self.cell.setItem(0,0, QtWidgets.QTableWidgetItem('00'))
                self.cell.setItem(0,1, QtWidgets.QTableWidgetItem('01'))
                self.cell.setItem(1,0, QtWidgets.QTableWidgetItem('10'))
                self.cell.setItem(1,1, QtWidgets.QTableWidgetItem('11'))
                dialogTableDiffusionMatrix.changeComboConfiguration(self, self.comboCell, self.cell)
                if matrix[x][y] == "None" or matrix[x][y] == '':
                 self.cell.item(0,0).setText('')
                 self.cell.item(0,1).setText('')
                 self.cell.item(1,0).setText('')
                 self.cell.item(1,1).setText('')
                else:
                 MatrixData.pullAndFormatTableDiffusion(self, x, y,  matrix, self.comboCell)
        self.showDialog()

    def showDialog(self):
        self.show()

