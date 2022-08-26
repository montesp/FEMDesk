"""
Created on Wed May 11 13:39:55 2022

@author:ruben.castaneda,
        Pavel Montes,
        Armando Terán
"""

#-*- coding: utf-8 -*-

from operator import le
import os, sys
from sqlite3 import connect
import imagen_rc
import array as arr
from PyQt5.QtCore import Qt, QObject
from PyQt5.QtGui import QPainter, QCloseEvent, QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QTabWidget, QGraphicsView, QButtonGroup, QTreeWidget ,QMessageBox, QPushButton, QLineEdit, QLabel, QCheckBox, QToolBox, QComboBox, QWidget
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtWidgets
from Base import *
from interfaz import *
from Modules.Materials import *
from Modules.SectionTabs.Geometry import *
from Modules.SectionTabs.Conditions import *
from Modules.SectionTabs.ConditionsPDE import *
from Modules.SectionTabs.CoefficientsPDE import * 
from Modules.ModelWizard import *
from Modules.LibraryButtons.DeleteMaterial import *
from Modules.LibraryButtons.OpenMaterial import *
from Modules.LibraryButtons.ResetLibrary import *
from Modules.LibraryButtons.SaveAsMaterial import *
from Modules.LibraryButtons.SaveMaterial import *
from Modules.LibraryButtons.NewMaterial import *
from Modules.LibraryButtons.changeNameM import *
from Modules.LibraryButtons.EditTypeHeatCond import *
from Modules.Matrix import *
from Modules.ManageFiles import *





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
    statusLibrary = 0 #0 initial value, 1 new material, 2 copy, 3 changes values

    def __init__(self):
        super(QMainWindow, self).__init__()
        self.app = app
        with open('Styles\styles.qss', 'r', encoding='utf-8') as file:
            str = file.read()
        self.setStyleSheet(str)
        root = os.path.dirname(os.path.realpath(__file__))
        loadUi(os.path.join(root, 'Interfaz.ui'), self)

        self.allMatrix = self.AllMatrix()
        

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
        arrayFiguresSection = []

        for i in range(self.figuresSection.count()):
            arrayFiguresSection.append(self.figuresSection.widget(i))

        for i in range(self.figuresSection.count()):
            self.figuresSection.removeItem(self.figuresSection.currentIndex())

        self.figuresSection.hide()
        self.cmbGeometricFigure.currentIndexChanged.connect(lambda: Geometry.currentCheckedComboBoxItem(self.figuresSection, self.cmbGeometricFigure, arrayFiguresSection))

        Geometry.currentCheckedComboBoxItem(self.figuresSection, self.cmbGeometricFigure, arrayFiguresSection)
        self.cmbGeometricFigure.currentIndexChanged.connect(lambda: Geometry.currentCheckedComboBoxItem(self.figuresSection, self.cmbGeometricFigure, arrayFiguresSection))
        self.btnGeometryApply.clicked.connect(lambda: Geometry.getData(self.figuresSection.currentWidget(), self.cmbGeometricFigure))

        # Conditions PDE
        self.CoefficientCheckBoxArray = []
        self.CoefficientCheckBoxArray.append(self.chkDiffusionCoefficient)
        self.CoefficientCheckBoxArray.append(self.chkAbsorptionCoefficient)
        self.CoefficientCheckBoxArray.append(self.chkSourceTerm)
        self.CoefficientCheckBoxArray.append(self.chkMassCoefficient)
        self.CoefficientCheckBoxArray.append(self.chkDampCoefficient)
        self.CoefficientCheckBoxArray.append(self.chkConservativeConvection)
        self.CoefficientCheckBoxArray.append(self.chkConvectionCoefficient)
        self.CoefficientCheckBoxArray.append(self.chkConservativeFluxSource)

        arrayTypeofConSection = []

        for i in range(self.toolBoxTypeOfCon.count()):
            arrayTypeofConSection.append(self.toolBoxTypeOfCon.widget(i))

        ConditionsPDE.currentCheckedComboBoxItemConditions(self.toolBoxTypeOfCon, self.cmbTypeConditionPDE, arrayTypeofConSection)
        self.cmbTypeConditionPDE.currentIndexChanged.connect(lambda: ConditionsPDE.currentCheckedComboBoxItemConditions(self.toolBoxTypeOfCon, self.cmbTypeConditionPDE, arrayTypeofConSection))

        #CheckBox Coefficients Form PDE
        self.arrayCoeffMSection = []
        self.arrayCheckNameCoeffM = []

        for i in range(self.CoefficentForM.count()):
            self.arrayCheckNameCoeffM.append(self.CoefficentForM.itemText(i))

        for i in range(self.CoefficentForM.count()):
            self.arrayCoeffMSection.append(self.CoefficentForM.widget(i))

        arrayDiffusionCoeff = []
        arrayDiffusionCoeff.append(self.lEditDiffusionCoef)
        arrayDiffusionCoeff.append(self.lEditDiffusionCoef11)
        arrayDiffusionCoeff.append(self.lEditDiffusionCoef12)
        arrayDiffusionCoeff.append(self.lEditDiffusionCoef21)
        arrayDiffusionCoeff.append(self.lEditDiffusionCoef22)
    

        Materials.currentHeatConduction(self.cmbDiffusionCoef,  arrayDiffusionCoeff)
        self.cmbDiffusionCoef.currentIndexChanged.connect(lambda: Materials.currentHeatConduction(self.cmbDiffusionCoef,  arrayDiffusionCoeff))
        self.lEditDiffusionCoef11.textChanged.connect(lambda: Materials.currentTextSimmetry(self.cmbDiffusionCoef, arrayDiffusionCoeff))
        CoefficientsPDE.currentCoefficientForM(self.CoefficentForM, CoefficientsPDE.CheckCoefficient(self.CoefficientCheckBoxArray), self.arrayCoeffMSection, self.arrayCheckNameCoeffM)
        self.btnCoefficientsApply.clicked.connect(lambda: CoefficientsPDE.currentCoefficientForM(self.CoefficentForM, CoefficientsPDE.CheckCoefficient(self.CoefficientCheckBoxArray), self.arrayCoeffMSection, self.arrayCheckNameCoeffM))

        #ComboBox HeatConduction
        inputKArray = []

        inputKArray.append(self.inputK)
        inputKArray.append(self.inputKD1)
        inputKArray.append(self.inputKD2)
        inputKArray.append(self.inputKD3)
        inputKArray.append(self.inputKD4)

        Materials.currentHeatConduction(self.cmbHeatConduction, inputKArray)
        self.inputKD1.textChanged.connect(lambda: Materials.currentTextSimmetry(self.cmbHeatConduction, inputKArray))
        self.cmbHeatConduction.currentIndexChanged.connect(lambda: Materials.currentHeatConduction(self.cmbHeatConduction, inputKArray))

        #Combobox TypeCondiction
        arrayTypeofConditionSection = []
        for i in range(self.toolBoxTypeOfCondition.count()):
            arrayTypeofConditionSection.append(self.toolBoxTypeOfCondition.widget(i))

        Conditions.currentTypeCondition(self.cmbTypeCondition, self.toolBoxTypeOfCondition, arrayTypeofConditionSection)
        self.cmbTypeCondition.currentIndexChanged.connect(lambda: Conditions.currentTypeCondition(self.cmbTypeCondition, self.toolBoxTypeOfCondition, arrayTypeofConditionSection))


        # -------------------------------------------------------------------------
        # COEFFICENT FORM PDE

        #Combobox Row and Columns Configuration
        arrayDiffusionRowColumn = [self.cmbRowDiffusionCoef, self.cmbColumnDiffusionCoef]
        arrayAbsorptionRowColumn = [self.cmbAbsorptionRow, self.cmbAbsorptionColumn]
        arraySourceRow = [self.cmbSourceRow]
        arrayMassRowColumn = [self.cmbMassCoefRow, self.cmbMassCoefColumn]
        arrayDampingRowColumn = [self.cmbDamMassCoefRow, self.cmbDamMassCoefColumn]
        arrayCFluxRowColumn = [self.cmbCFluxRow, self.cmbCFluxColumn]
        arrayConvectionRowColumn = [self.cmbConvectionRow, self.cmbConvectionColumn]
        arrayCSourceRow = [self.cmbCSourceRow]

        arrayCmbRowColumns = []
        arrayCmbRowColumns.append(arrayDiffusionRowColumn)
        arrayCmbRowColumns.append(arrayAbsorptionRowColumn)
        arrayCmbRowColumns.append(arraySourceRow)
        arrayCmbRowColumns.append(arrayMassRowColumn)
        arrayCmbRowColumns.append(arrayDampingRowColumn)
        arrayCmbRowColumns.append(arrayCFluxRowColumn)
        arrayCmbRowColumns.append(arrayConvectionRowColumn)
        arrayCmbRowColumns.append(arrayCSourceRow)

        #LineEdits Coefficients
        arrayAbsorption = [self.lEditAbsorCoef]
        arraySource = [self.lEditSourceTerm]
        arrayMassCoef = [self.lEditMassCoef]
        arrayDamMass = [self.lEditDamMassCoef]
        arrayConservFlux = [self.lEditAlphaXCFlux, self.lEditAlphaCYFlux]
        arrayConvectionFlux = [self.lEditBetaXConvCoef, self.lEditBetaYConvCoef]
        arrayCSource = [self.lEditGammaXCFluxSource, self.lEditGammaYCFluxSource]

        arraylEditsCoefficientsPDE = []
        arraylEditsCoefficientsPDE.append(arrayDiffusionCoeff)
        arraylEditsCoefficientsPDE.append(arrayAbsorption)
        arraylEditsCoefficientsPDE.append(arraySource)
        arraylEditsCoefficientsPDE.append(arrayMassCoef)
        arraylEditsCoefficientsPDE.append(arrayDamMass)
        arraylEditsCoefficientsPDE.append(arrayConservFlux)
        arraylEditsCoefficientsPDE.append(arrayConvectionFlux)
        arraylEditsCoefficientsPDE.append(arrayCSource)

        self.btnDiffusionApply.clicked.connect(lambda: CoefficientsPDE.showMessageBox(self, arrayCmbRowColumns, self.cmbDiffusionCoef, self.allMatrix, arraylEditsCoefficientsPDE, 1))
        self.btnAbsorptionApply.clicked.connect(lambda: CoefficientsPDE.showMessageBox(self, arrayCmbRowColumns, self.cmbDiffusionCoef,self.allMatrix, arraylEditsCoefficientsPDE, 2))
        self.btnSourceApply.clicked.connect(lambda: CoefficientsPDE.showMessageBox(self, arrayCmbRowColumns, self.cmbDiffusionCoef,self.allMatrix, arraylEditsCoefficientsPDE, 3))
        self.btnMassApply.clicked.connect(lambda: CoefficientsPDE.showMessageBox(self, arrayCmbRowColumns, self.cmbDiffusionCoef,self.allMatrix, arraylEditsCoefficientsPDE, 4))
        self.btnDampingApply.clicked.connect(lambda: CoefficientsPDE.showMessageBox(self, arrayCmbRowColumns, self.cmbDiffusionCoef,self.allMatrix, arraylEditsCoefficientsPDE, 5))
        self.btnCFluxApply.clicked.connect(lambda:  CoefficientsPDE.showMessageBox(self, arrayCmbRowColumns, self.cmbDiffusionCoef,self.allMatrix, arraylEditsCoefficientsPDE, 6))
        self.btnConvectionApply.clicked.connect(lambda:  CoefficientsPDE.showMessageBox(self, arrayCmbRowColumns,self.cmbDiffusionCoef, self.allMatrix, arraylEditsCoefficientsPDE, 7))
        self.btnCSourceApply.clicked.connect(lambda:  CoefficientsPDE.showMessageBox(self, arrayCmbRowColumns, self.cmbDiffusionCoef,self.allMatrix, arraylEditsCoefficientsPDE, 8))

        #Open Matrix with Button
        self.btnDiffusionPreview.clicked.connect(lambda: CoefficientsPDE.selectMatrix(self.allMatrix, self.cmbRowDiffusionCoef, 1))
        self.btnAbsorptionPreview.clicked.connect(lambda: CoefficientsPDE.selectMatrix(self.allMatrix, self.cmbAbsorptionRow, 2))
        self.btnSourcePreview.clicked.connect(lambda: CoefficientsPDE.selectMatrix(self.allMatrix, self.cmbSourceRow, 3))
        self.btnMassPreview.clicked.connect(lambda: CoefficientsPDE.selectMatrix(self.allMatrix, self.cmbMassCoefRow, 4))
        self.btnDampingPreview.clicked.connect(lambda: CoefficientsPDE.selectMatrix(self.allMatrix, self.cmbDamMassCoefRow, 5))
        self.btnCFluxPreview.clicked.connect(lambda: CoefficientsPDE.selectMatrix(self.allMatrix, self.cmbCFluxRow, 6))
        self.btnConvectionPreview.clicked.connect(lambda: CoefficientsPDE.selectMatrix(self.allMatrix, self.cmbConvectionRow, 7))
        self.btnCSourcePreview.clicked.connect(lambda: CoefficientsPDE.selectMatrix(self.allMatrix, self.cmbCSourceRow, 8))

        self.btnInitialValuesApply.clicked.connect(lambda:CoefficientsPDE.currentCombMatrix(self, self.CoefficientCheckBoxArray, arrayCmbRowColumns, self.cmbInitialValues))
        

        self.actionOpen.triggered.connect(lambda: FileData.getFileName(self))
        self.actionNew.triggered.connect(lambda: FileData.newFileName(self, CoefficientsPDE.CheckCoefficient(self.CoefficientCheckBoxArray), self.allMatrix, self.cmbRowDiffusionCoef))

    class AllMatrix():
          def __init__(self):
            self.matrix1X1 = Matrix1X1()
            self.matrix2X2 = Matrix2X2()
            self.matrix3X3 = Matrix3X3()
            
            self.matrix2X1 = Matrix2X1()
            self.matrix3X1 = Matrix3X1() 


            self.arrayM1X1 = [self.matrix1X1.lEdit11]
            self.arrayM2X2 = [self.matrix2X2.lEdit11, self.matrix2X2.lEdit12, self.matrix2X2.lEdit21, self.matrix2X2.lEdit22]
            self.arrayM3X3 = [self.matrix3X3.lEdit11, self.matrix3X3.lEdit12, self.matrix3X3.lEdit13, self.matrix3X3.lEdit21, self.matrix3X3.lEdit22, self.matrix3X3.lEdit23, self.matrix3X3.lEdit31, self.matrix3X3.lEdit32, self.matrix3X3.lEdit33]
            self.arrayM2X1 = [self.matrix2X1.lEdit11, self.matrix2X1.lEdit21]
            self.arrayM3X1 = [self.matrix3X1.lEdit11, self.matrix3X1.lEdit21, self.matrix3X1.lEdit31]
            self.arraylEditMatrix = [self.arrayM1X1, self.arrayM2X2, self.arrayM3X3, self.arrayM2X1, self.arrayM3X1]
            

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
