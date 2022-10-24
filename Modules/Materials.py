from Modules.Dictionary.DMatrix import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QColor
from PyQt5.QtWidgets import QTableWidgetItem
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

        if len(solids) != 0:
                for indexPoly in range(len(solids)):
                    text = 'figura ' + str(indexPoly + 1)
                    lwDomains.addItem(text)
                    tableDomainsMaterials.insertRow(indexPoly)
                    tableDomainsMaterials.setItem(indexPoly, 0, QTableWidgetItem(text))
                    tableDomainsMaterials.setItem(indexPoly, 1, QTableWidgetItem("No selected"))
        
        
        


    def selectionType(self,win):
        index = win.cmbSelection.currentIndex()
        text = win.cmbSelection.itemText(index)

        if text == "All domains":
            win.listDomains.setDisabled(True)
            canvas = win.canvas
            solids = canvas.getSolids()
            paint = QBrush(QColor(255,0,0,50))

            for item in solids:
                item.setBrush(paint)

        else:
            win.listDomains.setDisabled(False)
            canvas = win.canvas
            solids = canvas.getSolids()
            paint = QBrush(QColor(0,0,0,50))

            for item in solids:
                item.setBrush(paint)

    # Esta funcion es para cuando se hace click en un elemento
    def currentDomainSelected(self, element, canvas, win):
        elementExists = False
        index = element.currentRow()
        self.setFigure(index)

        # Obtiene la figuras que son solidas
        solids = canvas.getSolids()
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

        for data in self.__dataFigures:
          if data['figure'] == index:
              elementExists = True
        # Si el elemento de la figura ya tiene elementos guardados entra al if
        if elementExists:
            win.cmbMaterial.setCurrentIndex(int(data['material']))
            # Si el combo box es de definicion de usuario entra el if
            if data['material'] == 0:
                win.cmbHeatConduction.setCurrentIndex(data['heatConductionType'])

                if data['heatConductionType'] == 0:
                    win.inputK.setText(data['thermalConductivity'][0])
                else:
                    win.inputKD1.setText(data['thermalConductivity'][0])
                    win.inputKD2.setText(data['thermalConductivity'][1])
                    win.inputKD3.setText(data['thermalConductivity'][2])
                    win.inputKD4.setText(data['thermalConductivity'][3])
                win.inputRho.setText(data['density'])
                win.inputConsantPressure.setText(data['heatCapacity'])
            # El elemento si es un material
            else:
                win.tableDomains.setItem(0, 1, QTableWidgetItem(str(data['thermalConductivity']))) # Thermal conductivity
                win.tableDomains.setItem(1, 1, QTableWidgetItem(str(data['heatCapacity']))) #Heat Capacity
                win.tableDomains.setItem(2, 1, QTableWidgetItem(str(data['density']))) #Density
        # En caso de que no tenga datos guardados, entonces seteara datos por defecto
        else:
            win.cmbMaterial.setCurrentIndex(0)
            win.cmbHeatConduction.setCurrentIndex(0)
            win.inputK.setText("")
            win.inputKD1.setText("")
            win.inputKD2.setText("")
            win.inputKD3.setText("")
            win.inputKD4.setText("")
            win.inputRho.setText("")
            win.inputConsantPressure.setText("")


    def currentMaterialSelection(self,cmbMaterial, mainWin):
        if cmbMaterial.currentText() == 'User defined':
            mainWin.heatConductionSolid.setFocus(True)
            mainWin.tboxMaterialsConditions.setItemEnabled(0, True)
            mainWin.tboxMaterialsConditions.setItemEnabled(1, True)
            mainWin.tboxMaterialsConditions.setItemEnabled(2, True)
            mainWin.tboxMaterialsConditions.setItemEnabled(3, False)
        else:
            mainWin.tableDomains.setItem(0, 1, QTableWidgetItem(  str(mainWin.materialsDataBase[mainWin.cmbMaterial.currentIndex()-1][2]))) # Thermal conductivity
            mainWin.tableDomains.setItem(1, 1, QTableWidgetItem(str(mainWin.materialsDataBase[mainWin.cmbMaterial.currentIndex()-1][7]))) #Heat Capacity
            mainWin.tableDomains.setItem(2, 1, QTableWidgetItem(str(mainWin.materialsDataBase[mainWin.cmbMaterial.currentIndex()-1][8]))) #Density

            if mainWin.materialsDataBase[mainWin.cmbMaterial.currentIndex()-1][6] == 0:  #isotropic
                print('iso')
            elif mainWin.materialsDataBase[mainWin.cmbMaterial.currentIndex()-1][6] == 1 : #diagonal
                print('diag')
            elif mainWin.materialsDataBase[mainWin.cmbMaterial.currentIndex()-1][6] == 2 : #symmetric
                print('syme')
            elif mainWin.materialsDataBase[mainWin.cmbMaterial.currentIndex()-1][6] == 3 : #full
                print('full')


            mainWin.propertiesFromTheLibrary.setFocus(True)
            mainWin.tboxMaterialsConditions.setItemEnabled(0, False)
            mainWin.tboxMaterialsConditions.setItemEnabled(1, False)
            mainWin.tboxMaterialsConditions.setItemEnabled(2, False)
            mainWin.tboxMaterialsConditions.setItemEnabled(3, True)

    def applyMaterialChanges(self, win):
        # La figura que se quiere guardar
        thermalConductivity = []
        heatConvection = []
        heatCapacity = 0
        density = 0
        currentTextMaterial = win.cmbMaterial.currentIndex()
        heatConductionType = win.cmbHeatConduction.currentIndex()

        if currentTextMaterial == "User defined":
            headConductionSelection = win.cmbHeatConduction.currentText()
            if headConductionSelection == "Isotropic":
                thermalConductivity.append(win.inputK.text())
            elif headConductionSelection == "Diagonal":
                thermalConductivity.append(win.inputKD1.text())
                thermalConductivity.append(0)
                thermalConductivity.append(0)
                thermalConductivity.append(win.inputKD4.text())
            elif headConductionSelection == "Symmetric":
                thermalConductivity.append(win.inputKD1.text())
                thermalConductivity.append(win.inputKD2.text())
                thermalConductivity.append(win.inputKD3.text())
                thermalConductivity.append(win.inputKD4.text())
            elif headConductionSelection == "Full":
                thermalConductivity.append(win.inputKD1.text())
                thermalConductivity.append(win.inputKD2.text())
                thermalConductivity.append(win.inputKD3.text())
                thermalConductivity.append(win.inputKD4.text())
        else: # Material selected
            heatCapacity = str(win.materialsDataBase[win.cmbMaterial.currentIndex()-1][7]) #Heat Capacity
            density = str(win.materialsDataBase[win.cmbMaterial.currentIndex()-1][8]) #Density
            heatConvection.append(0)
            heatConvection.append(0)

            if win.cmbNameMaterials.currentIndex() != -1 :
                if win.materialsDataBase[win.cmbNameMaterials.currentIndex()][6] == 0:  #isotropic
                    thermalConductivity.append(str(win.materialsDataBase[win.cmbMaterial.currentIndex()-1][2]))
                elif win.materialsDataBase[win.cmbNameMaterials.currentIndex()][6] == 1 : #diagonal 
                    thermalConductivity.append(str(win.materialsDataBase[win.cmbMaterial.currentIndex()-1][2]))
                    thermalConductivity.append(0)
                    thermalConductivity.append(0)
                    thermalConductivity.append(str(win.materialsDataBase[win.cmbMaterial.currentIndex()-1][5]))
                elif win.materialsDataBase[win.cmbNameMaterials.currentIndex()][6] == 2 : #symmetric
                    thermalConductivity.append(str(win.materialsDataBase[win.cmbMaterial.currentIndex()-1][2]))
                    thermalConductivity.append(str(win.materialsDataBase[win.cmbMaterial.currentIndex()-1][3]))
                    thermalConductivity.append(str(win.materialsDataBase[win.cmbMaterial.currentIndex()-1][4]))
                    thermalConductivity.append(str(win.materialsDataBase[win.cmbMaterial.currentIndex()-1][5]))
                elif win.materialsDataBase[win.cmbNameMaterials.currentIndex()][6] == 3 : #full
                    thermalConductivity.append(str(win.materialsDataBase[win.cmbMaterial.currentIndex()-1][2]))
                    thermalConductivity.append(str(win.materialsDataBase[win.cmbMaterial.currentIndex()-1][3]))
                    thermalConductivity.append(str(win.materialsDataBase[win.cmbMaterial.currentIndex()-1][4]))
                    thermalConductivity.append(str(win.materialsDataBase[win.cmbMaterial.currentIndex()-1][5]))

        if not self.__dataFigures:
            self.__dataFigures.append({'figure':self.__figure, 'thermalConductivity': thermalConductivity, 'density': density, 'heatCapacity':  heatCapacity, 'heatConvection': heatConvection, 'material': currentTextMaterial, 'heatConductionType': heatConductionType })
        else:
            exists = False
            for figure in self.__dataFigures:
                if figure['figure'] == self.__figure:
                    exists = True
                    figure['thermalConductivity'] = thermalConductivity
                    figure['density'] = density
                    figure['heatCapacity'] = heatCapacity
                    figure['heatConvection'] = heatConvection

            if not exists:
                self.__dataFigures.append({'figure':self.__figure, 'thermalConductivity': thermalConductivity, 'density': density, 'heatCapacity':  heatCapacity, 'heatConvection': heatConvection, 'material': currentTextMaterial, 'heatConductionType': heatConductionType })

    def showData(self):
        print('data figures')
        print(self.__dataFigures)
        print('figure created')
        print(self.__figuresCount)
        