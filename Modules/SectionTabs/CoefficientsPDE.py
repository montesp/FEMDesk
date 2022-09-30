
import enum
from msilib.schema import Directory
from tkinter import dialog
from PyQt5.QtWidgets import QMessageBox
from Modules.Dictionary.DMatrix import *
from Modules.ManageFiles import *


class CoefficientsPDE():
    def CheckCoefficient(ar):
        CoefficientArray = []
    
        for index, item in enumerate(ar):
            if ar[index].isChecked() == True:
                CoefficientArray.append(index + 1)
        if len(CoefficientArray) != 0:
         noItemsCoeffM["noItems"] = len(CoefficientArray)
         noItemsCoeffM["items"] = CoefficientArray
        else:
         noItemsCoeffM["noItems"] = 0
         noItemsCoeffM["items"] = [0]
        print(noItemsCoeffM["items"])
        return CoefficientArray


    def clearCoefficientTbox(self,section, arrayCoeff, arrayCheck):
        for i in range(section.count()):
            section.removeItem(1)

        section.insertItem(100, arrayCoeff[9], arrayCheck[9])

    def currentCoefficientForM(self,section, check, arrayCoeff, arrayCheck):
        position = 1
        for i in range(section.count()):
            section.removeItem(1)

        section.insertItem(100, arrayCoeff[9], arrayCheck[9])

        FileData.checkUpdateFile(self)

        for i in check:
            if(i != 0):
                section.insertItem(position, arrayCoeff[i], arrayCheck[i])
                position+=1
        
        fileIndicator["*"] = "*"
        if directory["dir"] != '':
            self.lblDirectory.setText(directory["dir"] + fileIndicator["*"])
            self.actionSaves.setEnabled(True)
    
    def currentData(self, pos):
        if pos == 1:
            self.lEditDiffusionCoef.setText(allNewMatrix.diffusionM[self.cmbRowDiffusionCoef.currentIndex()][self.cmbColumnDiffusionCoef.currentIndex()])
        elif pos == 2:
            self.lEditAbsorCoef.setText(allNewMatrix.absorptionM[self.cmbAbsorptionRow.currentIndex()][self.cmbAbsorptionColumn.currentIndex()])
        elif pos == 3:
            self.lEditSourceTerm.setText(allNewMatrix.sourceM[self.cmbSourceRow.currentIndex()])
        elif pos == 4:
            self.lEditMassCoef.setText(allNewMatrix.massM[self.cmbMassCoefRow.currentIndex()][self.cmbMassCoefColumn.currentIndex()])
        elif pos == 5:
            self.lEditDamMassCoef.setText(allNewMatrix.damMassM[self.cmbDamMassCoefRow.currentIndex()][self.cmbDamMassCoefColumn.currentIndex()])