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

    def getDensityHeatCapacity():
        pass 
    
    def infoAdd():
        pass