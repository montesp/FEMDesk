
import enum


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
                
          
    """def currentInitialValues(comb, array):
        for i, item in enumerate(array):
            for j, item in enumerate(array[i]):
                array[i][j].hide()
        
        if comb.currentIndex() == 0:
            for i, item in enumerate(array[0]):
                array[0][i].show()

        if comb.currentIndex() == 1:
            
            for i, item in enumerate(array[1]):
                array[0][i].show()
                array[1][i].show()

        if comb.currentIndex() == 2:
            for i, item in enumerate(array[2]):
                array[0][i].show()
                array[1][i].show()
                array[2][i].show()"""

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

        

    def currentPreviewMatrix(comb, arrayMatrix, pos):
        for i, item in enumerate(arrayMatrix):
            arrayMatrix[i].hide()
        
            """if pos == 2 | pos == 8:
             CoefficientsPDE.Matrix1x1(comb, arrayMatrix)
            else:
             CoefficientsPDE.Matrix3x3(comb, arrayMatrix)"""
            
    
    def Matrix1x1(comb, arrayMatrix):
        if comb.currentIndex() == 0:
            arrayMatrix[0].show()
        if comb.currentIndex() == 1:
            arrayMatrix[0].show()
            arrayMatrix[3].show()
        if comb.currentIndex() == 2:
            arrayMatrix[0].show()
            arrayMatrix[3].show()
            arrayMatrix[6].show()

    def Matrix3x3(comb, arrayMatrix):
        if comb.currentIndex() == 0:
            arrayMatrix[0].show()
        if comb.currentIndex() == 1:
            arrayMatrix[0].show()
            arrayMatrix[1].show()
            arrayMatrix[3].show()
            arrayMatrix[4].show()
        if comb.currentIndex() == 2:
            for i, item in enumerate(arrayMatrix):
                arrayMatrix[i].show()