
class Materials():
     def currentHeatConduction(comb, ar):
        
        if comb.currentIndex() == 0:
            ar[0].setEnabled(True)
            ar[1].setEnabled(False)
            ar[2].setEnabled(False)
            ar[3].setEnabled(False)
            ar[4].setEnabled(False)
        if comb.currentIndex() == 3:
            ar[0].setEnabled(False)
            ar[1].setEnabled(True)
            ar[2].setEnabled(True)
            ar[3].setEnabled(True)
            ar[4].setEnabled(True)

class Geometry():
    def currentCheckedComboBoxItem(section, comb):
        for i in range(section.count()):
            section.widget(i).hide()
            section.setItemEnabled(i, False)
        if comb.currentIndex() <= 4:
            section.setItemEnabled(comb.currentIndex(), True)
            section.widget(comb.currentIndex()).show()
        

class Conditions():
    def currentTypeCondition(comb, tbox): 
        tbox.widget(0).hide()
        tbox.setItemEnabled(0, False)
        tbox.widget(1).hide()
        tbox.setItemEnabled(1, False)
         

        if comb.currentIndex() == 1:
            tbox.setItemEnabled(0, True)
            tbox.widget(0).show()
        if comb.currentIndex() == 2:
            tbox.setItemEnabled(1, True)
            tbox.widget(1).show()


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

        if (currentIndexRow == 0 and currentIndexColumn == 0):
            diffusionCoefElements[1].setEnabled(False)
            diffusionCoefElements[2].setEnabled(False)
            diffusionCoefElements[3].setEnabled(False)
            diffusionCoefElements[4].setEnabled(False)
            diffusionCoefElements[5].setEnabled(False)
            diffusionCoefElements[6].setEnabled(False)
            diffusionCoefElements[7].setEnabled(False)
            diffusionCoefElements[8].setEnabled(False)
        elif (currentIndexRow == 0 and currentIndexColumn == 1):
            diffusionCoefElements[1].setEnabled(True)
            diffusionCoefElements[2].setEnabled(False)
            diffusionCoefElements[3].setEnabled(False)
            diffusionCoefElements[4].setEnabled(False)
            diffusionCoefElements[5].setEnabled(False)
            diffusionCoefElements[6].setEnabled(False)
            diffusionCoefElements[7].setEnabled(False)
            diffusionCoefElements[8].setEnabled(False)
        elif (currentIndexRow == 0 and currentIndexColumn == 2):
            diffusionCoefElements[1].setEnabled(True)
            diffusionCoefElements[2].setEnabled(True)
            diffusionCoefElements[3].setEnabled(False)
            diffusionCoefElements[4].setEnabled(False)
            diffusionCoefElements[5].setEnabled(False)
            diffusionCoefElements[6].setEnabled(False)
            diffusionCoefElements[7].setEnabled(False)
            diffusionCoefElements[8].setEnabled(False)
        elif (currentIndexRow == 1 and currentIndexColumn == 0):
            diffusionCoefElements[1].setEnabled(False)
            diffusionCoefElements[2].setEnabled(False)
            diffusionCoefElements[3].setEnabled(True)
            diffusionCoefElements[4].setEnabled(False)
            diffusionCoefElements[5].setEnabled(False)
            diffusionCoefElements[6].setEnabled(False)
            diffusionCoefElements[7].setEnabled(False)
            diffusionCoefElements[8].setEnabled(False)
        elif (currentIndexRow == 1 and currentIndexColumn == 1):
            diffusionCoefElements[1].setEnabled(True)
            diffusionCoefElements[2].setEnabled(False)
            diffusionCoefElements[3].setEnabled(True)
            diffusionCoefElements[4].setEnabled(True)
            diffusionCoefElements[5].setEnabled(False)
            diffusionCoefElements[6].setEnabled(False)
            diffusionCoefElements[7].setEnabled(False)
            diffusionCoefElements[8].setEnabled(False)
        elif (currentIndexRow == 1 and currentIndexColumn == 2):
            diffusionCoefElements[1].setEnabled(True)
            diffusionCoefElements[2].setEnabled(True)
            diffusionCoefElements[3].setEnabled(True)
            diffusionCoefElements[4].setEnabled(True)
            diffusionCoefElements[5].setEnabled(True)
            diffusionCoefElements[6].setEnabled(False)
            diffusionCoefElements[7].setEnabled(False)
            diffusionCoefElements[8].setEnabled(False)
        elif (currentIndexRow == 2 and currentIndexColumn == 0):
            diffusionCoefElements[1].setEnabled(False)
            diffusionCoefElements[2].setEnabled(False)
            diffusionCoefElements[3].setEnabled(True)
            diffusionCoefElements[4].setEnabled(False)
            diffusionCoefElements[5].setEnabled(False)
            diffusionCoefElements[6].setEnabled(True)
            diffusionCoefElements[7].setEnabled(False)
            diffusionCoefElements[8].setEnabled(False)
        elif (currentIndexRow == 2 and currentIndexColumn == 1):
            diffusionCoefElements[1].setEnabled(True)
            diffusionCoefElements[2].setEnabled(False)
            diffusionCoefElements[3].setEnabled(True)
            diffusionCoefElements[4].setEnabled(True)
            diffusionCoefElements[5].setEnabled(False)
            diffusionCoefElements[6].setEnabled(True)
            diffusionCoefElements[7].setEnabled(True)
            diffusionCoefElements[8].setEnabled(False)
        elif (currentIndexRow == 2 and currentIndexColumn == 2):
            diffusionCoefElements[1].setEnabled(True)
            diffusionCoefElements[2].setEnabled(True)
            diffusionCoefElements[3].setEnabled(True)
            diffusionCoefElements[4].setEnabled(True)
            diffusionCoefElements[5].setEnabled(True)
            diffusionCoefElements[6].setEnabled(True)
            diffusionCoefElements[7].setEnabled(True)
            diffusionCoefElements[8].setEnabled(True)

class CoefficientsPDE():
    def CheckCoefficient(ar):
        CoefficientArray = []
        
        for i in ar:
            if ar[0].isChecked() == True:
                CoefficientArray.append(1)
            if ar[1].isChecked() == True:
                CoefficientArray.append(2)
            if ar[2].isChecked() == True:
                CoefficientArray.append(3)
            if ar[3].isChecked() == True:
                CoefficientArray.append(4)
            if ar[4].isChecked() == True:
                CoefficientArray.append(5)
            if ar[5].isChecked() == True:
                CoefficientArray.append(6)
            if ar[6].isChecked() == True:
                CoefficientArray.append(7)
            if ar[7].isChecked() == True:
                CoefficientArray.append(8)
            
        return CoefficientArray

    def currentCoefficientForM(section, check):
        for i in range(1, section.count()):
            section.widget(i).hide()
            section.setItemEnabled(i, False)
       
        for i in check:
            section.setItemEnabled(i, True)
            section.widget(i).show()


