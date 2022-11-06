

class Initialize():
    def takeToolBoxConditionWidgets(self):
        arrayTypeofConditionSection = []
        for i in range(self.toolBoxTypeOfCondition.count()): 
            arrayTypeofConditionSection.append(self.toolBoxTypeOfCondition.widget(i))
        return arrayTypeofConditionSection

    def takeInputLineEditsMaterials(self):
        inputKArray = [] 
        inputKArray.append(self.inputK)
        inputKArray.append(self.inputKD1)
        inputKArray.append(self.inputKD2)
        inputKArray.append(self.inputKD3)
        inputKArray.append(self.inputKD4)

        return inputKArray

    def hideMaterialsButtons(self):
        self.btnMaterialApply.setEnabled(False)
        self.btnMaterialsReset.setEnabled(False)
        self.btnMaterialsHelp.setEnabled(False)

    def takeCoefficientPDECheckBox(self):
        self.CoefficientCheckBoxArray = []
        self.CoefficientCheckBoxArray.append(self.chkDiffusionCoefficient)
        self.CoefficientCheckBoxArray.append(self.chkAbsorptionCoefficient)
        self.CoefficientCheckBoxArray.append(self.chkSourceTerm)
        self.CoefficientCheckBoxArray.append(self.chkMassCoefficient)
        self.CoefficientCheckBoxArray.append(self.chkDampCoefficient)
        self.CoefficientCheckBoxArray.append(self.chkConservativeConvection)
        self.CoefficientCheckBoxArray.append(self.chkConvectionCoefficient)
        self.CoefficientCheckBoxArray.append(self.chkConservativeFluxSource)

        return self.CoefficientCheckBoxArray

    def takeCoefficientPDEWidgets(self):
        self.arrayCoeffMSection = [] #Almacenar los widgets del QToolBox en un arreglo
        self.arrayCheckNameCoeffM = [] #Almacenar el texto de los widgets del QToolBox en un arreglo
        for i in range(self.CoefficentForM.count()):
            self.arrayCheckNameCoeffM.append(self.CoefficentForM.itemText(i))
        for i in range(self.CoefficentForM.count()):
            self.arrayCoeffMSection.append(self.CoefficentForM.widget(i))

        return self.arrayCoeffMSection, self.arrayCheckNameCoeffM

    def takeCoefficientPDELineEdits(self, arrayDiffusionCoeff):
        arrayAbsorption = [self.lEditAbsorCoef]
        arraySource = [self.lEditSourceTerm]
        arrayMassCoef = [self.lEditMassCoef]
        arrayDamMass = [self.lEditDamMassCoef]
        arrayConservFlux = [self.lEditAlphaXCFlux, self.lEditAlphaCYFlux]
        arrayConvectionFlux = [self.lEditBetaXConvCoef, self.lEditBetaYConvCoef]
        arrayCSource = [self.lEditGammaXCFluxSource, self.lEditGammaYCFluxSource]

        #Almacenar los arreglos que albergan QLineEdits en un solo arreglo (un arreglo de arreglos)
        self.arraylEditsCoefficientsPDE = []
        self.arraylEditsCoefficientsPDE.append(arrayDiffusionCoeff)
        self.arraylEditsCoefficientsPDE.append(arrayAbsorption)
        self.arraylEditsCoefficientsPDE.append(arraySource)
        self.arraylEditsCoefficientsPDE.append(arrayMassCoef)
        self.arraylEditsCoefficientsPDE.append(arrayDamMass)
        self.arraylEditsCoefficientsPDE.append(arrayConservFlux)
        self.arraylEditsCoefficientsPDE.append(arrayConvectionFlux)
        self.arraylEditsCoefficientsPDE.append(arrayCSource)

        return self.arraylEditsCoefficientsPDE

    def takeCoefficientPDECombobox(self):
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

        return self.arrayCmbRowColumns

    def takeDiffusionCoefficientLineEdits(self):
        arrayDiffusionCoeff = [] 
        arrayDiffusionCoeff.append(self.lEditDiffusionCoef)
        arrayDiffusionCoeff.append(self.lEditDiffusionCoef11)
        arrayDiffusionCoeff.append(self.lEditDiffusionCoef12)
        arrayDiffusionCoeff.append(self.lEditDiffusionCoef21)
        arrayDiffusionCoeff.append(self.lEditDiffusionCoef22)

        return arrayDiffusionCoeff
    
    def takeTypeConditionsPDEWidgets(self):
        arrayTypeofConSection = [] 
        for i in range(self.toolBoxTypeOfCon.count()):
            arrayTypeofConSection.append(self.toolBoxTypeOfCon.widget(i))

        return arrayTypeofConSection

    def takeTypeConditionsWidgets(self):
        arrayTypeofConditionSection = [] 
        for i in range(self.toolBoxTypeOfCondition.count()):
            arrayTypeofConditionSection.append(self.toolBoxTypeOfCondition.widget(i))

        return arrayTypeofConditionSection

    def takeGeometryWidgets(self):
        arrayFiguresSection = [] 
        for i in range(self.figuresSection.count()):
            arrayFiguresSection.append(self.figuresSection.widget(i))

        for i in range(self.figuresSection.count()): #Remover los widgets del QToolBox sin borrar sus layouts
            self.figuresSection.removeItem(self.figuresSection.currentIndex())

        return arrayFiguresSection

    def takeModelWizardTabs(self):
        modelWizardDict = {'widget': self.modelWizardTab, 'title': "Model Wizard", 'index': 0}
        materialsTabDict = {'widget': self.materialsTab, 'title': "Materials", 'index': 1}
        geometryTabDict = {'widget': self.geometryTab, 'title': "Geometry", 'index': 2}
        conditionsTabDict = {'widget': self.conditionsTab, 'title': "Conditions", 'index': 3}
        meshAndSettingStudyTabDict = {'widget': self.meshAndSettingStudyTab, 'title': "Mesh and Setting Study", 'index': 4}
        conditionsPDETabDict = {'widget': self.conditionsPDETab, 'title': "Conditions PDE", 'index': 5}
        coefficentFormPDETabDict = {'widget': self.CoefficentFormPDETab, 'title': "Coefficent Form PDE", 'index': 6}
        libraryTabDict = {'widget': self.libraryTab, 'title': "Library", 'index': 7}

        self.tabs = []
        self.tabs.append(modelWizardDict)           # 0
        self.tabs.append(materialsTabDict)             # 1
        self.tabs.append(geometryTabDict)              # 2
        self.tabs.append(conditionsTabDict)            # 3
        self.tabs.append(meshAndSettingStudyTabDict)   # 4
        self.tabs.append(conditionsPDETabDict)         # 5
        self.tabs.append(coefficentFormPDETabDict)     # 6
        self.tabs.append(libraryTabDict)               # 7

        return self.tabs