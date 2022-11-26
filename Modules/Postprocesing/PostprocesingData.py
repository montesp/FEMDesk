class PostprocesingData:
    def __init__(self) -> None:
        pass
    
    def getTypeConditions(self, win):
        sidesData = win.conditions.sidesData
        typeConditions = []
        typeConditonsBooleans = []
        

        for sideData in sidesData:
            if sideData['typeCondition'] == "Temperature":
                typeConditonsBooleans.append(False)
            if sideData['typeCondition'] == "Heat Flux" or sideData['typeCondition'] == "Thermal Insulation":
                typeConditonsBooleans.append(True)
            typeConditions.append(sideData['typeCondition'])




        print(typeConditions)
        print(typeConditonsBooleans)
        return typeConditonsBooleans, sidesData

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
