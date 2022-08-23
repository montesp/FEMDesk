
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

    def selectMatrix(m, comb1, pos):
        arComb = []

        for i in range(comb1.count()):
         arComb.append(int(comb1.itemText(i)))

        if pos == 3 or pos == 8:
            if 3 in arComb:
                m.matrix3X1.show()
            elif 2 in arComb:
                m.matrix2X1.show()
            else:
                m.matrix1X1.show()
        else:
            if 3 in arComb:
                m.matrix3X3.show()
            elif 2 in arComb:
                m.matrix2X2.show()
            else:
                m.matrix1X1.show()
    
    def selectCombs(arRowComb, pos):
        for i in range(arRowComb[pos - 1][0].count()):
            if arRowComb[pos - 1][0].currentIndex() == i:
             for j in range(arRowComb[pos][0].count()):
                if arRowComb[pos - 1][1].currentIndex() == j:
                 c1 = i
                 c2 = j
                 c = str(c1) + str(c2)
                 break
        return c

    def showMessageBox(self, arRowComb, typeComb, m, arraylEdits, pos):
        dialog = QMessageBox.question(self, 'Importante', "Seguro que quieres guardar los cambios?", QMessageBox.Cancel | QMessageBox.Yes)

        arComb = []
        for i in range(arRowComb[pos - 1][0].count()):
            arComb.append(int(arRowComb[pos - 1][0].itemText(i)))

        arC3 = ["00", "01", "02", "10", "11", "12", "20", "21", "22"]
        arC2 = ["00", "01", "10", "11",]

        if dialog == QMessageBox.Yes:
         if pos == 3 or pos == 8:
            if 3 in arComb:
                for i in range(arRowComb[pos - 1][0].count()):
                    if arRowComb[pos - 1][0].currentIndex() == i:
                         CoefficientsPDE.passData(m.arraylEditMatrix[4][i], typeComb, arraylEdits, pos, m.matrix3X1)
            elif 2 in arComb:
                for i in range(arRowComb[pos - 1][0].count()):
                    if arRowComb[pos - 1][0].currentIndex() == i:
                         CoefficientsPDE.passData(m.arraylEditMatrix[3][i], typeComb, arraylEdits, pos, m.matrix2X1)
            else:
                 CoefficientsPDE.passData(m.matrix1X1.lEdit11, typeComb, arraylEdits, pos, m.matrix1X1)
         else:
            if 3 in arComb:
                c = CoefficientsPDE.selectCombs(arRowComb, pos)
                for i in range(len(arC3)):
                    if c == arC3[i]:
                        CoefficientsPDE.passData(m.arraylEditMatrix[2][i], typeComb, arraylEdits, pos, m.matrix3X3)
                        break
            elif 2 in arComb:
                c = CoefficientsPDE.selectCombs(arRowComb, pos)
                for i in range(len(arC2)):
                    if c == arC2[i]:
                        CoefficientsPDE.passData(m.arraylEditMatrix[1][i], typeComb, arraylEdits, pos, m.matrix2X2)
                        break
            else:
                CoefficientsPDE.passData(m.matrix1X1.lEdit11, typeComb, arraylEdits, pos, m.matrix1X1)
        else:
            print("Cancelado")

    def passData(lEdit, typeComb, arraylEdits, pos, matrix):
     lEdit.setEnabled(True)
     lEdit.clear()

     if pos == 1:
        if typeComb.currentIndex() == 0:
            lEdit.insert(arraylEdits[0][0].text())
            lEdit.setEnabled(False)
            matrix.show()
        else:
            lEdit.insert(arraylEdits[0][1].text() + ",")
            lEdit.insert(arraylEdits[0][2].text() + ",")
            lEdit.insert(arraylEdits[0][3].text() + ",")
            lEdit.insert(arraylEdits[0][4].text())
            lEdit.setEnabled(False)
            matrix.show()
     if pos == 2:
        lEdit.insert(arraylEdits[1][0].text())
        lEdit.setEnabled(False)
        matrix.show()
     if pos == 3:
        lEdit.insert(arraylEdits[2][0].text())
        lEdit.setEnabled(False)
        matrix.show()
     if pos == 4:
        lEdit.insert(arraylEdits[3][0].text())
        lEdit.setEnabled(False)
        matrix.show()
     if pos == 5:
        lEdit.insert(arraylEdits[4][0].text())
        lEdit.setEnabled(False)
        matrix.show()
     if pos == 6:
        lEdit.insert(arraylEdits[5][0].text() + ",")
        lEdit.insert(arraylEdits[5][1].text())
        lEdit.setEnabled(False)
        matrix.show()
     if pos == 7:
        lEdit.insert(arraylEdits[6][0].text() + ",")
        lEdit.insert(arraylEdits[6][1].text())
        lEdit.setEnabled(False)
        matrix.show()
     if pos == 8:
        lEdit.insert(arraylEdits[7][0].text() + ",")
        lEdit.insert(arraylEdits[7][1].text())
        lEdit.setEnabled(False)
        matrix.show()
    