
from PyQt5.QtWidgets import QMessageBox
from Modules.Dictionary.DMatrix import *



class MatrixData():
    """def changeMatrixDimensions(self, n):
        self.dMatrix = dialogMatrix(n)
        self.dVector = dialogVector(n)
        initialValues["noVariables"] = n
        allNewMatrix.diffusionM = np.empty([n,n], dtype='U256')
        allNewMatrix.absorptionM = np.empty([n,n], dtype='U256')
        allNewMatrix.sourceM = np.empty(n, dtype='U256')
        allNewMatrix.massM = np.empty([n,n], dtype='U256')
        allNewMatrix.damMassM = np.empty([n,n], dtype='U256')
        allNewMatrix.cFluxM = np.empty([n,n], dtype='U256')
        allNewMatrix.convectionM = np.empty([n,n], dtype='U256')
        allNewMatrix.cSourceM = np.empty(n, dtype='U256')
        allNewMatrix.n = n"""

    def updateCombobox(self, n):
        #Actualizar el combobox según el numero de variables dependientes
        for index, item in enumerate(self.CoefficientCheckBoxArray):
                for j, item in enumerate(self.arrayCmbRowColumns[index]):
                        self.arrayCmbRowColumns[index][j].clear()

                for j, item in enumerate(self.arrayCmbRowColumns[index]):
                    for i in range(1, n + 1):
                        self.arrayCmbRowColumns[index][j].addItem(str(i))
        self.cmbInitialValues.clear()

        for i in range(1, n + 1):
            self.cmbInitialValues.addItem("u" + str(i))

    def setDiffusionMatrixSingleData(self, x, y, diffusionComb, lineEdit, matrix):
     #try:
        ar = []
        ar.append(float(lineEdit[0][0].text()))
        ar.append(float(lineEdit[0][0].text()))
        ar.append(float(lineEdit[0][0].text()))
        ar.append(float(lineEdit[0][0].text()))
        ar.append(diffusionComb.currentIndex())
        matrix[x,y] = str(ar)
        print(matrix)
        self.insertMatrix(matrix)
     #except Exception:
        #QMessageBox.warning(self, "Important message", "Solo puede ingresar valores numericos")
        #return
    
    def setDiffusionMatrixMultipleData(self, x, y, diffusionComb, lineEdit, matrix):
     try:
        ar = []
        ar.append(float(lineEdit[0][1].text()))
        ar.append(float(lineEdit[0][2].text()))
        ar.append(float(lineEdit[0][3].text()))
        ar.append(float(lineEdit[0][4].text()))
        ar.append(diffusionComb.currentIndex())
        matrix[x,y] = str(ar)
        print(matrix)
        self.insertMatrix(matrix)
     except Exception:
        QMessageBox.warning(self, "Important message", "Solo puede ingresar valores numericos")
        return

    def setMatrixSingleData(self, x, y, lineEdit, matrix):
     try:
        data = float(lineEdit.text())
        matrix[x,y] = data
        self.insertMatrix(matrix)
     except Exception:
        QMessageBox.warning(self, "Important message", "Solo puede ingresar valores numericos")
        return

    def setMatrixDoubleData(self, x, y, lineEdit, lineEdit2, matrix):
     try:
        ar = []
        ar.append(float(lineEdit.text()))
        ar.append(float(lineEdit2.text()))
        matrix[x,y] = str(ar)
        self.insertMatrix(matrix)
     except Exception:
        QMessageBox.warning(self, "Important message", "Solo puede ingresar valores numericos")
        return

    def setVectorSingleData(self, x, lineEdit, matrix):
     try:
        self.cell.insert(float(lineEdit.text()))
        matrix[x] = lineEdit.text()
        self.insertVector(matrix)
     except Exception:
        QMessageBox.warning(self, "Important message", "Solo puede ingresar valores numericos")
        return

    def setVectorDoubleData(self, x, lineEdit, lineEdit2, matrix):
     try:
        ar = []
        ar.append(float(lineEdit.text()))
        ar.append(float(lineEdit2.text()))
        self.cell.insert(str(ar))
        matrix[x] = str(ar)
        self.insertVector(matrix)
     except Exception:
        QMessageBox.warning(self, "Important message", "Solo puede ingresar valores numericos")
        return