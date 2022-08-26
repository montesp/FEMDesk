import opcode
import os
from openpyxl import Workbook
from PyQt5.QtWidgets import QFileDialog, QWidget, QLineEdit
from Modules.Dictionary.DMatrix import *


class openSaveDialog(QWidget):
    def __init__(self):
        super().__init__()
        self.windowTitle("Ingrese el nombre")


class FileData():
    def getFileName(self):
        option = QFileDialog.Option()
        #option|=QFileDialog.DontUseNativeDialog
        file_filter= 'Excel File (*.xlsx *.xls)'
        QFileDialog.getOpenFileName(
            self,
            caption='Select a file',
            directory= "Saves",
            filter=file_filter,
            initialFilter='Excel File (*.xlsx *.xls)',
            options=option
        )
        

    def newFileName(self, section, m, comb):
        wb = Workbook()
        sheet = wb.active

        option = QFileDialog.Options()
        file = QFileDialog.getSaveFileName(QWidget(), 
        "Save File", 
        "Saves\\.xlsx", 
        "Excel File (*.xlsx *.xls)", 
        options=option)

        FileData.newData(file, wb, sheet, section, m, comb)

    def newData(file, wb, sheet, section, m, comb):
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

        FileData.writeData(file, wb, sheet, section, comb)



    def writeData(file, wb, sheet, section, comb):
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
        