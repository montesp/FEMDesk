
import enum
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
                
    