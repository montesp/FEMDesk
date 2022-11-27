import numpy as np


class DataPost():
    ConditionsCF = None

    def recieveTypeConditions(ConditionsCFList, dataPost):
        start = 0
        DataPost.ConditionsCF = np.empty([len(ConditionsCFList) * len(ConditionsCFList[0]), 1] , dtype=np.object)
        for i in range(len(ConditionsCFList[0])):
            DataPost.ConditionsCF[start + i][0] = np.array(ConditionsCFList[0][i], dtype=np.int8)
        start += len(ConditionsCFList[0])
        for i in range(len(ConditionsCFList[1])):
            DataPost.ConditionsCF[start + i][0] = np.array(ConditionsCFList[1][i], dtype=np.float64)
        start += len(ConditionsCFList[1])
        for i in range(len(ConditionsCFList[2])):
            DataPost.ConditionsCF[start + i][0] = np.array(ConditionsCFList[2][i], dtype=np.int8)

        DataPost.ConditionsCF = np.asarray(DataPost.ConditionsCF)
        #ConditionsCF = np.array(ConditionsCFList[0], ConditionsCFList[1], ConditionsCFList[2])
        '''for i in range(ConditionsCF.shape[0]):
            for j in range(ConditionsCF.shape[1]):
                ConditionsCF[i][j] = np.array([ConditionsCF[i][j]])'''

        #np.reshape(ConditionsCF, (ConditionsCF.shape[0] * 3, 1))
        print('Postprocesado de Conditions Recibido')
        print(DataPost.ConditionsCF)
        dataPost.append(DataPost.ConditionsCF)
        

    
    # def getCoefficent():
    #     return DataPost.ConditionsCF