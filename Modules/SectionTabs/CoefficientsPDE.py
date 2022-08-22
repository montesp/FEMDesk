
import enum
from PyQt5.QtWidgets import QMessageBox

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
                

    def currentCombMatrix(arrayCoeff, arrayComb, comb):
        counter = 1
        for index, item in enumerate(arrayCoeff):
            #if arrayCoeff[index].isChecked() == True:
                for j, item in enumerate(arrayComb[index]):
                        arrayComb[index][j].clear()

                for j, item in enumerate(arrayComb[index]):
                    if comb.currentIndex() == 0:
                        counter = 1
                    if comb.currentIndex() == 1:
                        counter = 2
                    if comb.currentIndex() == 2:
                        counter = 3
                    for i in range(1, counter + 1):
                        arrayComb[index][j].addItem(str(i))

        

    