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
