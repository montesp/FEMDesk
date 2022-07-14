"""
Created on Wed May 11 13:39:55 2022

@author:ruben.castaneda,
        Pavel Montes,
        Armando Teran
"""

#-*- coding: utf-8 -*-

import os, sys
import imagen_rc
import array as arr
from PyQt5.QtCore import Qt, QObject
from PyQt5.QtGui import QPainter, QCloseEvent, QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsView, QButtonGroup, QMessageBox, QTabWidget
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from interfaz import *
from module import *


app = None
class EditorWindow(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()
        self.app = app
        with open('styles.qss', 'r', encoding='utf-8') as file:
            str = file.read()
        self.setStyleSheet(str)
        root = os.path.dirname(os.path.realpath(__file__))
        loadUi(os.path.join(root, 'Interfaz.ui'), self)


        # Geometric Figure
        # Combo box
        
        self.figuresSection = self.findChild(QtWidgets.QToolBox, "figuresSection")
        self.figuresSection.setItemEnabled(0, True)
        self.figuresSection.setItemEnabled(1, False)
        self.figuresSection.setItemEnabled(2, False)
        self.figuresSection.setItemEnabled(3, False)
        self.figuresSection.setItemEnabled(4, False)

        self.cmbGeometricFigure = self.findChild(QtWidgets.QComboBox, "cmbGeometricFigure")
        self.cmbGeometricFigure.currentIndexChanged.connect(lambda: Geometry.currentCheckedComboBoxItem(self.figuresSection, self.cmbGeometricFigure))

        # Conditions PDE
        self.chkDiffusionCoefficient = self.findChild(QtWidgets.QCheckBox, "chkDiffusionCoefficient")
        self.chkAbsorptionCoefficient = self.findChild(QtWidgets.QCheckBox, "chkAbsorptionCoefficient")
        self.chkSourceTerm = self.findChild(QtWidgets.QCheckBox, "chkSourceTerm")
        self.chkMassCoefficient = self.findChild(QtWidgets.QCheckBox, "chkMassCoefficient")
        self.chkDampCoefficient = self.findChild(QtWidgets.QCheckBox, "chkDampCoefficient")
        self.chkConservativeConvection = self.findChild(QtWidgets.QCheckBox, "chkConservativeConvection")
        self.chkConvectionCoefficient = self.findChild(QtWidgets.QCheckBox, "chkConvectionCoefficient")
        self.chkConservativeFluxSource = self.findChild(QtWidgets.QCheckBox, "chkConservativeFluxSource")

        CoefficientCheckBoxArray = []
        CoefficientCheckBoxArray.append(self.chkDiffusionCoefficient)
        CoefficientCheckBoxArray.append(self.chkAbsorptionCoefficient)
        CoefficientCheckBoxArray.append(self.chkSourceTerm)
        CoefficientCheckBoxArray.append(self.chkMassCoefficient)
        CoefficientCheckBoxArray.append(self.chkDampCoefficient)
        CoefficientCheckBoxArray.append(self.chkConservativeConvection)
        CoefficientCheckBoxArray.append(self.chkConvectionCoefficient)
        CoefficientCheckBoxArray.append(self.chkConservativeFluxSource)

        self.toolBoxTypeOfCon = self.findChild(QtWidgets.QToolBox, "toolBoxTypeOfCon")
        self.toolBoxTypeOfCon.setItemEnabled(0, True)
        self.toolBoxTypeOfCon.setItemEnabled(1, False)
        self.toolBoxTypeOfCon.setItemEnabled(2, False)
        self.toolBoxTypeOfCon.setItemEnabled(3, False)
        self.toolBoxTypeOfCon.setItemEnabled(4, False)


        self.cmbTypeConditionPDE = self.findChild(QtWidgets.QComboBox, "cmbTypeConditionPDE")
        self.cmbTypeConditionPDE.currentIndexChanged.connect(lambda: ConditionsPDE.currentCheckedComboBoxItemConditions(self.toolBoxTypeOfCon, self.cmbTypeConditionPDE))


        #CheckBox Coefficients Form PDE
        self.coefficientsforM = self.findChild(QtWidgets.QToolBox, "CoefficentForM")
        self.coefficientsforM.setItemEnabled(1, False)
        self.coefficientsforM.setItemEnabled(2, False)
        self.coefficientsforM.setItemEnabled(3, False)
        self.coefficientsforM.setItemEnabled(4, False)
        self.coefficientsforM.setItemEnabled(5, False)
        self.coefficientsforM.setItemEnabled(6, False)
        self.coefficientsforM.setItemEnabled(7, False)
        self.coefficientsforM.setItemEnabled(8, False)


        self.btnCoefficientsApply = self.findChild(QtWidgets.QPushButton, "btnCoefficientsApply")
        self.btnCoefficientsApply.clicked.connect(lambda: CoefficientsPDE.currentCoefficientForM(self.coefficientsforM, CoefficientsPDE.CheckCoefficient(CoefficientCheckBoxArray)))

        #ComboBox HeatConduction
        self.inputK = self.findChild(QtWidgets.QLineEdit, "inputK")
        self.inputKD1 = self.findChild(QtWidgets.QLineEdit, "inputKD1")
        self.inputKD2 = self.findChild(QtWidgets.QLineEdit, "inputKD2")
        self.inputKD3 = self.findChild(QtWidgets.QLineEdit, "inputKD3")
        self.inputKD4 = self.findChild(QtWidgets.QLineEdit, "inputKD4")

        inputKArray = []

        inputKArray.append(self.inputK)
        inputKArray.append(self.inputKD1)
        inputKArray.append(self.inputKD2)
        inputKArray.append(self.inputKD3)
        inputKArray.append(self.inputKD4)

        self.inputK.setEnabled(True)
        self.inputKD1.setEnabled(False)
        self.inputKD2.setEnabled(False)
        self.inputKD3.setEnabled(False)
        self.inputKD4.setEnabled(False)

        self.cmbHeatConduction = self.findChild(QtWidgets.QComboBox, "cmbHeatConduction")
        self.cmbHeatConduction.currentIndexChanged.connect(lambda: Materials.currentHeatConduction(self.cmbHeatConduction, inputKArray))

        #Combobox TypeCondiction
        self.tboxTypeCondition = self.findChild(QtWidgets.QWidget, "toolBoxTypeOfCondition")
        self.tboxTypeCondition.setItemEnabled(0, False)
        self.tboxTypeCondition.setItemEnabled(1, False)
        
        self.tboxTypeCondition.widget(0).hide()
        self.tboxTypeCondition.widget(1).hide()
      
        self.cmbtypecondition = self.findChild(QtWidgets.QComboBox, "cmbTypeCondition")
        self.cmbtypecondition.currentIndexChanged.connect(lambda: Conditions.currentTypeCondition(self.cmbtypecondition, self.tboxTypeCondition))

  

        # Coefficent form PDE
        self.cmbRowDiffusionCoef = self.findChild(QtWidgets.QComboBox, "cmbRowDiffusionCoef")
        self.cmbColumnDiffusionCoef = self.findChild(QtWidgets.QComboBox, "cmbColumnDiffusionCoef")


        self.diffusionCoefData = []
        self.lEditDiffusionCoef11 = self.findChild(QtWidgets.QLineEdit, "lEditDiffusionCoef11")
        self.lEditDiffusionCoef12 = self.findChild(QtWidgets.QLineEdit, "lEditDiffusionCoef12")
        self.lEditDiffusionCoef13 = self.findChild(QtWidgets.QLineEdit, "lEditDiffusionCoef13")
        self.lEditDiffusionCoef21 = self.findChild(QtWidgets.QLineEdit, "lEditDiffusionCoef21")
        self.lEditDiffusionCoef22 = self.findChild(QtWidgets.QLineEdit, "lEditDiffusionCoef22")
        self.lEditDiffusionCoef23 = self.findChild(QtWidgets.QLineEdit, "lEditDiffusionCoef23")
        self.lEditDiffusionCoef31 = self.findChild(QtWidgets.QLineEdit, "lEditDiffusionCoef31")
        self.lEditDiffusionCoef32 = self.findChild(QtWidgets.QLineEdit, "lEditDiffusionCoef32")
        self.lEditDiffusionCoef33 = self.findChild(QtWidgets.QLineEdit, "lEditDiffusionCoef33")

        self.lEditDiffusionCoef12.setEnabled(False)
        self.lEditDiffusionCoef13.setEnabled(False)
        self.lEditDiffusionCoef21.setEnabled(False)
        self.lEditDiffusionCoef22.setEnabled(False)
        self.lEditDiffusionCoef23.setEnabled(False)
        self.lEditDiffusionCoef31.setEnabled(False)
        self.lEditDiffusionCoef32.setEnabled(False)
        self.lEditDiffusionCoef33.setEnabled(False)


        self.diffusionCoefData.append(self.lEditDiffusionCoef11)
        self.diffusionCoefData.append(self.lEditDiffusionCoef12)
        self.diffusionCoefData.append(self.lEditDiffusionCoef13)
        self.diffusionCoefData.append(self.lEditDiffusionCoef21)
        self.diffusionCoefData.append(self.lEditDiffusionCoef22)
        self.diffusionCoefData.append(self.lEditDiffusionCoef23)
        self.diffusionCoefData.append(self.lEditDiffusionCoef31)
        self.diffusionCoefData.append(self.lEditDiffusionCoef32)
        self.diffusionCoefData.append(self.lEditDiffusionCoef33)

        # self.desactivateArrayLineEdit(self, self.diffusionCoefData)

        self.cmbRowDiffusionCoef.currentIndexChanged.connect(lambda: ConditionsPDE.currentRowDiffusionCoef(self.cmbRowDiffusionCoef.currentIndex(), self.cmbColumnDiffusionCoef.currentIndex(), self.diffusionCoefData))
        self.cmbColumnDiffusionCoef.currentIndexChanged.connect(lambda: ConditionsPDE.currentRowDiffusionCoef(self.cmbRowDiffusionCoef.currentIndex(), self.cmbColumnDiffusionCoef.currentIndex(), self.diffusionCoefData))

   
            
    def desactivateLineEdit(element, enabledStatus):
        element.setEnabled(enabledStatus)

    def desactivateArrayLineEdit(element):
        for i in element:
            element[i].setEnabled(False)

   
    def checkInfoDefaultModelWizard(self, text):
        # Realizar los calculos del model wizard, crear una funcion
        value = 1 if text == "" else text
        print(value)



def init_app():
    app = QApplication.instance()
    app = QApplication(sys.argv)

    return app

def main():
    app = init_app()
    
    widget = EditorWindow()
    widget.setWindowIcon(QIcon("icon-temperature.png"))
    widget.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
