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
from Modules.LibraryButtons.DeleteMaterial import *
from Modules.LibraryButtons.OpenMaterial import *
from Modules.LibraryButtons.ResetLibrary import *
from Modules.LibraryButtons.SaveAsMaterial import *
from Modules.LibraryButtons.SaveMaterial import *
from Modules.LibraryButtons.NewMaterial import *
from Modules.LibraryButtons.changeNameM import *
from Modules.LibraryButtons.EditTypeHeatCond import *


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
        with open('Styles\styles.qss', 'r', encoding='utf-8') as file:
            str = file.read()
        self.setStyleSheet(str)
        root = os.path.dirname(os.path.realpath(__file__))
        loadUi(os.path.join(root, 'Interfaz.ui'), self)

        # -------------------------------------------------------------------------
        # DataBase
        #Library Buttons
        self.conn = materials()
        self.materialsDataBase = select_all_materials(self.conn)
        self.DataProperties = PropertiesData()
        self.btnNewMaterial.clicked.connect(lambda: NewMaterial.click_btnNewMaterial(self))
        self.btnSaveMaterial.clicked.connect(lambda: SaveMaterial.click_btnSaveMaterial(self))
        self.btnResetLibrary.clicked.connect(lambda: ResetLibrary.click_btnResetLibrary(self))
        self.btnSaveAsMaterial.clicked.connect(lambda: SaveAsMaterial.click_btnSaveAsMaterial(self))
        self.btnOpenMaterial.clicked.connect(lambda: OpenMaterial.click_btnOpenMaterial(self))
        self.btnDeleteMaterial.clicked.connect(lambda: DeleteMaterial.click_btnDeleteMaterial(self))

        self.cmbTypeHeatConductionSolid.currentIndexChanged.connect(lambda: EditTypeHeatCond.change_cmbTypeHeatConductionSolid(self))
        self.cmbNameMaterials.currentIndexChanged.connect(lambda: changeNameMaterials.change_cmbNameMaterials(self))
        self.edtTermalConductivityIsotropicProperties.editingFinished.connect(lambda: EditTypeHeatCond.exit_edtTermalConductivityIsotropicProperties(self))
        self.edtTermalConductivityAnisotropicPropertiesA11.editingFinished.connect(lambda: EditTypeHeatCond.exit_edtTermalConductivityAnisotropicPropertiesA11(self))
        self.edtTermalConductivityAnisotropicPropertiesA12.editingFinished.connect(lambda: EditTypeHeatCond.exit_edtTermalConductivityAnisotropicPropertiesA12(self))
        self.edtTermalConductivityAnisotropicPropertiesA21.editingFinished.connect(lambda: EditTypeHeatCond.exit_edtTermalConductivityAnisotropicPropertiesA21(self))
        self.edtTermalConductivityAnisotropicPropertiesA22.editingFinished.connect(lambda: EditTypeHeatCond.exit_edtTermalConductivityAnisotropicPropertiesA22(self))
        self.edtRhoProperties.editingFinished.connect(lambda: EditTypeHeatCond.exit_edtRhoProperties(self))
        self.edtCpProperties.editingFinished.connect(lambda: EditTypeHeatCond.exit_edtCpProperties(self))
        self.addMaterials()

        # -------------------------------------------------------------------------
        # MENU TABS

        self.tabs = []
        modelWizardDict = {'widget': self.modelWizardTab, 'title': "Model Wizard", 'index': 0}
        materialsTabDict = {'widget': self.materialsTab, 'title': "Materials", 'index': 1}
        geometryTabDict = {'widget': self.geometryTab, 'title': "Geometry", 'index': 2}
        conditionsTabDict = {'widget': self.conditionsTab, 'title': "Conditions", 'index': 3}
        meshAndSettingStudyTabDict = {'widget': self.meshAndSettingStudyTab, 'title': "Mesh and Setting Study", 'index': 4}
        conditionsPDETabDict = {'widget': self.conditionsPDETab, 'title': "Conditions PDE", 'index': 5}
        coefficentFormPDETabDict = {'widget': self.CoefficentFormPDETab, 'title': "Coefficent Form PDE", 'index': 6}
        libraryTabDict = {'widget': self.libraryTab, 'title': "Library", 'index': 7}

        self.tabs.append(modelWizardDict)           # 0
        self.tabs.append(materialsTabDict)             # 1
        self.tabs.append(geometryTabDict)              # 2
        self.tabs.append(conditionsTabDict)            # 3
        self.tabs.append(meshAndSettingStudyTabDict)   # 4
        self.tabs.append(conditionsPDETabDict)         # 5
        self.tabs.append(coefficentFormPDETabDict)     # 6
        self.tabs.append(libraryTabDict)               # 7

        # -------------------------------------------------------------------------
        # MODEL WIZARD
        # tabWidgetMenu
        ModelWizard.hideInitialTabs( self.tabs, self.tabWidgetMenu )
        self.treeModelWizard.currentItemChanged.connect(lambda: ModelWizard.currentTreeItem(self.treeModelWizard.currentItem(), self.treeModelWizard.currentColumn(), self.tabs, self.tabWidgetMenu ))

        # -------------------------------------------------------------------------
        # GEOMETRIC FIGURE
        # Combo box
        #self.figuresSection = self.findChild(QToolBox, "figuresSection")
        self.figuresSection.setItemEnabled(0, True)
        self.figuresSection.setItemEnabled(1, False)
        self.figuresSection.setItemEnabled(2, False)
        self.figuresSection.setItemEnabled(3, False)
        self.figuresSection.setItemEnabled(4, False)

        self.cmbGeometricFigure.currentIndexChanged.connect(lambda: Geometry.currentCheckedComboBoxItem(self.figuresSection, self.cmbGeometricFigure))


        # Conditions PDE
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
        self.toolBoxTypeOfCon.setItemEnabled(0, True)
        self.toolBoxTypeOfCon.setItemEnabled(1, False)
        self.toolBoxTypeOfCon.setItemEnabled(2, False)
        self.toolBoxTypeOfCon.setItemEnabled(3, False)
        self.toolBoxTypeOfCon.setItemEnabled(4, False)

        self.cmbTypeConditionPDE.currentIndexChanged.connect(lambda: ConditionsPDE.currentCheckedComboBoxItemConditions(self.toolBoxTypeOfCon, self.cmbTypeConditionPDE))

        #CheckBox Coefficients Form PDE
        self.CoefficentForM.setItemEnabled(1, False)
        self.CoefficentForM.setItemEnabled(2, False)
        self.CoefficentForM.setItemEnabled(3, False)
        self.CoefficentForM.setItemEnabled(4, False)
        self.CoefficentForM.setItemEnabled(5, False)
        self.CoefficentForM.setItemEnabled(6, False)
        self.CoefficentForM.setItemEnabled(7, False)
        self.CoefficentForM.setItemEnabled(8, False)

        self.btnCoefficientsApply.clicked.connect(lambda: CoefficientsPDE.currentCoefficientForM(self.CoefficentForM, CoefficientsPDE.CheckCoefficient(CoefficientCheckBoxArray)))

        #ComboBox HeatConduction
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

        self.cmbHeatConduction.currentIndexChanged.connect(lambda: Materials.currentHeatConduction(self.cmbHeatConduction, inputKArray))

        #Combobox TypeCondiction
        self.toolBoxTypeOfCondition.setItemEnabled(0, False)
        self.toolBoxTypeOfCondition.setItemEnabled(1, False)
        self.toolBoxTypeOfCondition.widget(0).hide()
        self.toolBoxTypeOfCondition.widget(1).hide()

        self.cmbTypeCondition.currentIndexChanged.connect(lambda: Conditions.currentTypeCondition(self.cmbTypeCondition, self.toolBoxTypeOfCondition))


        # -------------------------------------------------------------------------
        # COEFFICENT FORM PDE
        # Diffusion Coeficient
        self.diffusionCoefData = []
       
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

        self.cmbRowDiffusionCoef.currentIndexChanged.connect(lambda: ConditionsPDE.changeMatrixCoefficient(self.cmbRowDiffusionCoef.currentIndex(), self.cmbColumnDiffusionCoef.currentIndex(), self.diffusionCoefData))
        self.cmbColumnDiffusionCoef.currentIndexChanged.connect(lambda: ConditionsPDE.changeMatrixCoefficient(self.cmbRowDiffusionCoef.currentIndex(), self.cmbColumnDiffusionCoef.currentIndex(), self.diffusionCoefData))

        # Absorption Coeficient
        self.lEditAbsorData = []
    
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

        self.cmbAbsorptionRow.currentIndexChanged.connect(lambda: ConditionsPDE.changeMatrixCoefficient(self.cmbAbsorptionRow.currentIndex(), self.cmbAbsorptionColumn.currentIndex(), self.lEditAbsorData))
        self.cmbAbsorptionColumn.currentIndexChanged.connect(lambda: ConditionsPDE.changeMatrixCoefficient(self.cmbAbsorptionRow.currentIndex(), self.cmbAbsorptionColumn.currentIndex(), self.lEditAbsorData))

        # Source term
        self.lEditSourceData = []
       
        self.lEditSourceData.append(self.lEditSourceTerm11)
        self.lEditSourceData.append(self.lEditSourceTerm12)
        self.lEditSourceData.append(self.lEditSourceTerm13)
        self.desabledLEdit(self.lEditSourceData)

        self.cmbSourceRow.currentIndexChanged.connect(lambda: ConditionsPDE.currentRowEdit(self.cmbSourceRow.currentIndex(), self.lEditSourceData))

        #Mass Coefficent
        self.lEditMassCoefData = []
   
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

        self.cmbMassCoefRow.currentIndexChanged.connect(lambda: ConditionsPDE.changeMatrixCoefficient(self.cmbMassCoefRow.currentIndex(),self.cmbMassCoefColumn.currentIndex(), self.lEditMassCoefData))
        self.cmbMassCoefColumn.currentIndexChanged.connect(lambda: ConditionsPDE.changeMatrixCoefficient(self.cmbMassCoefRow.currentIndex(),self.cmbMassCoefColumn.currentIndex() ,self.lEditMassCoefData))

        # Damping or mass coeficient
        self.lEditDamMassCoefData = []

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

        self.cmbDamMassCoefRow.currentIndexChanged.connect(lambda: ConditionsPDE.changeMatrixCoefficient(self.cmbDamMassCoefRow.currentIndex(),self.cmbDamMassCoefColumn.currentIndex(), self.lEditDamMassCoefData))
        self.cmbDamMassCoefColumn.currentIndexChanged.connect(lambda: ConditionsPDE.changeMatrixCoefficient(self.cmbDamMassCoefRow.currentIndex(),self.cmbDamMassCoefColumn.currentIndex(), self.lEditDamMassCoefData))

        # Consevative Flux convection coefficent
        self.lEditAlphaXCFluxData = []
        self.lEditAlphaCYFluxData = []

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

        self.cmbCFluxColumn.currentIndexChanged.connect(lambda: ConditionsPDE.activateIndexAlpha(self.lEditAlphaXCFluxData, self.lEditAlphaCYFluxData, self.cmbCFluxRow.currentIndex(), self.cmbCFluxColumn.currentIndex()))
        self.cmbCFluxRow.currentIndexChanged.connect(lambda: ConditionsPDE.activateIndexAlpha(self.lEditAlphaXCFluxData, self.lEditAlphaCYFluxData, self.cmbCFluxRow.currentIndex(), self.cmbCFluxColumn.currentIndex()))

        # Convection Coefficent
        # Beta X
        self.lEditBetaXConvCoefData = []
    
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

        self.cmbConvectionRow.currentIndexChanged.connect(lambda: ConditionsPDE.activateIndexAlpha(self.lEditBetaXConvCoefData, self.lEditBetaYConvCoefData, self.cmbConvectionRow.currentIndex(), self.cmbConvectionColumn.currentIndex()))
        self.cmbConvectionColumn.currentIndexChanged.connect(lambda: ConditionsPDE.activateIndexAlpha(self.lEditBetaXConvCoefData, self.lEditBetaYConvCoefData, self.cmbConvectionRow.currentIndex(), self.cmbConvectionColumn.currentIndex()))
       
        # Conservative Flux Source
        # Gamma X
        self.lEditGammaXCFluxSourceData = []
        # Llenar array de gamma x
        self.lEditGammaXCFluxSourceData.append(self.lEditGammaXCFluxSource1)
        self.lEditGammaXCFluxSourceData.append(self.lEditGammaXCFluxSource2)
        self.lEditGammaXCFluxSourceData.append(self.lEditGammaXCFluxSource3)
        self.desabledLEdit(self.lEditGammaXCFluxSourceData)

        # Gamma Y
        self.lEditGammaYCFluxSourceData = []
        
        # Llenar array de gamma Y
        self.lEditGammaYCFluxSourceData.append(self.lEditGammaYCFluxSource1)
        self.lEditGammaYCFluxSourceData.append(self.lEditGammaYCFluxSource2)
        self.lEditGammaYCFluxSourceData.append(self.lEditGammaYCFluxSource3)
        self.desabledLEdit(self.lEditGammaYCFluxSourceData)

        self.cmbCSourceRow.currentIndexChanged.connect(lambda: ConditionsPDE.disabledRowEdit( self.lEditGammaXCFluxSourceData,  self.lEditGammaYCFluxSourceData, self.cmbCSourceRow.currentIndex()))

    #DataBaseTools
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
