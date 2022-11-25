from PyQt5.QtCore import QPointF, Qt
from PyQt5.QtGui import QBrush, QPolygonF

import Modules.ManageFiles.ManageFiles
from Modules.Dictionary.DFiles import *
from Modules.Dictionary.DMatrix import *
from Modules.Dictionary.DModelWizard import *
from Modules.Matrix.dialogMatrix import dialogMatrix
from Modules.Matrix.dialogVector import dialogVector
from Modules.Matrix.dialogTableVector import dialogTableVector
from Modules.Matrix.dialogTableMatrix import dialogTableMatrix
from Modules.Matrix.dialogTableDiffusion import dialogTableDiffusionMatrix
from Modules.Matrix.createMatrix import allNewMatrix
import Modules.Matrix.createMatrix
import Modules.SectionTabs.ConditionsPDE
import numpy as np
import Modules.ModelWizard

class LoadExcel():

    def loadExcelMatrixDimensions(self, sheet, canvas, win):
        #Cargar en el diccionario el numero de variables
        initialValues["noVariables"] = sheet['B2'].value
        n = int(initialValues["noVariables"])
        win.modelwizard.setVariables(n)
        #Cargar las dimensiones de las matrices del Coefficient PDE
        allNewMatrix.changeMatrixDimensions(self, n, canvas, win)
        Modules.SectionTabs.ConditionsPDE.ConditionsPDEMatrix.changeMatrixDimensions(self, n, canvas)
        Modules.SectionTabs.ConditionsPDE.ConditionsPDE.addDimensionMatrixConditions(self, canvas, win)
        diffusionMatrix["inputMode"] = sheet['A2'].value

    
    def loadExcelItemsData(self, wbSheet):
        #Cargar el numero de Items del Coefficient PDE
        for row in range(allNewMatrix.domains):
            for column in range(8):
                if wbSheet.cell(row=row + 1, column=column + 1).value == 'None':
                    continue
                else:
                    Modules.Matrix.createMatrix.allNewMatrix.matrixItemsActivated[row][column] = wbSheet.cell(row=row 
                    + 1, column=column + 1).value
        print("Matriz de Items Activados Cargada")
        print(Modules.Matrix.createMatrix.allNewMatrix.matrixItemsActivated)


    def loadExcelCoordinates(self, sheet):
        #Cargar las coordenadas de los QComboBox de Coefficient PDE
        coordinates["coordinateDiffusion"] = sheet['A4'].value
        coordinates["coordinateAbsorption"] = sheet['B4'].value
        coordinates["coordinateSource"] = sheet['C4'].value
        coordinates["coordinateMass"] = sheet['D4'].value
        coordinates["coordinateDamMass"] = sheet['E4'].value
        coordinates["coordinateCFlux"] = sheet['F4'].value
        coordinates["coordinateConvection"] = sheet['G4'].value
        coordinates["coordinateCSource"] = sheet['H4'].value

        #Actualizar Combobox de cada seccion
        for index, item in enumerate(self.CoefficientCheckBoxArray):
                for j, item in enumerate(self.arrayCmbRowColumns[index]):
                        self.arrayCmbRowColumns[index][j].clear()

                for j, item in enumerate(self.arrayCmbRowColumns[index]):
                    for i in range(1, allNewMatrix.n + 1):
                        self.arrayCmbRowColumns[index][j].addItem(str(i))
        self.cmbInitialValues.clear()

         #Actualizar Combobox de los valores iniciales 
        for i in range(1, allNewMatrix.n + 1):
            self.cmbInitialValues.addItem("u" + str(i))

        #Actualizar el modo de input de la matrix Diffusion Coefficient
        self.cmbDiffusionCoef.setCurrentIndex(diffusionMatrix["inputMode"])

        #Cargar el modo del ModelWizard
        myFlags["ModelWizardMode"] = sheet['A6'].value
        Modules.ModelWizard.ModelWizard.flagModelWizardActivated = False

    def loadExcelItemsCoefficientPDE(self):
         #Actualizar la lista de Items activados del Coefficient PDE
        position = 1
        for i in range(self.CoefficentForM.count()):
            self.CoefficentForM.removeItem(1)

        self.CoefficentForM.insertItem(100, self.arrayCoeffMSection[9], self.arrayCheckNameCoeffM[9])

        #¿Cuales son las secciones que tiene activadas en el Coefficient PDE?
        for i in noItemsCoeffM["items"]:
            if(i != 0):
                #Activar las secciones del ToolBox
                self.CoefficentForM.insertItem(position, self.arrayCoeffMSection[i], self.arrayCheckNameCoeffM[i])
                self.CoefficientCheckBoxArray[i - 1].setChecked(True)
                position+=1

    def fillExcelMatrixData(self, sheetMatrix, start, domain, i):
        for x in range(allNewMatrix.n):
            for y in range(allNewMatrix.n):
                allNewMatrix.matrixCoefficientPDE[domain][i][x][y] =  sheetMatrix.cell(row=start + x + 1, 
                column=y + 1).value
        

    def fillExcelVectorData(self, sheetVector, start, domain, i):
        for x in range(allNewMatrix.n):
            allNewMatrix.vectorCoefficientPDE[domain][i][0][x] = sheetVector.cell(row=start + x + 1, 
            column = 1,).value
        

    def loadExcelMatrixData(self, wbSheet):
        #Insertar la información de cada sección en su respectiva matriz o vector
        for i in range(9):
                if i == 1: 
                        start = 0
                        for domain in range(allNewMatrix.domains):
                            LoadExcel.fillExcelMatrixData(self, wbSheet.wb1, start, domain, 0)
                            start+= allNewMatrix.n + 1
                if i == 2:
                        start = 0
                        for domain in range(allNewMatrix.domains):
                            LoadExcel.fillExcelMatrixData(self, wbSheet.wb2, start, domain, 1)
                            start+= allNewMatrix.n + 1
                if i == 3: 
                        start = 0
                        for domain in range(allNewMatrix.domains):
                            LoadExcel.fillExcelVectorData(self, wbSheet.wb3, start, domain, 0)
                            start+= allNewMatrix.n + 1
                if i == 4: 
                        start = 0
                        for domain in range(allNewMatrix.domains):
                            LoadExcel.fillExcelMatrixData(self, wbSheet.wb4, start, domain, 2)
                            start+= allNewMatrix.n + 1
                if i == 5: 
                        start = 0
                        for domain in range(allNewMatrix.domains):
                            LoadExcel.fillExcelMatrixData(self, wbSheet.wb5, start, domain, 3)
                            start+= allNewMatrix.n + 1
                if i == 6: 
                        start = 0
                        for domain in range(allNewMatrix.domains):
                            LoadExcel.fillExcelMatrixData(self, wbSheet.wb6, start, domain, 4)
                            start+= allNewMatrix.n + 1
                if i == 7: 
                        start = 0
                        for domain in range(allNewMatrix.domains):
                            LoadExcel.fillExcelMatrixData(self, wbSheet.wb7, start, domain, 5)
                            start+= allNewMatrix.n + 1
                if i == 8: 
                        start = 0
                        for domain in range(allNewMatrix.domains):
                            LoadExcel.fillExcelVectorData(self, wbSheet.wb8, start, domain, 1)
                            start+= allNewMatrix.n + 1
        print('Matriz Coefficients PDE')
        print(allNewMatrix.matrixCoefficientPDE)
        print('Vector Coefficients PDE')
        print(allNewMatrix.vectorCoefficientPDE)


    def fillExcelConditionsPDE(self, wbSheet, boundary, start):
        for row in range(allNewMatrix.n):
            for column in range(allNewMatrix.n + 1):
                Modules.SectionTabs.ConditionsPDE.ConditionsPDEMatrix.matrix3D[boundary][row][column] = wbSheet.cell(row=start 
                + row + 1, column= column + 1).value

    def loadExcelConditionsPDE(self, wbSheet):
        start = 0
        for boundary in range(Modules.SectionTabs.ConditionsPDE.ConditionsPDEMatrix.numberLines):
            LoadExcel.fillExcelConditionsPDE(self, wbSheet, boundary, start)
            start+= allNewMatrix.n + 1
        
        self.cmbBAbsorColumn.clear()
        self.cmbZeroFlux.clear()
        for i in range(1, allNewMatrix.n + 1):
            self.cmbBAbsorColumn.addItem(str(i))
        for i in range(1, allNewMatrix.n + 1):
            self.cmbZeroFlux.addItem("u" + str(i))
        print('Matriz Conditions PDE cargada')
        print(Modules.SectionTabs.ConditionsPDE.ConditionsPDEMatrix.matrix3D)

    def fillExcelConditionsPDEItems(self, wbSheet, boundary, start):
        for row in range(3):
         for column in range(allNewMatrix.n):
          Modules.SectionTabs.ConditionsPDE.ConditionsPDEMatrix.matrixCombobox[boundary][row][column] = wbSheet.cell(row= start 
          + row + 1, column = column + 1).value

    def loadExcelConditionsPDEItems(self, wbSheet):
        start = 0
        for boundary in range(Modules.SectionTabs.ConditionsPDE.ConditionsPDEMatrix.numberLines):
            LoadExcel.fillExcelConditionsPDEItems(self, wbSheet, boundary, start)
            start+= 3 + 1
        print('Conditions PDE Items Cargados')
        print(Modules.SectionTabs.ConditionsPDE.ConditionsPDEMatrix.matrixCombobox)

    def formatMaterialCell(self, wbSheet, index, indexcolumn):
        arrayCell = wbSheet.cell(row=index, column=indexcolumn).value
        arrayCell = arrayCell.strip("[]")
        arrayCell = arrayCell.split(',')

        tempArrayCell = []
        for i in arrayCell:
            i = i.replace("'", "")
            tempArrayCell.append(float(i))

        return tempArrayCell


    def loadExcelMaterialsData(self, wbSheet, material):
        #Cargar los datos de la clase Materials del archivo Excel
        dataFigures = []
        index = 2
        for i in range(int(wbSheet.cell(row=2, column=8).value)):
            cellFigure = int(wbSheet.cell(row=index, column=1).value)
            figure = 'figure'
            self.listDomains.addItem(figure)
            cellThermal = LoadExcel.formatMaterialCell(self, wbSheet, index, 2)
            cellDensity = float(wbSheet.cell(row=index, column=3).value)
            cellHeatCapacity = float((wbSheet.cell(row=index, column=4).value))
            cellHeatConvection = LoadExcel.formatMaterialCell(self, wbSheet, index, 5)
            cellMaterial = int(wbSheet.cell(row=index, column=6).value)
            cellHeatConduction = int(wbSheet.cell(row=index, column=7).value)
            dataFigures.append({'figure': cellFigure, 'thermalConductivity': cellThermal, 'density': cellDensity, 'heatCapacity': cellHeatCapacity, 'heatConvection': cellHeatConvection, 'material': cellMaterial, 'heatConductionType': cellHeatConduction}) 
            index+=1
        material.setDataFigures(dataFigures)
        figuredata = material.getDataFigures()
        print('Datos del Materials')
        print(figuredata)

    

    def formatConditionsCell(self, wbSheet, index, indexcolumn):
        arrayCell = wbSheet.cell(row=index, column=indexcolumn).value
        arrayCell = arrayCell.strip("[]")
        arrayCell = arrayCell.split(',')

        tempArrayCell = []
        for i in arrayCell:
            i = i.replace("'", "")
            tempArrayCell.append(float(i))

        return tempArrayCell

    def loadExcelConditionsData(self, wbSheet, condition):
        dataSides = []
        index = 2
        for i in range(int(wbSheet.cell(row=2, column=5).value)):
            cellSide = int(wbSheet.cell(row=index, column=1).value)
            side = 'Side'
            self.lWBoundarys.addItem(side)
            cellTypeCondition = wbSheet.cell(row=2, column=2).value
            cellHeatCondition = wbSheet.cell(row=2, column=3).value
            cellData = float(wbSheet.cell(row=2, column=4).value)
            dataSides.append({'side': cellSide, 'typeCondition': cellTypeCondition, 'heatConditionType': 
            cellHeatCondition, 'data': cellData})
            index+=1
        condition.setSidesData(dataSides)
        dataSides = condition.getSidesData()
        print('Datos del Conditions')
        print(dataSides)

    def loadExcelCoordinateData(self):
        Modules.ManageFiles.ManageFiles.Update.currentCoordinateMatrix(self, self.arrayCmbRowColumns)
        Modules.ManageFiles.ManageFiles.Update.currentData(self, 1)
        Modules.ManageFiles.ManageFiles.Update.currentData(self, 2)
        Modules.ManageFiles.ManageFiles.Update.currentData(self, 3)
        Modules.ManageFiles.ManageFiles.Update.currentData(self, 4)
        Modules.ManageFiles.ManageFiles.Update.currentData(self, 5)
        Modules.ManageFiles.ManageFiles. Update.currentData(self, 6)
        Modules.ManageFiles.ManageFiles.Update.currentData(self, 7)
        Modules.ManageFiles.ManageFiles.Update.currentData(self, 8)
        allNewMatrix.currentInitialVariable(self, allNewMatrix)

    def loadExcelModelWizard(self, canvas):
        #Actualizar la configuracion del Model Wizard        
        self.itemSpace[0].setExpanded(True)
        self.item2D[0].setExpanded(True)
        self.itemPhysics[0].setExpanded(True)
        self.itemHeat[0].setExpanded(True)
        self.itemMath[0].setExpanded(True)

        itemTree = self.treeModelWizard.findItems(myFlags["ModelWizardMode"], Qt.MatchExactly| Qt.MatchRecursive, 0)
        itemTree[0].setForeground(0, QBrush(Qt.blue))
        self.treeModelWizard.setCurrentItem(itemTree[0])
        #Modules.ModelWizard.ModelWizard.currentTreeWidgetConfiguration(self, self.tabs, self.tabWidgetMenu, canvas)

    def loadExcelFigures(self, wbSheet, canvas):
        #Cargar las figuras guardadas
        for i in range(1, wbSheet.wbPolygons.max_row + 1):
            tempPoly = QPolygonF()
            polyType = False if wbSheet.wbPolygons.cell(row=i, column=2).value == 1 else True
            for j in range(3, wbSheet.wbPolygons.max_column + 1):
                strPoint = wbSheet.wbPolygons.cell(row=i, column=j).value
                if strPoint:
                    point = strPoint.strip("[]")
                    point = point.split(",")
                    coords = [float(coord) for coord in point]
                    tempPoly << QPointF(coords[0], coords[1])
                else:
                    continue
            canvas.addPoly(tempPoly, holeMode = polyType)

    def activateTabs(self, arraySequence, tabs):
        for i in arraySequence:
            if i == 1: #Geometry
                self.tabWidgetMenu.insertTab(0, tabs[0]['widget'], tabs[0]['title'])
                self.tabWidgetMenu.insertTab(1, tabs[1]['widget'], tabs[1]['title'])
                self.tabWidgetMenu.insertTab(2, tabs[2]['widget'], tabs[2]['title'])
                self.btnDoneGeometry.setEnabled(False)
                self.cmbConstructionBy.setEnabled(False)
            if myFlags["ModelWizardMode"] == "Coefficient form PDE":
                Modules.ModelWizard.ModelWizard.sigPaso = 2
                if i == 2: #Mesh 2
                    print('Paso PDE mesh')
                    self.tabWidgetMenu.insertTab(0, tabs[0]['widget'], tabs[0]['title'])
                    self.tabWidgetMenu.insertTab(1, tabs[1]['widget'], tabs[1]['title'])
                    self.tabWidgetMenu.insertTab(2, tabs[2]['widget'], tabs[2]['title'])
                '''if i == 3: #Coefficients PDE
                    print('Paso PDE coefficients')
                    self.tabWidgetMenu.insertTab(0, tabs[0]['widget'], tabs[0]['title'])
                    self.tabWidgetMenu.insertTab(1, tabs[1]['widget'], tabs[1]['title'])
                    self.tabWidgetMenu.insertTab(5, tabs[5]['widget'], tabs[5]['title'])
                    self.tabWidgetMenu.insertTab(6, tabs[6]['widget'], tabs[6]['title'])'''
            else:
                Modules.ModelWizard.ModelWizard.sigPaso = 1
                if i == 2: #Mesh
                    print('Paso Solids Mesh')
                    self.tabWidgetMenu.insertTab(0, tabs[0]['widget'], tabs[0]['title'])
                    self.tabWidgetMenu.insertTab(1, tabs[1]['widget'], tabs[1]['title'])
                    self.tabWidgetMenu.insertTab(2, tabs[2]['widget'], tabs[2]['title'])
                '''if i == 3: #Materials
                    print('Paso solis material')
                    self.tabWidgetMenu.insertTab(0, tabs[0]['widget'], tabs[0]['title'])
                    self.tabWidgetMenu.insertTab(1, tabs[1]['widget'], tabs[1]['title'])
                    self.tabWidgetMenu.insertTab(2, tabs[2]['widget'], tabs[2]['title'])
                    self.tabWidgetMenu.insertTab(3, tabs[3]['widget'], tabs[3]['title'])
                    self.tabWidgetMenu.insertTab(4, tabs[4]['widget'], tabs[4]['title'])'''
                


    def loadExcelSequenceTab(self, sheet, tabs):
        arraySequence = sheet.cell(row=2, column=4).value
        arraySequence = arraySequence.strip('[]')
        arraySequence = arraySequence.split(',')
        arraySequence = [int(i) for i in arraySequence]
        Modules.ModelWizard.ModelWizard.sequence = arraySequence
        LoadExcel.activateTabs(self, arraySequence, tabs)

