from Modules.Dictionary.DConditionsPDE import *
class ConditionsPDE():
    def currentCheckedComboBoxItemConditions(section, comb):
        for i in range(section.count()):
            section.widget(i).hide()
            section.setItemEnabled(i, False)

        if comb.currentIndex() == 2:
            section.setItemEnabled(comb.currentIndex(), True)
            section.setItemEnabled(comb.currentIndex() + 1, True)
            section.widget(comb.currentIndex()).show()
            section.widget(comb.currentIndex() + 1).show()
        elif comb.currentIndex() == 3:
            section.setItemEnabled(comb.currentIndex()+1, True)
            section.widget(comb.currentIndex() + 1).show()
        else:
            section.setItemEnabled(comb.currentIndex(), True)
            section.widget(comb.currentIndex()).show()

    def currentRowDiffusionCoef(currentIndexRow, currentIndexColumn, diffusionCoefElements):
        # diffusionCoefElements[1].setEnabled(False)

        indexDictionary = {
            "00": DC00,
            "01": DC01,
            "02": DC02,
            "10": DC10,
            "11": DC11,
            "12": DC12,
            "20": DC20,
            "21": DC21,
            "22": DC22
        }

        if (currentIndexRow == 0 and currentIndexColumn == 0):
            indexDictionary["00"](diffusionCoefElements)
        elif (currentIndexRow == 0 and currentIndexColumn == 1):
            indexDictionary["01"](diffusionCoefElements)
        elif (currentIndexRow == 0 and currentIndexColumn == 2):
            indexDictionary["02"](diffusionCoefElements)
        elif (currentIndexRow == 1 and currentIndexColumn == 0):
            indexDictionary["10"](diffusionCoefElements)
        elif (currentIndexRow == 1 and currentIndexColumn == 1):
            indexDictionary["11"](diffusionCoefElements)
        elif (currentIndexRow == 1 and currentIndexColumn == 2):
            indexDictionary["12"](diffusionCoefElements)
        elif (currentIndexRow == 2 and currentIndexColumn == 0):
            indexDictionary["20"](diffusionCoefElements)
        elif (currentIndexRow == 2 and currentIndexColumn == 1):
            indexDictionary["21"](diffusionCoefElements)
        elif (currentIndexRow == 2 and currentIndexColumn == 2):
            indexDictionary["22"](diffusionCoefElements)
    
    def activateIndexAlpha(alphaXData, alphaYData, currentIndexRow, currentIndexColumn ):
        for i in range(len(alphaXData)):
            alphaXData[i].setEnabled(False)
            alphaYData[i].setEnabled(False)

        if (currentIndexRow == 0 and currentIndexColumn == 1):
            alphaXData[0].setEnabled(True)
            alphaYData[0].setEnabled(True)
        if (currentIndexRow == 0 and currentIndexColumn == 2):
            alphaXData[0].setEnabled(True)
            alphaYData[0].setEnabled(True)
            alphaXData[1].setEnabled(True)
            alphaYData[1].setEnabled(True)
        if (currentIndexRow == 1 and currentIndexColumn == 0):
            alphaXData[2].setEnabled(True)
            alphaYData[2].setEnabled(True)
        if (currentIndexRow == 1 and currentIndexColumn == 1):
            alphaXData[0].setEnabled(True)
            alphaYData[0].setEnabled(True)
            alphaXData[2].setEnabled(True)
            alphaYData[2].setEnabled(True)
            alphaXData[3].setEnabled(True)
            alphaYData[3].setEnabled(True)
        if (currentIndexRow == 1 and currentIndexColumn == 2):
            alphaXData[0].setEnabled(True)
            alphaYData[0].setEnabled(True)
            alphaXData[1].setEnabled(True)
            alphaYData[1].setEnabled(True)
            alphaXData[2].setEnabled(True)
            alphaYData[2].setEnabled(True)
            alphaXData[3].setEnabled(True)
            alphaYData[3].setEnabled(True)
            alphaXData[4].setEnabled(True)
            alphaYData[4].setEnabled(True)
        if (currentIndexRow == 2 and currentIndexColumn == 0):
            alphaXData[2].setEnabled(True)
            alphaYData[2].setEnabled(True)
            alphaXData[5].setEnabled(True)
            alphaYData[5].setEnabled(True)
        if (currentIndexRow == 2 and currentIndexColumn == 1):
            alphaXData[0].setEnabled(True)
            alphaYData[0].setEnabled(True)
            alphaXData[2].setEnabled(True)
            alphaYData[2].setEnabled(True)
            alphaXData[3].setEnabled(True)
            alphaYData[3].setEnabled(True)
            alphaXData[5].setEnabled(True)
            alphaYData[5].setEnabled(True)
            alphaXData[6].setEnabled(True)
            alphaYData[6].setEnabled(True)
        if (currentIndexRow == 2 and currentIndexColumn == 2):
            alphaXData[0].setEnabled(True)
            alphaYData[0].setEnabled(True)
            alphaXData[1].setEnabled(True)
            alphaYData[1].setEnabled(True)
            alphaXData[2].setEnabled(True)
            alphaYData[2].setEnabled(True)
            alphaXData[3].setEnabled(True)
            alphaYData[3].setEnabled(True)
            alphaXData[4].setEnabled(True)
            alphaYData[4].setEnabled(True)
            alphaXData[5].setEnabled(True)
            alphaYData[5].setEnabled(True)
            alphaXData[6].setEnabled(True)
            alphaYData[6].setEnabled(True)
            alphaXData[7].setEnabled(True)
            alphaYData[7].setEnabled(True)

    # currentRowEdit
    def currentRowEdit(currentIndexRow, diffusionCoefElements):
        if currentIndexRow == 0:
            diffusionCoefElements[0].setEnabled(False)
            diffusionCoefElements[1].setEnabled(False)
        elif currentIndexRow == 1:
            diffusionCoefElements[0].setEnabled(True)
            diffusionCoefElements[1].setEnabled(False)
        elif currentIndexRow == 2:
            diffusionCoefElements[0].setEnabled(True)
            diffusionCoefElements[1].setEnabled(True)

    def disabledRowEdit(dataX, dataY, currentIndexRow):
        if currentIndexRow == 0:
            dataX[0].setEnabled(False)
            dataY[0].setEnabled(False)
            dataX[1].setEnabled(False)
            dataY[1].setEnabled(False)

        elif currentIndexRow == 1:
            dataX[0].setEnabled(True)
            dataY[0].setEnabled(True)
            dataX[1].setEnabled(False)
            dataY[1].setEnabled(False)
        elif currentIndexRow == 2:
            dataX[0].setEnabled(True)
            dataY[0].setEnabled(True)
            dataX[1].setEnabled(True)
            dataY[1].setEnabled(True)
    