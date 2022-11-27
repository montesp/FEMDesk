class PostprocesingData:
    sidesData = None
    typeConditions = []
    typeConditionsBooleans = []
    typeConditionsValues = []
    matrixBeta = None
    
    def __init__(self) -> None:
        pass
    
    def createTypeConditions(self, win):
        PostprocesingData.sidesData = win.conditions.sidesData
        PostprocesingData.typeConditions = []
        PostprocesingData.typeConditionsBooleans = []
        PostprocesingData.typeConditionsValues = []
        PostprocesingData.matrixBeta = None

        for sideData in PostprocesingData.sidesData:
            if sideData['typeCondition'] == "Temperature":
                PostprocesingData.typeConditionsBooleans.append(False)
                PostprocesingData.typeConditionsValues.append(sideData['data'])
            if sideData['typeCondition'] == "Heat Flux" or sideData['typeCondition'] == "Thermal Insulation":
                PostprocesingData.typeConditionsBooleans.append(True)
                if sideData['typeCondition'] == 'Thermal Insulation':
                    PostprocesingData.typeConditionsValues.append(0)
                else:
                    if sideData['heatConditionType'] == 'General inward heat flux':
                        PostprocesingData.typeConditionsValues.append(sideData['data'])
                    if sideData['heatConditionType'] == 'Convective heat flux':
                        arrayHeat = sideData['data']
                        wmk = arrayHeat[0]
                        valueK = arrayHeat[1]
                        q0 = wmk * valueK
                        PostprocesingData.typeConditionsValues.append(q0)
            PostprocesingData.typeConditions.append(sideData['typeCondition'])

        PostprocesingData.matrixBeta = win.postprocesing .getMatrizBeta(win)
        print('tipo CF')
        print(PostprocesingData.typeConditions)
        print(PostprocesingData.typeConditionsBooleans)
        print('valor CF')
        print(PostprocesingData.typeConditionsValues)
        print('Matriz Beta')
        print(PostprocesingData.matrixBeta)

    def getTypeConditions(self):
        return [PostprocesingData.typeConditionsBooleans, PostprocesingData.typeConditionsValues, PostprocesingData.matrixBeta]

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
