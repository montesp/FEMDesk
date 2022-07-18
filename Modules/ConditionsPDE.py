from Modules.Dictionary.DConditionsPDEd import *
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