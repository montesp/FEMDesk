"""
Created on Wed May 11 13:39:55 2022
@author:ruben.castaneda,
        Pavel Montes,
        Armando Terán,
        Martin Lopez,
        Angel Vargas;
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
from Modules.SectionTabs.MeshSettings import *
from Modules.ModelWizard import *
from Modules.LibraryButtons.DeleteMaterial import *
from Modules.LibraryButtons.OpenMaterial import *
from Modules.LibraryButtons.ResetLibrary import *
from Modules.LibraryButtons.SaveAsMaterial import *
from Modules.LibraryButtons.SaveMaterial import *
from Modules.LibraryButtons.NewMaterial import *
from Modules.LibraryButtons.changeNameM import *
from Modules.LibraryButtons.EditTypeHeatCond import *
from PyQt5.QtWidgets import QGraphicsScene
from canvas.PP import Canvas
from Modules.Matrix import *
from Modules.ManageFiles import *
from Modules.Dictionary.DFiles import *
from dialogMatrix import *




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

    def setCanvasRef(self, canvas:Canvas):
        self.canvas = canvas

    def mouseDoubleClickEvent(self, event):
        if self.scene().selectedItems():
            Geometry.setTableData(self.editorWindow.figuresSection.currentWidget(), self.editorWindow.cmbGeometricFigure, self.scene().selectedItems()[0].polygon())

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
        self.cmbNameMaterials.currentIndexChanged.connect(lambda: changeNameMaterials.change_cmbNameMaterials(self))
        self.edtTermalConductivityIsotropicProperties.editingFinished.connect(lambda: EditTypeHeatCond.exit_edtTermalConductivityIsotropicProperties(self))
        self.edtTermalConductivityAnisotropicPropertiesA11.editingFinished.connect(lambda: EditTypeHeatCond.exit_edtTermalConductivityAnisotropicPropertiesA11(self))
        self.edtTermalConductivityAnisotropicPropertiesA12.editingFinished.connect(lambda: EditTypeHeatCond.exit_edtTermalConductivityAnisotropicPropertiesA12(self))
        self.edtTermalConductivityAnisotropicPropertiesA21.editingFinished.connect(lambda: EditTypeHeatCond.exit_edtTermalConductivityAnisotropicPropertiesA21(self))
        self.edtTermalConductivityAnisotropicPropertiesA22.editingFinished.connect(lambda: EditTypeHeatCond.exit_edtTermalConductivityAnisotropicPropertiesA22(self))
        self.edtRhoProperties.editingFinished.connect(lambda: EditTypeHeatCond.exit_edtRhoProperties(self))
        self.edtCpProperties.editingFinished.connect(lambda: EditTypeHeatCond.exit_edtCpProperties(self))
        self.addMaterials()

        # MENU-------------------------------------------------------------------------
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

        # MODEL WIZARD-------------------------------------------------------------------------
        # tabWidgetMenu
        ModelWizard.hideInitialTabs(self.tabs, self.tabWidgetMenu)
        self.treeModelWizard.currentItemChanged.connect(lambda: ModelWizard.currentTreeItem(self, self.treeModelWizard.currentItem(), self.treeModelWizard.currentColumn(), self.tabs, self.tabWidgetMenu))
        self.cmbGeneralStudie.hide()
        self.lblGeneralStudie.hide()
        self.tboxModelWizard.hide()
        # SECTION TABS-------------------------------------------------------------------------
        # GEOMETRY


        arrayFiguresSection = [] #Almacenar la direccion de los widgets en un arreglo
        for i in range(self.figuresSection.count()):
            arrayFiguresSection.append(self.figuresSection.widget(i))

        for i in range(self.figuresSection.count()): #Remover los widgets del QToolBox sin borrar sus layouts
            self.figuresSection.removeItem(self.figuresSection.currentIndex())

        self.figuresSection.hide() #Cada vez que cambie el QComboBox, mandar a llamar la funcion, no sin antes llamarla una sola vez 

        # Esta funcion revisara si el combo box tiene modo Mouse/Data, en cada caso va a tener una accion 
        # Mouse: Ocultara los datos del toolbox "self.figuresSection"
        # Data: Mostrara los datos de la figura seleccionada en el momento

        self.cmbConstructionBy.currentIndexChanged.connect(lambda:
            Geometry.currentTypeDrawing(self.figuresSection, self.cmbConstructionBy, self.cmbGeometricFigure, arrayFiguresSection))
        self.cmbConstructionBy.currentIndexChanged.connect(lambda: Geometry.currentTypeCheckBox( self.cmbConstructionBy, self.chkUnionFiguras))
        self.chkUnionFiguras.hide()


        self.cmbGeometricFigure.currentIndexChanged.connect(lambda:
            Geometry.currentTypeDrawing(self.figuresSection, self.cmbConstructionBy, self.cmbGeometricFigure, arrayFiguresSection))
        self.btnGeometryApply.clicked.connect(lambda:
            self.canvas.addPoly(Geometry.getTableData(self.figuresSection.currentWidget(), self.cmbGeometricFigure, scene.selectedItems()[0], self.canvas.deletePolygon), self.canvas.holeMode))
        self.sbNumPoints.valueChanged.connect(lambda: Geometry.updateTable(self.figuresSection.currentWidget(), self.cmbGeometricFigure ))

        # Mesh and Settings Study
        self.ghapMesh.hide()
        self.tabWidgetMenu.currentChanged.connect(lambda: MeshSettings.currentShowMeshTab(self.tabWidgetMenu.tabText(self.tabWidgetMenu.currentIndex()), self.ghapMesh))
        self.cmbConstructionBy.activated.connect(self.do_something)
        self.cmbTypeOfConstruction.activated.connect(self.changeMode)
        self.cmbGeometricFigure.activated.connect(self.changeDrawMode)
        self.tabWidgetMenu.currentChanged.connect(self.changeTab)
        self.btnMeshApply.clicked.connect(self.meshSettings)

 #####################################################       ################################333333
        self.chkUnionFiguras.clicked.connect(self.chkUnion)


        # CONDITIONS PDE
        arrayTypeofConSection = [] #Almacenar la direccion de los widgets en un arreglo
        for i in range(self.toolBoxTypeOfCon.count()):
            arrayTypeofConSection.append(self.toolBoxTypeOfCon.widget(i))

        #Cada vez que cambie el QComboBox, mandar a llamar la funcion, no sin antes llamarla una sola vez
        ConditionsPDE.currentCheckedComboBoxItemConditions(self.toolBoxTypeOfCon, self.cmbTypeConditionPDE, arrayTypeofConSection)
        self.cmbTypeConditionPDE.currentIndexChanged.connect(lambda: ConditionsPDE.currentCheckedComboBoxItemConditions(self.toolBoxTypeOfCon, self.cmbTypeConditionPDE, arrayTypeofConSection))

        # COEFFICIENTS PDE
        #Almacenar los QCheckBox en un solo arreglo
        self.CoefficientCheckBoxArray = []
        self.CoefficientCheckBoxArray.append(self.chkDiffusionCoefficient)
        self.CoefficientCheckBoxArray.append(self.chkAbsorptionCoefficient)
        self.CoefficientCheckBoxArray.append(self.chkSourceTerm)
        self.CoefficientCheckBoxArray.append(self.chkMassCoefficient)
        self.CoefficientCheckBoxArray.append(self.chkDampCoefficient)
        self.CoefficientCheckBoxArray.append(self.chkConservativeConvection)
        self.CoefficientCheckBoxArray.append(self.chkConvectionCoefficient)
        self.CoefficientCheckBoxArray.append(self.chkConservativeFluxSource)


        self.arrayCoeffMSection = [] #Almacenar los widgets del QToolBox en un arreglo
        self.arrayCheckNameCoeffM = [] #Almacenar el texto de los widgets del QToolBox en un arreglo
        for i in range(self.CoefficentForM.count()):
            self.arrayCheckNameCoeffM.append(self.CoefficentForM.itemText(i))
        for i in range(self.CoefficentForM.count()):
            self.arrayCoeffMSection.append(self.CoefficentForM.widget(i))

        arrayDiffusionCoeff = [] #Almacenar las direcciones de los LineEdits de la seccion Diffusion Coefficient en un arreglo
        arrayDiffusionCoeff.append(self.lEditDiffusionCoef)
        arrayDiffusionCoeff.append(self.lEditDiffusionCoef11)
        arrayDiffusionCoeff.append(self.lEditDiffusionCoef12)
        arrayDiffusionCoeff.append(self.lEditDiffusionCoef21)
        arrayDiffusionCoeff.append(self.lEditDiffusionCoef22)
    
        #Cada vez que cambie el QComboBox, Llamar la funcion que define el tipo de insercion de valores; (Isotropicos o Anisotropicos)
        #No sin antes mandar a llamar la funcion una sola vez
        Materials.currentHeatConduction(self.cmbDiffusionCoef,  arrayDiffusionCoeff)
        self.cmbDiffusionCoef.currentIndexChanged.connect(lambda: Materials.currentHeatConduction(self.cmbDiffusionCoef,  arrayDiffusionCoeff))
        self.lEditDiffusionCoef11.textChanged.connect(lambda: Materials.currentTextSimmetry(self.cmbDiffusionCoef, arrayDiffusionCoeff))

        #Cada vez que cambien el QComboBox, llamar la funcion que activa los widgets elegidos por el usuario
        CoefficientsPDE.clearCoefficientTbox(self, self.CoefficentForM, self.arrayCoeffMSection, self.arrayCheckNameCoeffM)
        self.btnCoefficientsApply.clicked.connect(lambda: CoefficientsPDE.currentCoefficientForM(self, self.CoefficentForM, CoefficientsPDE.CheckCoefficient(self.CoefficientCheckBoxArray), self.arrayCoeffMSection, self.arrayCheckNameCoeffM))

        #Almacenar los QComboxBox de Fila y Columna en un arreglo 
        arrayDiffusionRowColumn = [self.cmbRowDiffusionCoef, self.cmbColumnDiffusionCoef]
        arrayAbsorptionRowColumn = [self.cmbAbsorptionRow, self.cmbAbsorptionColumn]
        arraySourceRow = [self.cmbSourceRow]
        arrayMassRowColumn = [self.cmbMassCoefRow, self.cmbMassCoefColumn]
        arrayDampingRowColumn = [self.cmbDamMassCoefRow, self.cmbDamMassCoefColumn]
        arrayCFluxRowColumn = [self.cmbCFluxRow, self.cmbCFluxColumn]
        arrayConvectionRowColumn = [self.cmbConvectionRow, self.cmbConvectionColumn]
        arrayCSourceRow = [self.cmbCSourceRow]

        #Almacenar los arreglos que albergan QComboBox en un solo arreglo (un arreglo de arreglos)
        self.arrayCmbRowColumns = []
        self.arrayCmbRowColumns.append(arrayDiffusionRowColumn)
        self.arrayCmbRowColumns.append(arrayAbsorptionRowColumn)
        self.arrayCmbRowColumns.append(arraySourceRow)
        self.arrayCmbRowColumns.append(arrayMassRowColumn)
        self.arrayCmbRowColumns.append(arrayDampingRowColumn)
        self.arrayCmbRowColumns.append(arrayCFluxRowColumn)
        self.arrayCmbRowColumns.append(arrayConvectionRowColumn)
        self.arrayCmbRowColumns.append(arrayCSourceRow)

        #Almacenar los QLineEdits de cada seccion en un arreglo
        arrayAbsorption = [self.lEditAbsorCoef]
        arraySource = [self.lEditSourceTerm]
        arrayMassCoef = [self.lEditMassCoef]
        arrayDamMass = [self.lEditDamMassCoef]
        arrayConservFlux = [self.lEditAlphaXCFlux, self.lEditAlphaCYFlux]
        arrayConvectionFlux = [self.lEditBetaXConvCoef, self.lEditBetaYConvCoef]
        arrayCSource = [self.lEditGammaXCFluxSource, self.lEditGammaYCFluxSource]

        #Almacenar los arreglos que albergan QLineEdits en un soolo arreglo (un arreglo de arreglos)
        self.arraylEditsCoefficientsPDE = []
        self.arraylEditsCoefficientsPDE.append(arrayDiffusionCoeff)
        self.arraylEditsCoefficientsPDE.append(arrayAbsorption)
        self.arraylEditsCoefficientsPDE.append(arraySource)
        self.arraylEditsCoefficientsPDE.append(arrayMassCoef)
        self.arraylEditsCoefficientsPDE.append(arrayDamMass)
        self.arraylEditsCoefficientsPDE.append(arrayConservFlux)
        self.arraylEditsCoefficientsPDE.append(arrayConvectionFlux)
        self.arraylEditsCoefficientsPDE.append(arrayCSource)


        #Cada vez que el boton de "Apply" en una de las secciones se presione, mandar a llamar la funcion para:
        #Almacenar los datos obtenidos de los QLineEdits y mostrarlos en una matriz
        #Las dimensiones de la matriz dependeran del numero de variables elegidas por el usuario
        self.btnDiffusionApply.clicked.connect(lambda: self.dMatrix.marklineEdit(self.cmbRowDiffusionCoef, self.cmbColumnDiffusionCoef, initialValues["noVariables"], self.arraylEditsCoefficientsPDE, 1, self.cmbDiffusionCoef))
        self.btnDiffusionApply.clicked.connect(lambda: FileData.editedFile(self))

        self.btnAbsorptionApply.clicked.connect(lambda: self.dMatrix.marklineEdit(self.cmbAbsorptionRow, self.cmbAbsorptionColumn, initialValues["noVariables"], self.arraylEditsCoefficientsPDE, 2, self.cmbDiffusionCoef))
        self.btnAbsorptionApply.clicked.connect(lambda: FileData.editedFile(self))

        self.btnSourceApply.clicked.connect(lambda: self.dVector.marklineEdit(self.cmbSourceRow, initialValues["noVariables"], self.arraylEditsCoefficientsPDE, 3))
        self.btnSourceApply.clicked.connect(lambda: FileData.editedFile(self))

        self.btnMassApply.clicked.connect(lambda: self.dMatrix.marklineEdit(self.cmbMassCoefRow, self.cmbMassCoefColumn, initialValues["noVariables"], self.arraylEditsCoefficientsPDE, 4, self.cmbDiffusionCoef))
        self.btnMassApply.clicked.connect(lambda: FileData.editedFile(self))

        self.btnDampingApply.clicked.connect(lambda: self.dMatrix.marklineEdit(self.cmbDamMassCoefRow, self.cmbDamMassCoefColumn, initialValues["noVariables"], self.arraylEditsCoefficientsPDE, 5, self.cmbDiffusionCoef))
        self.btnDampingApply.clicked.connect(lambda: FileData.editedFile(self))

        self.btnCFluxApply.clicked.connect(lambda:  self.dMatrix.marklineEdit(self.cmbCFluxRow, self.cmbCFluxColumn, initialValues["noVariables"], self.arraylEditsCoefficientsPDE, 6, self.cmbDiffusionCoef))
        self.btnCFluxApply.clicked.connect(lambda: FileData.editedFile(self))

        self.btnConvectionApply.clicked.connect(lambda:  self.dMatrix.marklineEdit(self.cmbConvectionRow, self.cmbConvectionColumn, initialValues["noVariables"], self.arraylEditsCoefficientsPDE, 7, self.cmbDiffusionCoef))
        self.btnConvectionApply.clicked.connect(lambda: FileData.editedFile(self))

        self.btnCSourceApply.clicked.connect(lambda:  self.dVector.marklineEdit(self.cmbCSourceRow, initialValues["noVariables"], self.arraylEditsCoefficientsPDE, 8))
        self.btnCSourceApply.clicked.connect(lambda: FileData.editedFile(self))

        #Cada vez que el boton de "Preview" en una de la secciones se presione, mandar a llamar la funcion para:
        #Mostrar la matriz con los datos ya almacenados de los QlineEdits
        self.btnDiffusionPreview.clicked.connect(lambda: self.dMatrix.showMe(allNewMatrix.diffusionM))
        self.btnAbsorptionPreview.clicked.connect(lambda: self.dMatrix.showMe(allNewMatrix.absorptionM))
        self.btnSourcePreview.clicked.connect(lambda: self.dVector.showMe(allNewMatrix.sourceM))
        self.btnMassPreview.clicked.connect(lambda: self.dMatrix.showMe(allNewMatrix.massM))
        self.btnDampingPreview.clicked.connect(lambda: self.dMatrix.showMe(allNewMatrix.damMassM))
        self.btnCFluxPreview.clicked.connect(lambda: self.dMatrix.showMe(allNewMatrix.cFluxM))
        self.btnConvectionPreview.clicked.connect(lambda: self.dMatrix.showMe(allNewMatrix.convectionM))
        self.btnCSourcePreview.clicked.connect(lambda: self.dVector.showMe(allNewMatrix.cSourceM))

        #En la seccion Initial Values, cada vez que se presione el boton "Apply", llamar la funcion para establecer el numero de variables dependientes
        #Esto definira las dimensiones de las matrices con la que trabajara el usuario
        #self.btnInitialValuesApply.clicked.connect(lambda:CoefficientsPDE.currentCombMatrix(self, self.CoefficientCheckBoxArray, self.arrayCmbRowColumns, self.cmbInitialValues))

        # MATERIALS--------------------------------------------------------------------------------------------------
        inputKArray = [] #Almacenar los QlineEdtis de la pestaña MATERIALS en una arreglo
        inputKArray.append(self.inputK)
        inputKArray.append(self.inputKD1)
        inputKArray.append(self.inputKD2)
        inputKArray.append(self.inputKD3)
        inputKArray.append(self.inputKD4)

        #Cada vez que cambie el QComboBox, llamar la funcion que defina el tipo de insercion de datos (Isotropico o Anisotropico)
        Materials.currentHeatConduction(self.cmbHeatConduction, inputKArray)
        self.inputKD1.textChanged.connect(lambda: Materials.currentTextSimmetry(self.cmbHeatConduction, inputKArray))
        self.cmbHeatConduction.currentIndexChanged.connect(lambda: Materials.currentHeatConduction(self.cmbHeatConduction, inputKArray))

        # CONDITIONS---------------------------------------------------------------------------------------------
        arrayTypeofConditionSection = []
        for i in range(self.toolBoxTypeOfCondition.count()): #Almacenar los widgets del QToolBox en un arreglo
            arrayTypeofConditionSection.append(self.toolBoxTypeOfCondition.widget(i))

        self.btnReloadSides.clicked.connect(lambda: Conditions.reloadEdges(self.canvas, self.lWBoundarys))
        self.lWBoundarys.itemClicked.connect(lambda: Conditions.currentElementSelectListWidgets(  self.lWBoundarys.currentItem(), self.canvas))
        #Cada vez que cambie el QComboBox, llamar la funcion que active la seccion elegida por el usuario
        #No sin antes llamar primero una sola vez
        Conditions.currentTypeCondition(self.cmbTypeCondition, self.toolBoxTypeOfCondition, arrayTypeofConditionSection)
        self.cmbTypeCondition.currentIndexChanged.connect(lambda: Conditions.currentTypeCondition(self.cmbTypeCondition, self.toolBoxTypeOfCondition, arrayTypeofConditionSection))

        # MENU BAR (MANAGE FILES)------------------------------------------------------------------------------

        #Cada vez que se presione la pestaña "Open", abrir una ventana para ejecutar un archivo EXCEL
        self.actionOpen.triggered.connect(lambda: FileData.getFileName(self))
        #Cada vez que se presione la pestaña "New", abrir una ventana para crear un archivo EXCEL
        self.actionNew.triggered.connect(lambda: FileData.newFileName(self))
        #Cada vez que se presione la pestaña "Save", guardar el archivo EXCEL cargado
        self.actionSaves.triggered.connect(lambda: FileData.updateFile(self))
        #Cada vez que se presione la pestaña "Save As", guardar un archivo excel en una instancia nueva
        self.actionSave_As.triggered.connect(lambda: FileData.saveAsFile(self))
        #Cada vez que se presiones la pestaña "Close", cerrar el archivo cargado y resetear la configuracion del programa
        self.actionClose.triggered.connect(lambda: FileData.resetFile(self))


        self.btnModelWizardApply.clicked.connect(lambda: Matrix.newMatrix(self))

    def chkUnion(self):
        if(self.chkUnionFiguras.checkState() == 0):
            self.canvas.mode = "Data"
        elif(self.chkUnionFiguras.checkState() == 2):
            self.canvas.mode = "Union"

    def do_something(self):
        if(self.cmbConstructionBy.currentText() == "Data"):
            self.canvas.mode = "Arrow"
            self.canvas.enablePolygonSelect()
        elif(self.cmbConstructionBy.currentText() == "Mouse"):
            if(self.cmbGeometricFigure.currentText() == "Polygon"):
                self.canvas.mode = "Draw poly"
                self.canvas.enablePolygonSelect(False)
            elif(self.cmbGeometricFigure.currentText() == "Square"):
                self.canvas.mode = "Draw rect"
                self.canvas.enablePolygonSelect(False)
        elif(self.cmbConstructionBy.currentText() == "Combination"):
                self.canvas.mode = "Match points"
                self.canvas.enablePolygonSelect(False)
                
    def changeDrawMode(self):
        if(self.cmbConstructionBy.currentText() == "Data"):
            self.canvas.mode = "Arrow"
            self.canvas.enablePolygonSelect()
        elif(self.cmbConstructionBy.currentText() == "Mouse"):
            if(self.cmbGeometricFigure.currentText() == "Polygon"):
                self.canvas.mode = "Draw poly"
                self.canvas.enablePolygonSelect(False)
            elif(self.cmbGeometricFigure.currentText() == "Square"):
                self.canvas.mode = "Draw rect"
                self.canvas.enablePolygonSelect(False)
        elif(self.cmbConstructionBy.currentText() == "Combination"):
                self.canvas.mode = "Match points"
                self.canvas.enablePolygonSelect(False)


    def changeMode(self):
        if(self.cmbTypeOfConstruction.currentText() == "Solid"):
            self.canvas.holeMode = False
        else:
           self.canvas.holeMode = True
    def changeTab(self):
        if(self.tabWidgetMenu.tabText(self.tabWidgetMenu.currentIndex())) == "Geometry":
            if(self.cmbConstructionBy.currentText() == "Data"):
                self.canvas.mode = "Arrow"
                self.canvas.enablePolygonSelect()
            elif(self.cmbConstructionBy.currentText() == "Mouse"):
                if(self.cmbGeometricFigure.currentText() == "Polygon"):
                    self.canvas.mode = "Draw poly"
                    self.canvas.enablePolygonSelect(False)
                elif(self.cmbGeometricFigure.currentText() == "Square"):
                    self.canvas.mode = "Draw rect"
                    self.canvas.enablePolygonSelect(False)
            elif(self.cmbConstructionBy.currentText() == "Combination"):
                self.canvas.mode = "Match points"
                self.canvas.enablePolygonSelect(False)

    def meshSettings(self):
        if(self.cmbElementType.currentText()=="Triangle"):
            self.canvas.elType = 2
        elif(self.cmbElementType.currentText()=="Quadrangle"):
            self.canvas.elType = 3
        
        if(self.cmbElementSize.currentText()=="Finer"):
            self.canvas.elSizeFactor = 10
        elif(self.cmbElementSize.currentText()=="Fine"):
            self.canvas.elSizeFactor = 15
        elif(self.cmbElementSize.currentText()=="Normal"):
            self.canvas.elSizeFactor = 25
        elif(self.cmbElementSize.currentText()=="Coarse"):
            self.canvas.elSizeFactor = 35
        elif(self.cmbElementSize.currentText()=="Coarser"):
            self.canvas.elSizeFactor = 45

        self.canvas.showMesh()

    #Combobox Row and Columns Configuration


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