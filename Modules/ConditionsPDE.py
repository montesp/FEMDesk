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

    def changeMatrixCoefficient(currentIndexRow, currentIndexColumn, Elements):

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
            indexDictionary["00"](Elements)
        elif (currentIndexRow == 0 and currentIndexColumn == 1):
            indexDictionary["01"](Elements)
        elif (currentIndexRow == 0 and currentIndexColumn == 2):
            indexDictionary["02"](Elements)
        elif (currentIndexRow == 1 and currentIndexColumn == 0):
            indexDictionary["10"](Elements)
        elif (currentIndexRow == 1 and currentIndexColumn == 1):
            indexDictionary["11"](Elements)
        elif (currentIndexRow == 1 and currentIndexColumn == 2):
            indexDictionary["12"](Elements)
        elif (currentIndexRow == 2 and currentIndexColumn == 0):
            indexDictionary["20"](Elements)
        elif (currentIndexRow == 2 and currentIndexColumn == 1):
            indexDictionary["21"](Elements)
        elif (currentIndexRow == 2 and currentIndexColumn == 2):
            indexDictionary["22"](Elements)
    
    def activateIndexAlpha(alphaXData, alphaYData, currentIndexRow, currentIndexColumn ):

        indexDictionary = {
            "00": IndexA00,
            "01": IndexA01,
            "02": IndexA02,
            "10": IndexA10,
            "11": IndexA11,
            "12": IndexA12,
            "20": IndexA20,
            "21": IndexA21,
            "22": IndexA22
        }


        if (currentIndexRow == 0 and currentIndexColumn == 1):
            indexDictionary["01"](alphaXData, alphaYData)
        elif (currentIndexRow == 0 and currentIndexColumn == 2):
            indexDictionary["02"](alphaXData, alphaYData)
        elif (currentIndexRow == 1 and currentIndexColumn == 0):
            indexDictionary["10"](alphaXData, alphaYData)
        elif (currentIndexRow == 1 and currentIndexColumn == 1):
            indexDictionary["11"](alphaXData, alphaYData)
        elif (currentIndexRow == 1 and currentIndexColumn == 2):
            indexDictionary["12"](alphaXData, alphaYData)
        elif (currentIndexRow == 2 and currentIndexColumn == 0):
            indexDictionary["20"](alphaXData, alphaYData)
        elif (currentIndexRow == 2 and currentIndexColumn == 1):
            indexDictionary["21"](alphaXData, alphaYData)
        elif (currentIndexRow == 2 and currentIndexColumn == 2):
            indexDictionary["22"](alphaXData, alphaYData)

    # currentRowEdit
    def currentRowEdit(currentIndexRow, diffusionCoefElements):
        if currentIndexRow == 0:
            diffusionCoefElements[1].setEnabled(False)
            diffusionCoefElements[2].setEnabled(False)
        elif currentIndexRow == 1:
            diffusionCoefElements[1].setEnabled(True)
            diffusionCoefElements[2].setEnabled(False)
        elif currentIndexRow == 2:
            diffusionCoefElements[1].setEnabled(True)
            diffusionCoefElements[2].setEnabled(True)

    def disabledRowEdit(dataX, dataY, currentIndexRow):
        if currentIndexRow == 0:
            dataX[1].setEnabled(False)
            dataY[1].setEnabled(False)
            dataX[2].setEnabled(False)
            dataY[2].setEnabled(False)

        elif currentIndexRow == 1:
            dataX[1].setEnabled(True)
            dataY[1].setEnabled(True)
            dataX[2].setEnabled(False)
            dataY[2].setEnabled(False)
        elif currentIndexRow == 2:
            dataX[1].setEnabled(True)
            dataY[1].setEnabled(True)
            dataX[2].setEnabled(True)
            dataY[2].setEnabled(True)
    