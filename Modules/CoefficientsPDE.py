class CoefficientsPDE():
    def CheckCoefficient(ar):
        CoefficientArray = []
    
        for index, item in enumerate(ar):
            if ar[index].isChecked() == True:
                CoefficientArray.append(index + 1)

        return CoefficientArray

    def currentCoefficientForM(section, check):
        for i in range(1, section.count()):
            section.widget(i).hide()
            section.setItemEnabled(i, False)
       
        for i in check:
            section.setItemEnabled(i, True)
            section.widget(i).show()
