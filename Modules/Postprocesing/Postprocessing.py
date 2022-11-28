from Modules.Postprocesing.Global import resolverEq as motor
from PyQt5.QtWidgets import QLineEdit
import numpy as np

class Postprocessing():
    ConditionsCF = []
    def __init__(self):
        self.dataPost = []
        self.heatConvectionList = None
        self.densityHeat = None
        self.temp = None
        self.gradTx = None
        self.gradTy = None
        self.qx = None
        self.qy = None

    def recieveTypeConditions(self, ConditionsCFList):
        ConditionsCF = np.array(ConditionsCFList)
        print('Postprocesado de Conditions Recibido')
        print(ConditionsCF)
        self.dataPost.append(ConditionsCF)
        print(self.dataPost)

    def recieveHeatConvection(self, heatConvection):
        # heatC = np.array(heatConvection)
        # print('heat Convection Recibido')
        print('heat convection recive')
        print(heatConvection)
        self.heatConvectionList = heatConvection
        # print(self.heatConvectionList)
    
    def recieveDensityHeatCapacity(self, densityHeatCapacity):
        print('density heat capacity')
        print(densityHeatCapacity)
        self.densityHeat = densityHeatCapacity

    def changeResultsType(self, win):
        def setValuesIntoTable(tablePostData ,values:list):
            tableCells = []
            tablePostData.setRowCount(0)
            tablePostData.setRowCount(len(values))
            for r in range(tablePostData.rowCount()):
                for c in range(2):
                    lineEdit = QLineEdit()
                    lineEdit.setReadOnly(True)
                    tablePostData.setCellWidget(r,c, lineEdit)
                    tableCells.append(tablePostData.cellWidget(r,c))

            index = 0
            for val in values:
                tableCells[index].setText(str(index+1))
                tableCells[index+1].setText(str(val))
                index += 2

        tablePostData = win.tblNodesPost

        if win.cmbPostData.currentText() == "T (K)":
            setValuesIntoTable(tablePostData, self.temp)
        elif win.cmbPostData.currentText() == "gradTx (K/m)":
            setValuesIntoTable(tablePostData, self.gradTx)
        elif win.cmbPostData.currentText() == "gradTy (K/m)":
            setValuesIntoTable(tablePostData, self.gradTy)
        elif win.cmbPostData.currentText() == "qx (W/m^2)":
            setValuesIntoTable(tablePostData, self.qx)
        elif win.cmbPostData.currentText() == "qy (W/m^2)":
            setValuesIntoTable(tablePostData, self.qy)

    def generateResults(self, win):
        motor(win.canvas.nodes, win.canvas.bound, win.canvas.tabl, self.dataPost, self.heatConvectionList)
        temp = []
        file1 = open('u.txt', 'r')
        for line in file1:
            temp.append(line.strip())
        file1.close()
        self.temp = list(map(float, temp))

        gradTx = []
        file1 = open('ux.txt', 'r')
        for line in file1:
            gradTx.append(line.strip())
        file1.close()
        self.gradTx = list(map(float, gradTx))

        gradTy = []
        file1 = open('ux.txt', 'r')
        for line in file1:
            gradTy.append(line.strip())
        file1.close()
        self.gradTy = list(map(float, gradTy))

        qx = []
        file1 = open('ux.txt', 'r')
        for line in file1:
            qx.append(line.strip())
        file1.close()
        self.qx = list(map(float, qx))

        qy = []
        file1 = open('ux.txt', 'r')
        for line in file1:
            qy.append(line.strip())
        file1.close()
        self.qy = list(map(float, qy))

        win.canvas.showMeshPost(self.temp)