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
# from module import *

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
        self.cmbGeometricFigure.currentIndexChanged.connect(lambda: self.currentCheckedComboBoxItem(self.figuresSection, self.cmbGeometricFigure))

        # Conditions PDE
        self.toolBoxTypeOfCon = self.findChild(QtWidgets.QToolBox, "toolBoxTypeOfCon")
        self.toolBoxTypeOfCon.setItemEnabled(0, True)
        self.toolBoxTypeOfCon.setItemEnabled(1, False)
        self.toolBoxTypeOfCon.setItemEnabled(2, False)
        self.toolBoxTypeOfCon.setItemEnabled(3, False)
        self.toolBoxTypeOfCon.setItemEnabled(4, False)


        self.cmbTypeConditionPDE = self.findChild(QtWidgets.QComboBox, "cmbTypeConditionPDE")
        self.cmbTypeConditionPDE.currentIndexChanged.connect(lambda: self.currentCheckedComboBoxItemConditions(self.toolBoxTypeOfCon, self.cmbTypeConditionPDE))


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
        self.btnCoefficientsApply.clicked.connect(lambda: self.currentCoefficientForM(self.coefficientsforM, self.CheckCoefficient()))

        #ComboBox HeatConduction
        self.inputK = self.findChild(QtWidgets.QLineEdit, "inputK")
        self.inputKD1 = self.findChild(QtWidgets.QLineEdit, "inputKD1")
        self.inputKD2 = self.findChild(QtWidgets.QLineEdit, "inputKD2")
        self.inputKD3 = self.findChild(QtWidgets.QLineEdit, "inputKD3")
        self.inputKD4 = self.findChild(QtWidgets.QLineEdit, "inputKD4")

        self.inputK.setEnabled(True)
        self.inputKD1.setEnabled(False)
        self.inputKD2.setEnabled(False)
        self.inputKD3.setEnabled(False)
        self.inputKD4.setEnabled(False)

        self.cmbHeatConduction = self.findChild(QtWidgets.QComboBox, "cmbHeatConduction")
        self.cmbHeatConduction.currentIndexChanged.connect(lambda: self.currentHeatConduction(self.cmbHeatConduction))
        
        # Coefficent form PDE
        self.cmbDiffusionCoef = self.findChild(QtWidgets.QComboBox, "cmbDiffusionCoef")

    def currentHeatConduction(self, comb):
        self.inputK = self.findChild(QtWidgets.QLineEdit, "inputK")
        self.inputKD1 = self.findChild(QtWidgets.QLineEdit, "inputKD1")
        self.inputKD2 = self.findChild(QtWidgets.QLineEdit, "inputKD2")
        self.inputKD3 = self.findChild(QtWidgets.QLineEdit, "inputKD3")
        self.inputKD4 = self.findChild(QtWidgets.QLineEdit, "inputKD4")

        if comb.currentIndex() == 0:
            self.inputK.setEnabled(True)

            self.inputKD1.setEnabled(False)
            self.inputKD2.setEnabled(False)
            self.inputKD3.setEnabled(False)
            self.inputKD4.setEnabled(False)
        if comb.currentIndex() == 3:
            self.inputK.setEnabled(False)

            self.inputKD1.setEnabled(True)
            self.inputKD2.setEnabled(True)
            self.inputKD3.setEnabled(True)
            self.inputKD4.setEnabled(True)

    def currentPolygon(self, section, comb):
        section.setItemEnabled(0, False)
        section.setItemEnabled(1, False)
        section.setItemEnabled(2, False)
        section.setItemEnabled(3, False)
        section.setItemEnabled(4, False)
        section.setItemEnabled(comb.currentIndex(), True)
    
    def currentCheckedComboBoxItemConditions(self, section, comb):
        for i in range(comb.count()):
            section.setItemEnabled(i, False)

        if comb.currentIndex() == 2:
            section.setItemEnabled(comb.currentIndex(), True)
            section.setItemEnabled(comb.currentIndex()+1, True)
        elif comb.currentIndex() == 3:
            section.setItemEnabled(comb.currentIndex()+1, True)
        else:
            section.setItemEnabled(comb.currentIndex(), True)


    def CheckCoefficient(self):
        CoefficientArray = arr.array('i', [0])
        CoefficientArray = []
        self.chkDiffusionCoefficient = self.findChild(QtWidgets.QCheckBox, "chkDiffusionCoefficient")
        self.chkAbsorptionCoefficient = self.findChild(QtWidgets.QCheckBox, "chkAbsorptionCoefficient")
        self.chkSourceTerm = self.findChild(QtWidgets.QCheckBox, "chkSourceTerm")
        self.chkMassCoefficient = self.findChild(QtWidgets.QCheckBox, "chkMassCoefficient")
        self.chkDampCoefficient = self.findChild(QtWidgets.QCheckBox, "chkDampCoefficient")
        self.chkConservativeConvection = self.findChild(QtWidgets.QCheckBox, "chkConservativeConvection")
        self.chkConvectionCoefficient = self.findChild(QtWidgets.QCheckBox, "chkConvectionCoefficient")
        self.chkConservativeFluxSource = self.findChild(QtWidgets.QCheckBox, "chkConservativeFluxSource")



        if self.chkDiffusionCoefficient.isChecked() == True:
            CoefficientArray.append(1)
        if self.chkAbsorptionCoefficient.isChecked() == True:
            CoefficientArray.append(2)
        if self.chkSourceTerm.isChecked() == True:
            CoefficientArray.append(3)
        if self.chkMassCoefficient.isChecked() == True:
            CoefficientArray.append(4)
        if self.chkDampCoefficient.isChecked() == True:
            CoefficientArray.append(5)
        if self.chkConservativeConvection.isChecked() == True:
            CoefficientArray.append(6)
        if self.chkConvectionCoefficient.isChecked() == True:
            CoefficientArray.append(7)
        if self.chkConservativeFluxSource.isChecked() == True:
            CoefficientArray.append(8)

        return CoefficientArray


    def currentCoefficientForM(self, section, check):
        section.setItemEnabled(1, False)
        section.setItemEnabled(2, False)
        section.setItemEnabled(3, False)
        section.setItemEnabled(4, False)
        section.setItemEnabled(5, False)
        section.setItemEnabled(6, False)
        section.setItemEnabled(7, False)
        section.setItemEnabled(8, False)

        for i in check:
            section.setItemEnabled(i, True)

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
