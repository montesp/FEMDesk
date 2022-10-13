from logging.config import valid_ident
from msilib.schema import File
import opcode
import os
from openpyxl import Workbook, load_workbook
from PyQt5.QtWidgets import QFileDialog, QWidget, QLineEdit, QMessageBox
from Modules.Dictionary.DMatrix import *
from Modules.Dictionary.DFiles import *
from Modules.Matrix import *
import numpy as np


class openSaveDialog(QWidget):
    def __init__(self):
        super().__init__()
        self.windowTitle("Ingrese el nombre")


class FileData():
    #Función para buscar en el explorador un archivo excel para abrir la configuracion guardada y usarla en el programa
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
                FileData.loadData(self, sheet, wb)
                directory["dir"] = str(file[0])
                self.lblDirectory.setText(directory["dir"])
                print(directory)
          except Exception:
                print("Operacion Cancelada")


    def checkUpdateFile(self):
        if directory["dir"] != "":
          fileIndicator["*"] = "*"
          self.lblDirectory.setText(directory["dir"] + fileIndicator["*"])
        
    def newFileName(self):
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
                fileName = file[0]
                FileData.newData(self, fileName, wb, sheet)
                directory["dir"] = str(file[0])
                self.lblDirectory.setText(directory["dir"])
          except Exception:
                print("Operacion Cancelada")

    def saveAsFile(self):
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
                fileName = file[0]
                FileData.newData(self, fileName, wb, sheet)
                directory["dir"] = str(file[0])
                self.lblDirectory.setText(directory["dir"])
          except Exception:
                print("Operacion Cancelada")

    #Función mandada a llamar desde ActionSaves, se encarga de conectar con el archivo excel y actializarlo con nuevos datos
    def updateFile(self):
        wb = load_workbook(directory["dir"])
        sheet = wb.active
        print(wb.sheetnames)
        file = directory["dir"]
        
        wb1 = wb["diffusion"]
        
        wb2 = wb["absorption"]
        
        wb3 = wb["source"]
        
        wb4 = wb["mass"]
        
        wb5 = wb["damMass"]
        
        wb6 = wb["cFlux"]
        
        wb7 = wb["convection"]
        
        wb8 = wb["cSource"]

        FileData.newWriteData(self, file, wb, sheet, wb1, wb2, wb3, wb4, wb5, wb6, wb7, wb8)
        
        
    def resetFile(self):
        print(fileIndicator["*"])
        if fileIndicator["*"] == '*':
         dialog = QMessageBox()
         dialog.setWindowTitle('Aviso')
         dialog.setText('¿Seguro que quieres cerrar el archivo? Se borrarán los cambios no guardados')
         yesdialog = dialog.addButton('Si', QMessageBox.YesRole)
         nodialog = dialog.addButton('No', QMessageBox.NoRole)
         savedialog = dialog.addButton('Guardar Cambios', QMessageBox.YesRole)
         dialog.exec_()
         if dialog.clickedButton() == yesdialog: 
                FileData.resetData(self)
         elif dialog.clickedButton() == nodialog:
                print("Operación Cancelada")
         elif dialog.clickedButton() == savedialog:
                FileData.updateFile(self)
                FileData.resetData(self)
        else:
                FileData.resetData(self)

  
       

    def newData(self, file, wb, sheet):

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

        FileData.newWriteData(self, file, wb, sheet, wb1, wb2, wb3, wb4, wb5, wb6, wb7, wb8)
        


    def newWriteData(self, file, wb, sheet, wb1, wb2, wb3, wb4, wb5, wb6, wb7, wb8):
        strSection = ",".join(str(i) for i in noItemsCoeffM["items"])
        sheet.cell(row= 2, column = 1, value= diffusionMatrix["inputMode"])
        sheet.cell(row= 2, column = 2, value= initialValues["noVariables"])
        sheet.cell(row= 2, column = 3, value= noItemsCoeffM["noItems"])
        sheet.cell(row= 2, column = 4, value= strSection)
        print("Cuales son las secciones activadas a guardar?")
        print(noItemsCoeffM["items"])

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
                                
        wb.save(file)
        fileIndicator["*"] = ""
        self.lblDirectory.setText(directory["dir"] + fileIndicator["*"])
        self.actionSaves.setEnabled(False)
        self.actionSave_As.setEnabled(True)
        self.actionClose.setEnabled(True)
        QMessageBox.information(self, "Important message", "Guardado Exitoso")
        
    #Función para cargar la configuración
    def loadData(self, sheet, wb):
        print("¿Cuantas variables contiene el archivo?")
        initialValues["noVariables"] = sheet['B2'].value
        n = int(initialValues["noVariables"])
        print(n)
        print("¿Cuales son las casillas de sus matrices y vectores?")
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
        diffusionMatrix["inputMode"] = sheet['A2'].value

        noItemsCoeffM["noItems"] = sheet['C2'].value
        check = sheet['D2'].value
        arCheck = check.split(',')
        numCheck = list(map(int, arCheck))
        noItemsCoeffM["items"] = numCheck

        #Actualizar Combobox de cada seccion
        for index, item in enumerate(self.CoefficientCheckBoxArray):
                for j, item in enumerate(self.arrayCmbRowColumns[index]):
                        self.arrayCmbRowColumns[index][j].clear()

                for j, item in enumerate(self.arrayCmbRowColumns[index]):
                    for i in range(1, n + 1):
                        self.arrayCmbRowColumns[index][j].addItem(str(i))
        self.cmbInitialValues.clear()

        for i in range(1, n + 1):
            self.cmbInitialValues.addItem("u" + str(i))

        self.cmbDiffusionCoef.setCurrentIndex(diffusionMatrix["inputMode"])

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

        print("¿Cuales son las secciones que tiene activadas en el Coefficient PDE?")
        print(numCheck)
        for i in numCheck:
            if(i != 0):
                #Activar las secciones del ToolBox
                self.CoefficentForM.insertItem(position, self.arrayCoeffMSection[i], self.arrayCheckNameCoeffM[i])
                self.CoefficientCheckBoxArray[i - 1].setChecked(True)
                position+=1

        #Insertar la información de cada sección en su respectiva matriz o vector
        for i in numCheck:
                if i == 1: 
                        for x in range(allNewMatrix.n):
                                for y in range(allNewMatrix.n):
                                        allNewMatrix.diffusionM[x][y] =  wb1.cell(row=x + 1, column=y + 1).value
                        print("Valores de la Matrix Diffusion")
                        print(allNewMatrix.diffusionM)
                if i == 2: 
                        for x in range(allNewMatrix.n):
                                for y in range(allNewMatrix.n):
                                        allNewMatrix.absorptionM[x][y] =  wb2.cell(row=x + 1, column=y + 1).value
                        print("Valores de la Matrix Absorption")
                        print(allNewMatrix.absorptionM)
                if i == 3: 
                        for x in range(allNewMatrix.n):
                                for y in range(allNewMatrix.n):
                                        allNewMatrix.sourceM[x] =  wb3.cell(row=x + 1, column=1).value
                        print("Valores del Vector Source")
                        print(allNewMatrix.sourceM)
                if i == 4: 
                        for x in range(allNewMatrix.n):
                                for y in range(allNewMatrix.n):
                                        allNewMatrix.massM[x][y] =  wb4.cell(row=x + 1, column=y + 1).value
                        print("Valores de la Matrix Mass")
                        print(allNewMatrix.massM)
                if i == 5: 
                        for x in range(allNewMatrix.n):
                                for y in range(allNewMatrix.n):
                                        allNewMatrix.damMassM[x][y] =  wb5.cell(row=x + 1, column=y + 1).value
                        print("Valores de la Matrix Damping Mass")
                        print(allNewMatrix.damMassM)
                if i == 6: 
                        for x in range(allNewMatrix.n):
                                for y in range(allNewMatrix.n):
                                        allNewMatrix.cFluxM[x][y] =  wb6.cell(row=x + 1, column=y + 1).value
                        print("Valores de la Matrix CFlux")
                        print(allNewMatrix.cFluxM)
                if i == 7: 
                        for x in range(allNewMatrix.n):
                                for y in range(allNewMatrix.n):
                                        allNewMatrix.convectionM[x][y] =  wb7.cell(row=x + 1, column=y + 1).value
                        print("Valores de la Matrix Convection")
                        print(allNewMatrix.convectionM)
                if i == 8: 
                        for x in range(allNewMatrix.n):
                                for y in range(allNewMatrix.n):
                                        allNewMatrix.cSourceM[x] =  wb8.cell(row=x + 1, column=1).value
                        print("Valores del Vector CSource")
                        print(allNewMatrix.cSourceM)


        Update.currentData(self, 1)
        Update.currentData(self, 2)
        Update.currentData(self, 3)
        Update.currentData(self, 4)
        Update.currentData(self, 5)
        Update.currentData(self, 6)
        Update.currentData(self, 7)
        Update.currentData(self, 8)
        Matrix.currentInitialVariable(self)

        fileIndicator["*"] = ""
        self.lblDirectory.setText(directory["dir"] + fileIndicator["*"])
        self.actionSaves.setEnabled(False)
        self.actionSave_As.setEnabled(True)
        self.actionClose.setEnabled(True)


 
    def resetData(self):
        #Ocultar todos los items del ToolBox Coefficients PDE y dejar solo el item Initial Values
        for i in range(1, self.CoefficentForM.count()):
            self.CoefficentForM.removeItem(1)

        for i, item in enumerate(self.CoefficientCheckBoxArray):
                self.CoefficientCheckBoxArray[i - 1].setChecked(False)

        #Resetear todos los combobox de las secciones y dejarles solo el valor de 1
        for i, item in enumerate(self.arrayCmbRowColumns):
         for j, item in enumerate(self.arrayCmbRowColumns[i]):
                        self.arrayCmbRowColumns[i][j].clear()
                        self.arrayCmbRowColumns[i][j].addItem("1")

        #Limpiar todos los lineEdits de cada seccion
        for i, item in enumerate(self.arraylEditsCoefficientsPDE):
         for j, item in enumerate(self.arraylEditsCoefficientsPDE[i]):
                        self.arraylEditsCoefficientsPDE[i][j].setText("")

        #Resetear el combobox de Initial Values
        self.cmbInitialValues.clear()
        self.cmbInitialValues.addItem("u1")
        #Eliminar la dirección del archivo excel actual del QLabel
        self.lblDirectory.setText("")

        self.actionSaves.setEnabled(False)
        self.actionSave_As.setEnabled(False)
        self.actionClose.setEnabled(False)

        #Resetear el modo de input del diffusion matrix a 1 (isotrópico)
        diffusionMatrix["inputMode"] = 0
        self.cmbDiffusionCoef.setCurrentIndex(diffusionMatrix["inputMode"])
        noItemsCoeffM["noItems"] = 0
        noItemsCoeffM["items"] = 0
        initialValues["noVariables"] = 1

        fileIndicator["*"] = ""
        #Eliminar la dirección del archivo excel en la memoria de la variable
        directory["dir"] = ""

    #Función para decirle al indicador si la configuración del programa fue modificada
    #Esto solo en caso de quw se encuentre un archivo excel cargado
    def editedFile(self):
        fileIndicator["*"] = "*"
        if directory["dir"] != '':
            self.lblDirectory.setText(directory["dir"] + fileIndicator["*"])
            self.actionSaves.setEnabled(True)

        
class Update():
 def currentData(self, pos):
        if pos == 1:
            if self.cmbDiffusionCoef.currentIndex() == 0:
             if allNewMatrix.diffusionM[self.cmbRowDiffusionCoef.currentIndex()][self.cmbColumnDiffusionCoef.currentIndex()] == 'None' or allNewMatrix.diffusionM[self.cmbRowDiffusionCoef.currentIndex()][self.cmbColumnDiffusionCoef.currentIndex()] == '':
              self.lEditDiffusionCoef.setText("")
             else: 
              strCell = allNewMatrix.diffusionM[self.cmbRowDiffusionCoef.currentIndex()][self.cmbColumnDiffusionCoef.currentIndex()]
              strCell = strCell.strip("[]")
              strCell = strCell.split(',')
              self.lEditDiffusionCoef.setText(strCell[0])
            elif self.cmbDiffusionCoef.currentIndex() == 1:
             if allNewMatrix.diffusionM[self.cmbRowDiffusionCoef.currentIndex()][self.cmbColumnDiffusionCoef.currentIndex()] == 'None' or allNewMatrix.diffusionM[self.cmbRowDiffusionCoef.currentIndex()][self.cmbColumnDiffusionCoef.currentIndex()] == '':
              self.lEditDiffusionCoef11.setText("")
              self.lEditDiffusionCoef22.setText("")
             else:
              strCell = allNewMatrix.diffusionM[self.cmbRowDiffusionCoef.currentIndex()][self.cmbColumnDiffusionCoef.currentIndex()]
              strCell = strCell.strip("[]")
              strCell = strCell.split(',')
              self.lEditDiffusionCoef11.setText(strCell[0])
              self.lEditDiffusionCoef22.setText(strCell[3])

            elif self.cmbDiffusionCoef.currentIndex() == 2 or self.cmbDiffusionCoef.currentIndex() == 3:
              if allNewMatrix.diffusionM[self.cmbRowDiffusionCoef.currentIndex()][self.cmbColumnDiffusionCoef.currentIndex()] == 'None' or allNewMatrix.diffusionM[self.cmbRowDiffusionCoef.currentIndex()][self.cmbColumnDiffusionCoef.currentIndex()] == '':
                self.lEditDiffusionCoef11.setText("")
                self.lEditDiffusionCoef12.setText("")
                self.lEditDiffusionCoef21.setText("")
                self.lEditDiffusionCoef22.setText("")
              else:
                strCell = allNewMatrix.diffusionM[self.cmbRowDiffusionCoef.currentIndex()][self.cmbColumnDiffusionCoef.currentIndex()]
                strCell = strCell.strip("[]")
                strCell = strCell.split(',')
                self.lEditDiffusionCoef11.setText(strCell[0])
                self.lEditDiffusionCoef12.setText(strCell[1])
                self.lEditDiffusionCoef21.setText(strCell[2])
                self.lEditDiffusionCoef22.setText(strCell[3])

        if pos == 2:
            if allNewMatrix.absorptionM[self.cmbAbsorptionRow.currentIndex()][self.cmbAbsorptionColumn.currentIndex()] == 'None' or allNewMatrix.absorptionM[self.cmbAbsorptionRow.currentIndex()][self.cmbAbsorptionColumn.currentIndex()] == '':    
             self.lEditAbsorCoef.setText("")
            else:
             self.lEditAbsorCoef.setText(allNewMatrix.absorptionM[self.cmbAbsorptionRow.currentIndex()][self.cmbAbsorptionColumn.currentIndex()])
        if pos == 3:
            if allNewMatrix.sourceM[self.cmbSourceRow.currentIndex()] == 'None' or allNewMatrix.sourceM[self.cmbSourceRow.currentIndex()] == '':
             self.lEditSourceTerm.setText("")
            else:
             self.lEditSourceTerm.setText(allNewMatrix.sourceM[self.cmbSourceRow.currentIndex()])
        if pos == 4:
            if allNewMatrix.massM[self.cmbMassCoefRow.currentIndex()][self.cmbMassCoefColumn.currentIndex()] == 'None' or allNewMatrix.massM[self.cmbMassCoefRow.currentIndex()][self.cmbMassCoefColumn.currentIndex()] == '':
             self.lEditMassCoef.setText("")
            else:
             self.lEditMassCoef.setText(allNewMatrix.massM[self.cmbMassCoefRow.currentIndex()][self.cmbMassCoefColumn.currentIndex()])
        if pos == 5:
            if allNewMatrix.damMassM[self.cmbDamMassCoefRow.currentIndex()][self.cmbDamMassCoefColumn.currentIndex()] == 'None' or allNewMatrix.damMassM[self.cmbDamMassCoefRow.currentIndex()][self.cmbDamMassCoefColumn.currentIndex()] == '':
             self.lEditDamMassCoef.setText("")
            else:
             self.lEditDamMassCoef.setText(allNewMatrix.damMassM[self.cmbDamMassCoefRow.currentIndex()][self.cmbDamMassCoefColumn.currentIndex()])
        if pos == 6:
            if allNewMatrix.cFluxM[self.cmbCFluxRow.currentIndex()][self.cmbCFluxColumn.currentIndex()] == 'None' or allNewMatrix.cFluxM[self.cmbCFluxRow.currentIndex()][self.cmbCFluxColumn.currentIndex()] == '':
                self.lEditAlphaXCFlux.setText("")
                self.lEditAlphaCYFlux.setText("")
            else:
                strCell = allNewMatrix.cFluxM[self.cmbCFluxRow.currentIndex()][self.cmbCFluxColumn.currentIndex()]
                strCell = strCell.strip("[]")
                strCell = strCell.split(',')
                self.lEditAlphaXCFlux.setText(strCell[0])
                self.lEditAlphaCYFlux.setText(strCell[1])
        if pos == 7:
            if allNewMatrix.convectionM[self.cmbConvectionRow.currentIndex()][self.cmbConvectionColumn.currentIndex()] == 'None' or allNewMatrix.convectionM[self.cmbConvectionRow.currentIndex()][self.cmbConvectionColumn.currentIndex()] == '':
                self.lEditBetaXConvCoef.setText("")
                self.lEditBetaYConvCoef.setText("")
            else:
                strCell = allNewMatrix.convectionM[self.cmbConvectionRow.currentIndex()][self.cmbConvectionColumn.currentIndex()]
                strCell = strCell.strip("[]")
                strCell = strCell.split(',')
                self.lEditBetaXConvCoef.setText(strCell[0])
                self.lEditBetaYConvCoef.setText(strCell[1])
        if pos == 8: 
            if allNewMatrix.cSourceM[self.cmbCSourceRow.currentIndex()] == 'None' or allNewMatrix.cSourceM[self.cmbCSourceRow.currentIndex()] == '':
                self.lEditGammaXCFluxSource.setText("")
                self.lEditGammaYCFluxSource.setText("") 
            else:
                strCell = allNewMatrix.cSourceM[self.cmbCSourceRow.currentIndex()]
                strCell = strCell.strip("[]")
                strCell = strCell.split(',')
                self.lEditGammaXCFluxSource.setText(strCell[0])
                self.lEditGammaYCFluxSource.setText(strCell[1])
        







        

        