from Modules.Dictionary.DMatrix import *
from Modules.Dictionary.DFiles import *
from Modules.Dictionary.DModelWizard import *
import Modules.Matrix.createMatrix
import Modules.SectionTabs.ConditionsPDE
import numpy as np
import Modules.ModelWizard

class SaveExcel():

  def adjustExcelDimensions(self, sheet):
        #Ajustar dimensiones de las columnas
        sheet.column_dimensions['A'].width = 18
        sheet.column_dimensions['B'].width = 18
        sheet.column_dimensions['C'].width = 18
        sheet.column_dimensions['D'].width = 18
        sheet.column_dimensions['E'].width = 18
        sheet.column_dimensions['F'].width = 18
        sheet.column_dimensions['G'].width = 18
        sheet.column_dimensions['H'].width = 18

  def writeExcelText(self, sheet, wbSheet):
         #Items del Coefficient PDE
        inputModeDiffusion = sheet.cell(row=1, column=1, value="Diffusion InputMode")
        nVariables = sheet.cell(row=1, column=2, value="No.Variables")
        nSectionCoeffM = sheet.cell(row=1, column=3, value="No.ItemsCoeffM")
        tabsSequence = sheet.cell(row=1, column=4, value="Tabs Sequence")

        #Coordenadas de los QCombobox
        coordinateDiffusion = sheet.cell(row=3, column=1, value="Coord Diffusion")
        coordinateAbsorption = sheet.cell(row=3, column=2, value="Coord Absorption")
        coordinateSource = sheet.cell(row=3, column=3, value="Coord Source")
        coordinateMass = sheet.cell(row=3, column=4, value="Coord Mass")
        coordinateDamMass = sheet.cell(row=3, column=5, value="Coord DamMass")
        coordinateCFlux = sheet.cell(row=3, column=6, value="Coord CFlux")
        coordinateConvection = sheet.cell(row=3, column=7, value="Coord Convection")
        coordinateCSource = sheet.cell(row=3, column=8, value="Coord CSource")

        flagModelWizard = sheet.cell(row=5, column=1, value="ModelWizardMode")

        figureMaterials = wbSheet.wbMaterials.cell(row=1, column=1, value="Figure")
        thermalConductivity = wbSheet.wbMaterials.cell(row=1, column=2, value="Thermal Conductivity")
        density = wbSheet.wbMaterials.cell(row=1, column=3, value= "Density")
        heatCapacity = wbSheet.wbMaterials.cell(row=1, column=4, value="Heat Capacity")
        heatConvection = wbSheet.wbMaterials.cell(row=1, column=5, value="HeatConvection")
        materialtext = wbSheet.wbMaterials.cell(row=1, column=6, value="Material")
        heatConduction = wbSheet.wbMaterials.cell(row=1, column=7, value="HeatConduction")
        noFigures = wbSheet.wbMaterials.cell(row=1, column=8, value="noFigures")

        side = wbSheet.wbConditions.cell(row=1, column=1, value="Side")
        typeCondition = wbSheet.wbConditions.cell(row=1, column=2, value="TypeCondition")
        heatConditionType = wbSheet.wbConditions.cell(row=1, column =3, value="HeatConditionType")
        data = wbSheet.wbConditions.cell(row=1, column=4, value="Data")
        noSides = wbSheet.wbConditions.cell(row=1, column=5, value="NumberSides")


  def saveExcelItemsPDE(self, sheet):
        #Guardar items del Coefficient PDE
        sheet.cell(row= 2, column = 1, value= diffusionMatrix["inputMode"])
        sheet.cell(row= 2, column = 2, value= initialValues["noVariables"])
        sheet.cell(row= 2, column = 3, value= noItemsCoeffM["noItems"])
        sheet.cell(row= 2, column = 4, value= str(Modules.ModelWizard.ModelWizard.sequence))
        

  def saveExcelCoordinates(self, sheet):
        #Guardar las coordenadas de los QComboBox
        sheet.cell(row= 4, column= 1, value= str(coordinates["coordinateDiffusion"]))
        sheet.cell(row= 4, column= 2, value= str(coordinates["coordinateAbsorption"]))
        sheet.cell(row= 4, column= 3, value= str(coordinates["coordinateSource"]))
        sheet.cell(row= 4, column= 4, value= str(coordinates["coordinateMass"]))
        sheet.cell(row= 4, column= 5, value= str(coordinates["coordinateDamMass"]))
        sheet.cell(row= 4, column= 6, value= str(coordinates["coordinateCFlux"]))
        sheet.cell(row= 4, column= 7, value= str(coordinates["coordinateConvection"]))
        sheet.cell(row= 4, column= 8, value= str(coordinates["coordinateCSource"]))
        sheet.cell(row=6, column=1, value= myFlags["ModelWizardMode"])

  def saveExcelMaterialsData(self, wbSheet, material):
        #Guardar los datos de la clase Materials
        figuredata = material.getDataFigures()
        print(figuredata)
        index = 2
        for i in figuredata:
            wbSheet.wbMaterials.cell(row=index, column=1, value= i["figure"])
            wbSheet.wbMaterials.cell(row=index, column=2, value= str(i["thermalConductivity"]))
            wbSheet.wbMaterials.cell(row=index, column=3, value= i["density"])
            wbSheet.wbMaterials.cell(row=index, column=4, value= i["heatCapacity"])
            wbSheet.wbMaterials.cell(row=index, column=5, value= str(i["heatConvection"]))
            wbSheet.wbMaterials.cell(row=index, column=6, value= i["material"])
            wbSheet.wbMaterials.cell(row=index, column=7, value= i["heatConductionType"])
            index+=1
        wbSheet.wbMaterials.cell(row=2, column=8, value=len(figuredata))
        print(len(figuredata))

  def fillExcelMatrix(self, sheet, row, column, domain, start, numberMatrix):
       for row in range(Modules.Matrix.createMatrix.allNewMatrix.n):
              for column in range(Modules.Matrix.createMatrix.allNewMatrix.n):
                     print('fila desde la funcion')
                     print(start)
                     sheet.cell(row=start + row + 1, column=column + 1, value= 
                     Modules.Matrix.createMatrix.allNewMatrix.matrixCoefficientPDE[domain][numberMatrix][row][column])

  def fillExcelVector(self, sheet, row, domain, start, numberMatrix):
       for row in range(Modules.Matrix.createMatrix.allNewMatrix.n):
                     print('fila desde la funcion')
                     print(start)
                     sheet.cell(row=start + row + 1, column= 1, value= 
                     Modules.Matrix.createMatrix.allNewMatrix.vectorCoefficientPDE[domain][numberMatrix][0][row])

  def saveExcelMatrixData(self, wbSheet):
         #Guardar los datos de las matrices del Coefficient PDE
              for i in range(1, 9):
                if i == 1:
                     row = 0
                     column = 0
                     start = 0
                     for domain in range(Modules.Matrix.createMatrix.allNewMatrix.domains):
                            SaveExcel.fillExcelMatrix(self, wbSheet.wb1, row, column, domain, start, 0)
                            start += Modules.Matrix.createMatrix.allNewMatrix.n + 1
                elif i == 2:
                     row = 0
                     column = 0
                     start = 0
                     for domain in range(Modules.Matrix.createMatrix.allNewMatrix.domains):
                            SaveExcel.fillExcelMatrix(self, wbSheet.wb2, row, column, domain, start, 1)
                            start += Modules.Matrix.createMatrix.allNewMatrix.n + 1
                elif i == 3: 
                     row = 0
                     column = 0
                     start = 0
                     for domain in range(Modules.Matrix.createMatrix.allNewMatrix.domains):
                            SaveExcel.fillExcelVector(self, wbSheet.wb3, row, domain, start, 0)
                            start += Modules.Matrix.createMatrix.allNewMatrix.n + 1
                elif i == 4:
                     row = 0
                     column = 0
                     start = 0
                     for domain in range(Modules.Matrix.createMatrix.allNewMatrix.domains):
                            SaveExcel.fillExcelMatrix(self, wbSheet.wb4, row, column, domain, start, 2)
                            start += Modules.Matrix.createMatrix.allNewMatrix.n + 1
                elif i == 5:
                     row = 0
                     column = 0
                     start = 0
                     for domain in range(Modules.Matrix.createMatrix.allNewMatrix.domains):
                            SaveExcel.fillExcelMatrix(self, wbSheet.wb5, row, column, domain, start, 3)
                            start += Modules.Matrix.createMatrix.allNewMatrix.n + 1
                elif i == 6:
                     row = 0
                     column = 0
                     start = 0
                     for domain in range(Modules.Matrix.createMatrix.allNewMatrix.domains):
                            SaveExcel.fillExcelMatrix(self, wbSheet.wb6, row, column, domain, start, 4)
                            start += Modules.Matrix.createMatrix.allNewMatrix.n + 1
                elif i == 7:
                     row = 0
                     column = 0
                     start = 0
                     for domain in range(Modules.Matrix.createMatrix.allNewMatrix.domains):
                            SaveExcel.fillExcelMatrix(self, wbSheet.wb7, row, column, domain, start, 5)
                            start += Modules.Matrix.createMatrix.allNewMatrix.n + 1
                elif i == 8:
                     row = 0
                     column = 0
                     start = 0
                     for domain in range(Modules.Matrix.createMatrix.allNewMatrix.domains):
                            SaveExcel.fillExcelVector(self, wbSheet.wb8, row, domain, start, 1)
                            start += Modules.Matrix.createMatrix.allNewMatrix.n + 1
    
  def fillExcelMatrixItems(self, wbSheet, matrixItems, start, domain):
       for column in range(8):
              wbSheet.cell(row=start, column=column +1, value= matrixItems[domain][column])

  def saveExcelMatrixItems(self, wbSheet):
       start = 1
       intDomains = np.shape(Modules.Matrix.createMatrix.allNewMatrix.matrixItemsActivated)
       intDomains = intDomains[0]
       for domain in range(intDomains):
              SaveExcel.fillExcelMatrixItems(self, wbSheet.wbMatrixItems, 
              Modules.Matrix.createMatrix.allNewMatrix.matrixItemsActivated, start, domain)
              start+= 1

  def fillExcelConditionsPDE(self, wbSheet, boundary, start):
       for row in range(Modules.Matrix.createMatrix.allNewMatrix.n):
              for column in range(Modules.Matrix.createMatrix.allNewMatrix.n + 1):
                     wbSheet.cell(row=start + row + 1, column=column+1, 
                     value=Modules.SectionTabs.ConditionsPDE.ConditionsPDEMatrix.matrix3D[boundary][row][column])

  def saveExcelConditionsPDE(self, wbSheet):
       start = 0
       for boundary in range(Modules.SectionTabs.ConditionsPDE.ConditionsPDEMatrix.numberLines):
              SaveExcel.fillExcelConditionsPDE(self, wbSheet.wbConditionsPDE, boundary, start)
              start+= Modules.Matrix.createMatrix.allNewMatrix.n + 1

  def fillExcelItemsConditions(self, wbSheet, boundary, start):
       for row in range(2):
              for column in range(Modules.Matrix.createMatrix.allNewMatrix.n):
                     wbSheet.cell(row=start+ row + 1, column=column + 1, 
                     value= Modules.SectionTabs.ConditionsPDE.ConditionsPDEMatrix.matrixCombobox[boundary][row][column])

  def saveExcelItemsConditions(self, wbSheet):
       start = 0
       for boundary in range(Modules.SectionTabs.ConditionsPDE.ConditionsPDEMatrix.numberLines):
              SaveExcel.fillExcelItemsConditions(self, wbSheet.wbConditionsPDEItems, boundary, start)              
              start+= 3 + 1


  def saveExcelConditionsData(self, wbSheet, conditions):
       sidesData = conditions.getSidesData()
       print('Datos del Conditions')
       print(sidesData)
       index = 2
       for i in sidesData:
            wbSheet.wbConditions.cell(row=index, column=1, value= i["side"])
            wbSheet.wbConditions.cell(row=index, column=2, value= str(i["typeCondition"]))
            wbSheet.wbConditions.cell(row=index, column=3, value= i["heatConditionType"])
            wbSheet.wbConditions.cell(row=index, column=4, value= str(i["data"]))
            index+=1
       wbSheet.wbConditions.cell(row=2, column=5, value=len(sidesData))
       print(len(sidesData))

  def saveExcelFigures(self, wbSheet, canvas):
         #Guardar los datos de todas las figuras
        polygonsList = canvas.getAll()
        for i in polygonsList[0]:
            print("Cuales son los datos de la figura?")
            for j in i[1:]:
                print(j)
                wbSheet.wbPolygons.cell(row=i[1][0], column=1, value=i[1][0])
                wbSheet.wbPolygons.cell(row=i[1][0], column=2, value=i[2][0])

            print("Coordenadas")
            counter = 3
            for j in i[0]:
                print(j)
                wbSheet.wbPolygons.cell(row=i[1][0], column=counter, value=str(j))
                counter+=1