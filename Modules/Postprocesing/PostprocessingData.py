class PostprocessingData:
    sidesData = None
    typeConditions = []
    typeConditionsBooleans = []
    typeConditionsValues = []
    heatConduction = []
    densityHeat = []
    matrixBeta = []

    
    def __init__(self) -> None:
        pass
    
    def createTypeConditions(self, win):
        PostprocessingData.sidesData = win.conditions.sidesData
        PostprocessingData.typeConditions = []
        PostprocessingData.typeConditionsBooleans = []
        PostprocessingData.typeConditionsValues = []
        print(win.canvas.polyList)
        pint = []
        for poly in win.canvas.polyList:
            puntos = 0
            for point in poly.polygon():
                # puntos.append(point)
                puntos = puntos + 1
            pint.append(puntos)
        print("lados")
        print(pint)

        for sideData in PostprocessingData.sidesData:
            if sideData['typeCondition'] == "Temperature":
                PostprocessingData.typeConditionsBooleans.append(False)
                PostprocessingData.typeConditionsValues.append(sideData['data'])
                PostprocessingData.matrixBeta.append(0)

            if sideData['typeCondition'] == "Heat Flux" or sideData['typeCondition'] == "Thermal Insulation":
                PostprocessingData.typeConditionsBooleans.append(True)
                PostprocessingData.matrixBeta.append(0)
                if sideData['typeCondition'] == 'Thermal Insulation':
                    PostprocessingData.typeConditionsValues.append(0)
                else:
                    if sideData['heatConditionType'] == 'General inward heat flux':
                        PostprocessingData.typeConditionsValues.append(sideData['data'])
                    if sideData['heatConditionType'] == 'Convective heat flux':
                        arrayHeat = sideData['data']
                        wmk = arrayHeat[0]
                        valueK = arrayHeat[1]
                        q0 = wmk * valueK
                        PostprocessingData.typeConditionsValues.append(q0)
            PostprocessingData.typeConditions.append(sideData['typeCondition'])

        # Matriz beta
        # PostprocessingData.matrixBeta = self.getMatrizBeta(win)
        # print('tipo CF')
        # print(PostprocessingData.typeConditions)
        # print(PostprocessingData.typeConditionsBooleans)
        # print('valor CF')
        # print(PostprocessingData.typeConditionsValues)

    def getTypeConditions(self):
        return [PostprocessingData.typeConditionsBooleans, PostprocessingData.typeConditionsValues, PostprocessingData.matrixBeta]

    def getMatrizBeta(self, win):
        conditions = self.getTypeConditions()
        valuesCFMatriz = []
        matrixBeta = []


        for condition in conditions:
            if condition:
                valuesCFMatriz.append(0)
            else:
                pass
                # valuesCFMatriz.append() # Poner cf
            matrixBeta.append(0)
        return matrixBeta
    # Funciones EQ_b, mandar los datos
    def createDensityHeatCapacity(self, win):
        # rho * cp
        # Density * Heat capacity at constant presuare
        materials = win.material.getDataFigures()
        densityHeatCapacity = []
        for material in materials:
            rhocp = material['density'] * material['heatCapacity']
            PostprocessingData.densityHeat.append(rhocp)
        # print("rho * cp")
        # print(densityHeatCapacity)
    
    def getDensityHeatCapacity(self):
        return PostprocessingData.densityHeat


    # Funciones eq_c11, eq_c12, eq_c13, eq_c14, mandar los datos
    def createHeatConduction(self, win):
        materials = win.material.getDataFigures()
        PostprocessingData.heatConduction = []

        for material in materials:
            if len(material['thermalConductivity']) == 1:
                PostprocessingData.heatConduction.append([material['thermalConductivity'][0]])
                PostprocessingData.heatConduction.append([0])
                PostprocessingData.heatConduction.append([0])
                PostprocessingData.heatConduction.append([material['thermalConductivity'][0]])

            if len(material['thermalConductivity']) == 4:
                PostprocessingData.heatConduction.append([material['thermalConductivity'][0]])
                PostprocessingData.heatConduction.append([material['thermalConductivity'][1]])
                PostprocessingData.heatConduction.append([material['thermalConductivity'][2]])
                PostprocessingData.heatConduction.append([material['thermalConductivity'][3]])

    def getHeatConduction(self):
        return PostprocessingData.heatConduction
