
import enum
from tkinter import dialog
from PyQt5.QtWidgets import QMessageBox
from Modules.Dictionary.DMatrix import *

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
                
    def currentCombMatrix(self, arrayCoeff, arrayComb, comb):
        dialog = QMessageBox.question(self, 'Importante', '¿Seguro que quieres cambiar el numero de variables dependientes? Harán cambios en todas las matrices', QMessageBox.Cancel | QMessageBox.Yes)
        
        if dialog == QMessageBox.Yes:
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
        else: 
            print("Cancelado")

    def selectMatrix(m, comb1, pos):
        arComb = []

        for i in range(comb1.count()):
         arComb.append(int(comb1.itemText(i)))

        if pos == 3 or pos == 8:
            if 3 in arComb:
                CoefficientsPDE.showMatrix(m.matrix3X1, m.arrayM3X1, pos)
            elif 2 in arComb:
                CoefficientsPDE.showMatrix(m.matrix2X1, m.arrayM2X1,pos)
            else:
                CoefficientsPDE.showMatrix(m.matrix1X1,m.arrayM1X1, pos)
        else:
            if 3 in arComb:
                CoefficientsPDE.showMatrix(m.matrix3X3, m.arrayM3X3, pos)
            elif 2 in arComb:
                CoefficientsPDE.showMatrix(m.matrix2X2, m.arrayM2X2,pos)
            else:
                CoefficientsPDE.showMatrix(m.matrix1X1, m.arrayM1X1,pos)

    def showMatrix(matrix, arM, pos):

     for i in range(len(arM)):
        arM[i].clear()

     if pos == 1:
        for i in range(len(arM)):
            arM[i].insert(diffusionMatrix[arM[i].objectName()])  
        matrix.show()
     if pos == 2:
        for i in range(len(arM)):
            arM[i].insert(absorptionMatrix[arM[i].objectName()])
        matrix.show()
     if pos == 3:
        for i in range(len(arM)):
            arM[i].insert(sourceMatrix[arM[i].objectName()])
        matrix.show()
     if pos == 4:
        for i in range(len(arM)):
            arM[i].insert(massMatrix[arM[i].objectName()])
        matrix.show()
     if pos == 5:
        for i in range(len(arM)):
            arM[i].insert(damMassMatrix[arM[i].objectName()])
        matrix.show()
     if pos == 6:
        for i in range(len(arM)):
            arM[i].insert(cFluxMatrix[arM[i].objectName()])
        matrix.show()
     if pos == 7:
        for i in range(len(arM)):
            arM[i].insert(convectionMatrix[arM[i].objectName()]) 
        matrix.show()
     if pos == 8:
        for i in range(len(arM)):
            arM[i].insert(cSourceMatrix[arM[i].objectName()]) 
        matrix.show()

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
                         CoefficientsPDE.passData(m.arraylEditMatrix[4][i], typeComb, arraylEdits, pos, m.matrix3X1, m.arrayM3X1, 3)
            elif 2 in arComb:
                for i in range(arRowComb[pos - 1][0].count()):
                    if arRowComb[pos - 1][0].currentIndex() == i:
                         CoefficientsPDE.passData(m.arraylEditMatrix[3][i], typeComb, arraylEdits, pos, m.matrix2X1, m.arrayM2X1, 2)
            else:
                 CoefficientsPDE.passData(m.matrix1X1.lEdit11, typeComb, arraylEdits, pos, m.matrix1X1, m.arrayM1X1, 1)
         else:
            if 3 in arComb:
                c = CoefficientsPDE.selectCombs(arRowComb, pos)
                for i in range(len(arC3)):
                    if c == arC3[i]:
                        CoefficientsPDE.passData(m.arraylEditMatrix[2][i], typeComb, arraylEdits, pos, m.matrix3X3, m.arrayM3X3, 3)
                        break
            elif 2 in arComb:
                c = CoefficientsPDE.selectCombs(arRowComb, pos)
                for i in range(len(arC2)):
                    if c == arC2[i]:
                        CoefficientsPDE.passData(m.arraylEditMatrix[1][i], typeComb, arraylEdits, pos, m.matrix2X2, m.arrayM2X2, 2)
                        break
            else:
                CoefficientsPDE.passData(m.matrix1X1.lEdit11, typeComb, arraylEdits, pos, m.matrix1X1, m.arrayM1X1, 1)
        else:
            print("Cancelado")

    def passData(lEdit, typeComb, arraylEdits, pos, matrix, arM, noVariables):
     lEdit.setEnabled(True)
     lEdit.clear()
     initialValues["noVariables"] = noVariables

     if pos == 1:
        if typeComb.currentIndex() == 0:
            lEdit.insert(arraylEdits[0][0].text())
            diffusionMatrix[lEdit.objectName()] = lEdit.text()
            diffusionMatrix["inputMode"] = typeComb.currentIndex()
            print(lEdit.objectName())
            print(diffusionMatrix)
            lEdit.setEnabled(False)
            CoefficientsPDE.showMatrix(matrix, arM, pos)
        else:
            lEdit.insert(arraylEdits[0][1].text() + ",")
            lEdit.insert(arraylEdits[0][2].text() + ",")
            lEdit.insert(arraylEdits[0][3].text() + ",")
            lEdit.insert(arraylEdits[0][4].text())
            diffusionMatrix[lEdit.objectName()] = lEdit.text()
            diffusionMatrix["inputMode"] = typeComb.currentIndex()
            print(lEdit.objectName())
            print(diffusionMatrix)
            lEdit.setEnabled(False)
            CoefficientsPDE.showMatrix(matrix, arM, pos)
     if pos == 2:
        lEdit.insert(arraylEdits[1][0].text())
        absorptionMatrix[lEdit.objectName()] = lEdit.text()
        print(lEdit.objectName())
        print(absorptionMatrix)
        lEdit.setEnabled(False)
        CoefficientsPDE.showMatrix(matrix, arM, pos)
     if pos == 3:
        lEdit.insert(arraylEdits[2][0].text())
        sourceMatrix[lEdit.objectName()] = lEdit.text()
        print(lEdit.objectName())
        print(sourceMatrix)
        lEdit.setEnabled(False)
        CoefficientsPDE.showMatrix(matrix, arM, pos)
     if pos == 4:
        lEdit.insert(arraylEdits[3][0].text())
        massMatrix[lEdit.objectName()] = lEdit.text()
        print(lEdit.objectName())
        print(massMatrix)
        lEdit.setEnabled(False)
        CoefficientsPDE.showMatrix(matrix, arM, pos)
     if pos == 5:
        lEdit.insert(arraylEdits[4][0].text())
        damMassMatrix[lEdit.objectName()] = lEdit.text()
        print(lEdit.objectName())
        print(damMassMatrix)
        lEdit.setEnabled(False)
        CoefficientsPDE.showMatrix(matrix, arM, pos)
     if pos == 6:
        lEdit.insert(arraylEdits[5][0].text() + ",")
        lEdit.insert(arraylEdits[5][1].text())
        cFluxMatrix[lEdit.objectName()] = lEdit.text()
        print(lEdit.objectName())
        print(cFluxMatrix)
        lEdit.setEnabled(False)
        CoefficientsPDE.showMatrix(matrix, arM, pos)
     if pos == 7:
        lEdit.insert(arraylEdits[6][0].text() + ",")
        lEdit.insert(arraylEdits[6][1].text())
        convectionMatrix[lEdit.objectName()] = lEdit.text()
        print(lEdit.objectName())
        print(convectionMatrix)
        lEdit.setEnabled(False)
        CoefficientsPDE.showMatrix(matrix, arM, pos)
     if pos == 8:
        lEdit.insert(arraylEdits[7][0].text() + ",")
        lEdit.insert(arraylEdits[7][1].text())
        cSourceMatrix[lEdit.objectName()] = lEdit.text()
        print(lEdit.objectName())
        print(cSourceMatrix)
        lEdit.setEnabled(False)
        CoefficientsPDE.showMatrix(matrix, arM, pos)
    