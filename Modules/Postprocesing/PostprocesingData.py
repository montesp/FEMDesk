class PostprocesingData:
    sidesData = None
    typeConditions = []
    typeConditionsBooleans = []
    typeConditionsValues = []
    
    def __init__(self) -> None:
        pass
    
    def createTypeConditions(self, win):
        PostprocesingData.sidesData = win.conditions.sidesData
        PostprocesingData.typeConditions = []
        PostprocesingData.typeConditionsBooleans = []
        PostprocesingData.typeConditionsValues = []

        for sideData in PostprocesingData.sidesData:
            if sideData['typeCondition'] == "Temperature":
                PostprocesingData.typeConditionsBooleans.append(False)
                PostprocesingData.typeConditionsValues.append(0)
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


            



        print('tipo CF')
        print(PostprocesingData.typeConditions)
        print(PostprocesingData.typeConditionsBooleans)
        print('valor CF')
        print(PostprocesingData.typeConditionsValues)

    def getTypeConditions(self):
        return [PostprocesingData.typeConditionsBooleans, PostprocesingData.typeConditionsValues]

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