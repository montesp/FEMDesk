
class CoefficientsPDE():
    def CheckCoefficient(ar):
        CoefficientArray = []
    
        for index, item in enumerate(ar):
            if ar[index].isChecked() == True:
                CoefficientArray.append(index + 1)

        return CoefficientArray

    def currentCoefficientForM(section, check, arrayCoeff, arrayCheck):
        position = 1
        for i in range(section.count()):
            section.removeItem(1)

        section.insertItem(100, arrayCoeff[9], arrayCheck[9])

        for i in check:
            if(i != 0):
                section.insertItem(position, arrayCoeff[i], arrayCheck[i])
                position+=1
                
          

