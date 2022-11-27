import numpy as np


class DataPost():
    ConditionsCF = []

    def recieveTypeConditions(ConditionsCFList, dataPost):
        ConditionsCF = np.array(ConditionsCFList)
        print('Postprocesado de Conditions Recibido')
        print(ConditionsCF)
        dataPost.append(ConditionsCF)
        

    
    # def getCoefficent():
    #     return DataPost.ConditionsCF