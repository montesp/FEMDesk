from Modules.Dictionary.DMatrix import *
from Modules.Dictionary.DFiles import *
from Modules.Dictionary.DModelWizard import *
from Modules.Matrix.Matrix import *
import Modules.ManageFiles.ManageFiles
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QBrush, QPolygonF

class LoadExcel():

    def loadExcelMatrixDimensions(self, sheet):
        #Cargar en el diccionario el numero de variables
        initialValues["noVariables"] = sheet['B2'].value
        n = int(initialValues["noVariables"])
        
        #Cargar las dimensiones de las matrices del Coefficient PDE
        self.dMatrix = dialogMatrix(n)
        self.dVector = dialogVector(n)
        allNewMatrix.changeMatrixDimensions(self, n)
        allNewMatrix.n = n
        diffusionMatrix["inputMode"] = sheet['A2'].value

    
    def loadExcelItemsData(self, sheet):
        #Cargar el numero de Items del Coefficient PDE
        noItemsCoeffM["noItems"] = sheet['C2'].value
        check = sheet['D2'].value
        arCheck = check.split(',')
        numCheck = list(map(int, arCheck))
        noItemsCoeffM["items"] = numCheck


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

    def loadExcelMatrixData(self, wbSheet):
        #Insertar la información de cada sección en su respectiva matriz o vector
        for i in noItemsCoeffM["items"]:
                if i == 1: 
                        for x in range(allNewMatrix.n):
                                for y in range(allNewMatrix.n):
                                        allNewMatrix.matrixCoefficientPDE[0][x][y] =  wbSheet.wb1.cell(row=x + 1, column=y + 1).value
                if i == 2:
                        for x in range(allNewMatrix.n):
                                for y in range(allNewMatrix.n):
                                        allNewMatrix.matrixCoefficientPDE[1][x][y] =  wbSheet.wb2.cell(row=x + 1, column=y + 1).value
                if i == 3: 
                        for x in range(allNewMatrix.n):
                                for y in range(allNewMatrix.n):
                                        allNewMatrix.vectorCoefficientPDE[0][0][x] =  wbSheet.wb3.cell(row=x + 1, column=1).value
                if i == 4: 
                        for x in range(allNewMatrix.n):
                                for y in range(allNewMatrix.n):
                                        allNewMatrix.matrixCoefficientPDE[2][x][y] =  wbSheet.wb4.cell(row=x + 1, column=y + 1).value
                if i == 5: 
                        for x in range(allNewMatrix.n):
                                for y in range(allNewMatrix.n):
                                        allNewMatrix.matrixCoefficientPDE[3][x][y] =  wbSheet.wb5.cell(row=x + 1, column=y + 1).value
                if i == 6: 
                        for x in range(allNewMatrix.n):
                                for y in range(allNewMatrix.n):
                                        allNewMatrix.matrixCoefficientPDE[4][x][y] =  wbSheet.wb6.cell(row=x + 1, column=y + 1).value
                if i == 7: 
                        for x in range(allNewMatrix.n):
                                for y in range(allNewMatrix.n):
                                        allNewMatrix.matrixCoefficientPDE[5][x][y] =  wbSheet.wb7.cell(row=x + 1, column=y + 1).value
                if i == 8: 
                        for x in range(allNewMatrix.n):
                                for y in range(allNewMatrix.n):
                                        allNewMatrix.vectorCoefficientPDE[1][0][x] =  wbSheet.wb8.cell(row=x + 1, column=1).value


    def formatMaterialCell(self, wbSheet, index, indexcolumn):
        arrayCell = wbSheet.wbMaterials.cell(row=index, column=indexcolumn).value
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
        for i in range(int(wbSheet.wbMaterials.cell(row=2, column=8).value)):
            cellFigure = int(wbSheet.wbMaterials.cell(row=index, column=1).value)
            figure = 'figure'
            self.listDomains.addItem(figure)
            cellThermal = LoadExcel.formatMaterialCell(self, wbSheet, index, 2)
            cellDensity = float(wbSheet.wbMaterials.cell(row=index, column=3).value)
            cellHeatCapacity = float((wbSheet.wbMaterials.cell(row=index, column=4).value))
            cellHeatConvection = LoadExcel.formatMaterialCell(self, wbSheet, index, 5)
            cellMaterial = int(wbSheet.wbMaterials.cell(row=index, column=6).value)
            cellHeatConduction = int(wbSheet.wbMaterials.cell(row=index, column=7).value)
            dataFigures.append({'figure': cellFigure, 'thermalConductivity': cellThermal, 'density': cellDensity, 'heatCapacity': cellHeatCapacity, 'heatConvection': cellHeatConvection, 'material': cellMaterial, 'heatConductionType': cellHeatConduction}) 
            index+=1
        material.setDataFigures(dataFigures)
        figuredata = material.getDataFigures()
    

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
        Matrix.currentInitialVariable(self)

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
        Modules.ModelWizard.ModelWizard.currentTreeWidgetConfiguration(self, self.tabs, self.tabWidgetMenu, canvas)

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
