class PostprocessingData:
    sidesData = None
    typeConditions = []
    typeConditionsBooleans = []
    typeConditionsValues = []
    
    def __init__(self) -> None:
        pass
    
    def createTypeConditions(self, win):
        PostprocessingData.sidesData = win.conditions.sidesData
        PostprocessingData.typeConditions = []
        PostprocessingData.typeConditionsBooleans = []
        PostprocessingData.typeConditionsValues = []

        for sideData in PostprocessingData.sidesData:
            if sideData['typeCondition'] == "Temperature":
                PostprocessingData.typeConditionsBooleans.append(False)
                PostprocessingData.typeConditionsValues.append(sideData['data'])
            if sideData['typeCondition'] == "Heat Flux" or sideData['typeCondition'] == "Thermal Insulation":
                PostprocessingData.typeConditionsBooleans.append(True)
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


        print('tipo CF')
        print(PostprocessingData.typeConditions)
        print(PostprocessingData.typeConditionsBooleans)
        print('valor CF')
        print(PostprocessingData.typeConditionsValues)

    def getTypeConditions(self):
        return [PostprocessingData.typeConditionsBooleans, PostprocessingData.typeConditionsValues]

    def getMatrizBeta(self, win):
        conditions = self.getTypeConditions(win)
        valuesCFMatriz = []
        matrixBeta = []


        for condition in conditions:
            if condition:
                valuesCFMatriz.append(0)
            else:
                pass
                # valuesCFMatriz.append() # Poner cf
            matrixBeta.append(0)
    # Funciones EQ_b, mandar los datos
    def getDensityHeatCapacity(self, win):
        # rho * cp
        # Density * Heat capacity at constant presuare
        materials = win.material.getDataFigures()
        densityHeatCapacity = []
        for material in materials:
            rhocp = material['density'] * material['heatCapacity']
            densityHeatCapacity.append(rhocp)
        print("rho * cp")
        print(densityHeatCapacity)

    # Funciones eq_c11, eq_c12, eq_c13, eq_c14, mandar los datos
    def getheatConduction(self, win):
        materials = win.material.getDataFigures()
        heatConduction = []

        for material in materials:
            if len(material['thermalConductivity']) == 1:
                heatConduction.append([material['thermalConductivity'][0],0,0, material['thermalConductivity'][0]])
            if len(material['thermalConductivity']) == 4:
                heatConduction.append([material['thermalConductivity'][0],material['thermalConductivity'][1], material['thermalConductivity'][2], material['thermalConductivity'][3]])
        print("heat conduction")
        print(heatConduction)
