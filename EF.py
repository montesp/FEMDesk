#-*- coding: utf-8 -*-
"""
Created on Wed May 11 13:39:55 2022

@author: ruben.castaneda
"""

#-*- coding: utf-8 -*-
"""
Created on Tue May 10 14:30:09 2022

@author: ruben.castaneda
"""

import os, sys
import imagen_rc
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


        # Combo box Geometric Figure
        self.figuresSection = self.findChild(QtWidgets.QToolBox, "figuresSection")
        self.figuresSection.setItemEnabled(0, True)
        self.figuresSection.setItemEnabled(1, False)
        self.figuresSection.setItemEnabled(2, False)
        self.figuresSection.setItemEnabled(3, False)
        self.figuresSection.setItemEnabled(4, False)

        self.cmbGeometricFigure = self.findChild(QtWidgets.QComboBox, "cmbGeometricFigure")
        self.cmbGeometricFigure.currentIndexChanged.connect(lambda: self.currentPolygon(self.figuresSection, self.cmbGeometricFigure))

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
        

    def currentPolygon(self, section, comb):
        section.setItemEnabled(0, False)
        section.setItemEnabled(1, False)
        section.setItemEnabled(2, False)
        section.setItemEnabled(3, False)
        section.setItemEnabled(4, False)
        section.setItemEnabled(comb.currentIndex(), True)

    def CheckCoefficient(self):
        self.chkDiffusionCoefficient = self.findChild(QtWidgets.QCheckBox, "chkDiffusionCoefficient")
        self.chkAbsorptionCoefficient = self.findChild(QtWidgets.QCheckBox, "chkAbsorptionCoefficient")
        self.chkSourceTerm = self.findChild(QtWidgets.QCheckBox, "chkSourceTerm")
        self.chkMassCoefficient = self.findChild(QtWidgets.QCheckBox, "chkMassCoefficient")
        self.chkDampCoefficient = self.findChild(QtWidgets.QCheckBox, "chkDampCoefficient")
        self.chkConservativeConvection = self.findChild(QtWidgets.QCheckBox, "chkConservativeConvection")
        self.chkConvectionCoefficient = self.findChild(QtWidgets.QCheckBox, "chkConvectionCoefficient")
        self.chkConservativeFluxSource = self.findChild(QtWidgets.QCheckBox, "chkConservativeFluxSource")

        if self.chkDiffusionCoefficient.isChecked() == True:
            return 1
        if self.chkAbsorptionCoefficient.isChecked() == True:
            return 2
        if self.chkSourceTerm.isChecked() == True:
            return 3
        if self.chkMassCoefficient.isChecked() == True:
            return 4
        if self.chkDampCoefficient.isChecked() == True:
            return 5
        if self.chkConservativeConvection.isChecked() == True:
            return 6
        if self.chkConvectionCoefficient.isChecked() == True:
            return 7
        if self.chkConservativeFluxSource.isChecked() == True:
            return 8


    def currentCoefficientForM(self, section, check):
        section.setItemEnabled(check, True)




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
