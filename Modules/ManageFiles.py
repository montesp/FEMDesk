from logging.config import valid_ident
import opcode
import os
from openpyxl import Workbook, load_workbook
from PyQt5.QtWidgets import QFileDialog, QWidget, QLineEdit
from Modules.Dictionary.DMatrix import *
from Modules.Dictionary.DFiles import *


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
          try:
                wb = load_workbook(file[0])
                sheet = wb.active
                FileData.loadData(self, sheet)
                directory["dir"] = str(file[0])
                self.lblDirectory.setText(directory["dir"])
                print(directory)
          except Exception:
                print("Operacion Cancelada")


    def checkUpdateFile(self):
        if directory["dir"] != "":
          fileIndicator["*"] = "*"
          self.lblDirectory.setText(directory["dir"] + fileIndicator["*"])
        
    def newFileName(self, section, m, comb):
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

    def newData(self, file, wb, sheet, section, m, comb):
        sheet.column_dimensions['B'].width = 10
        sheet.column_dimensions['C'].width = 15
        sheet.column_dimensions['D'].width = 15
        sheet.column_dimensions['E'].width = 15
        sheet.column_dimensions['F'].width = 15
        sheet.column_dimensions['G'].width = 15
        sheet.column_dimensions['H'].width = 15
        sheet.column_dimensions['I'].width = 15
        sheet.column_dimensions['J'].width = 15
        sheet.column_dimensions['K'].width = 15

        pos33 = sheet['B3']
        pos33.value = "Position"
        lEdit11M33 = sheet['C3']
        lEdit11M33.value = "LineEdit11"
        lEdit12M33 = sheet['D3']
        lEdit12M33.value = "LineEdit12"
        lEdit13M33 = sheet['E3']
        lEdit13M33.value = "LineEdit13"
        lEdit21M33 = sheet['F3']
        lEdit21M33.value = "LineEdit21"
        lEdit22M33 = sheet['G3']
        lEdit22M33.value = "LineEdit22"
        lEdit23M33 = sheet['H3']
        lEdit23M33.value = "LineEdit23"
        lEdit31M33 = sheet['I3']
        lEdit31M33.value = "LineEdit31"
        lEdit32M33 = sheet['J3']
        lEdit32M33.value = "LineEdit32"
        lEdit33M33 = sheet['K3']
        lEdit33M33.value = "LineEdit33"

        pos22 = sheet['B13']
        pos22.value = "Position"
        lEdit11M22 = sheet['C13']
        lEdit11M22.value = "LineEdit11"
        lEdit12M22 = sheet['D13']
        lEdit12M22.value = "LineEdit12"
        lEdit21M22 = sheet['E13']
        lEdit21M22.value = "LineEdit21"
        lEdit22M22 = sheet['F13']
        lEdit22M22.value = "LineEdit22"

        pos11 = sheet['B23']
        pos11.value = "Position"
        lEdit11M11 = sheet['C23']
        lEdit11M11.value = "LineEdit11"

        pos31 = sheet['B33']
        pos31.value = "Position"
        lEdit11M31 = sheet['C33']
        lEdit11M31.value = "LineEdit11"
        lEdit21M31 = sheet['D33']
        lEdit21M31.value = "LineEdit21"
        lEdit31M31 = sheet['E33']
        lEdit31M31.value = "LineEdit31"

        pos21 = sheet['B43']
        pos21.value = "Position"
        lEdit11M21 = sheet['C43']
        lEdit11M21.value = "LineEdit11"
        lEdit21M21 = sheet['D43']
        lEdit21M21.value = "LineEdit21"

        inputMode = sheet['H18']
        inputMode.value = "Input Mode"

        nVariables = sheet['I18']
        nVariables.value = "No.Variables"

        nSectionCoeffM = sheet['J18']
        nSectionCoeffM.value = "No.ItemsCoeffM"

        itemSectionCoeffM = sheet['K18']
        itemSectionCoeffM.value = "ItemsCoeffM"

        FileData.writeData(self, file, wb, sheet, section, comb)
        fileIndicator["*"] = ""
        self.lblDirectory.setText(directory["dir"])
        self.actionSaves.setEnabled(True)
        self.actionSave_As.setEnabled(True)
        self.actionClose.setEnabled(True)

    def loadData(self, sheet):
        noItemsCoeffM["items"] = sheet['K19'].value
        check = noItemsCoeffM.get('items')
        arCheck = check.split(',')
        numCheck = list(map(int, arCheck))
        print(numCheck)
        initialValues["noVariables"] = sheet['I19'].value
        noVar = initialValues.get('noVariables')
        print(noVar)
        
        position = 1
        for i in range(self.CoefficentForM.count()):
            self.CoefficentForM.removeItem(1)

        self.CoefficentForM.insertItem(100, self.arrayCoeffMSection[9], self.arrayCheckNameCoeffM[9])

        for i in numCheck:
            if(i != 0):
                self.CoefficentForM.insertItem(position, self.arrayCoeffMSection[i], self.arrayCheckNameCoeffM[i])
                self.CoefficientCheckBoxArray[i - 1].setChecked(True)
                position+=1

        a33 = 0
        a22 = 0
        a11 = 0
        a31 = 0
        a21 = 0

        for i in range(len(numCheck)):
          if numCheck[i] == 3 or numCheck[i] == 8:
           if noVar == 3:
                j = 34 + a31
                if numCheck[i] == 3:
                        sourceMatrix["lEdit11M31"] = sheet['C' + str(j)].value
                        sourceMatrix["lEdit21M31"] = sheet['D' + str(j)].value
                        sourceMatrix["lEdit31M31"] = sheet['E' + str(j)].value
                if numCheck[i] == 8:
                        cSourceMatrix["lEdit11M31"] = sheet['C' + str(j)].value
                        cSourceMatrix["lEdit21M31"] = sheet['D' + str(j)].value
                        cSourceMatrix["lEdit31M31"] = sheet['E' + str(j)].value
                a31+=1
           if noVar == 2:
                j = 44 + a21
                if numCheck[i] == 3:
                        sourceMatrix["lEdit11M21"] = sheet['C' + str(j)].value
                        sourceMatrix["lEdit21M21"] = sheet['D' + str(j)].value
                if numCheck[i] == 8:
                        cSourceMatrix["lEdit11M21"] = sheet['C' + str(j)].value
                        cSourceMatrix["lEdit21M21"] = sheet['D' + str(j)].value
                a21+=1
           if noVar == 1:
                j = 24 + a11
                if numCheck[i] == 3:
                        sourceMatrix["lEdit11M11"] = sheet['C' + str(j)].value
                if numCheck[i] == 8:
                        cSourceMatrix["lEdit11M11"] = sheet['C' + str(j)].value
                a11+=1
          else:
              if noVar == 3:
                j = 4 + a33
                if numCheck[i] == 1:
                        diffusionMatrix["lEdit11M33"] = sheet['C' + str(j)].value
                        diffusionMatrix["lEdit12M33"] = sheet['D' + str(j)].value
                        diffusionMatrix["lEdit13M33"] = sheet['E' + str(j)].value
                        diffusionMatrix["lEdit21M33"] = sheet['F' + str(j)].value
                        diffusionMatrix["lEdit22M33"] = sheet['G' + str(j)].value
                        diffusionMatrix["lEdit23M33"] = sheet['H' + str(j)].value
                        diffusionMatrix["lEdit31M33"] = sheet['I' + str(j)].value
                        diffusionMatrix["lEdit32M33"] = sheet['J' + str(j)].value
                        diffusionMatrix["lEdit33M33"] = sheet['K' + str(j)].value
                if numCheck[i] == 2:
                        absorptionMatrix["lEdit11M33"] = sheet['C' + str(j)].value
                        absorptionMatrix["lEdit12M33"] = sheet['D' + str(j)].value
                        absorptionMatrix["lEdit13M33"] = sheet['E' + str(j)].value
                        absorptionMatrix["lEdit21M33"] = sheet['F' + str(j)].value
                        absorptionMatrix["lEdit22M33"] = sheet['G' + str(j)].value
                        absorptionMatrix["lEdit23M33"] = sheet['H' + str(j)].value
                        absorptionMatrix["lEdit31M33"] = sheet['I' + str(j)].value
                        absorptionMatrix["lEdit32M33"] = sheet['J' + str(j)].value
                        absorptionMatrix["lEdit33M33"] = sheet['K' + str(j)].value
                if numCheck[i] == 4:
                        massMatrix["lEdit11M33"] = sheet['C' + str(j)].value
                        massMatrix["lEdit12M33"] = sheet['D' + str(j)].value
                        massMatrix["lEdit13M33"] = sheet['E' + str(j)].value
                        massMatrix["lEdit21M33"] = sheet['F' + str(j)].value
                        massMatrix["lEdit22M33"] = sheet['G' + str(j)].value
                        massMatrix["lEdit23M33"] = sheet['H' + str(j)].value
                        massMatrix["lEdit31M33"] = sheet['I' + str(j)].value
                        massMatrix["lEdit32M33"] = sheet['J' + str(j)].value
                        massMatrix["lEdit33M33"] = sheet['K' + str(j)].value
                if numCheck[i] == 5:
                        damMassMatrix["lEdit11M33"] = sheet['C' + str(j)].value
                        damMassMatrix["lEdit12M33"] = sheet['D' + str(j)].value
                        damMassMatrix["lEdit13M33"] = sheet['E' + str(j)].value
                        damMassMatrix["lEdit21M33"] = sheet['F' + str(j)].value
                        damMassMatrix["lEdit22M33"] = sheet['G' + str(j)].value
                        damMassMatrix["lEdit23M33"] = sheet['H' + str(j)].value
                        damMassMatrix["lEdit31M33"] = sheet['I' + str(j)].value
                        damMassMatrix["lEdit32M33"] = sheet['J' + str(j)].value
                        damMassMatrix["lEdit33M33"] = sheet['K' + str(j)].value
                if numCheck[i] == 6:
                        cFluxMatrix["lEdit11M33"] = sheet['C' + str(j)].value
                        cFluxMatrix["lEdit12M33"] = sheet['D' + str(j)].value
                        cFluxMatrix["lEdit13M33"] = sheet['E' + str(j)].value
                        cFluxMatrix["lEdit21M33"] = sheet['F' + str(j)].value
                        cFluxMatrix["lEdit22M33"] = sheet['G' + str(j)].value
                        cFluxMatrix["lEdit23M33"] = sheet['H' + str(j)].value
                        cFluxMatrix["lEdit31M33"] = sheet['I' + str(j)].value
                        cFluxMatrix["lEdit32M33"] = sheet['J' + str(j)].value
                        cFluxMatrix["lEdit33M33"] = sheet['K' + str(j)].value
                if numCheck[i] == 7:
                        convectionMatrix["lEdit11M33"] = sheet['C' + str(j)].value
                        convectionMatrix["lEdit12M33"] = sheet['D' + str(j)].value
                        convectionMatrix["lEdit13M33"] = sheet['E' + str(j)].value
                        convectionMatrix["lEdit21M33"] = sheet['F' + str(j)].value
                        convectionMatrix["lEdit22M33"] = sheet['G' + str(j)].value
                        convectionMatrix["lEdit23M33"] = sheet['H' + str(j)].value
                        convectionMatrix["lEdit31M33"] = sheet['I' + str(j)].value
                        convectionMatrix["lEdit32M33"] = sheet['J' + str(j)].value
                        convectionMatrix["lEdit33M33"] = sheet['K' + str(j)].value
                a33+=1
              if noVar == 2:
                j = 14 + a22
                if numCheck[i] == 1:
                        diffusionMatrix["lEdit11M22"] = sheet['C' + str(j)].value
                        diffusionMatrix["lEdit12M22"] = sheet['D' + str(j)].value
                        diffusionMatrix["lEdit21M22"] = sheet['E' + str(j)].value
                        diffusionMatrix["lEdit22M22"] = sheet['F' + str(j)].value
                if numCheck[i] == 2:
                        absorptionMatrix["lEdit11M22"] = sheet['C' + str(j)].value
                        absorptionMatrix["lEdit12M22"] = sheet['D' + str(j)].value
                        absorptionMatrix["lEdit21M22"] = sheet['E' + str(j)].value
                        absorptionMatrix["lEdit22M22"] = sheet['F' + str(j)].value
                if numCheck[i] == 4:
                        massMatrix["lEdit11M22"] = sheet['C' + str(j)].value
                        massMatrix["lEdit12M22"] = sheet['D' + str(j)].value
                        massMatrix["lEdit21M22"] = sheet['E' + str(j)].value
                        massMatrix["lEdit22M22"] = sheet['F' + str(j)].value
                if numCheck[i] == 5:
                        damMassMatrix["lEdit11M22"] = sheet['C' + str(j)].value
                        damMassMatrix["lEdit12M22"] = sheet['D' + str(j)].value
                        damMassMatrix["lEdit21M22"] = sheet['E' + str(j)].value
                        damMassMatrix["lEdit22M22"] = sheet['F' + str(j)].value
                if numCheck[i] == 6:
                        cFluxMatrix["lEdit11M22"] = sheet['C' + str(j)].value
                        cFluxMatrix["lEdit12M22"] = sheet['D' + str(j)].value
                        cFluxMatrix["lEdit21M22"] = sheet['E' + str(j)].value
                        cFluxMatrix["lEdit22M22"] = sheet['F' + str(j)].value
                if numCheck[i] == 7:
                        convectionMatrix["lEdit11M22"] = sheet['C' + str(j)].value
                        convectionMatrix["lEdit12M22"] = sheet['D' + str(j)].value
                        convectionMatrix["lEdit21M22"] = sheet['E' + str(j)].value
                        convectionMatrix["lEdit22M22"] = sheet['F' + str(j)].value
                a22+=1
              if noVar == 1:
                j = 24 + a11
                if numCheck[i] == 1:
                        diffusionMatrix["lEdit11M11"] = sheet['C' + str(j)].value
                if numCheck[i] == 2:
                        absorptionMatrix["lEdit11M11"] = sheet['C' + str(j)].value
                if numCheck[i] == 4:
                        massMatrix["lEdit11M11"] = sheet['C' + str(j)].value
                if numCheck[i] == 5:
                        damMassMatrix["lEdit11M11"] = sheet['C' + str(j)].value
                if numCheck[i] == 6:
                        cFluxMatrix["lEdit11M11"] = sheet['C' + str(j)].value
                if numCheck[i] == 7:
                        convectionMatrix["lEdit11M11"] = sheet['C' + str(j)].value
                a11+=1
        fileIndicator["*"] = ""
        self.lblDirectory.setText(directory["dir"])
        self.actionSaves.setEnabled(True)
        self.actionSave_As.setEnabled(True)
        self.actionClose.setEnabled(True)


    def updateData(self, file, wb, sheet, section, comb):
        sheet.column_dimensions['B'].width = 10
        sheet.column_dimensions['C'].width = 15
        sheet.column_dimensions['D'].width = 15
        sheet.column_dimensions['E'].width = 15
        sheet.column_dimensions['F'].width = 15
        sheet.column_dimensions['G'].width = 15
        sheet.column_dimensions['H'].width = 15
        sheet.column_dimensions['I'].width = 15
        sheet.column_dimensions['J'].width = 15
        sheet.column_dimensions['K'].width = 15

        pos33 = sheet['B3']
        pos33.value = "Position"
        lEdit11M33 = sheet['C3']
        lEdit11M33.value = "LineEdit11"
        lEdit12M33 = sheet['D3']
        lEdit12M33.value = "LineEdit12"
        lEdit13M33 = sheet['E3']
        lEdit13M33.value = "LineEdit13"
        lEdit21M33 = sheet['F3']
        lEdit21M33.value = "LineEdit21"
        lEdit22M33 = sheet['G3']
        lEdit22M33.value = "LineEdit22"
        lEdit23M33 = sheet['H3']
        lEdit23M33.value = "LineEdit23"
        lEdit31M33 = sheet['I3']
        lEdit31M33.value = "LineEdit31"
        lEdit32M33 = sheet['J3']
        lEdit32M33.value = "LineEdit32"
        lEdit33M33 = sheet['K3']
        lEdit33M33.value = "LineEdit33"

        pos22 = sheet['B13']
        pos22.value = "Position"
        lEdit11M22 = sheet['C13']
        lEdit11M22.value = "LineEdit11"
        lEdit12M22 = sheet['D13']
        lEdit12M22.value = "LineEdit12"
        lEdit21M22 = sheet['E13']
        lEdit21M22.value = "LineEdit21"
        lEdit22M22 = sheet['F13']
        lEdit22M22.value = "LineEdit22"

        pos11 = sheet['B23']
        pos11.value = "Position"
        lEdit11M11 = sheet['C23']
        lEdit11M11.value = "LineEdit11"

        pos31 = sheet['B33']
        pos31.value = "Position"
        lEdit11M31 = sheet['C33']
        lEdit11M31.value = "LineEdit11"
        lEdit21M31 = sheet['D33']
        lEdit21M31.value = "LineEdit21"
        lEdit31M31 = sheet['E33']
        lEdit31M31.value = "LineEdit31"

        pos21 = sheet['B43']
        pos21.value = "Position"
        lEdit11M21 = sheet['C43']
        lEdit11M21.value = "LineEdit11"
        lEdit21M21 = sheet['D43']
        lEdit21M21.value = "LineEdit21"

        inputMode = sheet['H18']
        inputMode.value = "Input Mode"

        nVariables = sheet['I18']
        nVariables.value = "No.Variables"

        nSectionCoeffM = sheet['J18']
        nSectionCoeffM.value = "No.ItemsCoeffM"

        itemSectionCoeffM = sheet['K18']
        itemSectionCoeffM.value = "ItemsCoeffM"


        arComb = []

        for i in range(comb.count()):
            arComb.append(int(comb.itemText(i)))

        a33  = 0
        a22 = 0
        a11 = 0
        a31 = 0
        a21 = 0
        print(section)
        print(len(section))


        strSection = ",".join(str(i) for i in noItemsCoeffM["items"])

        sheet.cell(row=19, column=8, value = diffusionMatrix["inputMode"])
        sheet.cell(row=19, column=9, value = initialValues["noVariables"])
        sheet.cell(row=19, column=10, value = noItemsCoeffM["noItems"])
        sheet.cell(row=19, column=11, value = strSection)

        for i in range(len(section)):
         if section[i] == 3 or section[i] == 8:
            if 3 in arComb:
                j = 34 + a31
                if section[i] == 3:
                        sheet.cell(row=j, column=2, value= section[i])
                        sheet.cell(row=j, column = 3, value = sourceMatrix["lEdit11M31"])
                        sheet.cell(row=j, column = 4, value = sourceMatrix["lEdit21M31"])
                        sheet.cell(row=j, column = 5, value = sourceMatrix["lEdit31M31"])
                if section[i] == 8:
                        sheet.cell(row=j, column=2, value= section[i])
                        sheet.cell(row=j, column = 3, value = cSourceMatrix["lEdit11M31"])
                        sheet.cell(row=j, column = 4, value = cSourceMatrix["lEdit21M31"])
                        sheet.cell(row=j, column = 5, value = cSourceMatrix["lEdit31M31"])
                a31+=1

            elif 2 in arComb:
                j = 44 + a21
                if section[i] == 3:
                        sheet.cell(row=j, column=2, value= section[i])
                        sheet.cell(row=j, column = 3, value = sourceMatrix["lEdit11M21"])
                        sheet.cell(row=j, column = 4, value = sourceMatrix["lEdit21M21"])
                if section[i] == 8:
                        sheet.cell(row=j, column=2, value= section[i])
                        sheet.cell(row=j, column = 3, value = cSourceMatrix["lEdit11M21"])
                        sheet.cell(row=j, column = 4, value = cSourceMatrix["lEdit21M21"])
                a21+=1
            else: 
                j = 24 + a11
                if section[i] == 3:
                        sheet.cell(row=j, column=2, value= section[i])
                        sheet.cell(row=j, column = 3, value = sourceMatrix["lEdit11M11"])
                if section[i] == 8:
                        sheet.cell(row=j, column=2, value= section[i])
                        sheet.cell(row=j, column = 3, value = cSourceMatrix["lEdit11M11"])
                a11+=1

         else:
            if 3 in arComb:
                j = 4 + a33
                if section[i] == 1:
                        sheet.cell(row=j, column=2, value= section[i])
                        sheet.cell(row=j, column = 3, value = diffusionMatrix["lEdit11M33"])
                        sheet.cell(row=j, column = 4, value = diffusionMatrix["lEdit12M33"])
                        sheet.cell(row=j, column = 5, value = diffusionMatrix["lEdit13M33"])
                        sheet.cell(row=j, column = 6, value = diffusionMatrix["lEdit21M33"])
                        sheet.cell(row=j, column = 7, value = diffusionMatrix["lEdit22M33"])
                        sheet.cell(row=j, column = 8, value = diffusionMatrix["lEdit23M33"])
                        sheet.cell(row=j, column = 9, value = diffusionMatrix["lEdit31M33"])
                        sheet.cell(row=j, column = 10, value = diffusionMatrix["lEdit32M33"])
                        sheet.cell(row=j, column = 11, value = diffusionMatrix["lEdit33M33"])
                if section[i] == 2:
                        sheet.cell(row=j, column=2, value= section[i])
                        sheet.cell(row=j, column = 3, value = absorptionMatrix["lEdit11M33"])
                        sheet.cell(row=j, column = 4, value = absorptionMatrix["lEdit12M33"])
                        sheet.cell(row=j, column = 5, value = absorptionMatrix["lEdit13M33"])
                        sheet.cell(row=j, column = 6, value = absorptionMatrix["lEdit21M33"])
                        sheet.cell(row=j, column = 7, value = absorptionMatrix["lEdit22M33"])
                        sheet.cell(row=j, column = 8, value = absorptionMatrix["lEdit23M33"])
                        sheet.cell(row=j, column = 9, value = absorptionMatrix["lEdit31M33"])
                        sheet.cell(row=j, column = 10, value = absorptionMatrix["lEdit32M33"])
                        sheet.cell(row=j, column = 11, value = absorptionMatrix["lEdit33M33"])
                if section[i] == 4:
                        sheet.cell(row=j, column=2, value= section[i])
                        sheet.cell(row=j, column = 3, value = massMatrix["lEdit11M33"])
                        sheet.cell(row=j, column = 4, value = massMatrix["lEdit12M33"])
                        sheet.cell(row=j, column = 5, value = massMatrix["lEdit13M33"])
                        sheet.cell(row=j, column = 6, value = massMatrix["lEdit21M33"])
                        sheet.cell(row=j, column = 7, value = massMatrix["lEdit22M33"])
                        sheet.cell(row=j, column = 8, value = massMatrix["lEdit23M33"])
                        sheet.cell(row=j, column = 9, value = massMatrix["lEdit31M33"])
                        sheet.cell(row=j, column = 10, value = massMatrix["lEdit32M33"])
                        sheet.cell(row=j, column = 11, value = massMatrix["lEdit33M33"])
                if section[i] == 5:
                        sheet.cell(row=j, column=2, value= section[i])
                        sheet.cell(row=j, column = 3, value = damMassMatrix["lEdit11M33"])
                        sheet.cell(row=j, column = 4, value = damMassMatrix["lEdit12M33"])
                        sheet.cell(row=j, column = 5, value = damMassMatrix["lEdit13M33"])
                        sheet.cell(row=j, column = 6, value = damMassMatrix["lEdit21M33"])
                        sheet.cell(row=j, column = 7, value = damMassMatrix["lEdit22M33"])
                        sheet.cell(row=j, column = 8, value = damMassMatrix["lEdit23M33"])
                        sheet.cell(row=j, column = 9, value = damMassMatrix["lEdit31M33"])
                        sheet.cell(row=j, column = 10, value = damMassMatrix["lEdit32M33"])
                        sheet.cell(row=j, column = 11, value = damMassMatrix["lEdit33M33"])
                if section[i] == 6:
                        sheet.cell(row=j, column=2, value= section[i])
                        sheet.cell(row=j, column = 3, value = cFluxMatrix["lEdit11M33"])
                        sheet.cell(row=j, column = 4, value = cFluxMatrix["lEdit12M33"])
                        sheet.cell(row=j, column = 5, value = cFluxMatrix["lEdit13M33"])
                        sheet.cell(row=j, column = 6, value = cFluxMatrix["lEdit21M33"])
                        sheet.cell(row=j, column = 7, value = cFluxMatrix["lEdit22M33"])
                        sheet.cell(row=j, column = 8, value = cFluxMatrix["lEdit23M33"])
                        sheet.cell(row=j, column = 9, value = cFluxMatrix["lEdit31M33"])
                        sheet.cell(row=j, column = 10, value = cFluxMatrix["lEdit32M33"])
                        sheet.cell(row=j, column = 11, value = cFluxMatrix["lEdit33M33"])
                if section[i] == 7:
                        sheet.cell(row=j, column=2, value= section[i])
                        sheet.cell(row=j, column = 3, value = convectionMatrix["lEdit11M33"])
                        sheet.cell(row=j, column = 4, value = convectionMatrix["lEdit12M33"])
                        sheet.cell(row=j, column = 5, value = convectionMatrix["lEdit13M33"])
                        sheet.cell(row=j, column = 6, value = convectionMatrix["lEdit21M33"])
                        sheet.cell(row=j, column = 7, value = convectionMatrix["lEdit22M33"])
                        sheet.cell(row=j, column = 8, value = convectionMatrix["lEdit23M33"])
                        sheet.cell(row=j, column = 9, value = convectionMatrix["lEdit31M33"])
                        sheet.cell(row=j, column = 10, value = convectionMatrix["lEdit32M33"])
                        sheet.cell(row=j, column = 11, value = convectionMatrix["lEdit33M33"])
                a33+=1
            elif 2 in arComb:
                j = 14 + a22
                if section[i] == 1:
                        sheet.cell(row=j, column=2, value= section[i])
                        sheet.cell(row=j, column = 3, value = diffusionMatrix["lEdit11M22"])
                        sheet.cell(row=j, column = 4, value = diffusionMatrix["lEdit12M22"])
                        sheet.cell(row=j, column = 5, value = diffusionMatrix["lEdit21M22"])
                        sheet.cell(row=j, column = 6, value = diffusionMatrix["lEdit22M22"])
                if section[i] == 2:
                        sheet.cell(row=j, column=2, value= section[i])
                        sheet.cell(row=j, column = 3, value = absorptionMatrix["lEdit11M22"])
                        sheet.cell(row=j, column = 4, value = absorptionMatrix["lEdit12M22"])
                        sheet.cell(row=j, column = 5, value = absorptionMatrix["lEdit21M22"])
                        sheet.cell(row=j, column = 6, value = absorptionMatrix["lEdit22M22"])
                if section[i] == 4:
                        sheet.cell(row=j, column=2, value= section[i])
                        sheet.cell(row=j, column = 3, value = massMatrix["lEdit11M22"])
                        sheet.cell(row=j, column = 4, value = massMatrix["lEdit12M22"])
                        sheet.cell(row=j, column = 5, value = massMatrix["lEdit21M22"])
                        sheet.cell(row=j, column = 6, value = massMatrix["lEdit22M22"])
                if section[i] == 5:
                        sheet.cell(row=j, column=2, value= section[i])
                        sheet.cell(row=j, column = 3, value = damMassMatrix["lEdit11M22"])
                        sheet.cell(row=j, column = 4, value = damMassMatrix["lEdit12M22"])
                        sheet.cell(row=j, column = 5, value = damMassMatrix["lEdit21M22"])
                        sheet.cell(row=j, column = 6, value = damMassMatrix["lEdit22M22"])
                if section[i] == 6:
                        sheet.cell(row=j, column=2, value= section[i])
                        sheet.cell(row=j, column = 3, value = cFluxMatrix["lEdit11M22"])
                        sheet.cell(row=j, column = 4, value = cFluxMatrix["lEdit12M22"])
                        sheet.cell(row=j, column = 5, value = cFluxMatrix["lEdit21M22"])
                        sheet.cell(row=j, column = 6, value = cFluxMatrix["lEdit22M22"])
                if section[i] == 7:
                        sheet.cell(row=j, column=2, value= section[i])
                        sheet.cell(row=j, column = 3, value = convectionMatrix["lEdit11M22"])
                        sheet.cell(row=j, column = 4, value = convectionMatrix["lEdit12M22"])
                        sheet.cell(row=j, column = 5, value = convectionMatrix["lEdit21M22"])
                        sheet.cell(row=j, column = 6, value = convectionMatrix["lEdit22M22"])
                a22+=1
                    
            else: 
                j = 24 + a11
                if section[i] == 1:
                        sheet.cell(row=j, column=2, value= section[i])
                        sheet.cell(row=j, column = 3, value = diffusionMatrix["lEdit11M11"])
                if section[i] == 2:
                        sheet.cell(row=j, column=2, value= section[i])
                        sheet.cell(row=j, column = 3, value = absorptionMatrix["lEdit11M11"])
                if section[i] == 4:
                        sheet.cell(row=j, column=2, value= section[i])
                        sheet.cell(row=j, column = 3, value = massMatrix["lEdit11M11"])
                if section[i] == 5:
                        sheet.cell(row=j, column=2, value= section[i])
                        sheet.cell(row=j, column = 3, value = damMassMatrix["lEdit11M11"])
                if section[i] == 6:
                        sheet.cell(row=j, column=2, value= section[i])
                        sheet.cell(row=j, column = 3, value = cFluxMatrix["lEdit11M11"])
                if section[i] == 7:
                        sheet.cell(row=j, column=2, value= section[i])
                        sheet.cell(row=j, column = 3, value = convectionMatrix["lEdit11M11"])
                a11+=1

        wb.save(directory["dir"])
        fileIndicator["*"] = ""
        self.lblDirectory.setText(directory["dir"])

    def writeData(self, file, wb, sheet, section, comb):
        arComb = []

        for i in range(comb.count()):
            arComb.append(int(comb.itemText(i)))

        a33  = 0
        a22 = 0
        a11 = 0
        a31 = 0
        a21 = 0
        print(section)
        print(len(section))


        strSection = ",".join(str(i) for i in noItemsCoeffM["items"])

        sheet.cell(row=19, column=8, value = diffusionMatrix["inputMode"])
        sheet.cell(row=19, column=9, value = initialValues["noVariables"])
        sheet.cell(row=19, column=10, value = noItemsCoeffM["noItems"])
        sheet.cell(row=19, column=11, value = strSection)

        for i in range(len(section)):
         if section[i] == 3 or section[i] == 8:
            if 3 in arComb:
                j = 34 + a31
                if section[i] == 3:
                        sheet.cell(row=j, column=2, value= section[i])
                        sheet.cell(row=j, column = 3, value = sourceMatrix["lEdit11M31"])
                        sheet.cell(row=j, column = 4, value = sourceMatrix["lEdit21M31"])
                        sheet.cell(row=j, column = 5, value = sourceMatrix["lEdit31M31"])
                if section[i] == 8:
                        sheet.cell(row=j, column=2, value= section[i])
                        sheet.cell(row=j, column = 3, value = cSourceMatrix["lEdit11M31"])
                        sheet.cell(row=j, column = 4, value = cSourceMatrix["lEdit21M31"])
                        sheet.cell(row=j, column = 5, value = cSourceMatrix["lEdit31M31"])
                a31+=1

            elif 2 in arComb:
                j = 44 + a21
                if section[i] == 3:
                        sheet.cell(row=j, column=2, value= section[i])
                        sheet.cell(row=j, column = 3, value = sourceMatrix["lEdit11M21"])
                        sheet.cell(row=j, column = 4, value = sourceMatrix["lEdit21M21"])
                if section[i] == 8:
                        sheet.cell(row=j, column=2, value= section[i])
                        sheet.cell(row=j, column = 3, value = cSourceMatrix["lEdit11M21"])
                        sheet.cell(row=j, column = 4, value = cSourceMatrix["lEdit21M21"])
                a21+=1
            else: 
                j = 24 + a11
                if section[i] == 3:
                        sheet.cell(row=j, column=2, value= section[i])
                        sheet.cell(row=j, column = 3, value = sourceMatrix["lEdit11M11"])
                if section[i] == 8:
                        sheet.cell(row=j, column=2, value= section[i])
                        sheet.cell(row=j, column = 3, value = cSourceMatrix["lEdit11M11"])
                a11+=1

         else:
            if 3 in arComb:
                j = 4 + a33
                if section[i] == 1:
                        sheet.cell(row=j, column=2, value= section[i])
                        sheet.cell(row=j, column = 3, value = diffusionMatrix["lEdit11M33"])
                        sheet.cell(row=j, column = 4, value = diffusionMatrix["lEdit12M33"])
                        sheet.cell(row=j, column = 5, value = diffusionMatrix["lEdit13M33"])
                        sheet.cell(row=j, column = 6, value = diffusionMatrix["lEdit21M33"])
                        sheet.cell(row=j, column = 7, value = diffusionMatrix["lEdit22M33"])
                        sheet.cell(row=j, column = 8, value = diffusionMatrix["lEdit23M33"])
                        sheet.cell(row=j, column = 9, value = diffusionMatrix["lEdit31M33"])
                        sheet.cell(row=j, column = 10, value = diffusionMatrix["lEdit32M33"])
                        sheet.cell(row=j, column = 11, value = diffusionMatrix["lEdit33M33"])
                if section[i] == 2:
                        sheet.cell(row=j, column=2, value= section[i])
                        sheet.cell(row=j, column = 3, value = absorptionMatrix["lEdit11M33"])
                        sheet.cell(row=j, column = 4, value = absorptionMatrix["lEdit12M33"])
                        sheet.cell(row=j, column = 5, value = absorptionMatrix["lEdit13M33"])
                        sheet.cell(row=j, column = 6, value = absorptionMatrix["lEdit21M33"])
                        sheet.cell(row=j, column = 7, value = absorptionMatrix["lEdit22M33"])
                        sheet.cell(row=j, column = 8, value = absorptionMatrix["lEdit23M33"])
                        sheet.cell(row=j, column = 9, value = absorptionMatrix["lEdit31M33"])
                        sheet.cell(row=j, column = 10, value = absorptionMatrix["lEdit32M33"])
                        sheet.cell(row=j, column = 11, value = absorptionMatrix["lEdit33M33"])
                if section[i] == 4:
                        sheet.cell(row=j, column=2, value= section[i])
                        sheet.cell(row=j, column = 3, value = massMatrix["lEdit11M33"])
                        sheet.cell(row=j, column = 4, value = massMatrix["lEdit12M33"])
                        sheet.cell(row=j, column = 5, value = massMatrix["lEdit13M33"])
                        sheet.cell(row=j, column = 6, value = massMatrix["lEdit21M33"])
                        sheet.cell(row=j, column = 7, value = massMatrix["lEdit22M33"])
                        sheet.cell(row=j, column = 8, value = massMatrix["lEdit23M33"])
                        sheet.cell(row=j, column = 9, value = massMatrix["lEdit31M33"])
                        sheet.cell(row=j, column = 10, value = massMatrix["lEdit32M33"])
                        sheet.cell(row=j, column = 11, value = massMatrix["lEdit33M33"])
                if section[i] == 5:
                        sheet.cell(row=j, column=2, value= section[i])
                        sheet.cell(row=j, column = 3, value = damMassMatrix["lEdit11M33"])
                        sheet.cell(row=j, column = 4, value = damMassMatrix["lEdit12M33"])
                        sheet.cell(row=j, column = 5, value = damMassMatrix["lEdit13M33"])
                        sheet.cell(row=j, column = 6, value = damMassMatrix["lEdit21M33"])
                        sheet.cell(row=j, column = 7, value = damMassMatrix["lEdit22M33"])
                        sheet.cell(row=j, column = 8, value = damMassMatrix["lEdit23M33"])
                        sheet.cell(row=j, column = 9, value = damMassMatrix["lEdit31M33"])
                        sheet.cell(row=j, column = 10, value = damMassMatrix["lEdit32M33"])
                        sheet.cell(row=j, column = 11, value = damMassMatrix["lEdit33M33"])
                if section[i] == 6:
                        sheet.cell(row=j, column=2, value= section[i])
                        sheet.cell(row=j, column = 3, value = cFluxMatrix["lEdit11M33"])
                        sheet.cell(row=j, column = 4, value = cFluxMatrix["lEdit12M33"])
                        sheet.cell(row=j, column = 5, value = cFluxMatrix["lEdit13M33"])
                        sheet.cell(row=j, column = 6, value = cFluxMatrix["lEdit21M33"])
                        sheet.cell(row=j, column = 7, value = cFluxMatrix["lEdit22M33"])
                        sheet.cell(row=j, column = 8, value = cFluxMatrix["lEdit23M33"])
                        sheet.cell(row=j, column = 9, value = cFluxMatrix["lEdit31M33"])
                        sheet.cell(row=j, column = 10, value = cFluxMatrix["lEdit32M33"])
                        sheet.cell(row=j, column = 11, value = cFluxMatrix["lEdit33M33"])
                if section[i] == 7:
                        sheet.cell(row=j, column=2, value= section[i])
                        sheet.cell(row=j, column = 3, value = convectionMatrix["lEdit11M33"])
                        sheet.cell(row=j, column = 4, value = convectionMatrix["lEdit12M33"])
                        sheet.cell(row=j, column = 5, value = convectionMatrix["lEdit13M33"])
                        sheet.cell(row=j, column = 6, value = convectionMatrix["lEdit21M33"])
                        sheet.cell(row=j, column = 7, value = convectionMatrix["lEdit22M33"])
                        sheet.cell(row=j, column = 8, value = convectionMatrix["lEdit23M33"])
                        sheet.cell(row=j, column = 9, value = convectionMatrix["lEdit31M33"])
                        sheet.cell(row=j, column = 10, value = convectionMatrix["lEdit32M33"])
                        sheet.cell(row=j, column = 11, value = convectionMatrix["lEdit33M33"])
                a33+=1
            elif 2 in arComb:
                j = 14 + a22
                if section[i] == 1:
                        sheet.cell(row=j, column=2, value= section[i])
                        sheet.cell(row=j, column = 3, value = diffusionMatrix["lEdit11M22"])
                        sheet.cell(row=j, column = 4, value = diffusionMatrix["lEdit12M22"])
                        sheet.cell(row=j, column = 5, value = diffusionMatrix["lEdit21M22"])
                        sheet.cell(row=j, column = 6, value = diffusionMatrix["lEdit22M22"])
                if section[i] == 2:
                        sheet.cell(row=j, column=2, value= section[i])
                        sheet.cell(row=j, column = 3, value = absorptionMatrix["lEdit11M22"])
                        sheet.cell(row=j, column = 4, value = absorptionMatrix["lEdit12M22"])
                        sheet.cell(row=j, column = 5, value = absorptionMatrix["lEdit21M22"])
                        sheet.cell(row=j, column = 6, value = absorptionMatrix["lEdit22M22"])
                if section[i] == 4:
                        sheet.cell(row=j, column=2, value= section[i])
                        sheet.cell(row=j, column = 3, value = massMatrix["lEdit11M22"])
                        sheet.cell(row=j, column = 4, value = massMatrix["lEdit12M22"])
                        sheet.cell(row=j, column = 5, value = massMatrix["lEdit21M22"])
                        sheet.cell(row=j, column = 6, value = massMatrix["lEdit22M22"])
                if section[i] == 5:
                        sheet.cell(row=j, column=2, value= section[i])
                        sheet.cell(row=j, column = 3, value = damMassMatrix["lEdit11M22"])
                        sheet.cell(row=j, column = 4, value = damMassMatrix["lEdit12M22"])
                        sheet.cell(row=j, column = 5, value = damMassMatrix["lEdit21M22"])
                        sheet.cell(row=j, column = 6, value = damMassMatrix["lEdit22M22"])
                if section[i] == 6:
                        sheet.cell(row=j, column=2, value= section[i])
                        sheet.cell(row=j, column = 3, value = cFluxMatrix["lEdit11M22"])
                        sheet.cell(row=j, column = 4, value = cFluxMatrix["lEdit12M22"])
                        sheet.cell(row=j, column = 5, value = cFluxMatrix["lEdit21M22"])
                        sheet.cell(row=j, column = 6, value = cFluxMatrix["lEdit22M22"])
                if section[i] == 7:
                        sheet.cell(row=j, column=2, value= section[i])
                        sheet.cell(row=j, column = 3, value = convectionMatrix["lEdit11M22"])
                        sheet.cell(row=j, column = 4, value = convectionMatrix["lEdit12M22"])
                        sheet.cell(row=j, column = 5, value = convectionMatrix["lEdit21M22"])
                        sheet.cell(row=j, column = 6, value = convectionMatrix["lEdit22M22"])
                a22+=1
                    
            else: 
                j = 24 + a11
                if section[i] == 1:
                        sheet.cell(row=j, column=2, value= section[i])
                        sheet.cell(row=j, column = 3, value = diffusionMatrix["lEdit11M11"])
                if section[i] == 2:
                        sheet.cell(row=j, column=2, value= section[i])
                        sheet.cell(row=j, column = 3, value = absorptionMatrix["lEdit11M11"])
                if section[i] == 4:
                        sheet.cell(row=j, column=2, value= section[i])
                        sheet.cell(row=j, column = 3, value = massMatrix["lEdit11M11"])
                if section[i] == 5:
                        sheet.cell(row=j, column=2, value= section[i])
                        sheet.cell(row=j, column = 3, value = damMassMatrix["lEdit11M11"])
                if section[i] == 6:
                        sheet.cell(row=j, column=2, value= section[i])
                        sheet.cell(row=j, column = 3, value = cFluxMatrix["lEdit11M11"])
                if section[i] == 7:
                        sheet.cell(row=j, column=2, value= section[i])
                        sheet.cell(row=j, column = 3, value = convectionMatrix["lEdit11M11"])
                a11+=1

        wb.save(file[0])
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

        diffusionMatrix["lEdit11M33"] = ""
        diffusionMatrix["lEdit12M33"] = ""
        diffusionMatrix["lEdit13M33"] = ""
        diffusionMatrix["lEdit21M33"] = ""
        diffusionMatrix["lEdit22M33"] = ""
        diffusionMatrix["lEdit23M33"] = ""
        diffusionMatrix["lEdit31M33"] = ""
        diffusionMatrix["lEdit32M33"] = ""
        diffusionMatrix["lEdit33M33"] = ""

        absorptionMatrix["lEdit11M33"] = ""
        absorptionMatrix["lEdit12M33"] = ""
        absorptionMatrix["lEdit13M33"] = ""
        absorptionMatrix["lEdit21M33"] = ""
        absorptionMatrix["lEdit22M33"] = ""
        absorptionMatrix["lEdit23M33"] = ""
        absorptionMatrix["lEdit31M33"] = ""
        absorptionMatrix["lEdit32M33"] = ""
        absorptionMatrix["lEdit33M33"] = ""

        sourceMatrix["lEdit11M33"] = ""
        sourceMatrix["lEdit12M33"] = ""
        sourceMatrix["lEdit13M33"] = ""
        sourceMatrix["lEdit21M33"] = ""
        sourceMatrix["lEdit22M33"] = ""
        sourceMatrix["lEdit23M33"] = ""
        sourceMatrix["lEdit31M33"] = ""
        sourceMatrix["lEdit32M33"] = ""
        sourceMatrix["lEdit33M33"] = ""

        massMatrix["lEdit11M33"] = ""
        massMatrix["lEdit12M33"] = ""
        massMatrix["lEdit13M33"] = ""
        massMatrix["lEdit21M33"] = ""
        massMatrix["lEdit22M33"] = ""
        massMatrix["lEdit23M33"] = ""
        massMatrix["lEdit31M33"] = ""
        massMatrix["lEdit32M33"] = ""
        massMatrix["lEdit33M33"] = ""

        damMassMatrix["lEdit11M33"] = ""
        damMassMatrix["lEdit12M33"] = ""
        damMassMatrix["lEdit13M33"] = ""
        damMassMatrix["lEdit21M33"] = ""
        damMassMatrix["lEdit22M33"] = ""
        damMassMatrix["lEdit23M33"] = ""
        damMassMatrix["lEdit31M33"] = ""
        damMassMatrix["lEdit32M33"] = ""
        damMassMatrix["lEdit33M33"] = ""

        cFluxMatrix["lEdit11M33"] = ""
        cFluxMatrix["lEdit12M33"] = ""
        cFluxMatrix["lEdit13M33"] = ""
        cFluxMatrix["lEdit21M33"] = ""
        cFluxMatrix["lEdit22M33"] = ""
        cFluxMatrix["lEdit23M33"] = ""
        cFluxMatrix["lEdit31M33"] = ""
        cFluxMatrix["lEdit32M33"] = ""
        cFluxMatrix["lEdit33M33"] = ""

        convectionMatrix["lEdit11M33"] = ""
        convectionMatrix["lEdit12M33"] = ""
        convectionMatrix["lEdit13M33"] = ""
        convectionMatrix["lEdit21M33"] = ""
        convectionMatrix["lEdit22M33"] = ""
        convectionMatrix["lEdit23M33"] = ""
        convectionMatrix["lEdit31M33"] = ""
        convectionMatrix["lEdit32M33"] = ""
        convectionMatrix["lEdit33M33"] = ""

        cSourceMatrix["lEdit11M33"] = ""
        cSourceMatrix["lEdit12M33"] = ""
        cSourceMatrix["lEdit13M33"] = ""
        cSourceMatrix["lEdit21M33"] = ""
        cSourceMatrix["lEdit22M33"] = ""
        cSourceMatrix["lEdit23M33"] = ""
        cSourceMatrix["lEdit31M33"] = ""
        cSourceMatrix["lEdit32M33"] = ""
        cSourceMatrix["lEdit33M33"] = ""

        diffusionMatrix["lEdit11M22"] = ""
        diffusionMatrix["lEdit12M22"] = ""
        diffusionMatrix["lEdit21M22"] = ""
        diffusionMatrix["lEdit22M22"] = ""

        absorptionMatrix["lEdit11M22"] = ""
        absorptionMatrix["lEdit12M22"] = ""
        absorptionMatrix["lEdit21M22"] = ""
        absorptionMatrix["lEdit22M22"] = ""

        sourceMatrix["lEdit11M22"] = ""
        sourceMatrix["lEdit12M22"] = ""
        sourceMatrix["lEdit21M22"] = ""
        sourceMatrix["lEdit22M22"] = ""

        massMatrix["lEdit11M22"] = ""
        massMatrix["lEdit12M22"] = ""
        massMatrix["lEdit21M22"] = ""
        massMatrix["lEdit22M22"] = ""

        damMassMatrix["lEdit11M22"] = ""
        damMassMatrix["lEdit12M22"] = ""
        damMassMatrix["lEdit21M22"] = ""
        damMassMatrix["lEdit22M22"] = ""

        convectionMatrix["lEdit11M22"] = ""
        convectionMatrix["lEdit12M22"] = ""
        convectionMatrix["lEdit21M22"] = ""
        convectionMatrix["lEdit22M22"] = ""

        cSourceMatrix["lEdit11M22"] = ""
        cSourceMatrix["lEdit12M22"] = ""
        cSourceMatrix["lEdit21M22"] = ""
        cSourceMatrix["lEdit22M22"] = ""

        diffusionMatrix["lEdit11M11"] = ""
        absorptionMatrix["lEdit11M11"] = ""
        sourceMatrix["lEdit11M11"] = ""
        massMatrix["lEdit11M11"] = ""
        damMassMatrix["lEdit11M11"] = ""
        convectionMatrix["lEdit11M11"] = ""
        cSourceMatrix["lEdit11M11"] = ""
        







        

        