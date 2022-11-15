"""
Created on Wed May 11 13:39:55 2022
@author:ruben.castaneda,
        Pavel Montes,
        Armando Terán https://github.com/ArmandoTeranCastillo,
        Martin Lopez,
        Angel Vargas;
"""

#-*- coding: utf-8 -*-

import array as arr
import os
import sys
from operator import le
from sqlite3 import connect

from PyQt5 import QtWidgets
from PyQt5.QtCore import QObject, Qt
from PyQt5.QtGui import QCloseEvent, QIcon, QPainter
from PyQt5.QtWidgets import (QApplication, QButtonGroup, QCheckBox, QComboBox,
                             QDialog, QGraphicsScene, QGraphicsView, QLabel,
                             QLineEdit, QMainWindow, QMessageBox, QPushButton,
                             QTabWidget, QToolBox, QTreeWidget, QWidget)
from PyQt5.uic import loadUi

import imagen_rc
from Base import *
from canvas.PP import Canvas
from canvas.vis_mpl import figure
from dialogMatrix import *
from interfaz import *
from Modules.Dictionary.DFiles import *
from Modules.FunctionsEF import Initialize
from Modules.LibraryButtons.changeNameM import *
from Modules.LibraryButtons.DeleteMaterial import *
from Modules.LibraryButtons.EditTypeHeatCond import *
from Modules.LibraryButtons.NewMaterial import *
from Modules.LibraryButtons.OpenMaterial import *
from Modules.LibraryButtons.ResetLibrary import *
from Modules.LibraryButtons.SaveAsMaterial import *
from Modules.LibraryButtons.SaveMaterial import *
from Modules.ManageFiles.ManageFiles import *
from Modules.Materials import *
from Modules.Matrix.Matrix import *
from Modules.ModelWizard import *
from Modules.SectionTabs.CoefficientsPDE import *
from Modules.SectionTabs.Conditions import *
from Modules.SectionTabs.ConditionsPDE import *
from Modules.SectionTabs.Geometry import *
from Modules.SectionTabs.MeshSettings import *

app = None

class PropertiesData:
    kappa=[]
    rho=[]
    Cp=[]
    def __init__(self):
        self.kappa = [[-1.0,-1.0],[-1.0,-1.0]]
        self.rho = -1.0
        self.Cp = -1.0


class CanvasGraphicsView(QGraphicsView):
    def __init__(self, editorWindow:QMainWindow, baseModel):
        super(QGraphicsView, self).__init__(baseModel)
        self.editorWindow = editorWindow
        self.setRenderHint(QPainter.Antialiasing)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def getEditorWindow(self):
        return self.editorWindow

    def setCanvasRef(self, canvas:Canvas):
        self.canvas = canvas

    def getEditorWindow(self):
        return self.editorWindow

    # resetea los colores del relleno de las figuras al cambiar las pestañas
    def resetRelleno(self):
        for poly in self.canvas.polyList:
            poly.setBrush(QColor(0,0,0,50))

    # resetea los colores de las lineas al cambiar las pestañas
    def resetLines(self):
        for line in self.canvas.edgeList:
            line.setPen(QPen(QColor(156, 97, 20), 3))

    def mouseDoubleClickEvent(self, event):
        targetItem = None
        if self.scene().selectedItems():
            if self.scene().selectedItems() != targetItem:
                self.resetRelleno()
                targetItem = self.scene().selectedItems()[0]
                polygon = targetItem.polygon()
                targetItem.setBrush(QColor(0,0,250,50))

                if hasattr(targetItem, "qRectObj"):
                    polygon.__setattr__("qRectObj",targetItem.qRectObj)
                    polygon.__setattr__("rotation",targetItem.rotation)
                
            
            Geometry.setData(self.editorWindow.figuresSection.currentWidget(), self.editorWindow.cmbGeometricFigure, polygon)

    def mouseMoveEvent(self, event):
        self.canvas.mouseMoveEvent(event)

class EditorWindow(QMainWindow):
    DataProperties = []
    materialsDataBase = []
    conn = []
    statusLibrary = 0 #0 initial value, 1 new material, 2 copy, 3 changes values


    def __init__(self):
        super(QMainWindow, self).__init__()
        self.app = app
        try:
            with open('Styles\styles.qss', 'r', encoding='utf-8') as file:
                str = file.read()
        except:
            with open('./Styles/styles.qss', 'r', encoding='utf-8') as file:
                str = file.read()
        self.setStyleSheet(str)

        root = os.path.dirname(os.path.realpath(__file__))
        loadUi(os.path.join(root, 'Interfaz.ui'), self)

        self.setMouseTracking(True)

        # Creamos una view en base a ghapModel
        graphicsView = CanvasGraphicsView(self, self.ghapModel)

        # Inicializamos la escena de dibujo
        scene = QGraphicsScene()
        scene.mplWidget = self.ghapMesh
        graphicsView.setScene(scene)
        # Inicializamos una instancia al materials
        self.material = Materials()
        # Inicializamos una instancia al materials
        self.coefficientsPDE = CoefficientsPDE()
        #Inicializamos una instancia del modelwizard
        self.modelwizard = ModelWizard()
        #Inicializamos una instancia de allnewmatrix
        self.allnewmatrix = allNewMatrix()
        # Inicializamos el Canvas
        self.canvas = Canvas(graphicsView)
        self.canvas.setStyleSheet("background-color: transparent;")
        self.canvas.resize(self.ghapModel.width(), self.ghapModel.height())
        scene.addWidget(self.canvas)
        graphicsView.setCanvasRef(self.canvas)

        self.return_g = False

        self.dMatrix = dialogMatrix(1)
        self.dVector = dialogVector(1)

        if directory["dir"] == "":
            self.actionSaves.setEnabled(False)
            self.actionSave_As.setEnabled(False)
            self.actionClose.setEnabled(False)

        # LIBRARY---------------------------------------------
        # LIBRARY BUTTONS
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
        self.cmbNameMaterials.currentIndexChanged.connect(lambda: changeNameMaterials.change_cmbNameMaterials(self)) # Function i shd use
        self.edtTermalConductivityIsotropicProperties.editingFinished.connect(lambda: EditTypeHeatCond.exit_edtTermalConductivityIsotropicProperties(self))
        self.edtTermalConductivityAnisotropicPropertiesA11.editingFinished.connect(lambda: EditTypeHeatCond.exit_edtTermalConductivityAnisotropicPropertiesA11(self))
        self.edtTermalConductivityAnisotropicPropertiesA12.editingFinished.connect(lambda: EditTypeHeatCond.exit_edtTermalConductivityAnisotropicPropertiesA12(self))
        self.edtTermalConductivityAnisotropicPropertiesA21.editingFinished.connect(lambda: EditTypeHeatCond.exit_edtTermalConductivityAnisotropicPropertiesA21(self))
        self.edtTermalConductivityAnisotropicPropertiesA22.editingFinished.connect(lambda: EditTypeHeatCond.exit_edtTermalConductivityAnisotropicPropertiesA22(self))
        self.edtRhoProperties.editingFinished.connect(lambda: EditTypeHeatCond.exit_edtRhoProperties(self))
        self.edtCpProperties.editingFinished.connect(lambda: EditTypeHeatCond.exit_edtCpProperties(self))
        self.addMaterials()
        self.addMaterialsComboBox()

        # MENU-------------------------------------------------------------------------
        #Guardar la direccion de las paginas del programa en un arreglo
        self.tabs = Initialize.takeModelWizardTabs(self)

        # MODEL WIZARD-------------------------------------------------------------------------
        # tabWidgetMenu
        self.itemSpace = self.treeModelWizard.findItems("Space Dimension", Qt.MatchExactly| Qt.MatchRecursive, 0)
        self.item2D = self.treeModelWizard.findItems("2D", Qt.MatchExactly| Qt.MatchRecursive, 0)
        self.itemPhysics = self.treeModelWizard.findItems("Physics", Qt.MatchExactly| Qt.MatchRecursive, 0)
        self.itemHeat = self.treeModelWizard.findItems("Heat Transfer", Qt.MatchExactly| Qt.MatchRecursive, 0)
        self.itemMath = self.treeModelWizard.findItems("Mathematics", Qt.MatchExactly| Qt.MatchRecursive, 0)
        self.itemSolids = self.treeModelWizard.findItems("Heat Transfer in Solids", Qt.MatchExactly| Qt.MatchRecursive, 0)
        self.itemFluids = self.treeModelWizard.findItems("Heat Transfer in Fluids", Qt.MatchExactly| Qt.MatchRecursive, 0)
        self.itemPDE = self.treeModelWizard.findItems("Coefficient form PDE", Qt.MatchExactly| Qt.MatchRecursive, 0)

        ModelWizard.hideInitialTabs(self.tabs, self.tabWidgetMenu)
        self.treeModelWizard.itemDoubleClicked.connect(lambda: ModelWizard.currentTreeItem(self, self.treeModelWizard.currentItem(), self.treeModelWizard.currentColumn(), self.canvas))
        self.btnModelWizardApply.clicked.connect(lambda: ModelWizard.currentTreeWidgetConfiguration(self, self.tabs, self.tabWidgetMenu, self.canvas))
        self.inputDepedentVarial.setEnabled(False)
        self.btnModelWizardReset.setEnabled(False)
        self.btnModelWizardApply.setEnabled(False)

        # SECTION TABS-------------------------------------------------------------------------
        # GEOMETRY
        #Almacenar la direccion de los widgets en un arreglo
        arrayFiguresSection = Initialize.takeGeometryWidgets(self)
        #Cada vez que cambie el QComboBox, mandar a llamar la funcion, no sin antes llamarla una sola vez 
        self.figuresSection.show() 

        # Esta funcion revisara si el combo box tiene modo Mouse/Data, en cada caso va a tener una accion 
        # Mouse: Ocultara los datos del toolbox "self.figuresSection"
        # Data: Mostrara los datos de la figura seleccionada en el momento
        Geometry.currentTypeDrawing(self.figuresSection, self.cmbConstructionBy, self.cmbGeometricFigure, arrayFiguresSection)
        self.cmbConstructionBy.currentIndexChanged.connect(lambda:
            Geometry.currentTypeDrawing(self.figuresSection, self.cmbConstructionBy, self.cmbGeometricFigure, arrayFiguresSection))


        self.cmbGeometricFigure.currentIndexChanged.connect(lambda:
            Geometry.currentTypeDrawing(self.figuresSection, self.cmbConstructionBy, self.cmbGeometricFigure, arrayFiguresSection))
        self.btnGeometryReset.clicked.connect(lambda: Geometry.resetData(self.figuresSection.currentWidget(), self.cmbGeometricFigure))
        self.btnGeometryApply.clicked.connect(lambda: Geometry.getData(self.figuresSection.currentWidget(), self.cmbGeometricFigure, scene.selectedItems(), self.canvas))
        self.sbNumPoints.valueChanged.connect(lambda: Geometry.updateTable(self.figuresSection.currentWidget(), self.canvas))

        # Boton de union
        self.btnUnion.clicked.connect(lambda:
            Geometry.unionClicked(self))
        # Boton de insersection
        self.btnIntersection.clicked.connect(lambda:
            Geometry.intersectionClicked(self))
        # Boton de diferencia
        self.btnDifference.clicked.connect(lambda: 
            Geometry.diferenceClicked(self))
        # Boton de ayuda
        self.btnBooleansPartitionsHelp.clicked.connect(lambda: 
            Geometry.helpClicked(self))

        self.btnGeometryHelp.clicked.connect(lambda: Geometry.helpClicked2(self))

        self.btnDeletePolygon.clicked.connect(lambda: Geometry.borrar(self))

        self.btnBoleansAndPartitionsApply.clicked.connect(lambda: Geometry.mode2(self))
        self.btnBoleansAndPartitionsCancel.clicked.connect(lambda: Geometry.mode2Cancel(self))

        # Mesh and Settings Study
        self.ghapMesh.hide()
        self.tabWidgetMenu.currentChanged.connect(lambda: MeshSettings.currentShowMeshTab(self.tabWidgetMenu.tabText(self.tabWidgetMenu.currentIndex()), self.ghapMesh))
        self.cmbConstructionBy.activated.connect(self.do_something)
        self.cmbTypeOfConstruction.activated.connect(self.changeMode)
        self.cmbGeometricFigure.activated.connect(self.changeDrawMode)
        self.tabWidgetMenu.currentChanged.connect(self.changeTab)
        self.btnMeshApply.clicked.connect(self.meshSettings)



        # CONDITIONS PDE
        #Almacenar la direccion de los widgets en un arreglo
         # Obtiene la scena del canvas
        scen = self.canvas.getParentView().scene()
        scen.changed.connect(lambda:
            Conditions.reloadEdges(self.canvas, self.lWBoundarysPDE))
        # Cuando se haga click en una figura
        self.lWBoundarysPDE.itemClicked.connect(lambda:
            ConditionsPDE.currentElementSelectElementPDE(self.lWBoundarysPDE.currentItem(), self.canvas, self.lblFigureSelected))


        arrayTypeofConditionsPDESection = Initialize.takeTypeConditionsPDEWidgets(self)

        #Al presionar el checkbox de Zero Flux, bloquear los items que no sean Zero Flux
        self.chkZeroFlux.stateChanged.connect(lambda: ConditionsPDE.turnZeroFlux(self, arrayTypeofConditionsPDESection))

        #Al presionar el boton de Dirichlet Apply, insertar la informacion
        #Junto con la variable independiente seleccionada
        self.btnDirichletApply.clicked.connect(lambda: ConditionsPDE.applyConditionVariable(self, self.cmbDirichletCondition))
        #Al presionar el boton de Boundary Apply, insertar la informacion
        #Junto con la variable independiente seleccionada
        self.btnBFluxApply.clicked.connect(lambda: ConditionsPDE.applyConditionVariable(self, self.cmbBoundaryFluxCondition))

        # COEFFICIENTS PDE
        self.cmbCoefficientSelection.currentIndexChanged.connect(lambda:
            self.coefficientsPDE.currentCoefficentSelection(self))

        self.CoefficentForM.hide()
        self.lWDomainsPDE.itemClicked.connect(lambda:
            self.coefficientsPDE.currentItemDomainPDESelected(self))
        #Almacenar los QCheckBox en un solo arreglo
        self.CoefficientCheckBoxArray = Initialize.takeCoefficientPDECheckBox(self)
        #Almacenar los widgets del QToolBox en un arreglo
        self.arrayCoeffMSection = Initialize.takeCoefficientPDEWidgets(self)[0]
        #Almacenar el texto de los widgets del QToolBox en un arreglo
        self.arrayCheckNameCoeffM = Initialize.takeCoefficientPDEWidgets(self)[1]
        #Almacenar las direcciones de los LineEdits de la seccion Diffusion Coefficient en un arreglo
        arrayDiffusionCoeff = Initialize.takeDiffusionCoefficientLineEdits(self)


        #Cada vez que cambie el QComboBox, Llamar la funcion que define el tipo de insercion de valores; (Isotropicos o Anisotropicos)
        #No sin antes mandar a llamar la funcion una sola vez
        self.coefficientsPDE.currentDiffusionCoef(self.cmbDiffusionCoef,  arrayDiffusionCoeff)
        self.cmbDiffusionCoef.currentIndexChanged.connect(lambda: self.coefficientsPDE.currentDiffusionCoef(self.cmbDiffusionCoef,  arrayDiffusionCoeff))
        self.lEditDiffusionCoef12.textChanged.connect(lambda: self.coefficientsPDE.currentTextSimmetry(self, self.cmbDiffusionCoef, arrayDiffusionCoeff))

        #Cada vez que cambien el QComboBox, llamar la funcion que activa los widgets elegidos por el usuario
        self.coefficientsPDE.clearCoefficientTbox(self.CoefficentForM, self.arrayCoeffMSection, self.arrayCheckNameCoeffM)
        self.btnCoefficientsApply.clicked.connect(lambda:
            self.coefficientsPDE.currentCoefficientForM(self.CoefficentForM, self.coefficientsPDE.CheckCoefficient(self.CoefficientCheckBoxArray), self.arrayCoeffMSection, self.arrayCheckNameCoeffM))

        #Almacenar los QComboxBox de Fila y Columna en un arreglo 
        self.arrayCmbRowColumns = Initialize.takeCoefficientPDECombobox(self)

        self.btnCoefficientsHelp.clicked.connect(lambda:
            self.coefficientsPDE.showMatrixInfo())

        #Almacenar los QLineEdits de cada seccion en un arreglo
        self.arraylEditsCoefficientsPDE = Initialize.takeCoefficientPDELineEdits(self, arrayDiffusionCoeff)

        #Cada vez que el boton de "Apply" en una de las secciones se presione, mandar a llamar la funcion para:
        #Almacenar los datos obtenidos de los QLineEdits y mostrarlos en una matriz
        #Las dimensiones de la matriz dependeran del numero de variables elegidas por el usuario
        self.btnDiffusionApply.clicked.connect(lambda: self.dMatrix.marklineEdit(self.cmbRowDiffusionCoef, self.cmbColumnDiffusionCoef, initialValues["noVariables"], self.arraylEditsCoefficientsPDE, 1, self.cmbDiffusionCoef, self))
        self.btnAbsorptionApply.clicked.connect(lambda: self.dMatrix.marklineEdit(self.cmbAbsorptionRow, self.cmbAbsorptionColumn, initialValues["noVariables"], self.arraylEditsCoefficientsPDE, 2, self.cmbDiffusionCoef, self))
        self.btnSourceApply.clicked.connect(lambda: self.dVector.marklineEdit(self.cmbSourceRow, initialValues["noVariables"], self.arraylEditsCoefficientsPDE, 3, self))
        self.btnMassApply.clicked.connect(lambda: self.dMatrix.marklineEdit(self.cmbMassCoefRow, self.cmbMassCoefColumn, initialValues["noVariables"], self.arraylEditsCoefficientsPDE, 4, self.cmbDiffusionCoef, self))
        self.btnDampingApply.clicked.connect(lambda: self.dMatrix.marklineEdit(self.cmbDamMassCoefRow, self.cmbDamMassCoefColumn, initialValues["noVariables"], self.arraylEditsCoefficientsPDE, 5, self.cmbDiffusionCoef, self))
        self.btnCFluxApply.clicked.connect(lambda:  self.dMatrix.marklineEdit(self.cmbCFluxRow, self.cmbCFluxColumn, initialValues["noVariables"], self.arraylEditsCoefficientsPDE, 6, self.cmbDiffusionCoef, self))
        self.btnConvectionApply.clicked.connect(lambda:  self.dMatrix.marklineEdit(self.cmbConvectionRow, self.cmbConvectionColumn, initialValues["noVariables"], self.arraylEditsCoefficientsPDE, 7, self.cmbDiffusionCoef, self))
        self.btnCSourceApply.clicked.connect(lambda:  self.dVector.marklineEdit(self.cmbCSourceRow, initialValues["noVariables"], self.arraylEditsCoefficientsPDE, 8, self))
  

        #Cada vez que el boton de "Preview" en una de la secciones se presione, mandar a llamar la funcion para:
        #Mostrar la matriz con los datos ya almacenados de los QlineEdits
        self.btnDiffusionPreview.clicked.connect(lambda: self.dMatrix.showMeDiffusion(allNewMatrix.matrixCoefficientPDE[domains["domain"]][0], self.arrayCmbRowColumns[0]))
        self.btnAbsorptionPreview.clicked.connect(lambda: self.dMatrix.showMe(allNewMatrix.matrixCoefficientPDE[domains["domain"]][1], self.arrayCmbRowColumns[1]))
        self.btnSourcePreview.clicked.connect(lambda: self.dVector.showMe(allNewMatrix.vectorCoefficientPDE[domains["domain"]][0][0], self.arrayCmbRowColumns[2]))
        self.btnMassPreview.clicked.connect(lambda: self.dMatrix.showMe(allNewMatrix.matrixCoefficientPDE[domains["domain"]][2], self.arrayCmbRowColumns[3]))
        self.btnDampingPreview.clicked.connect(lambda: self.dMatrix.showMe(allNewMatrix.matrixCoefficientPDE[domains["domain"]][3], self.arrayCmbRowColumns[4]))
        self.btnCFluxPreview.clicked.connect(lambda: self.dMatrix.showMe(allNewMatrix.matrixCoefficientPDE[domains["domain"]][4], self.arrayCmbRowColumns[5]))
        self.btnConvectionPreview.clicked.connect(lambda: self.dMatrix.showMe(allNewMatrix.matrixCoefficientPDE[domains["domain"]][5], self.arrayCmbRowColumns[6]))
        self.btnCSourcePreview.clicked.connect(lambda: self.dVector.showMe(allNewMatrix.vectorCoefficientPDE[domains["domain"]][1][0], self.arrayCmbRowColumns[7]))

        #Cada vez que se presione el boton de "Reset" en una de las secciones, se mandará a llamar un función para:
        #Limpiar todos los datos de la matriz
        self.btnDiffusionReset.clicked.connect(lambda: self.dMatrix.clearMatrixData(allNewMatrix.matrixCoefficientPDE))
        self.btnAbsorptionReset.clicked.connect(lambda: self.dMatrix.clearMatrixData(allNewMatrix.matrixCoefficientPDE))
        self.btnSourceReset.clicked.connect(lambda: self.dMatrix.clearMatrixData(allNewMatrix.vectorCoefficientPDE))
        self.btnMassReset.clicked.connect(lambda: self.dMatrix.clearMatrixData(allNewMatrix.matrixCoefficientPDE))
        self.btnDampingReset.clicked.connect(lambda: self.dMatrix.clearMatrixData(allNewMatrix.matrixCoefficientPDE))
        self.btnCFluxReset.clicked.connect(lambda: self.dMatrix.clearMatrixData(allNewMatrix.matrixCoefficientPDE))
        self.btnConvectionReset.clicked.connect(lambda: self.dMatrix.clearMatrixData(allNewMatrix.matrixCoefficientPDE))
        self.btnCSourceReset.clicked.connect(lambda: self.dMatrix.clearMatrixData(allNewMatrix.vectorCoefficientPDE))

        self.btnOpenMatrix_1.clicked.connect(lambda: self.dMatrix.showMeDiffusion(allNewMatrix.matrixCoefficientPDE[domains["domain"]][0], self.arrayCmbRowColumns[0]))
        self.btnOpenMatrix_2.clicked.connect(lambda: self.dMatrix.showMe(allNewMatrix.matrixCoefficientPDE[domains["domain"]][1], self.arrayCmbRowColumns[1]))
        self.btnOpenMatrix_3.clicked.connect(lambda: self.dVector.showMe(allNewMatrix.vectorCoefficientPDE[domains["domain"]][0][0], self.arrayCmbRowColumns[2]))
        self.btnOpenMatrix_4.clicked.connect(lambda: self.dMatrix.showMe(allNewMatrix.matrixCoefficientPDE[domains["domain"]][2], self.arrayCmbRowColumns[3]))
        self.btnOpenMatrix_5.clicked.connect(lambda: self.dMatrix.showMe(allNewMatrix.matrixCoefficientPDE[domains["domain"]][3], self.arrayCmbRowColumns[4]))
        self.btnOpenMatrix_6.clicked.connect(lambda: self.dMatrix.showMe(allNewMatrix.matrixCoefficientPDE[domains["domain"]][4], self.arrayCmbRowColumns[5]))
        self.btnOpenMatrix_7.clicked.connect(lambda: self.dMatrix.showMe(allNewMatrix.matrixCoefficientPDE[domains["domain"]][5], self.arrayCmbRowColumns[6]))
        self.btnOpenMatrix_8.clicked.connect(lambda: self.dVector.showMe(allNewMatrix.vectorCoefficientPDE[domains["domain"]][1][0], self.arrayCmbRowColumns[7]))

        # MATERIALS--------------------------------------------------------------------------------------------------
        #Almacenar los QlineEdtis de la pestaña MATERIALS en una arreglo
        inputKArray = Initialize.takeInputLineEditsMaterials(self)

        self.material.changeTableCeld(self)

        # Ocultar los botones para que no se puedan usar desde el inicio
        Initialize.hideMaterialsButtons(self)

        #Cada vez que cambie el QComboBox, llamar la funcion que defina el tipo de insercion de datos (Isotropico o Anisotropico)
        self.material.currentHeatConduction(self.cmbHeatConduction, inputKArray)
        self.inputKD2.textChanged.connect(lambda: self.material.currentTextSimmetry(self.cmbHeatConduction, inputKArray))
        self.cmbHeatConduction.currentIndexChanged.connect(lambda: self.material.currentHeatConduction(self.cmbHeatConduction, inputKArray))

        self.cmbSelection.currentIndexChanged.connect(lambda: 
            self.material.selectionType(self))
        # Se aplica los cambios del poligono seleccionado
        self.btnMaterialApply.clicked.connect(lambda:
            self.material.applyMaterialChanges(self))
        self.btnMaterialsReset.clicked.connect(lambda:
            self.material.resetMaterialChanges(self))


        # Actualiza las figuras que son creadas en la pestaña materials
        scene.changed.connect(lambda:
            self.material.currentDomains(self, self.listDomains, self.canvas, self.tboxMaterialsConditions, self.tableDomainsMaterials))

        # Actualiza las figuras que son creadas en la pestaña coefficent s PDE
        scene.changed.connect(lambda:
            self.material.currentDomains(self, self.lWDomainsPDE, self.canvas, self.tboxMaterialsConditions, self.tableDomainsMaterials))


        # Sirve para mostar los datos que son creados
        self.btnMaterialsHelp.clicked.connect( lambda:
            self.material.showData())

        # Evento cuando se hace click a un elemento de la pestaña materials
        self.listDomains.itemClicked.connect(lambda:
            self.material.currentDomainSelected( self.listDomains, self))

        self.lWDomainsPDE.itemClicked.connect(lambda:
            self.coefficientsPDE.currentDomainSelected(self, self.lWDomainsPDE))

        # Sirve para esconder o mostar los elementos de los materiales
        self.material.currentMaterialSelection(self.cmbMaterial, self)
        self.cmbMaterial.currentIndexChanged.connect(lambda:
            self.material.currentMaterialSelection(self.cmbMaterial, self))

        # CONDITIONS---------------------------------------------------------------------------------------------
        #Almacenar los widgets del QToolBox en un arreglo
        arrayTypeofConditionSection = Initialize.takeToolBoxConditionWidgets(self)
        # Esta funcion marca con color rojo, el lado seleccionado
        self.lWBoundarys.itemClicked.connect(lambda: Conditions.currentElementSelectListWidgets(  self.lWBoundarys.currentItem(), self.canvas, self.lblFigureSelected))
        #Cada vez que cambie el QComboBox, llamar la funcion que active la seccion elegida por el usuario
        #No sin antes llamar primero una sola vez

        scene.changed.connect(lambda:
            Conditions.reloadEdges(self.canvas, self.lWBoundarys))


        #Cada vez que cambie el QComboBox, llamar la funcion que active la seccion elegida por el usuario
        #No sin antes llamar primero una sola vez
        # Conditions.currentTypeCondition(self.cmbTypeCondition, self.toolBoxTypeOfCondition, arrayTypeofConditionSection)
        # self.cmbTypeCondition.currentIndexChanged.connect(lambda: Conditions.currentTypeCondition(self.cmbTypeCondition, self.toolBoxTypeOfCondition, arrayTypeofConditionSection))


        # MENU BAR (MANAGE FILES)------------------------------------------------------------------------------
        #Cada vez que se presione la pestaña "Open", abrir una ventana para ejecutar un archivo EXCEL
        self.actionOpen.triggered.connect(lambda: FileData.getFileName(self, self.material, self.canvas))
        #Cada vez que se presione la pestaña "New", abrir una ventana para crear un archivo EXCEL
        self.actionNew.triggered.connect(lambda: FileData.newFileName(self, self.material, self.canvas))
        #Cada vez que se presione la pestaña "Save", guardar el archivo EXCEL cargado
        self.actionSaves.triggered.connect(lambda: FileData.updateFile(self, self.material, self.canvas))
        #Cada vez que se presione la pestaña "Save As", guardar un archivo excel en una instancia nueva
        self.actionSave_As.triggered.connect(lambda: FileData.saveAsFile(self, self.material, self.canvas))
        #Cada vez que se presiones la pestaña "Close", cerrar el archivo cargado y resetear la configuracion del programa
        self.actionClose.triggered.connect(lambda: FileData.resetFile(self, self.material, self.canvas))

        #Funcion para poner el numero de variables dependientes en el QLineEdit
        Matrix.currentInitialVariable(self, self.allnewmatrix)
        #Boton par resetear las dimensiones de las matrices a 1
        self.btnModelWizardReset.clicked.connect(lambda: Matrix.resetMatrix(self))

        #Mostrar el dato de determinada casilla de la matrix, segun los QComboBox de cada seccion
        self.cmbRowDiffusionCoef.activated.connect(lambda: Update.currentData(self, 1))
        self.cmbColumnDiffusionCoef.activated.connect(lambda: Update.currentData(self, 1))
        self.cmbAbsorptionRow.activated.connect(lambda: Update.currentData(self, 2))
        self.cmbAbsorptionColumn.activated.connect(lambda: Update.currentData(self, 2))
        self.cmbAbsorptionRow.activated.connect(lambda: Update.currentData(self, 2))
        self.cmbSourceRow.activated.connect(lambda: Update.currentData(self, 3))
        self.cmbMassCoefRow.activated.connect(lambda: Update.currentData(self, 4))
        self.cmbMassCoefColumn.activated.connect(lambda: Update.currentData(self, 4))
        self.cmbDamMassCoefRow.activated.connect(lambda: Update.currentData(self, 5))
        self.cmbDamMassCoefColumn.activated.connect(lambda: Update.currentData(self, 5))
        self.cmbCFluxRow.activated.connect(lambda: Update.currentData(self, 6))
        self.cmbCFluxColumn.activated.connect(lambda: Update.currentData(self, 6))
        self.cmbConvectionRow.activated.connect(lambda: Update.currentData(self, 7))
        self.cmbConvectionColumn.activated.connect(lambda: Update.currentData(self, 7))
        self.cmbCSourceRow.activated.connect(lambda:Update.currentData(self, 8))
        

        self.cmbGeneralStudie.setEnabled(False)
        self.tboxModelWizard.hide()
        self.lblGeometricFigure.hide()
        self.cmbGeometricFigure.hide()
        self.lblTypeConstruction.hide()
        self.cmbTypeOfConstruction.hide()
        self.figuresSection.hide()
        self.btnGeometryApply.hide()
        self.btnGeometryReset.hide()
        self.btnGeometryHelp.hide()
        self.toolBoxBooleansAndPartitions.hide()
        


        self.canvas.mode = "None"   

    def getEditorWindow(self):
        return self.editorWindow

    def resetConstructionBy(self):
        self.cmbConstructionBy.setCurrentIndex(0)
        self.do_something()

    # esconde todos los widgets de la ventana geometry
    def hideAll(self):
        self.lblGeometricFigure.hide()
        self.cmbGeometricFigure.hide()
        self.lblTypeConstruction.hide()
        self.cmbTypeOfConstruction.hide()
        self.figuresSection.hide()
        self.btnGeometryApply.hide()
        self.btnGeometryReset.hide()
        self.btnGeometryHelp.hide()
        self.toolBoxBooleansAndPartitions.hide()

    # Funcion que se ejecuta al cambiar de pestaña
    def do_something(self):
        self.btnUnion.setEnabled(True)
        self.btnDeletePolygon.setEnabled(True)
        self.btnIntersection.setEnabled(True)
        self.btnDifference.setEnabled(True)
        # Si el texto en el combo box esta vacio esconde todo
        if(self.cmbConstructionBy.currentText() == ""):
            self.canvas.mode = "None"
            self.canvas.enablePolygonSelect(False)
            self.hideAll()
        # Si el texto en el combo box de modo es data muestra los widgets para data y habilita la seleccion de poligonos
        if(self.cmbConstructionBy.currentText() == "Data"):
            self.canvas.mode = "Arrow"
            self.canvas.enablePolygonSelect()
            self.toolBoxBooleansAndPartitions.hide()
            self.btnGeometryApply.show()
            self.btnGeometryReset.show()
            self.btnGeometryHelp.show()
            self.figuresSection.show()
            self.lblGeometricFigure.show()
            self.cmbGeometricFigure.show()
            self.lblTypeConstruction.show()
            self.cmbTypeOfConstruction.show()
        # Si el texto en el combo box de modo es mouse muestra los widgets para data y deshabilita la seleccion de poligonos
        if(self.cmbConstructionBy.currentText() == "Mouse"):
            # Si el texto del combox de dibujo es polygon cambia el modo del camvas a dibujar poligono
            # deshabilita la seleccion de poligonos y muestra los widgets para el dibujado de poligonos
            if(self.cmbGeometricFigure.currentText() == "Polygon"):
                self.canvas.mode = "Draw poly"
                self.canvas.enablePolygonSelect(False)
                self.hideAll()
                self.lblGeometricFigure.show()
                self.cmbGeometricFigure.show()
                self.lblTypeConstruction.show()
                self.cmbTypeOfConstruction.show()
            # Si el texto del combox de dibujo es square cambia el modo del camvas a dibujar cuadrado
            # deshabilita la seleccion de poligonos y muestra los widgets para el dibujado de cuadrados
            if(self.cmbGeometricFigure.currentText() == "Square"):
                self.canvas.mode = "Draw rect"
                self.canvas.enablePolygonSelect(False)
                self.hideAll()
                self.lblGeometricFigure.show()
                self.cmbGeometricFigure.show()
                self.lblTypeConstruction.show()
                self.cmbTypeOfConstruction.show()
        # Si el texto en el combo box de modo es Combination muestra los widgets para combination y deshabilita la seleccion de poligonos
        if(self.cmbConstructionBy.currentText() == "Combination"):
                self.canvas.mode = "Match points"
                self.canvas.enablePolygonSelect(False)
                self.hideAll()
                self.lblGeometricFigure.show()
                self.cmbGeometricFigure.show()
                self.lblTypeConstruction.show()
                self.cmbTypeOfConstruction.show()
        # Si el texto en el combo box de modo es Booleans and partitions muestra los widgets para Booleans and partitions y deshabilita la seleccion de poligonos
        if(self.cmbConstructionBy.currentText() == "Booleans and partitions"):
            self.canvas.mode = "Arrow"
            self.canvas.enablePolygonSelect()
            self.hideAll()
            self.toolBoxBooleansAndPartitions.show()

    # funcion que se llama cuando cambias de modo en el combobox de dibujo y habilita o deshabilita la seleccion de figuras
    def changeDrawMode(self):
        if(self.cmbConstructionBy.currentText() == "Data"):
            self.canvas.mode = "Arrow"
            self.canvas.enablePolygonSelect()
        if(self.cmbConstructionBy.currentText() == "Mouse"):
            if(self.cmbGeometricFigure.currentText() == "Polygon"):
                self.canvas.mode = "Draw poly"
                self.canvas.enablePolygonSelect(False)
            if(self.cmbGeometricFigure.currentText() == "Square"):
                self.canvas.mode = "Draw rect"
                self.canvas.enablePolygonSelect(False)
        if(self.cmbConstructionBy.currentText() == "Combination"):
                self.canvas.mode = "Match points"
                self.canvas.enablePolygonSelect(False)

    def changeMode(self):
        if(self.cmbTypeOfConstruction.currentText() == "Solid"):
            self.canvas.holeMode = False
        else:
           self.canvas.holeMode = True

    # resetea los colores del relleno de las figuras al cambiar las pestañas
    def resetRelleno(self):
        for poly in self.canvas.polyList:
            poly.setBrush(QColor(0,0,0,50))

    # resetea los colores de las lineas al cambiar las pestañas
    def resetLines(self):
        for line in self.canvas.edgeList:
            line.setPen(QPen(QColor(156, 97, 20), 3))
    
    # R
    def resetFigureValue(self):
        self.lblFigureSelected.setText("")

    # se encarga de esconder y mostrar los elementos de las pestañas y resetear el color del relleno y lineas
    def changeTab(self):
        self.resetLines()
        self.resetRelleno()
        self.resetFigureValue()
        self.CoefficentForM.hide()
        self.tboxMaterialsConditions.hide()
        self.cmbMaterial.hide()
        self.lblMaterial.hide()
        self.cmbSelection.setCurrentIndex(0)
        self.cmbCoefficientSelection.setCurrentIndex(0)
        if(self.tabWidgetMenu.tabText(self.tabWidgetMenu.currentIndex())) == "Geometry":
            if(self.cmbConstructionBy.currentText() == "Data"):
                self.canvas.mode = "Arrow"
                self.canvas.enablePolygonSelect()
                self.toolBoxBooleansAndPartitions.show()
                self.btnGeometryApply.show()
                self.btnGeometryReset.show()
                self.btnGeometryHelp.show()
            elif(self.cmbConstructionBy.currentText() == "Mouse"):
                if(self.cmbGeometricFigure.currentText() == "Polygon"):
                    self.canvas.mode = "Draw poly"
                    self.canvas.enablePolygonSelect(False)
                    self.toolBoxBooleansAndPartitions.hide()
                    self.btnGeometryApply.hide()
                    self.btnGeometryReset.hide()
                    self.btnGeometryHelp.hide()
                elif(self.cmbGeometricFigure.currentText() == "Square"):
                    self.canvas.mode = "Draw rect"
                    self.canvas.enablePolygonSelect(False)
                    self.toolBoxBooleansAndPartitions.hide()
                    self.btnGeometryApply.hide()
                    self.btnGeometryReset.hide()
                    self.btnGeometryHelp.hide()
            elif(self.cmbConstructionBy.currentText() == "Combination"):
                self.canvas.mode = "Match points"
                self.canvas.enablePolygonSelect(False)
                self.toolBoxBooleansAndPartitions.hide()
                self.btnGeometryApply.hide()
                self.btnGeometryReset.hide()
                self.btnGeometryHelp.hide()

    # elType define la figura del mallado, 2 es para triangulos, 3 es para cuadrilateros
    # elSizeFactor define los grados de libertad del mallado, mientras mas grados tenga la figura será mas pequeña
    def meshSettings(self):
        if(self.cmbElementType.currentText()=="Triangle"):
            self.canvas.elType = 2
        if(self.cmbElementType.currentText()=="Quadrangle"):
            self.canvas.elType = 3
        if(self.cmbElementSize.currentText()=="Finer"):
            self.canvas.elSizeFactor = 10
        if(self.cmbElementSize.currentText()=="Fine"):
            self.canvas.elSizeFactor = 15
        if(self.cmbElementSize.currentText()=="Normal"):
            self.canvas.elSizeFactor = 25
        if(self.cmbElementSize.currentText()=="Coarse"):
            self.canvas.elSizeFactor = 35
        if(self.cmbElementSize.currentText()=="Coarser"):
            self.canvas.elSizeFactor = 45

        self.canvas.showMesh()

    #DataBaseTools

    def addMaterialsComboBox(self):
        for i in range(len(self.materialsDataBase)):
            self.cmbMaterial.addItem(self.materialsDataBase[i][1])

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