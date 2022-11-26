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

        for sideData in PostprocesingData.sidesData:
            if sideData['typeCondition'] == "Temperature":
                PostprocesingData.typeConditionsBooleans.append(False)
            if sideData['typeCondition'] == "Heat Flux" or sideData['typeCondition'] == "Thermal Insulation":
                PostprocesingData.typeConditionsBooleans.append(True)
            PostprocesingData.typeConditions.append(sideData['typeCondition'])

            



        print('tipo CF')
        print(PostprocesingData.typeConditions)
        print(PostprocesingData.typeConditionsBooleans)

    def getTypeConditions(self):
        return PostprocesingData.typeConditionsBooleans;

    

    def infoAdd():
        pass