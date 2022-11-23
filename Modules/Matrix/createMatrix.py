from PyQt5.QtWidgets import QDialog, QMessageBox
import Modules.Matrix.dialogMatrix 
import Modules.Matrix.dialogVector
import Modules.Matrix.dialogTableDiffusion
import Modules.Matrix.dialogTableMatrix
import Modules.Matrix.dialogTableVector
from Modules.Dictionary.DMatrix import *
from Modules.Matrix.MatrixData import MatrixData
import numpy as np
from Modules.Dictionary.DModelWizard import *
import Modules.ManageFiles.ManageFiles

class allNewMatrix():
        matrixCoefficientPDE = None
        vectorCoefficientPDE = None
        matrixItemsActivated = None
        n = 1
        domains = 0

        def __init__(self):
         pass

        def changeMatrixDimensions(self, n, canvas, win):
            self.dMatrix = Modules.Matrix.dialogMatrix.dialogMatrix(n)
            self.dVector = Modules.Matrix.dialogVector.dialogVector(n)
            self.dTableDiffusion = Modules.Matrix.dialogTableDiffusion.dialogTableDiffusionMatrix(n)
            self.dTableMatrix = Modules.Matrix.dialogTableMatrix.dialogTableMatrix(n)
            self.dTableVector = Modules.Matrix.dialogTableVector.dialogTableVector(n)
            numberDomains = canvas.getSolids()
            initialValues["noVariables"] = n

            allNewMatrix.domains = len(numberDomains)
            MatrixData.domains = len(numberDomains)
            allNewMatrix.n = win.modelwizard.getVariables()
            print("Dominios desde el allnewmatrix")
            print(allNewMatrix.domains)
            allNewMatrix.matrixCoefficientPDE = np.empty([allNewMatrix.domains, 6, 
            allNewMatrix.n, allNewMatrix.n], dtype= 'U256')
            allNewMatrix.vectorCoefficientPDE = np.empty([allNewMatrix.domains, 2,1,
            allNewMatrix.n], dtype= 'U256')
            allNewMatrix.matrixItemsActivated = np.empty([allNewMatrix.domains, 8], 
            dtype='U256')
            
            print("Matrices de Coefficients PDE")
            print(allNewMatrix.matrixCoefficientPDE)

        def addDimensionMatrix3D(self, canvas):
            numberDomains = canvas.getSolids()
            allNewMatrix.domains = len(numberDomains)
            MatrixData.domains = len(numberDomains)
            updatedMatrix = np.resize(self.matrixCoefficientPDE, (len(numberDomains), 
            6, allNewMatrix.n, allNewMatrix.n))
            updatedVector = np.resize(self.vectorCoefficientPDE, (len(numberDomains), 
            2, 1, allNewMatrix.n))
            updatedItemsMatrix = np.resize(self.matrixItemsActivated,
            (len(numberDomains), 8))

            #Limpíar los datos que pudieron ser copiados de las otras dimensiones
            for i in range(len(updatedMatrix[len(numberDomains) - 1])):
                updatedMatrix[len(numberDomains) - 1][i].fill('')

            for i in range(len(updatedVector[len(numberDomains) - 1])):
                updatedVector[len(numberDomains) - 1][i].fill('')

            for i in range(len(updatedItemsMatrix[len(numberDomains) - 1])):
                updatedItemsMatrix[len(numberDomains) - 1][i] = ''

            print(updatedMatrix)
            allNewMatrix.matrixCoefficientPDE = updatedMatrix
            allNewMatrix.vectorCoefficientPDE = updatedVector
            allNewMatrix.matrixItemsActivated = updatedItemsMatrix

        def removeDimensionMatrix3D(self, solids, poly):
            if myFlags["ModelWizardMode"] == "Coefficient form PDE":
                print(solids.index(poly))
                print("Dimension de la matriz nxn")
                print(allNewMatrix.n)
                print(self.n)
                updatedMatrix = np.reshape(self.matrixCoefficientPDE, (len(solids), 
                8, allNewMatrix.n, allNewMatrix.n))
                updatedVector = np.reshape(self.vectorCoefficientPDE, (len(solids), 
                2, 1, allNewMatrix.n))
                updatedItemsMatrix = np.reshape(self.matrixItemsActivated, (len(solids), 8))

                updatedMatrix = np.delete(self.matrixCoefficientPDE, solids.index(poly), 0)
                updatedVector = np.delete(self.vectorCoefficientPDE, solids.index(poly), 0)
                updatedItemsMatrix = np.delete(self.matrixItemsActivated, solids.index(poly), 0)

                print("Matrix con fila borrada")
                print(updatedMatrix)
                print("Vector con fila borrada")
                print(updatedVector)

                allNewMatrix.matrixCoefficientPDE = updatedMatrix
                allNewMatrix.vectorCoefficientPDE = updatedVector
                allNewMatrix.matrixItemsActivated = updatedItemsMatrix

        def newMatrix(self, canvas):
                try:
                    #Cambiar las dimensiones de las matrices
                    n = int(self.inputDepedentVarial.text())
                    if n == '':
                        n = 1
                    allNewMatrix.changeMatrixDimensions(self, n, canvas, self)
                    #Actualizar los combobox segun el numero de variables dependientes
                    MatrixData.updateCombobox(self, n)
                    #Decirle al programa el archivo Excel fue editado
                    Modules.ManageFiles.ManageFiles.FileData.checkUpdateFile(self)

                    self.btnModelWizardApply.setEnabled(False)
                except Exception:
                    QMessageBox.warning(self, "Important message", "You can only enter numeric values")
                    return

        def resetMatrix(self):
            dialog = QMessageBox.question(self, 'Important', 'Are you sure you want to reset the number of dependent variables? This will reset all arrays', QMessageBox.Cancel | QMessageBox.Yes)
            if dialog == QMessageBox.Yes:
                #Cambiar las dimensiones de las matrices
                n = 1
                Modules.Matrix.createMatrix.allNewMatrix.changeMatrixDimensions(self, n)
                #Cambiar el lineEdit de las variables iniciales
                allNewMatrix.currentInitialVariable(self)
                #Actualizar el combobox según el numero de variables dependientes
                MatrixData.updateCombobox(self, n)
                #Decirle al programa que el archivo Excel fue editado
                Modules.ManageFiles.ManageFiles.FileData.checkUpdateFile(self)
            else:
                print("Operacion Cancelada")

        def currentInitialVariable(self, allnewmatrix):
                noVar = "{}".format(allnewmatrix.n)
                self.inputDepedentVarial.setText(noVar)
            
