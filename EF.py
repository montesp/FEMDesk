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
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QLabel, QCheckBox, QToolBox, QComboBox, QWidget
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
        self.figuresSection = self.findChild(QToolBox, "figuresSection")
        self.figuresSection.setItemEnabled(0, True)
        self.figuresSection.setItemEnabled(1, False)
        self.figuresSection.setItemEnabled(2, False)
        self.figuresSection.setItemEnabled(3, False)
        self.figuresSection.setItemEnabled(4, False)

        self.cmbGeometricFigure = self.findChild(QComboBox, "cmbGeometricFigure")
        self.cmbGeometricFigure.currentIndexChanged.connect(lambda: Geometry.currentCheckedComboBoxItem(self.figuresSection, self.cmbGeometricFigure))

        # Conditions PDE
        self.chkDiffusionCoefficient = self.findChild(QCheckBox, "chkDiffusionCoefficient")
        self.chkAbsorptionCoefficient = self.findChild(QCheckBox, "chkAbsorptionCoefficient")
        self.chkSourceTerm = self.findChild(QCheckBox, "chkSourceTerm")
        self.chkMassCoefficient = self.findChild(QCheckBox, "chkMassCoefficient")
        self.chkDampCoefficient = self.findChild(QCheckBox, "chkDampCoefficient")
        self.chkConservativeConvection = self.findChild(QCheckBox, "chkConservativeConvection")
        self.chkConvectionCoefficient = self.findChild(QCheckBox, "chkConvectionCoefficient")
        self.chkConservativeFluxSource = self.findChild(QCheckBox, "chkConservativeFluxSource")

        CoefficientCheckBoxArray = []
        CoefficientCheckBoxArray.append(self.chkDiffusionCoefficient)
        CoefficientCheckBoxArray.append(self.chkAbsorptionCoefficient)
        CoefficientCheckBoxArray.append(self.chkSourceTerm)
        CoefficientCheckBoxArray.append(self.chkMassCoefficient)
        CoefficientCheckBoxArray.append(self.chkDampCoefficient)
        CoefficientCheckBoxArray.append(self.chkConservativeConvection)
        CoefficientCheckBoxArray.append(self.chkConvectionCoefficient)
        CoefficientCheckBoxArray.append(self.chkConservativeFluxSource)

        # Coefficient

        self.toolBoxTypeOfCon = self.findChild(QToolBox, "toolBoxTypeOfCon")
        self.toolBoxTypeOfCon.setItemEnabled(0, True)
        self.toolBoxTypeOfCon.setItemEnabled(1, False)
        self.toolBoxTypeOfCon.setItemEnabled(2, False)
        self.toolBoxTypeOfCon.setItemEnabled(3, False)
        self.toolBoxTypeOfCon.setItemEnabled(4, False)


        self.cmbTypeConditionPDE = self.findChild(QComboBox, "cmbTypeConditionPDE")
        self.cmbTypeConditionPDE.currentIndexChanged.connect(lambda: ConditionsPDE.currentCheckedComboBoxItemConditions(self.toolBoxTypeOfCon, self.cmbTypeConditionPDE))


        #CheckBox Coefficients Form PDE
        self.coefficientsforM = self.findChild(QToolBox, "CoefficentForM")
        self.coefficientsforM.setItemEnabled(1, False)
        self.coefficientsforM.setItemEnabled(2, False)
        self.coefficientsforM.setItemEnabled(3, False)
        self.coefficientsforM.setItemEnabled(4, False)
        self.coefficientsforM.setItemEnabled(5, False)
        self.coefficientsforM.setItemEnabled(6, False)
        self.coefficientsforM.setItemEnabled(7, False)
        self.coefficientsforM.setItemEnabled(8, False)


        self.btnCoefficientsApply = self.findChild(QPushButton, "btnCoefficientsApply")
        self.btnCoefficientsApply.clicked.connect(lambda: CoefficientsPDE.currentCoefficientForM(self.coefficientsforM, CoefficientsPDE.CheckCoefficient(CoefficientCheckBoxArray)))

        #ComboBox HeatConduction
        self.inputK = self.findChild(QLineEdit, "inputK")
        self.inputKD1 = self.findChild(QLineEdit, "inputKD1")
        self.inputKD2 = self.findChild(QLineEdit, "inputKD2")
        self.inputKD3 = self.findChild(QLineEdit, "inputKD3")
        self.inputKD4 = self.findChild(QLineEdit, "inputKD4")

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

        self.cmbHeatConduction = self.findChild(QComboBox, "cmbHeatConduction")
        self.cmbHeatConduction.currentIndexChanged.connect(lambda: Materials.currentHeatConduction(self.cmbHeatConduction, inputKArray))

        #Combobox TypeCondiction
        self.tboxTypeCondition = self.findChild(QWidget, "toolBoxTypeOfCondition")
        self.tboxTypeCondition.setItemEnabled(0, False)
        self.tboxTypeCondition.setItemEnabled(1, False)

        self.tboxTypeCondition.widget(0).hide()
        self.tboxTypeCondition.widget(1).hide()

        self.cmbtypecondition = self.findChild(QComboBox, "cmbTypeCondition")
        self.cmbtypecondition.currentIndexChanged.connect(lambda: Conditions.currentTypeCondition(self.cmbtypecondition, self.tboxTypeCondition))



        # Coefficent form PDE

        # Diffusion Coeficient
        self.diffusionCoefData = []
        self.lEditDiffusionCoef11 = self.findChild(QLineEdit, "lEditDiffusionCoef11")
        self.lEditDiffusionCoef12 = self.findChild(QLineEdit, "lEditDiffusionCoef12")
        self.lEditDiffusionCoef13 = self.findChild(QLineEdit, "lEditDiffusionCoef13")
        self.lEditDiffusionCoef21 = self.findChild(QLineEdit, "lEditDiffusionCoef21")
        self.lEditDiffusionCoef22 = self.findChild(QLineEdit, "lEditDiffusionCoef22")
        self.lEditDiffusionCoef23 = self.findChild(QLineEdit, "lEditDiffusionCoef23")
        self.lEditDiffusionCoef31 = self.findChild(QLineEdit, "lEditDiffusionCoef31")
        self.lEditDiffusionCoef32 = self.findChild(QLineEdit, "lEditDiffusionCoef32")
        self.lEditDiffusionCoef33 = self.findChild(QLineEdit, "lEditDiffusionCoef33")

        self.diffusionCoefData.append(self.lEditDiffusionCoef12)
        self.diffusionCoefData.append(self.lEditDiffusionCoef13)
        self.diffusionCoefData.append(self.lEditDiffusionCoef21)
        self.diffusionCoefData.append(self.lEditDiffusionCoef22)
        self.diffusionCoefData.append(self.lEditDiffusionCoef23)
        self.diffusionCoefData.append(self.lEditDiffusionCoef31)
        self.diffusionCoefData.append(self.lEditDiffusionCoef32)
        self.diffusionCoefData.append(self.lEditDiffusionCoef33)

        self.desabledLEdit(self.diffusionCoefData)

        self.cmbRowDiffusionCoef = self.findChild(QComboBox, "cmbRowDiffusionCoef")
        self.cmbColumnDiffusionCoef = self.findChild(QComboBox, "cmbColumnDiffusionCoef")
        self.cmbRowDiffusionCoef.currentIndexChanged.connect(lambda: ConditionsPDE.currentRowDiffusionCoef(self.cmbRowDiffusionCoef.currentIndex(), self.cmbColumnDiffusionCoef.currentIndex(), self.diffusionCoefData))
        self.cmbColumnDiffusionCoef.currentIndexChanged.connect(lambda: ConditionsPDE.currentRowDiffusionCoef(self.cmbRowDiffusionCoef.currentIndex(), self.cmbColumnDiffusionCoef.currentIndex(), self.diffusionCoefData))

        # Absorption Coeficient 
        self.lEditAbsorData = []
        self.lEditAbsorCoef11 = self.findChild(QLineEdit, "lEditAbsorCoef11")
        self.lEditAbsorCoef12 = self.findChild(QLineEdit, "lEditAbsorCoef12")
        self.lEditAbsorCoef13 = self.findChild(QLineEdit, "lEditAbsorCoef13")
        self.lEditAbsorCoef21 = self.findChild(QLineEdit, "lEditAbsorCoef21")
        self.lEditAbsorCoef22 = self.findChild(QLineEdit, "lEditAbsorCoef22")
        self.lEditAbsorCoef23 = self.findChild(QLineEdit, "lEditAbsorCoef23")
        self.lEditAbsorCoef31 = self.findChild(QLineEdit, "lEditAbsorCoef31")
        self.lEditAbsorCoef32 = self.findChild(QLineEdit, "lEditAbsorCoef32")
        self.lEditAbsorCoef33 = self.findChild(QLineEdit, "lEditAbsorCoef33")

        self.lEditAbsorData.append(self.lEditAbsorCoef12)
        self.lEditAbsorData.append(self.lEditAbsorCoef13)
        self.lEditAbsorData.append(self.lEditAbsorCoef21)
        self.lEditAbsorData.append(self.lEditAbsorCoef22)
        self.lEditAbsorData.append(self.lEditAbsorCoef23)
        self.lEditAbsorData.append(self.lEditAbsorCoef31)
        self.lEditAbsorData.append(self.lEditAbsorCoef32)
        self.lEditAbsorData.append(self.lEditAbsorCoef33)

        self.desabledLEdit(self.lEditAbsorData)

        self.cmbAbsorptionRow = self.findChild(QComboBox, "cmbAbsorptionRow")
        self.cmbAbsorptionColumn = self.findChild(QComboBox, "cmbAbsorptionColumn")
        self.cmbAbsorptionRow.currentIndexChanged.connect(lambda: ConditionsPDE.currentRowDiffusionCoef(self.cmbAbsorptionRow.currentIndex(), self.cmbAbsorptionColumn.currentIndex(), self.lEditAbsorData))
        self.cmbAbsorptionColumn.currentIndexChanged.connect(lambda: ConditionsPDE.currentRowDiffusionCoef(self.cmbAbsorptionRow.currentIndex(), self.cmbAbsorptionColumn.currentIndex(), self.lEditAbsorData))

        # Source term
        self.lEditSourceData = []
        self.lEditSourceTerm11 = self.findChild(QLineEdit, "lEditSourceTerm11")
        self.lEditSourceTerm12 = self.findChild(QLineEdit, "lEditSourceTerm12")
        self.lEditSourceTerm13 = self.findChild(QLineEdit, "lEditSourceTerm13")


        self.lEditSourceData.append(self.lEditSourceTerm12)
        self.lEditSourceData.append(self.lEditSourceTerm13)
        self.desabledLEdit(self.lEditSourceData)

        self.cmbSourceRow = self.findChild(QComboBox, "cmbSourceRow")
        self.cmbSourceRow.currentIndexChanged.connect(lambda: ConditionsPDE.currentRowEdit(self.cmbSourceRow.currentIndex(), self.lEditSourceData))

        #Mass Coefficent
        self.lEditMassCoefData = []
        self.lEditMassCoef11 = self.findChild(QLineEdit, "lEditMassCoef11")
        self.lEditMassCoef12 = self.findChild(QLineEdit, "lEditMassCoef12")
        self.lEditMassCoef13 = self.findChild(QLineEdit, "lEditMassCoef13")
        self.lEditMassCoef21 = self.findChild(QLineEdit, "lEditMassCoef21")
        self.lEditMassCoef22 = self.findChild(QLineEdit, "lEditMassCoef22")
        self.lEditMassCoef23 = self.findChild(QLineEdit, "lEditMassCoef23")
        self.lEditMassCoef31 = self.findChild(QLineEdit, "lEditMassCoef31")
        self.lEditMassCoef32 = self.findChild(QLineEdit, "lEditMassCoef32")
        self.lEditMassCoef33 = self.findChild(QLineEdit, "lEditMassCoef33")

        self.lEditMassCoefData.append(self.lEditMassCoef12)
        self.lEditMassCoefData.append(self.lEditMassCoef13)
        self.lEditMassCoefData.append(self.lEditMassCoef21)
        self.lEditMassCoefData.append(self.lEditMassCoef22)
        self.lEditMassCoefData.append(self.lEditMassCoef23)
        self.lEditMassCoefData.append(self.lEditMassCoef31)
        self.lEditMassCoefData.append(self.lEditMassCoef32)
        self.lEditMassCoefData.append(self.lEditMassCoef33)

        self.desabledLEdit(self.lEditMassCoefData)

        self.cmbMassCoefRow = self.findChild(QComboBox, "cmbMassCoefRow")
        self.cmbMassCoefColumn = self.findChild(QComboBox, "cmbMassCoefColumn")
        self.cmbMassCoefRow.currentIndexChanged.connect(lambda: ConditionsPDE.currentRowDiffusionCoef(self.cmbMassCoefRow.currentIndex(),self.cmbMassCoefColumn.currentIndex(), self.lEditMassCoefData))
        self.cmbMassCoefColumn.currentIndexChanged.connect(lambda: ConditionsPDE.currentRowDiffusionCoef(self.cmbMassCoefRow.currentIndex(),self.cmbMassCoefColumn.currentIndex() ,self.lEditMassCoefData))

        # Damping or mass coeficient
        self.lEditDamMassCoefData = []
        self.lEditDamMassCoef11 = self.findChild(QLineEdit, "lEditDamMassCoef11")
        self.lEditDamMassCoef12 = self.findChild(QLineEdit, "lEditDamMassCoef12")
        self.lEditDamMassCoef13 = self.findChild(QLineEdit, "lEditDamMassCoef13")
        self.lEditDamMassCoef21 = self.findChild(QLineEdit, "lEditDamMassCoef21")
        self.lEditDamMassCoef22 = self.findChild(QLineEdit, "lEditDamMassCoef22")
        self.lEditDamMassCoef23 = self.findChild(QLineEdit, "lEditDamMassCoef23")
        self.lEditDamMassCoef31 = self.findChild(QLineEdit, "lEditDamMassCoef31")
        self.lEditDamMassCoef32 = self.findChild(QLineEdit, "lEditDamMassCoef32")
        self.lEditDamMassCoef33 = self.findChild(QLineEdit, "lEditDamMassCoef33")

        self.lEditDamMassCoefData.append( self.lEditDamMassCoef12 )
        self.lEditDamMassCoefData.append( self.lEditDamMassCoef13 )
        self.lEditDamMassCoefData.append( self.lEditDamMassCoef21 )
        self.lEditDamMassCoefData.append( self.lEditDamMassCoef22 )
        self.lEditDamMassCoefData.append( self.lEditDamMassCoef23 )
        self.lEditDamMassCoefData.append( self.lEditDamMassCoef31 )
        self.lEditDamMassCoefData.append( self.lEditDamMassCoef32 )
        self.lEditDamMassCoefData.append( self.lEditDamMassCoef33 )

        self.desabledLEdit( self.lEditDamMassCoefData )

        self.cmbDamMassCoefRow = self.findChild(QComboBox, "cmbDamMassCoefRow")
        self.cmbDamMassCoefColumn = self.findChild(QComboBox, "cmbDamMassCoefColumn")
        self.cmbDamMassCoefRow.currentIndexChanged.connect(lambda: ConditionsPDE.currentRowDiffusionCoef(self.cmbDamMassCoefRow.currentIndex(),self.cmbDamMassCoefColumn.currentIndex(), self.lEditDamMassCoefData))
        self.cmbDamMassCoefColumn.currentIndexChanged.connect(lambda: ConditionsPDE.currentRowDiffusionCoef(self.cmbDamMassCoefRow.currentIndex(),self.cmbDamMassCoefColumn.currentIndex(), self.lEditDamMassCoefData))

        # Consevative Flux convection coefficent
        self.lEditAlphaXCFluxData = []
        self.lEditAlphaCYFluxData = []
        self.lEditAlphaXCFlux11 = self.findChild(QLineEdit, "lEditAlphaXCFlux11")
        self.lEditAlphaCYFlux11 = self.findChild(QLineEdit, "lEditAlphaCYFlux11")
        self.lEditAlphaXCFlux12 = self.findChild(QLineEdit, "lEditAlphaXCFlux12")
        self.lEditAlphaCYFlux12 = self.findChild(QLineEdit, "lEditAlphaCYFlux12")
        self.lEditAlphaXCFlux13 = self.findChild(QLineEdit, "lEditAlphaXCFlux13")
        self.lEditAlphaCYFlux13 = self.findChild(QLineEdit, "lEditAlphaCYFlux13")
        self.lEditAlphaXCFlux21 = self.findChild(QLineEdit, "lEditAlphaXCFlux21")
        self.lEditAlphaCYFlux21 = self.findChild(QLineEdit, "lEditAlphaCYFlux21")
        self.lEditAlphaXCFlux22 = self.findChild(QLineEdit, "lEditAlphaXCFlux22")
        self.lEditAlphaCYFlux22 = self.findChild(QLineEdit, "lEditAlphaCYFlux22")
        self.lEditAlphaXCFlux23 = self.findChild(QLineEdit, "lEditAlphaXCFlux23")
        self.lEditAlphaCYFlux23 = self.findChild(QLineEdit, "lEditAlphaCYFlux23")
        self.lEditAlphaXCFlux31 = self.findChild(QLineEdit, "lEditAlphaXCFlux31")
        self.lEditAlphaCYFlux31 = self.findChild(QLineEdit, "lEditAlphaCYFlux31")
        self.lEditAlphaXCFlux32 = self.findChild(QLineEdit, "lEditAlphaXCFlux32")
        self.lEditAlphaCYFlux32 = self.findChild(QLineEdit, "lEditAlphaCYFlux32")
        self.lEditAlphaXCFlux33 = self.findChild(QLineEdit, "lEditAlphaXCFlux33")
        self.lEditAlphaCYFlux33 = self.findChild(QLineEdit, "lEditAlphaCYFlux33")

        # Agregar en la lista el alpha X
        self.lEditAlphaXCFluxData.append( self.lEditAlphaXCFlux12 )
        self.lEditAlphaXCFluxData.append( self.lEditAlphaXCFlux13 )
        self.lEditAlphaXCFluxData.append( self.lEditAlphaXCFlux21 )
        self.lEditAlphaXCFluxData.append( self.lEditAlphaXCFlux22 )
        self.lEditAlphaXCFluxData.append( self.lEditAlphaXCFlux23 )
        self.lEditAlphaXCFluxData.append( self.lEditAlphaXCFlux31 )
        self.lEditAlphaXCFluxData.append( self.lEditAlphaXCFlux32 )
        self.lEditAlphaXCFluxData.append( self.lEditAlphaXCFlux33 )

        # Agregar en la lista el alpha y
        self.lEditAlphaCYFluxData.append( self.lEditAlphaCYFlux12 )
        self.lEditAlphaCYFluxData.append( self.lEditAlphaCYFlux13 )
        self.lEditAlphaCYFluxData.append( self.lEditAlphaCYFlux21 )
        self.lEditAlphaCYFluxData.append( self.lEditAlphaCYFlux22 )
        self.lEditAlphaCYFluxData.append( self.lEditAlphaCYFlux23 )
        self.lEditAlphaCYFluxData.append( self.lEditAlphaCYFlux31 )
        self.lEditAlphaCYFluxData.append( self.lEditAlphaCYFlux32 )
        self.lEditAlphaCYFluxData.append( self.lEditAlphaCYFlux33 )

        self.cmbCFluxRow = self.findChild(QComboBox, "cmbCFluxRow")
        self.cmbCFluxColumn = self.findChild(QComboBox, "cmbCFluxColumn")
        self.cmbCFluxColumn.currentIndexChanged.connect(lambda: ConditionsPDE.activateIndexAlpha(self.lEditAlphaXCFluxData, self.lEditAlphaCYFluxData, self.cmbCFluxRow.currentIndex(), self.cmbCFluxColumn.currentIndex()))
        self.cmbCFluxRow.currentIndexChanged.connect(lambda: ConditionsPDE.activateIndexAlpha(self.lEditAlphaXCFluxData, self.lEditAlphaCYFluxData, self.cmbCFluxRow.currentIndex(), self.cmbCFluxColumn.currentIndex()))

        # Convection Coefficent
        # Conservative Flux Source


    def desabledLEdit(self, edit):
        for i in edit:
            i.setEnabled(False)

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
