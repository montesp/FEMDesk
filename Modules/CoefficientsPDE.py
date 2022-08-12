
class CoefficientsPDE():
    def CheckCoefficient(ar):
        CoefficientArray = []
    
        for index, item in enumerate(ar):
            if ar[index].isChecked() == True:
                CoefficientArray.append(index + 1)

        return CoefficientArray

    def currentCoefficientForM(section, check, arrayCoeff, arrayCheck):
        j = 0
        for i in range(1, section.count()):
            section.removeItem(i)
       
        for i in check:
            if(i == arrayCheck[i]):
                section.insertItem(j, arrayCoeff[i], arrayCheck[i])
                j+=1
            else:
                continue

