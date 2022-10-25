import enum
from tkinter.tix import TEXT
from Modules.Dictionary.DMatrix import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QColor
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox
class Materials():
    def __init__(self):
        self.__figure = None        # La figura actualmente seleccionada
        self.__dataFigures = []     # Las figuras que tienen datos son cargas aqui
        self.__figuresCount = 0     # cuenta cuantas figuras existen

    def getFigure(self):
        return self.__figure

    def setFigure(self, figure):
        self.__figure = figure

    def getDataFigures(self):
        return self.__dataFigures

    def setFiguresCount(self, figuresCount):
        self.__figuresCount = figuresCount

    def getFiguresCount(self):
        return self.__figuresCount

    def setDataFigures(self, dataFigures):
        self.__dataFigures = dataFigures

    def currentHeatConduction(self, comb, ar):
        for i, item in enumerate(ar):
            ar[i].clear()
            ar[i].setEnabled(False)

        if comb.currentIndex() == 0:
            diffusionMatrix["inputMode"] = 0
            ar[0].setEnabled(True)
        if comb.currentIndex() == 1:
            diffusionMatrix["inputMode"] = 1
            ar[1].setEnabled(True)
            ar[4].setEnabled(True)
            ar[2].insert("0")
            ar[3].insert("0")
        if comb.currentIndex() == 2:
            diffusionMatrix["inputMode"] = 2
            ar[1].setEnabled(True)
            ar[2].setEnabled(True)
            ar[4].setEnabled(True)
        if comb.currentIndex() == 3:
            diffusionMatrix["inputMode"] = 3
            ar[1].setEnabled(True)
            ar[2].setEnabled(True)
            ar[3].setEnabled(True)
            ar[4].setEnabled(True)

    def currentTextSimmetry(self, comb, ar):
        if comb.currentIndex() == 2:
            ar[3].clear()
            ar[3].insert(ar[1].text())

    # Carga las figuras que estan creadas en la ventana
    def currentDomains(self, win, lwDomains, canvas, tboxMaterialsConditions, tableDomainsMaterials):
        solids = canvas.getSolids()
        self.setFiguresCount(solids)

        if lwDomains.count() != 0:
            lwDomains.clear()
        else:
            tboxMaterialsConditions.hide()
            win.cmbMaterial.hide()
            win.lblMaterial.hide()

        # Borra todos los elementos de la tabla, ya que se van a cargar previamente
        tableDomainsMaterials.setRowCount(0)

        # Guardas las figuras que han sido creadas
        self.__figuresCount = len(solids)



        if not self.__dataFigures:
            if len(solids) != 0:
                for indexPoly in range(len(solids)):
                    text = 'figura ' + str(indexPoly + 1)
                    lwDomains.addItem(text)
                    tableDomainsMaterials.insertRow(indexPoly)
                    tableDomainsMaterials.setItem(indexPoly, 0, QTableWidgetItem(text))
                    tableDomainsMaterials.setItem(indexPoly, 1, QTableWidgetItem("No selected"))
        else:
            for indexPoly in range(len(solids)):
                added = False
                text = 'figura ' + str(indexPoly + 1)
                lwDomains.addItem(text)
                tableDomainsMaterials.insertRow(indexPoly)

                for data in self.__dataFigures:
                    if data['figure'] == indexPoly:
                        added = True
                        tableDomainsMaterials.setItem(indexPoly, 0, QTableWidgetItem(text))
                        tableDomainsMaterials.setItem(indexPoly, 1, QTableWidgetItem(win.cmbMaterial.itemText(data['material'])))

                if not added:
                    tableDomainsMaterials.setItem(indexPoly, 0, QTableWidgetItem(text))
                    tableDomainsMaterials.setItem(indexPoly, 1, QTableWidgetItem("No selected"))



    def selectionType(self, win):
        index = win.cmbSelection.currentIndex()
        text = win.cmbSelection.itemText(index)

        if text == "All domains":
            win.listDomains.setDisabled(True)
            canvas = win.canvas
            solids = canvas.getSolids()
            paint = QBrush(QColor(255,0,0,50))

            win.lblMaterial.show()
            win.cmbMaterial.show()
            win.tboxMaterialsConditions.show()

            for item in solids:
                item.setBrush(paint)

        else:
            win.listDomains.setDisabled(False)
            canvas = win.canvas
            solids = canvas.getSolids()
            paint = QBrush(QColor(0,0,0,50))

            win.lblMaterial.hide()
            win.cmbMaterial.hide()
            win.tboxMaterialsConditions.hide()

            for item in solids:
                item.setBrush(paint)

    # Esta funcion es para cuando se hace click en un elemento
    def currentDomainSelected(self, element, win):
        dataExists = False
        index = int(element.currentRow())
        currentElement = {}
        self.setFigure(index)

        # Obtiene la figuras que son solidas
        solids = win.canvas.getSolids()
        paint = QBrush(QColor(255,0,0,50))

        # Pinta todoso los poligonos para resetear todos
        for item in solids:
            item.setBrush(QBrush(QColor(0, 0, 0, 50)))
        # Pinta la figura seleccionada
        solids[index].setBrush(paint)
        
        # Si selecciona un material, se activan los botones
        win.btnMaterialApply.setEnabled(True)
        win.btnMaterialsReset.setEnabled(True)
        win.btnMaterialsHelp.setEnabled(True)
        win.cmbMaterial.show()
        win.lblMaterial.show()
        # Mostrar todas las pestañas
        win.tboxMaterialsConditions.show()

        # Si existen valores en el data figures entra al if
        if self.__dataFigures:
            for data in self.__dataFigures:
                # Busca que el index actual de la lista tenga un material comparando los datos con los dataFigures
                if data['figure'] == index:
                    dataExists = True
                    currentData = data

        # Si existe los datos en el material entra
        if dataExists:
            win.cmbMaterial.setCurrentIndex(currentData['material'])
            win.cmbHeatConduction.setCurrentIndex(currentData['heatConductionType'])

            # Si el combo box es de user defined entra el if
            if currentData['material'] == 0:
                # Si es isotropico solo va a ingresar los datos
                if currentData['heatConductionType'] == 0:
                    win.inputK.setText(str(currentData['thermalConductivity'][0]))
                else:
                    win.inputKD1.setText(str(currentData['thermalConductivity'][0]))
                    win.inputKD2.setText(str(currentData['thermalConductivity'][1]))
                    win.inputKD3.setText(str(currentData['thermalConductivity'][2]))
                    win.inputKD4.setText(str(currentData['thermalConductivity'][3]))
                win.inputRho.setText(str(currentData['density']))
                win.inputConsantPressure.setText(str(currentData['heatCapacity']))
                win.lEditUy1.setText(str(currentData['heatConvection'][0]))
                win.lEditUy2.setText(str(currentData['heatConvection'][1]))
            #else: El elemento si es un material lo carga automaticamente
        # En caso de que no tenga datos guardados, entonces pondran datos por defecto
        else:
            win.cmbMaterial.setCurrentIndex(0)
            win.cmbHeatConduction.setCurrentIndex(0)
            win.inputK.setText("")
            win.inputKD1.setText("")
            win.inputKD2.setText("")
            win.inputKD3.setText("")
            win.inputKD4.setText("")
            win.inputRho.setText("")
            win.lEditUy1.setText(str(0))
            win.lEditUy2.setText(str(0))
            win.inputConsantPressure.setText("")


    def currentMaterialSelection(self,cmbMaterial, mainWin):
        # Si el combo el material es seleccionado por el usuairo
        if cmbMaterial.currentText() == 'User defined':
            mainWin.heatConductionSolid.setFocus(True)
            mainWin.tboxMaterialsConditions.setItemEnabled(0, True)
            mainWin.tboxMaterialsConditions.setItemEnabled(1, True)
            mainWin.tboxMaterialsConditions.setItemEnabled(2, True)
            mainWin.tboxMaterialsConditions.setItemEnabled(3, False)
        else:
            mainWin.tableDomains.setItem(0, 1, QTableWidgetItem(str(mainWin.materialsDataBase[mainWin.cmbMaterial.currentIndex()-1][2]))) # Thermal conductivity
            mainWin.tableDomains.setItem(1, 1, QTableWidgetItem(str(mainWin.materialsDataBase[mainWin.cmbMaterial.currentIndex()-1][7]))) #Heat Capacity
            mainWin.tableDomains.setItem(2, 1, QTableWidgetItem(str(mainWin.materialsDataBase[mainWin.cmbMaterial.currentIndex()-1][8]))) #Density

            mainWin.propertiesFromTheLibrary.setFocus(True)
            mainWin.tboxMaterialsConditions.setItemEnabled(0, False)
            mainWin.tboxMaterialsConditions.setItemEnabled(1, False)
            mainWin.tboxMaterialsConditions.setItemEnabled(2, False)
            mainWin.tboxMaterialsConditions.setItemEnabled(3, True)

    def applyMaterialChanges(self, win):
        # Esto es para saber si esta seleccionado el all domains o el 
        index = win.cmbSelection.currentIndex()
        text = win.cmbSelection.itemText(index)

        # La figura que se quiere guardar
        thermalConductivity = []
        heatConvection = []
        heatCapacity = 0
        density = 0
        currentTextMaterial = win.cmbMaterial.currentIndex()
        heatConductionType = win.cmbHeatConduction.currentIndex()

        if currentTextMaterial == 0: # User selected
            # Extrrae los datos de los input
            headConductionSelection = win.cmbHeatConduction.currentText()
            heatConvection.append(float(win.lEditUy1.text()))
            heatConvection.append(float(win.lEditUy2.text()))
            heatCapacity = float(win.inputConsantPressure.text())
            density = float(win.inputRho.text())
            if headConductionSelection == "Isotropic":
                thermalConductivity.append(float(win.inputK.text()))

            elif headConductionSelection == "Diagonal":
                thermalConductivity.append(float(win.inputKD1.text()))
                thermalConductivity.append(0)
                thermalConductivity.append(0)
                thermalConductivity.append(float(win.inputKD4.text()))
            else:
                thermalConductivity.append(float(win.inputKD1.text()))
                thermalConductivity.append(float(win.inputKD2.text()))
                thermalConductivity.append(float(win.inputKD3.text()))
                thermalConductivity.append(float(win.inputKD4.text()))
        else: # Material selected
            heatCapacity = float(win.materialsDataBase[win.cmbMaterial.currentIndex()-1][7]) #Heat Capacity
            density = float(win.materialsDataBase[win.cmbMaterial.currentIndex()-1][8]) #Density
            # Pasamos dos valores de 0, ya que los materiales no tienen heat convection
            heatConvection.append(0)
            heatConvection.append(0)

            # Extraccion de los datos de la base de datos
            if win.cmbNameMaterials.currentIndex() != -1 :
                if win.materialsDataBase[win.cmbNameMaterials.currentIndex()][6] == 0:  #isotropic
                    thermalConductivity.append(float(win.materialsDataBase[win.cmbMaterial.currentIndex()-1][2]))
                elif win.materialsDataBase[win.cmbNameMaterials.currentIndex()][6] == 1 : #diagonal 
                    thermalConductivity.append(float(win.materialsDataBase[win.cmbMaterial.currentIndex()-1][2]))
                    thermalConductivity.append(0)
                    thermalConductivity.append(0)
                    thermalConductivity.append(float(win.materialsDataBase[win.cmbMaterial.currentIndex()-1][5]))
                elif win.materialsDataBase[win.cmbNameMaterials.currentIndex()][6] == 2 : #symmetric
                    thermalConductivity.append(float(win.materialsDataBase[win.cmbMaterial.currentIndex()-1][2]))
                    thermalConductivity.append(float(win.materialsDataBase[win.cmbMaterial.currentIndex()-1][3]))
                    thermalConductivity.append(float(win.materialsDataBase[win.cmbMaterial.currentIndex()-1][4]))
                    thermalConductivity.append(float(win.materialsDataBase[win.cmbMaterial.currentIndex()-1][5]))
                elif win.materialsDataBase[win.cmbNameMaterials.currentIndex()][6] == 3 : #full
                    thermalConductivity.append(float(win.materialsDataBase[win.cmbMaterial.currentIndex()-1][2]))
                    thermalConductivity.append(float(win.materialsDataBase[win.cmbMaterial.currentIndex()-1][3]))
                    thermalConductivity.append(float(win.materialsDataBase[win.cmbMaterial.currentIndex()-1][4]))
                    thermalConductivity.append(float(win.materialsDataBase[win.cmbMaterial.currentIndex()-1][5]))

        if text == "All domains":
            print("All domains")
            solids = win.canvas.getSolids()
            # Si no hay informacion creada, crear los datos
            if not self.__dataFigures:
                for [indexSolid, solid] in enumerate(solids):
                    # Va adjuntando los nuevos elementos de los solidos creados en la figura
                    self.__dataFigures.append({'figure':indexSolid, 'thermalConductivity': thermalConductivity, 'density': density, 'heatCapacity':  heatCapacity, 'heatConvection': heatConvection, 'material': currentTextMaterial, 'heatConductionType': heatConductionType})
            else:
                # Si se agrega un nuevo valor agregar un una nueva figura con un if
                if len(self.__dataFigures) == self.__figuresCount:
                    for figure in self.__dataFigures:
                        # Renscribe los datos de cada interacion
                        figure['thermalConductivity'] = thermalConductivity
                        figure['density'] = density
                        figure['heatCapacity'] = heatCapacity
                        figure['heatConvection'] = heatConvection
                        figure['material'] = currentTextMaterial
                        figure['heatConductionType'] = heatConductionType
                # Si la data de los valores guardados son diferentes a los solids del canvas, se crean todos los datos de nuevo
                else:
                    self.setDataFigures([])
                    for [indexSolid, solid] in enumerate(solids):
                    # Va adjuntando los nuevos elementos de los solidos creados en la figura
                        self.__dataFigures.append({'figure':indexSolid, 'thermalConductivity': thermalConductivity, 'density': density, 'heatCapacity':  heatCapacity, 'heatConvection': heatConvection, 'material': currentTextMaterial, 'heatConductionType': heatConductionType})

        else:
            print("Manual")
            # En caso de que no haya ninguna figura con materiales
            if not self.__dataFigures:
                self.__dataFigures.append({'figure':self.__figure, 'thermalConductivity': thermalConductivity, 'density': density, 'heatCapacity':  heatCapacity, 'heatConvection': heatConvection, 'material': currentTextMaterial, 'heatConductionType': heatConductionType})
            # Si ya existe una figura con materiales comprobar si tiene materiales para rescribirlos
            else:
                exists = False
                # Recorre las figuras buscando si ya tiene elementos creados
                # Se rescriben
                for figure in self.__dataFigures:
                    # Si la figura existe, transcribe los valores que ya estaban anteriormente almacenados
                    if figure['figure'] == self.__figure:
                        exists = True #Ignora esta
                        figure['thermalConductivity'] = thermalConductivity
                        figure['density'] = density
                        figure['heatCapacity'] = heatCapacity
                        figure['heatConvection'] = heatConvection
                        figure['material'] = currentTextMaterial
                        figure['heatConductionType'] = heatConductionType

                # Si el elemento seleccionado no tiene datos cargados, crea nuevo elementos
                if not exists:
                    self.__dataFigures.append({'figure':self.__figure, 'thermalConductivity': thermalConductivity, 'density': density, 'heatCapacity':  heatCapacity, 'heatConvection': heatConvection, 'material': currentTextMaterial, 'heatConductionType': heatConductionType})

    def resetMaterialChanges(self, win):
        # print(self.__figure)
        qm = QMessageBox()
        ret = qm.question(win,'', "Are you sure to reset the values?", qm.Yes | qm.No)
        if ret == qm.Yes:
            if self.__dataFigures:
                for [index, data] in enumerate(self.__dataFigures):
                    if data['figure'] == self.__figure:
                        print("elemento borrado")
                        self.__dataFigures.pop(index)
            else:
                print("No existen")
        else:
            return

    # Funcion para mostrar los datos
    def showData(self):
        print('data figures')
        print(self.__dataFigures)
        print('figure created')
        print(self.__figuresCount)
