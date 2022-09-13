from logging.config import valid_ident
import opcode
import os
from openpyxl import Workbook, load_workbook
from PyQt5.QtWidgets import QFileDialog, QWidget, QLineEdit
from Modules.Dictionary.DMatrix import *
from Modules.Dictionary.DFiles import *
from Modules.Matrix import *
import numpy as np


class openSaveDialog(QWidget):
    def __init__(self):
        super().__init__()
        self.windowTitle("Ingrese el nombre")


class FileData():
    def getFileName(self):
        option = QFileDialog.Option()
        file_filter= 'Excel File (*.xlsx *.xls)'
        file = QFileDialog.getOpenFileName(
            self,
            caption='Select a file',
            directory= "Saves",
            filter=file_filter,
            initialFilter='Excel File (*.xlsx *.xls)',
            options=option
        )
        if file != '':
          #try:
                wb = load_workbook(file[0])
                sheet = wb.active
                FileData.loadData(self, sheet, wb)
                directory["dir"] = str(file[0])
                self.lblDirectory.setText(directory["dir"])
                print(directory)
          #except Exception:
                #print("Operacion Cancelada")


    def checkUpdateFile(self):
        if directory["dir"] != "":
          fileIndicator["*"] = "*"
          self.lblDirectory.setText(directory["dir"] + fileIndicator["*"])
        
    def newFileName(self, section, comb):
        wb = Workbook()
        sheet = wb.active

        option = QFileDialog.Options()
        file = QFileDialog.getSaveFileName(QWidget(), 
        "Save File", 
        "Saves\\.xlsx", 
        "Excel File (*.xlsx *.xls)", 
        options=option)

        if file != '':
          #try:
                fileName = file[0]
                FileData.newData(self, file, wb, sheet, section, comb)
                directory["dir"] = str(file[0])
                self.lblDirectory.setText(directory["dir"])
          #except Exception:
                #print("Operacion Cancelada")

    def saveAsFile(self, section, m, comb):
        wb = Workbook()
        sheet = wb.active

        option = QFileDialog.Options()
        file = QFileDialog.getSaveFileName(QWidget(), 
        "Save File", 
        "Saves\\.xlsx", 
        "Excel File (*.xlsx *.xls)", 
        options=option)

        if file != '':
          try:
                FileData.newData(self, file, wb, sheet, section, m, comb)
                directory["dir"] = str(file[0])
                self.lblDirectory.setText(directory["dir"])
          except Exception:
                print("Operacion Cancelada")

    def updateFile(self, section, m, comb):
        wb = Workbook()
        sheet = wb.active
        file = directory["dir"]
        FileData.updateData(self, file, wb, sheet, section, comb)

    def newData(self, file, wb, sheet, section, comb):
        """for i in range(comb.count()):
          strSection = ",".join(i for i in noItemsCoeffM["items"])"""

        wb1 = wb.create_sheet('diffusion')
        
        wb2 = wb.create_sheet('absorption')
        
        wb3 = wb.create_sheet('source')
        
        wb4 = wb.create_sheet('mass')
        
        wb5 = wb.create_sheet('damMass')
        
        wb6 = wb.create_sheet('cFlux')
        
        wb7 = wb.create_sheet('convection')
        
        wb8 = wb.create_sheet('cSource')
  


        sheet.column_dimensions['A'].width = 18
        sheet.column_dimensions['B'].width = 18
        sheet.column_dimensions['C'].width = 18
        sheet.column_dimensions['D'].width = 18

        inputMode = sheet['A1']
        inputMode.value = "Input Mode"

        nVariables = sheet['B1']
        nVariables.value = "No.Variables"

        nSectionCoeffM = sheet['C1']
        nSectionCoeffM.value = "No.ItemsCoeffM"

        itemSectionCoeffM = sheet['D1']
        itemSectionCoeffM.value = "ItemsCoeffM"

        FileData.writeData(self, file, wb, sheet, section, comb, wb1, wb2, wb3, wb4, wb5, wb6, wb7, wb8)
        fileIndicator["*"] = ""
        self.lblDirectory.setText(directory["dir"])
        self.actionSaves.setEnabled(True)
        self.actionSave_As.setEnabled(True)
        self.actionClose.setEnabled(True)


    def writeData(self, file, wb, sheet, section, comb, wb1, wb2, wb3, wb4, wb5, wb6, wb7, wb8):
        strSection = ",".join(str(i) for i in noItemsCoeffM["items"])
        sheet.cell(row= 2, column = 1, value= diffusionMatrix["inputMode"])
        sheet.cell(row= 2, column = 2, value= initialValues["noVariables"])
        sheet.cell(row= 2, column = 3, value= noItemsCoeffM["noItems"])
        sheet.cell(row= 2, column = 4, value= strSection)
        print(allNewMatrix.cSourceM)

        for i in noItemsCoeffM["items"]:
                if i == 1:
                        for row in range(allNewMatrix.n):
                         for column in range(allNewMatrix.n):
                                wb1.cell(row=row + 1, column=column + 1, value= allNewMatrix.diffusionM[row][column])
                elif i == 2:
                        for row in range(allNewMatrix.n):
                         for column in range(allNewMatrix.n):
                                wb2.cell(row=row + 1, column=column + 1, value= allNewMatrix.absorptionM[row][column])
                elif i == 3: 
                        for row in range(allNewMatrix.n):
                                wb3.cell(row=row + 1, column=1, value= allNewMatrix.sourceM[row])
                elif i == 4:
                       for row in range(allNewMatrix.n):
                         for column in range(allNewMatrix.n):
                                wb4.cell(row=row + 1, column=column + 1, value= allNewMatrix.massM[row][column])
                elif i == 5:
                       for row in range(allNewMatrix.n):
                         for column in range(allNewMatrix.n):
                                wb5.cell(row=row + 1, column=column + 1, value= allNewMatrix.damMassM[row][column])
                elif i == 6:
                       for row in range(allNewMatrix.n):
                         for column in range(allNewMatrix.n):
                                wb6.cell(row=row + 1, column=column + 1, value= allNewMatrix.cFluxM[row][column])
                elif i == 7:
                       for row in range(allNewMatrix.n):
                         for column in range(allNewMatrix.n):
                                wb7.cell(row=row + 1, column=column + 1, value= allNewMatrix.convectionM[row][column])
                elif i == 8:
                       for row in range(allNewMatrix.n):
                                wb8.cell(row=row + 1, column=1, value= allNewMatrix.cSourceM[row])
                                


        wb.save(file[0])
        fileIndicator["*"] = ""
        self.lblDirectory.setText(directory["dir"])

    def loadData(self, sheet, wb):
        initialValues["noVariables"] = sheet['B2'].value
        n = int(initialValues["noVariables"])
        print(n)
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
        allNewMatrix.n = n


        noItemsCoeffM["items"] = sheet['D2'].value
        check = noItemsCoeffM["items"]
        arCheck = check.split(',')
        numCheck = list(map(int, arCheck))

        wb1 = wb["diffusion"]
        
        wb2 = wb["absorption"]
        
        wb3 = wb["source"]
        
        wb4 = wb["mass"]
        
        wb5 = wb["damMass"]
        
        wb6 = wb["cFlux"]
        
        wb7 = wb["convection"]
        
        wb8 = wb["cSource"]

        
        position = 1
        for i in range(self.CoefficentForM.count()):
            self.CoefficentForM.removeItem(1)

        self.CoefficentForM.insertItem(100, self.arrayCoeffMSection[9], self.arrayCheckNameCoeffM[9])

        print(numCheck)
        for i in numCheck:
            if(i != 0):
                self.CoefficentForM.insertItem(position, self.arrayCoeffMSection[i], self.arrayCheckNameCoeffM[i])
                self.CoefficientCheckBoxArray[i - 1].setChecked(True)
                position+=1

        for i in numCheck:
                if i == 1: 
                        for x in range(allNewMatrix.n):
                                for y in range(allNewMatrix.n):
                                        allNewMatrix.diffusionM[x][y] =  wb1.cell(row=x + 1, column=y + 1).value
                                        print(allNewMatrix.diffusionM[x][y])
                if i == 2: 
                        for x in range(allNewMatrix.n):
                                for y in range(allNewMatrix.n):
                                        allNewMatrix.absorptionM[x][y] =  wb2.cell(row=x + 1, column=y + 1).value
                                        print(allNewMatrix.absorptionM[x][y])
                if i == 3: 
                        for x in range(allNewMatrix.n):
                                for y in range(allNewMatrix.n):
                                        allNewMatrix.sourceM[x] =  wb3.cell(row=x + 1, column=1).value
                                        print(allNewMatrix.sourceM[x])
                if i == 4: 
                        for x in range(allNewMatrix.n):
                                for y in range(allNewMatrix.n):
                                        allNewMatrix.massM[x][y] =  wb4.cell(row=x + 1, column=y + 1).value
                                        print(allNewMatrix.massM[x][y])
                if i == 5: 
                        for x in range(allNewMatrix.n):
                                for y in range(allNewMatrix.n):
                                        allNewMatrix.damMassM[x][y] =  wb5.cell(row=x + 1, column=y + 1).value
                                        print(allNewMatrix.damMassM[x][y])
                if i == 6: 
                        for x in range(allNewMatrix.n):
                                for y in range(allNewMatrix.n):
                                        allNewMatrix.cFluxM[x][y] =  wb6.cell(row=x + 1, column=y + 1).value
                                        print(allNewMatrix.cFluxM[x][y])
                if i == 7: 
                        for x in range(allNewMatrix.n):
                                for y in range(allNewMatrix.n):
                                        allNewMatrix.convectionM[x][y] =  wb7.cell(row=x + 1, column=y + 1).value
                                        print(allNewMatrix.convectionM[x][y])
                if i == 8: 
                        for x in range(allNewMatrix.n):
                                for y in range(allNewMatrix.n):
                                        allNewMatrix.cSourceM[x] =  wb8.cell(row=x + 1, column=1).value
                                        print(allNewMatrix.cSourceM[x])

        fileIndicator["*"] = ""
        self.lblDirectory.setText(directory["dir"])
        self.actionSaves.setEnabled(True)
        self.actionSave_As.setEnabled(True)
        self.actionClose.setEnabled(True)


    def updateData(self, file, wb, sheet, section, comb):
        self.writeData(directory["dir"])
        wb.save(directory["dir"])
        fileIndicator["*"] = ""
        self.lblDirectory.setText(directory["dir"])


 
    def resetData(self):
        for i in range(1, self.CoefficentForM.count()):
            self.CoefficentForM.removeItem(1)

        for i, item in enumerate(self.CoefficientCheckBoxArray):
                self.CoefficientCheckBoxArray[i - 1].setChecked(False)

        for i, item in enumerate(self.arrayCmbRowColumns):
         for j, item in enumerate(self.arrayCmbRowColumns[i]):
                        self.arrayCmbRowColumns[i][j].clear()
                        self.arrayCmbRowColumns[i][j].addItem("1")

        for i, item in enumerate(self.arraylEditsCoefficientsPDE):
         for j, item in enumerate(self.arraylEditsCoefficientsPDE[i]):
                        self.arraylEditsCoefficientsPDE[i][j].setText("")

        self.cmbInitialValues.setCurrentIndex(0)
        self.lblDirectory.setText("")

        self.actionSaves.setEnabled(False)
        self.actionSave_As.setEnabled(False)
        self.actionClose.setEnabled(False)

        diffusionMatrix["inputMode"] = 1
        noItemsCoeffM["noItems"] = 0
        noItemsCoeffM["items"] = 0
        initialValues["noVariables"] = 1

        fileIndicator["*"] = ""
        directory["dir"] = ""

       
        







        

        