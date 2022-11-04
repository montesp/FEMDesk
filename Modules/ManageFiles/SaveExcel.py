from Modules.Dictionary.DMatrix import *
from Modules.Dictionary.DFiles import *
from Modules.Dictionary.DModelWizard import *
from Modules.Matrix.Matrix import *

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
        inputMode = sheet.cell(row=1, column=1, value="Input Mode")
        nVariables = sheet.cell(row=1, column=2, value="No.Variables")
        nSectionCoeffM = sheet.cell(row=1, column=3, value="No.ItemsCoeffM")
        itemSectionCoeffM = sheet.cell(row=1, column=4, value="ItemsCoeffM")

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

  def saveExcelItemsPDE(self, sheet):
        #Guardar items del Coefficient PDE
        strSection = ",".join(str(i) for i in noItemsCoeffM["items"])
        sheet.cell(row= 2, column = 1, value= diffusionMatrix["inputMode"])
        sheet.cell(row= 2, column = 2, value= initialValues["noVariables"])
        sheet.cell(row= 2, column = 3, value= noItemsCoeffM["noItems"])
        sheet.cell(row= 2, column = 4, value= strSection)

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
            wbSheet.wbMaterials.cell(row=index, column=1, value= str(i["figure"]))
            wbSheet.wbMaterials.cell(row=index, column=2, value= str(i["thermalConductivity"]))
            wbSheet.wbSheet.bMaterials.cell(row=index, column=3, value= str(i["density"]))
            wbSheet.wbMaterials.cell(row=index, column=4, value= str(i["heatCapacity"]))
            wbSheet.wbMaterials.cell(row=index, column=5, value= str(i["heatConvection"]))
            wbSheet.wbMaterials.cell(row=index, column=6, value= str(i["material"]))
            wbSheet.wbMaterials.cell(row=index, column=7, value= str(i["heatConductionType"]))
            index+=1
        wbSheet.wbMaterials.cell(row=2, column=8, value=len(figuredata))
        print(len(figuredata))

  def saveExcelMatrixData(self, wbSheet):
         #Guardar los datos de las matrices del Coefficient PDE
        for i in noItemsCoeffM["items"]:
                if i == 1:
                        for row in range(allNewMatrix.n):
                         for column in range(allNewMatrix.n):
                                wbSheet.wb1.cell(row=row + 1, column=column + 1, value= allNewMatrix.diffusionM[row][column])
                elif i == 2:
                        for row in range(allNewMatrix.n):
                         for column in range(allNewMatrix.n):
                                wbSheet.wb2.cell(row=row + 1, column=column + 1, value= allNewMatrix.absorptionM[row][column])
                elif i == 3: 
                        for row in range(allNewMatrix.n):
                                wbSheet.wb3.cell(row=row + 1, column=1, value= allNewMatrix.sourceM[row])
                elif i == 4:
                       for row in range(allNewMatrix.n):
                         for column in range(allNewMatrix.n):
                                wbSheet.wb4.cell(row=row + 1, column=column + 1, value= allNewMatrix.massM[row][column])
                elif i == 5:
                       for row in range(allNewMatrix.n):
                         for column in range(allNewMatrix.n):
                                wbSheet.wb5.cell(row=row + 1, column=column + 1, value= allNewMatrix.damMassM[row][column])
                elif i == 6:
                       for row in range(allNewMatrix.n):
                         for column in range(allNewMatrix.n):
                                wbSheet.wb6.cell(row=row + 1, column=column + 1, value= allNewMatrix.cFluxM[row][column])
                elif i == 7:
                       for row in range(allNewMatrix.n):
                         for column in range(allNewMatrix.n):
                                wbSheet.wb7.cell(row=row + 1, column=column + 1, value= allNewMatrix.convectionM[row][column])
                elif i == 8:
                       for row in range(allNewMatrix.n):
                                wbSheet.wb8.cell(row=row + 1, column=1, value= allNewMatrix.cSourceM[row])
    
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