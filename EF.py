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
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QGraphicsView, QButtonGroup, QTreeWidget ,QMessageBox, QPushButton, QLineEdit, QLabel, QCheckBox, QToolBox, QComboBox, QWidget
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtWidgets
from Base import *
from interfaz import *
from Modules.Materials import *
from Modules.Geometry import *
from Modules.Conditions import *
from Modules.ConditionsPDE import *
from Modules.CoefficientsPDE import *
from Modules.ModelWizard import *

app = None
class PropertiesData:
    kappa=[]
    rho=[]
    Cp=[]
    def __init__(self):
        self.kappa = [[-1.0,-1.0],[-1.0,-1.0]]
        self.rho = -1.0
        self.Cp = -1.0

class EditorWindow(QMainWindow):
    DataProperties = []
    materialsDataBase = []
    conn = []
    statusLibrary = 0 #0 initial value, 1 new material, 2 copyas, 3 changes values

    def __init__(self):
        super(QMainWindow, self).__init__()
        self.app = app
        with open('styles.qss', 'r', encoding='utf-8') as file:
            str = file.read()
        self.setStyleSheet(str)
        root = os.path.dirname(os.path.realpath(__file__))
        loadUi(os.path.join(root, 'Interfaz.ui'), self)

        # -------------------------------------------------------------------------
        # DataBase
        self.conn = materials()
        self.materialsDataBase = select_all_materials(self.conn)
        self.DataProperties = PropertiesData()
        self.btnNewMaterial.clicked.connect(self.click_btnNewMaterial)
        self.btnSaveMaterial.clicked.connect(self.click_btnSaveMaterial)
        self.btnResetLibrary.clicked.connect(self.click_btnResetLibrary)
        self.btnSaveAsMaterial.clicked.connect(self.click_btnSaveAsMaterial)
        self.btnOpenMaterial.clicked.connect(self.click_btnOpenMaterial)
        self.btnDeleteMaterial.clicked.connect(self.click_btnDeleteMaterial)

        self.cmbTypeHeatConductionSolid.currentIndexChanged.connect(self.change_cmbTypeHeatConductionSolid)
        self.cmbNameMaterials.currentIndexChanged.connect(self.change_cmbNameMaterials)
        self.edtTermalConductivityIsotropicProperties.editingFinished.connect(self.exit_edtTermalConductivityIsotropicProperties)
        self.edtTermalConductivityAnisotropicPropertiesA11.editingFinished.connect(self.exit_edtTermalConductivityAnisotropicPropertiesA11)
        self.edtTermalConductivityAnisotropicPropertiesA12.editingFinished.connect(self.exit_edtTermalConductivityAnisotropicPropertiesA12)
        self.edtTermalConductivityAnisotropicPropertiesA21.editingFinished.connect(self.exit_edtTermalConductivityAnisotropicPropertiesA21)
        self.edtTermalConductivityAnisotropicPropertiesA22.editingFinished.connect(self.exit_edtTermalConductivityAnisotropicPropertiesA22)
        self.edtRhoProperties.editingFinished.connect(self.exit_edtRhoProperties)
        self.edtCpProperties.editingFinished.connect(self.exit_edtCpProperties)
        self.addMaterials()

        # -------------------------------------------------------------------------
        # MENU TABS

        self.tabs = []
        self.tabs.append(self.modelWizardTab)           # 0
        self.tabs.append(self.materialsTab)             # 1
        self.tabs.append(self.geometryTab)              # 2
        self.tabs.append(self.conditionsTab)            # 3
        self.tabs.append(self.meshAndSettingStudyTab)   # 4
        self.tabs.append(self.conditionsPDETab)         # 5
        self.tabs.append(self.CoefficentFormPDETab)     # 6
        self.tabs.append(self.libraryTab)               # 7

        # -------------------------------------------------------------------------
        # MODEL WIZARD
        # tabWidgetMenu
        # ModelWizard.hideElementTab(self.tabWidgetMenu.currentIndex(), self.tabs, self.tabWidgetMenu )
        # Heat transfer
        # self.tabWidgetMenu.currentChanged.connect(lambda: ModelWizard.hideElementTab(self.tabWidgetMenu.currentIndex(), self.tabWidgetMenu ))
        # # Heat transfer
        # # Agrega las tabs que fueron borradas
        # self.treeModelWizard.currentItemChanged.connect(lambda: ModelWizard.addTabElement(self.treeModelWizard.currentItem(), self.treeModelWizard.currentColumn() , self.tabs, self.tabWidgetMenu ))
        
        self.treeModelWizard.currentItemChanged.connect(lambda: ModelWizard.currentTreeItem(self.treeModelWizard.currentItem(), self.treeModelWizard.currentColumn(), 1 , self.tabs, self.tabWidgetMenu ))

        # -------------------------------------------------------------------------
        # GEOMETRIC FIGURE
        # Combo box
        self.figuresSection = self.findChild(QToolBox, "figuresSection")
        self.figuresSection.setItemEnabled(0, True)
        self.figuresSection.setItemEnabled(1, False)
        self.figuresSection.setItemEnabled(2, False)
        self.figuresSection.setItemEnabled(3, False)
        self.figuresSection.setItemEnabled(4, False)

        self.cmbGeometricFigure = self.findChild(QComboBox, "cmbGeometricFigure")
        self.cmbGeometricFigure.currentIndexChanged.connect(lambda: Geometry.currentCheckedComboBoxItem(self.figuresSection, self.cmbGeometricFigure))

        # -------------------------------------------------------------------------
        # CONDITIONS PDE
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

        # -------------------------------------------------------------------------
        # COEFFICENT FORM PDE
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


        # -------------------------------------------------------------------------
        # COEFFICENT FORM PDE
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

        self.diffusionCoefData.append(self.lEditDiffusionCoef11)
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

        self.lEditAbsorData.append(self.lEditAbsorCoef11)
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

        self.lEditSourceData.append(self.lEditSourceTerm11)
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

        self.lEditMassCoefData.append(self.lEditMassCoef11)
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

        self.lEditDamMassCoefData.append( self.lEditDamMassCoef11 )
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
        self.lEditAlphaXCFluxData.append( self.lEditAlphaXCFlux11 )
        self.lEditAlphaXCFluxData.append( self.lEditAlphaXCFlux12 )
        self.lEditAlphaXCFluxData.append( self.lEditAlphaXCFlux13 )
        self.lEditAlphaXCFluxData.append( self.lEditAlphaXCFlux21 )
        self.lEditAlphaXCFluxData.append( self.lEditAlphaXCFlux22 )
        self.lEditAlphaXCFluxData.append( self.lEditAlphaXCFlux23 )
        self.lEditAlphaXCFluxData.append( self.lEditAlphaXCFlux31 )
        self.lEditAlphaXCFluxData.append( self.lEditAlphaXCFlux32 )
        self.lEditAlphaXCFluxData.append( self.lEditAlphaXCFlux33 )
        self.desabledLEdit(self.lEditAlphaXCFluxData)

        # Agregar en la lista el alpha y
        self.lEditAlphaCYFluxData.append( self.lEditAlphaCYFlux11 )
        self.lEditAlphaCYFluxData.append( self.lEditAlphaCYFlux12 )
        self.lEditAlphaCYFluxData.append( self.lEditAlphaCYFlux13 )
        self.lEditAlphaCYFluxData.append( self.lEditAlphaCYFlux21 )
        self.lEditAlphaCYFluxData.append( self.lEditAlphaCYFlux22 )
        self.lEditAlphaCYFluxData.append( self.lEditAlphaCYFlux23 )
        self.lEditAlphaCYFluxData.append( self.lEditAlphaCYFlux31 )
        self.lEditAlphaCYFluxData.append( self.lEditAlphaCYFlux32 )
        self.lEditAlphaCYFluxData.append( self.lEditAlphaCYFlux33 )
        self.desabledLEdit(self.lEditAlphaCYFluxData)

        self.cmbCFluxRow = self.findChild(QComboBox, "cmbCFluxRow")
        self.cmbCFluxColumn = self.findChild(QComboBox, "cmbCFluxColumn")
        self.cmbCFluxColumn.currentIndexChanged.connect(lambda: ConditionsPDE.activateIndexAlpha(self.lEditAlphaXCFluxData, self.lEditAlphaCYFluxData, self.cmbCFluxRow.currentIndex(), self.cmbCFluxColumn.currentIndex()))
        self.cmbCFluxRow.currentIndexChanged.connect(lambda: ConditionsPDE.activateIndexAlpha(self.lEditAlphaXCFluxData, self.lEditAlphaCYFluxData, self.cmbCFluxRow.currentIndex(), self.cmbCFluxColumn.currentIndex()))

        # Convection Coefficent
        # Beta X
        self.lEditBetaXConvCoefData = []
        self.lEditBetaXConvCoef11 = self.findChild(QLineEdit, 'lEditBetaXConvCoef11');
        self.lEditBetaXConvCoef12 = self.findChild(QLineEdit, 'lEditBetaXConvCoef12');
        self.lEditBetaXConvCoef13 = self.findChild(QLineEdit, 'lEditBetaXConvCoef13');
        self.lEditBetaXConvCoef21 = self.findChild(QLineEdit, 'lEditBetaXConvCoef21');
        self.lEditBetaXConvCoef22 = self.findChild(QLineEdit, 'lEditBetaXConvCoef22');
        self.lEditBetaXConvCoef23 = self.findChild(QLineEdit, 'lEditBetaXConvCoef23');
        self.lEditBetaXConvCoef31 = self.findChild(QLineEdit, 'lEditBetaXConvCoef31');
        self.lEditBetaXConvCoef32 = self.findChild(QLineEdit, 'lEditBetaXConvCoef32');
        self.lEditBetaXConvCoef33 = self.findChild(QLineEdit, 'lEditBetaXConvCoef33');
        # Llenar beta x
        self.lEditBetaXConvCoefData.append(self.lEditBetaXConvCoef11)
        self.lEditBetaXConvCoefData.append(self.lEditBetaXConvCoef12)
        self.lEditBetaXConvCoefData.append(self.lEditBetaXConvCoef13)
        self.lEditBetaXConvCoefData.append(self.lEditBetaXConvCoef21)
        self.lEditBetaXConvCoefData.append(self.lEditBetaXConvCoef22)
        self.lEditBetaXConvCoefData.append(self.lEditBetaXConvCoef23)
        self.lEditBetaXConvCoefData.append(self.lEditBetaXConvCoef31)
        self.lEditBetaXConvCoefData.append(self.lEditBetaXConvCoef32)
        self.lEditBetaXConvCoefData.append(self.lEditBetaXConvCoef33)
        self.desabledLEdit(self.lEditBetaXConvCoefData)
        
        # Beta Y
        self.lEditBetaYConvCoefData = []
        self.lEditBetaYConvCoef11 = self.findChild(QLineEdit, 'lEditBetaYConvCoef11');
        self.lEditBetaYConvCoef12 = self.findChild(QLineEdit, 'lEditBetaYConvCoef12');
        self.lEditBetaYConvCoef13 = self.findChild(QLineEdit, 'lEditBetaYConvCoef13');
        self.lEditBetaYConvCoef21 = self.findChild(QLineEdit, 'lEditBetaYConvCoef21');
        self.lEditBetaYConvCoef22 = self.findChild(QLineEdit, 'lEditBetaYConvCoef22');
        self.lEditBetaYConvCoef23 = self.findChild(QLineEdit, 'lEditBetaYConvCoef23');
        self.lEditBetaYConvCoef31 = self.findChild(QLineEdit, 'lEditBetaYConvCoef31');
        self.lEditBetaYConvCoef32 = self.findChild(QLineEdit, 'lEditBetaYConvCoef32');
        self.lEditBetaYConvCoef33 = self.findChild(QLineEdit, 'lEditBetaYConvCoef33');
        # Llenar data de beta y
        self.lEditBetaYConvCoefData.append(self.lEditBetaYConvCoef11)
        self.lEditBetaYConvCoefData.append(self.lEditBetaYConvCoef12)
        self.lEditBetaYConvCoefData.append(self.lEditBetaYConvCoef13)
        self.lEditBetaYConvCoefData.append(self.lEditBetaYConvCoef21)
        self.lEditBetaYConvCoefData.append(self.lEditBetaYConvCoef22)
        self.lEditBetaYConvCoefData.append(self.lEditBetaYConvCoef23)
        self.lEditBetaYConvCoefData.append(self.lEditBetaYConvCoef31)
        self.lEditBetaYConvCoefData.append(self.lEditBetaYConvCoef32)
        self.lEditBetaYConvCoefData.append(self.lEditBetaYConvCoef33)
        self.desabledLEdit(self.lEditBetaYConvCoefData)

        self.cmbConvectionRow = self.findChild(QComboBox, 'cmbConvectionRow')
        self.cmbConvectionColumn = self.findChild(QComboBox, 'cmbConvectionColumn')

        self.cmbConvectionRow.currentIndexChanged.connect(lambda: ConditionsPDE.activateIndexAlpha(self.lEditBetaXConvCoefData, self.lEditBetaYConvCoefData, self.cmbConvectionRow.currentIndex(), self.cmbConvectionColumn.currentIndex()))
        self.cmbConvectionColumn.currentIndexChanged.connect(lambda: ConditionsPDE.activateIndexAlpha(self.lEditBetaXConvCoefData, self.lEditBetaYConvCoefData, self.cmbConvectionRow.currentIndex(), self.cmbConvectionColumn.currentIndex()))
       
        # Conservative Flux Source
        # Gamma X
        self.lEditGammaXCFluxSourceData = []
        self.lEditGammaXCFluxSource1 = self.findChild(QLineEdit, 'lEditGammaXCFluxSource1')
        self.lEditGammaXCFluxSource2 = self.findChild(QLineEdit, 'lEditGammaXCFluxSource2')
        self.lEditGammaXCFluxSource3 = self.findChild(QLineEdit, 'lEditGammaXCFluxSource3')
        # Llenar array de gamma x
        self.lEditGammaXCFluxSourceData.append(self.lEditGammaXCFluxSource1)
        self.lEditGammaXCFluxSourceData.append(self.lEditGammaXCFluxSource2)
        self.lEditGammaXCFluxSourceData.append(self.lEditGammaXCFluxSource3)
        self.desabledLEdit(self.lEditGammaXCFluxSourceData)


        # Gamma Y
        self.lEditGammaYCFluxSourceData = []
        self.lEditGammaYCFluxSource1 = self.findChild(QLineEdit, 'lEditGammaYCFluxSource1')
        self.lEditGammaYCFluxSource2 = self.findChild(QLineEdit, 'lEditGammaYCFluxSource2')
        self.lEditGammaYCFluxSource3 = self.findChild(QLineEdit, 'lEditGammaYCFluxSource3')
        # Llenar array de gamma Y
        self.lEditGammaYCFluxSourceData.append(self.lEditGammaYCFluxSource1)
        self.lEditGammaYCFluxSourceData.append(self.lEditGammaYCFluxSource2)
        self.lEditGammaYCFluxSourceData.append(self.lEditGammaYCFluxSource3)
        self.desabledLEdit(self.lEditGammaYCFluxSourceData)

        self.cmbCSourceRow = self.findChild(QComboBox, 'cmbCSourceRow')
        self.cmbCSourceRow.currentIndexChanged.connect(lambda: ConditionsPDE.disabledRowEdit( self.lEditGammaXCFluxSourceData,  self.lEditGammaYCFluxSourceData, self.cmbCSourceRow.currentIndex()))

        # -------------------------------------------------------------------------

    def click_btnDeleteMaterial(self) :
        buttonReply = QMessageBox.question(self, 'Important message', "Are you sure you want to delete the material from the database?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if buttonReply == QMessageBox.Yes:
            delete_task(self.conn, self.materialsDataBase[self.cmbNameMaterials.currentIndex()][0])
            self.materialsDataBase = select_all_materials(self.conn)
            self.btnNewMaterial.setEnabled(True)
            self.btnDeleteMaterial.setEnabled(True)
            self.btnSaveMaterial.setEnabled(False)
            self.btnSaveAsMaterial.setEnabled(True)
            self.btnOpenMaterial.setEnabled(True)
            self.btnResetLibrary.setEnabled(False)
            self.btnHelpLibrary.setEnabled(True)
            self.cmbNameMaterials.setEnabled(True)
            self.edtNameMaterial.setEnabled(False)
            self.edtNameMaterial.setText("")
            self.cmbTypeHeatConductionSolid.setEnabled(False)
            self.cmbTypeHeatConductionSolid.setCurrentIndex (0)
            self.edtTermalConductivityIsotropicProperties.setEnabled(False)
            self.edtTermalConductivityIsotropicProperties.setText("")
            self.edtTermalConductivityAnisotropicPropertiesA11.setEnabled(False)
            self.edtTermalConductivityAnisotropicPropertiesA12.setEnabled(False)
            self.edtTermalConductivityAnisotropicPropertiesA21.setEnabled(False)
            self.edtTermalConductivityAnisotropicPropertiesA22.setEnabled(False)
            self.edtTermalConductivityAnisotropicPropertiesA11.setText("")
            self.edtTermalConductivityAnisotropicPropertiesA12.setText("")
            self.edtTermalConductivityAnisotropicPropertiesA21.setText("")
            self.edtTermalConductivityAnisotropicPropertiesA22.setText("")
            self.edtRhoProperties.setEnabled(False)
            self.edtRhoProperties.setText("")
            self.edtCpProperties.setEnabled(False)
            self.edtCpProperties.setText("")
            self.addMaterials()
            QMessageBox.information(self, "Important message", "Material deleted in the database") 
    
    def click_btnOpenMaterial(self):
        self.btnNewMaterial.setEnabled(False)
        self.btnDeleteMaterial.setEnabled(False)
        self.btnSaveMaterial.setEnabled(True)
        self.btnSaveAsMaterial.setEnabled(False)
        self.btnOpenMaterial.setEnabled(False)
        self.btnResetLibrary.setEnabled(True)
        self.btnHelpLibrary.setEnabled(True)
        self.cmbNameMaterials.setEnabled(False)
        self.edtNameMaterial.setEnabled(False)
        self.edtNameMaterial.setText(self.cmbNameMaterials.currentText())
        self.cmbTypeHeatConductionSolid.setEnabled(True)

        if self.cmbTypeHeatConductionSolid.currentIndex() == 0 : #isotropic
            self.edtTermalConductivityIsotropicProperties.setEnabled(True)
            self.edtTermalConductivityAnisotropicPropertiesA11.setEnabled(False)
            self.edtTermalConductivityAnisotropicPropertiesA12.setEnabled(False)
            self.edtTermalConductivityAnisotropicPropertiesA21.setEnabled(False)
            self.edtTermalConductivityAnisotropicPropertiesA22.setEnabled(False)                  
        elif self.cmbTypeHeatConductionSolid.currentIndex() == 1 : #diagonal
            self.edtTermalConductivityIsotropicProperties.setEnabled(False)
            self.edtTermalConductivityAnisotropicPropertiesA11.setEnabled(True)
            self.edtTermalConductivityAnisotropicPropertiesA12.setEnabled(False)
            self.edtTermalConductivityAnisotropicPropertiesA21.setEnabled(False)
            self.edtTermalConductivityAnisotropicPropertiesA22.setEnabled(True)
        elif self.cmbTypeHeatConductionSolid.currentIndex() == 2 : #symmetric
            self.edtTermalConductivityIsotropicProperties.setEnabled(False)
            self.edtTermalConductivityAnisotropicPropertiesA11.setEnabled(True)
            self.edtTermalConductivityAnisotropicPropertiesA12.setEnabled(True)
            self.edtTermalConductivityAnisotropicPropertiesA21.setEnabled(False)
            self.edtTermalConductivityAnisotropicPropertiesA22.setEnabled(True)
        elif self.cmbTypeHeatConductionSolid.currentIndex() == 3 : #full
            self.edtTermalConductivityIsotropicProperties.setEnabled(True)
            self.edtTermalConductivityAnisotropicPropertiesA11.setEnabled(True)
            self.edtTermalConductivityAnisotropicPropertiesA12.setEnabled(True)
            self.edtTermalConductivityAnisotropicPropertiesA21.setEnabled(True)
            self.edtTermalConductivityAnisotropicPropertiesA22.setEnabled(True)
        self.edtCpProperties.setEnabled(True)
        self.edtRhoProperties.setEnabled(True)         
        self.statusLibrary = 3

    def click_btnSaveAsMaterial(self):
        self.btnNewMaterial.setEnabled(False)
        self.btnDeleteMaterial.setEnabled(False)
        self.btnSaveMaterial.setEnabled(True)
        self.btnSaveAsMaterial.setEnabled(False)
        self.btnOpenMaterial.setEnabled(False)
        self.btnResetLibrary.setEnabled(True)
        self.btnHelpLibrary.setEnabled(True)
        self.cmbNameMaterials.setEnabled(False)
        self.edtNameMaterial.setEnabled(True)
        self.edtNameMaterial.setText("Copy"+self.cmbNameMaterials.currentText())
        self.statusLibrary = 2

    def click_btnResetLibrary(self):
        self.btnNewMaterial.setEnabled(True)
        self.btnDeleteMaterial.setEnabled(True)
        self.btnSaveMaterial.setEnabled(False)
        self.btnSaveAsMaterial.setEnabled(True)
        self.btnOpenMaterial.setEnabled(True)
        self.btnResetLibrary.setEnabled(False)
        self.btnHelpLibrary.setEnabled(True)
        self.cmbNameMaterials.setEnabled(True)
        self.edtNameMaterial.setEnabled(False)
        self.edtNameMaterial.setText("")
        self.cmbTypeHeatConductionSolid.setCurrentIndex (0)
        self.edtTermalConductivityIsotropicProperties.setEnabled(False)
        self.edtTermalConductivityIsotropicProperties.setText("")
        self.edtRhoProperties.setEnabled(False)
        self.edtRhoProperties.setText("")
        self.edtCpProperties.setEnabled(False)
        self.edtCpProperties.setText("")
        self.addMaterials()

    def click_btnNewMaterial(self):
        self.cmbNameMaterials.setEnabled(False)
        self.edtNameMaterial.setEnabled(True)
        self.edtNameMaterial.setText("Material_Name")
        self.cmbTypeHeatConductionSolid.setEnabled(True)
        self.cmbTypeHeatConductionSolid.setCurrentIndex (0)
        self.edtTermalConductivityIsotropicProperties.setEnabled(True)
        self.edtTermalConductivityIsotropicProperties.setText("")
        self.edtRhoProperties.setEnabled(True)
        self.edtRhoProperties.setText("")
        self.edtCpProperties.setEnabled(True)
        self.edtCpProperties.setText("")
        self.btnNewMaterial.setEnabled(False)
        self.btnSaveMaterial.setEnabled(True)
        self.btnDeleteMaterial.setEnabled(False)
        self.btnSaveAsMaterial.setEnabled(False)
        self.btnOpenMaterial.setEnabled(False)
        self.btnResetLibrary.setEnabled(True)
        self.kappa = [[-1.0,-1.0],[-1.0,-1.0]]
        self.rho = -1.0
        self.Cp = -1.0
        self.statusLibrary = 1

    def click_btnSaveMaterial(self):
        reviews = [0,0,0] #review each variable before saving
        reName = 0 #review material name

        dato = self.edtNameMaterial.text()
        if not (dato.isspace() or len(dato) == 0):
            mat = select_material(self.conn,dato)
            if len(mat) == 0:
                reName = 1
        
        if self.cmbTypeHeatConductionSolid.currentIndex() == 0 : #isotropic
            if self.DataProperties.kappa[0][0] != -1.0:
                reviews[0] = 1       
        elif self.cmbTypeHeatConductionSolid.currentIndex() == 1 : #diagonal
            if self.DataProperties.kappa[0][0] != -1.0 and self.DataProperties.kappa[1][1] != -1.0 :   
                reviews[0] = 1
        elif self.cmbTypeHeatConductionSolid.currentIndex() == 2 : #symmetric
            if self.DataProperties.kappa[0][0] != -1.0 and self.DataProperties.kappa[0][1] != -1.0 and self.DataProperties.kappa[1][0] != -1.0 and self.DataProperties.kappa[1][1] != -1.0:    
                reviews[0] = 1
        elif self.cmbTypeHeatConductionSolid.currentIndex() == 3 : #full
            if self.DataProperties.kappa[0][0] != -1.0 and self.DataProperties.kappa[0][1] != -1.0 and self.DataProperties.kappa[1][0] != -1.0 and self.DataProperties.kappa[1][1] != -1.0:    
                reviews[0] = 1

        if self.DataProperties.rho != -1.0:
            reviews[1] = 1 

        if self.DataProperties.Cp != -1.0:
            reviews[2] = 1 

        if self.statusLibrary == 1 :
            if sum(reviews) == 3 and reName == 1:
                material = (self.edtNameMaterial.text(),self.DataProperties.kappa[0][0],self.DataProperties.kappa[0][1],self.DataProperties.kappa[1][0],self.DataProperties.kappa[1][1],self.DataProperties.Cp,self.DataProperties.rho,self.cmbTypeHeatConductionSolid.currentIndex())
                add_material(self.conn, material)
                self.materialsDataBase = select_all_materials(self.conn)
                self.btnNewMaterial.setEnabled(True)
                self.btnDeleteMaterial.setEnabled(True)
                self.btnSaveMaterial.setEnabled(False)
                self.btnSaveAsMaterial.setEnabled(True)
                self.btnOpenMaterial.setEnabled(True)
                self.btnResetLibrary.setEnabled(False)
                self.btnHelpLibrary.setEnabled(True)
                self.cmbNameMaterials.setEnabled(True)
                self.edtNameMaterial.setEnabled(False)
                self.edtNameMaterial.setText("")
                self.cmbTypeHeatConductionSolid.setEnabled(False)
                self.cmbTypeHeatConductionSolid.setCurrentIndex (0)
                self.edtTermalConductivityIsotropicProperties.setEnabled(False)
                self.edtTermalConductivityIsotropicProperties.setText("")
                self.edtTermalConductivityAnisotropicPropertiesA11.setEnabled(False)
                self.edtTermalConductivityAnisotropicPropertiesA12.setEnabled(False)
                self.edtTermalConductivityAnisotropicPropertiesA21.setEnabled(False)
                self.edtTermalConductivityAnisotropicPropertiesA22.setEnabled(False)
                self.edtTermalConductivityAnisotropicPropertiesA11.setText("")
                self.edtTermalConductivityAnisotropicPropertiesA12.setText("")
                self.edtTermalConductivityAnisotropicPropertiesA21.setText("")
                self.edtTermalConductivityAnisotropicPropertiesA22.setText("")
                self.edtRhoProperties.setEnabled(False)
                self.edtRhoProperties.setText("")
                self.edtCpProperties.setEnabled(False)
                self.edtCpProperties.setText("")
                self.addMaterials()
                QMessageBox.information(self, "Important message", "Material registered in the database")               
            else:
                QMessageBox.critical(self, "Important message", "Null values ​​exist, please check")
        elif self.statusLibrary == 2:
            if reName == 1:
                material = (self.edtNameMaterial.text(),self.DataProperties.kappa[0][0],self.DataProperties.kappa[0][1],self.DataProperties.kappa[1][0],self.DataProperties.kappa[1][1],self.DataProperties.Cp,self.DataProperties.rho,self.cmbTypeHeatConductionSolid.currentIndex())
                add_material(self.conn, material)
                self.materialsDataBase = select_all_materials(self.conn)
                self.btnNewMaterial.setEnabled(True)
                self.btnDeleteMaterial.setEnabled(True)
                self.btnSaveMaterial.setEnabled(False)
                self.btnSaveAsMaterial.setEnabled(True)
                self.btnOpenMaterial.setEnabled(True)
                self.btnResetLibrary.setEnabled(False)
                self.btnHelpLibrary.setEnabled(True)
                self.cmbNameMaterials.setEnabled(True)
                self.edtNameMaterial.setEnabled(False)
                self.edtNameMaterial.setText("")
                self.cmbTypeHeatConductionSolid.setEnabled(False)
                self.cmbTypeHeatConductionSolid.setCurrentIndex (0)
                self.edtTermalConductivityIsotropicProperties.setEnabled(False)
                self.edtTermalConductivityIsotropicProperties.setText("")
                self.edtTermalConductivityAnisotropicPropertiesA11.setEnabled(False)
                self.edtTermalConductivityAnisotropicPropertiesA12.setEnabled(False)
                self.edtTermalConductivityAnisotropicPropertiesA21.setEnabled(False)
                self.edtTermalConductivityAnisotropicPropertiesA22.setEnabled(False)
                self.edtTermalConductivityAnisotropicPropertiesA11.setText("")
                self.edtTermalConductivityAnisotropicPropertiesA12.setText("")
                self.edtTermalConductivityAnisotropicPropertiesA21.setText("")
                self.edtTermalConductivityAnisotropicPropertiesA22.setText("")
                self.edtRhoProperties.setEnabled(False)
                self.edtRhoProperties.setText("")
                self.edtCpProperties.setEnabled(False)
                self.edtCpProperties.setText("")
                self.addMaterials()
                QMessageBox.information(self, "Important message", "Material registered in the database")               
            else:
                QMessageBox.criti|cal(self, "Important message", "Null values ​​exist, please check")    
        elif self.statusLibrary == 3 :
            if sum(reviews) == 3 :
                display(self.materialsDataBase[self.cmbNameMaterials.currentIndex()][0])
                material = (self.edtNameMaterial.text(),self.DataProperties.kappa[0][0],self.DataProperties.kappa[0][1],self.DataProperties.kappa[1][0],self.DataProperties.kappa[1][1],self.DataProperties.Cp,self.DataProperties.rho,self.cmbTypeHeatConductionSolid.currentIndex(),self.materialsDataBase[self.cmbNameMaterials.currentIndex()][0])
                update_material(self.conn, material)
                self.materialsDataBase = select_all_materials(self.conn)
                self.btnNewMaterial.setEnabled(True)
                self.btnDeleteMaterial.setEnabled(True)
                self.btnSaveMaterial.setEnabled(False)
                self.btnSaveAsMaterial.setEnabled(True)
                self.btnOpenMaterial.setEnabled(True)
                self.btnResetLibrary.setEnabled(False)
                self.btnHelpLibrary.setEnabled(True)
                self.cmbNameMaterials.setEnabled(True)
                self.edtNameMaterial.setEnabled(False)
                self.edtNameMaterial.setText("")
                self.cmbTypeHeatConductionSolid.setEnabled(False)
                self.cmbTypeHeatConductionSolid.setCurrentIndex(0)
                self.edtTermalConductivityIsotropicProperties.setEnabled(False)
                self.edtTermalConductivityIsotropicProperties.setText("")
                self.edtTermalConductivityAnisotropicPropertiesA11.setEnabled(False)
                self.edtTermalConductivityAnisotropicPropertiesA12.setEnabled(False)
                self.edtTermalConductivityAnisotropicPropertiesA21.setEnabled(False)
                self.edtTermalConductivityAnisotropicPropertiesA22.setEnabled(False)
                self.edtTermalConductivityAnisotropicPropertiesA11.setText("")
                self.edtTermalConductivityAnisotropicPropertiesA12.setText("")
                self.edtTermalConductivityAnisotropicPropertiesA21.setText("")
                self.edtTermalConductivityAnisotropicPropertiesA22.setText("")
                self.edtRhoProperties.setEnabled(False)
                self.edtRhoProperties.setText("")
                self.edtCpProperties.setEnabled(False)
                self.edtCpProperties.setText("")
                self.addMaterials()
                QMessageBox.information(self, "Important message", "material registered in the database")               
            else:
                QMessageBox.critical(self, "Important message", "Null values ​​exist, please check")    
        self.statusLibrary = 0

    def change_cmbNameMaterials(self) :
        if self.cmbNameMaterials.currentIndex() != -1 :
            if self.materialsDataBase[self.cmbNameMaterials.currentIndex()][6] == 0:  #isotropic
                self.cmbTypeHeatConductionSolid.setCurrentIndex(0)
                self.edtTermalConductivityIsotropicProperties.setText(str(self.materialsDataBase[self.cmbNameMaterials.currentIndex()][2]))  
                self.edtTermalConductivityAnisotropicPropertiesA11.setText("")
                self.edtTermalConductivityAnisotropicPropertiesA12.setText("")
                self.edtTermalConductivityAnisotropicPropertiesA21.setText("")
                self.edtTermalConductivityAnisotropicPropertiesA22.setText("")    
                self.edtCpProperties.setText(str(self.materialsDataBase[self.cmbNameMaterials.currentIndex()][7]))
                self.edtRhoProperties.setText(str(self.materialsDataBase[self.cmbNameMaterials.currentIndex()][8]))
                dato = self.edtTermalConductivityIsotropicProperties.text()
                self.DataProperties.kappa[0][0] = float(dato)
                self.DataProperties.kappa[0][1] = -1.0
                self.DataProperties.kappa[1][0] = -1.0
                self.DataProperties.kappa[1][1] = -1.0
            elif self.materialsDataBase[self.cmbNameMaterials.currentIndex()][6] == 1 : #diagonal  
                self.cmbTypeHeatConductionSolid.setCurrentIndex(1)
                self.edtTermalConductivityIsotropicProperties.setText("")  
                self.edtTermalConductivityAnisotropicPropertiesA11.setText(str(self.materialsDataBase[self.cmbNameMaterials.currentIndex()][2]))
                self.edtTermalConductivityAnisotropicPropertiesA12.setText("0")
                self.edtTermalConductivityAnisotropicPropertiesA21.setText("0")
                self.edtTermalConductivityAnisotropicPropertiesA22.setText(str(self.materialsDataBase[self.cmbNameMaterials.currentIndex()][5]))    
                self.edtCpProperties.setText(str(self.materialsDataBase[self.cmbNameMaterials.currentIndex()][7]))
                self.edtRhoProperties.setText(str(self.materialsDataBase[self.cmbNameMaterials.currentIndex()][8]))
                dato = self.edtTermalConductivityAnisotropicPropertiesA11.text()
                self.DataProperties.kappa[0][0] = float(dato)
                self.DataProperties.kappa[0][1] = 0.0
                self.DataProperties.kappa[1][0] = 0.0
                dato = self.edtTermalConductivityAnisotropicPropertiesA22.text()
                self.DataProperties.kappa[1][1] = float(dato)
            elif self.materialsDataBase[self.cmbNameMaterials.currentIndex()][6] == 2 : #symmetric   
                self.cmbTypeHeatConductionSolid.setCurrentIndex(2)
                self.edtTermalConductivityIsotropicProperties.setText("")  
                self.edtTermalConductivityAnisotropicPropertiesA11.setText(str(self.materialsDataBase[self.cmbNameMaterials.currentIndex()][2]))
                self.edtTermalConductivityAnisotropicPropertiesA12.setText(str(self.materialsDataBase[self.cmbNameMaterials.currentIndex()][3]))
                self.edtTermalConductivityAnisotropicPropertiesA21.setText(str(self.materialsDataBase[self.cmbNameMaterials.currentIndex()][4]))
                self.edtTermalConductivityAnisotropicPropertiesA22.setText(str(self.materialsDataBase[self.cmbNameMaterials.currentIndex()][5]))
                dato = self.edtTermalConductivityAnisotropicPropertiesA11.text()
                self.DataProperties.kappa[0][0] = float(dato)
                dato = self.edtTermalConductivityAnisotropicPropertiesA12.text()
                self.DataProperties.kappa[0][1] = float(dato)
                self.DataProperties.kappa[1][0] = float(dato)
                dato = self.edtTermalConductivityAnisotropicPropertiesA22.text()
                self.DataProperties.kappa[1][1] = float(dato)
            elif self.materialsDataBase[self.cmbNameMaterials.currentIndex()][6] == 3 : #full
                self.cmbTypeHeatConductionSolid.setCurrentIndex(3)
                self.edtTermalConductivityIsotropicProperties.setText("")  
                self.edtTermalConductivityAnisotropicPropertiesA11.setText(str(self.materialsDataBase[self.cmbNameMaterials.currentIndex()][2]))
                self.edtTermalConductivityAnisotropicPropertiesA12.setText(str(self.materialsDataBase[self.cmbNameMaterials.currentIndex()][3]))
                self.edtTermalConductivityAnisotropicPropertiesA21.setText(str(self.materialsDataBase[self.cmbNameMaterials.currentIndex()][4]))
                self.edtTermalConductivityAnisotropicPropertiesA22.setText(str(self.materialsDataBase[self.cmbNameMaterials.currentIndex()][5]))
                dato = self.edtTermalConductivityAnisotropicPropertiesA11.text()
                self.DataProperties.kappa[0][0] = float(dato)
                dato = self.edtTermalConductivityAnisotropicPropertiesA12.text()
                self.DataProperties.kappa[0][1] = float(dato)
                dato = self.edtTermalConductivityAnisotropicPropertiesA21.text()
                self.DataProperties.kappa[1][0] = float(dato)
                dato = self.edtTermalConductivityAnisotropicPropertiesA22.text()
            self.edtCpProperties.setText(str(self.materialsDataBase[self.cmbNameMaterials.currentIndex()][7]))
            self.edtRhoProperties.setText(str(self.materialsDataBase[self.cmbNameMaterials.currentIndex()][8]))
            dato = self.edtRhoProperties.text()
            self.DataProperties.rho = float(dato)
            dato = self.edtCpProperties.text()
            self.DataProperties.Cp = float(dato)
            self.edtTermalConductivityIsotropicProperties.setEnabled(False)
            self.edtTermalConductivityAnisotropicPropertiesA11.setEnabled(False)
            self.edtTermalConductivityAnisotropicPropertiesA12.setEnabled(False)
            self.edtTermalConductivityAnisotropicPropertiesA21.setEnabled(False)
            self.edtTermalConductivityAnisotropicPropertiesA22.setEnabled(False)
            self.edtCpProperties.setEnabled(False)
            self.edtRhoProperties.setEnabled(False)

    def change_cmbTypeHeatConductionSolid(self):
        if self.cmbTypeHeatConductionSolid.currentIndex() == 0 : #isotropic
            self.edtTermalConductivityIsotropicProperties.setEnabled(True)
            self.edtTermalConductivityIsotropicProperties.setText("")
            self.edtTermalConductivityAnisotropicPropertiesA11.setEnabled(False)
            self.edtTermalConductivityAnisotropicPropertiesA11.setText("")
            self.edtTermalConductivityAnisotropicPropertiesA12.setEnabled(False)
            self.edtTermalConductivityAnisotropicPropertiesA12.setText("")
            self.edtTermalConductivityAnisotropicPropertiesA21.setEnabled(False)
            self.edtTermalConductivityAnisotropicPropertiesA21.setText("")
            self.edtTermalConductivityAnisotropicPropertiesA22.setEnabled(False)
            self.edtTermalConductivityAnisotropicPropertiesA22.setText("")
        elif self.cmbTypeHeatConductionSolid.currentIndex() == 1 : #diagonal
            self.edtTermalConductivityIsotropicProperties.setEnabled(False)
            self.edtTermalConductivityIsotropicProperties.setText("")
            self.edtTermalConductivityAnisotropicPropertiesA11.setEnabled(True)
            self.edtTermalConductivityAnisotropicPropertiesA11.setText("")
            self.edtTermalConductivityAnisotropicPropertiesA12.setEnabled(False)
            self.edtTermalConductivityAnisotropicPropertiesA12.setText("0")
            self.edtTermalConductivityAnisotropicPropertiesA21.setEnabled(False)
            self.edtTermalConductivityAnisotropicPropertiesA21.setText("0")
            self.edtTermalConductivityAnisotropicPropertiesA22.setEnabled(True)
            self.edtTermalConductivityAnisotropicPropertiesA22.setText("")
        elif self.cmbTypeHeatConductionSolid.currentIndex() == 2 : #symmetric
            self.edtTermalConductivityIsotropicProperties.setEnabled(False)
            self.edtTermalConductivityIsotropicProperties.setText("")
            self.edtTermalConductivityAnisotropicPropertiesA11.setEnabled(True)
            self.edtTermalConductivityAnisotropicPropertiesA11.setText("")
            self.edtTermalConductivityAnisotropicPropertiesA12.setEnabled(True)
            self.edtTermalConductivityAnisotropicPropertiesA12.setText("")
            self.edtTermalConductivityAnisotropicPropertiesA21.setEnabled(False)
            self.edtTermalConductivityAnisotropicPropertiesA21.setText("")
            self.edtTermalConductivityAnisotropicPropertiesA22.setEnabled(True)
            self.edtTermalConductivityAnisotropicPropertiesA22.setText("")
        elif self.cmbTypeHeatConductionSolid.currentIndex() == 3 : #full
            self.edtTermalConductivityIsotropicProperties.setEnabled(False)
            self.edtTermalConductivityIsotropicProperties.setText("")
            self.edtTermalConductivityAnisotropicPropertiesA11.setEnabled(True)
            self.edtTermalConductivityAnisotropicPropertiesA11.setText("")
            self.edtTermalConductivityAnisotropicPropertiesA12.setEnabled(True)
            self.edtTermalConductivityAnisotropicPropertiesA12.setText("")
            self.edtTermalConductivityAnisotropicPropertiesA21.setEnabled(True)
            self.edtTermalConductivityAnisotropicPropertiesA21.setText("")
            self.edtTermalConductivityAnisotropicPropertiesA22.setEnabled(True)
            self.edtTermalConductivityAnisotropicPropertiesA22.setText("")

    def exit_edtTermalConductivityIsotropicProperties(self):
        dato = self.edtTermalConductivityIsotropicProperties.text()
        if not (dato.isspace() or len(dato) ==0):
            if float(dato) >= 0:
                self.DataProperties.kappa[0][0] = float(dato)
                self.DataProperties.kappa[0][1] = -1.0
                self.DataProperties.kappa[1][0] = -1.0
                self.DataProperties.kappa[1][1] = -1.0
            else:
                QMessageBox.critical(self, "Important message", "The value must be greater than or equal to zero")
                self.edtTermalConductivityIsotropicProperties.setText("")

    def exit_edtTermalConductivityAnisotropicPropertiesA11(self):
        dato = self.edtTermalConductivityAnisotropicPropertiesA11.text()
        if not (dato.isspace() or len(dato) ==0):
            if float(dato) >= 0:
                self.DataProperties.kappa[0][0] = float(dato)
                if self.cmbTypeHeatConductionSolid.currentIndex () == 1 : #diagonal
                    self.DataProperties.kappa[0][1] = 0.0
                    self.DataProperties.kappa[1][0] = 0.0
            else:
                QMessageBox.critical(self, "Important message", "The value must be greater than or equal to zero")
                self.edtTermalConductivityAnisotropicPropertiesA11.setText("")

    def exit_edtTermalConductivityAnisotropicPropertiesA12(self):
        dato = self.edtTermalConductivityAnisotropicPropertiesA12.text()
        if not (dato.isspace() or len(dato) ==0):
            if float(dato) >= 0:
                self.DataProperties.kappa[0][1] = float(dato)
                if self.cmbTypeHeatConductionSolid.currentIndex () == 2 : #symmetric
                    self.DataProperties.kappa[1][0] = float(dato)
                    self.edtTermalConductivityAnisotropicPropertiesA21.setText(dato)
            else:
                QMessageBox.critical(self, "Important message", "The value must be greater than or equal to zero")
                self.edtTermalConductivityAnisotropicPropertiesA12.setText("")


    def exit_edtTermalConductivityAnisotropicPropertiesA21(self):
        dato = self.edtTermalConductivityAnisotropicPropertiesA21.text()
        if not (dato.isspace() or len(dato) ==0):
            if float(dato) >= 0:
                self.DataProperties.kappa[1][0] = float(dato)
            else:
                QMessageBox.critical(self, "Important message", "The value must be greater than or equal to zero")
                self.edtTermalConductivityAnisotropicPropertiesA21.setText("")

    def exit_edtTermalConductivityAnisotropicPropertiesA22(self):
        dato = self.edtTermalConductivityAnisotropicPropertiesA22.text()
        if not (dato.isspace() or len(dato) ==0):
            if float(dato) >= 0:
                self.DataProperties.kappa[1][1] = float(dato)
                if self.cmbTypeHeatConductionSolid.currentIndex () == 1 : #diagonal
                    self.DataProperties.kappa[0][1] = 0.0
                    self.DataProperties.kappa[1][0] = 0.0   
            else:
                QMessageBox.critical(self, "Important message", "The value must be greater than or equal to zero")
                self.edtTermalConductivityAnisotropicPropertiesA22.setText("")

    def exit_edtRhoProperties(self):
        dato = self.edtRhoProperties.text()
        if not (dato.isspace() or len(dato) ==0):
            if float(dato) > 0:
                self.DataProperties.rho = float(dato)
            else:
                QMessageBox.critical(self, "Important message", "The value must be greater than zero")
                self.edtRhoProperties.setText("")  

    def exit_edtCpProperties(self) :
        dato = self.edtCpProperties.text()
        if not (dato.isspace() or len(dato) ==0):
            if float(dato) > 0:
                self.DataProperties.Cp = float(dato)
            else:
                QMessageBox.critical(self, "Important message", "The value must be greater than zero")
                self.edtCpProperties.setText("")      


    def addMaterials(self) :       
        self.cmbNameMaterials.clear()
        for i in range(len(self.materialsDataBase)):
            self.cmbNameMaterials.addItem(self.materialsDataBase[i][1])


    def desabledLEdit(self, edit):
        for i in range(len(edit)):
            if i > 0:
                edit[i].setEnabled(False)

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
    widget.setWindowIcon(QIcon("Assets\icon-temperature.png"))
    widget.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
