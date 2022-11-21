from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPen, QColor, QBrush
from PyQt5.QtWidgets import QMessageBox

class Conditions():
    def __init__(self):
        self.sidesData = []
        self.currentSide = None

    def createData(self, win, n):
        try:
            for i in range(n):
                self.sidesData.append({'side':i+1, 'typeCondition': "Thermal Insulation", 'heatConditionType': "", 'data': 0})
        except:
            print("No puede ingresar datos asi")
    
    def showData(self):
        print(self.sidesData)


    def reloadEdges(self, canvas, listWid):
        edges = canvas.getEdges()
        listOfPolys = []

        if listWid.count() != 0:
            listWid.clear()

        for i in range(len(edges)):
            polygon = str(i+1)
            listOfPolys.append({'edge':edges[i], 'text':polygon, '' 'indice':i })
            listWid.addItem(polygon)


    def currentElementSelectListWidgets(self, win, element, canvas, lblFigureSelected):
        index = int(element.text())
        edges = canvas.getEdges()
        line = edges[index-1]
        LUBronze = QColor(156, 87, 20)
        defaultColor = QPen(LUBronze)
        defaultColor.setWidth(3)
        for elem in edges:
            elem.setPen(defaultColor)

        paint = QPen(Qt.red)
        paint.setWidth(5)
        line.setPen(paint)

        lblFigureSelected.setText("Lado " + str(index) )

        win.lblTypeConditionTitle.show()
        win.cmbTypeCondition.show()
        win.toolBoxTypeOfCondition.show()
        win.btnConditionsApply.show()
        win.btnConditionsReset.show()
        win.btnConditionsHelp.show()


        side = 0
        typeCondition = 0
        heatConditionType = ""
        data = 0
        self.currentSide = index

        for sideData in self.sidesData:
            if sideData['side'] == index:
                side = sideData['side']
                typeCondition = sideData['typeCondition']
                heatConditionType = sideData['heatConditionType']
                data = sideData['data']
        self.selectedChangeTypeOfCondition(win, typeCondition)
        
        # Thermal insulation
        if typeCondition == "Thermal Insulation":
            print('Thermal Insulation')
        # Temperature
        if typeCondition == "Temperature":
            print('Temperature')

        # Heat Flux
        if typeCondition == "Heat Flux":
            self.selectedCurrentHeatFluxConditionType(win, heatConditionType)
            print("Heat Flux")

    def applyCurrentBoundaryData(self, win):
        conditionsSelection = win.cmbConditionsSelection.currentText()
        typeCondition = win.cmbTypeCondition.currentText()
        # side':i+1, 'typeCondition': "Thermal Insulation", 'heatConditionType': "", 'data:
        if conditionsSelection == "Manual":
            # Thermal Insulation
            if typeCondition == "Thermal Insulation":
                # print("Thermal Insulation")
                for side in self.sidesData:
                    if self.currentSide == side['side']:
                        side['typeCondition'] =  typeCondition
                        side['heatConditionType'] = ""
                        side['data'] = 0
            # Temperature
            if typeCondition == "Temperature":
                # print("Temperature")
                try:
                    temperature = int(win.lEditTemperature.text())
                    for side in self.sidesData:
                        if self.currentSide == side['side']:
                            side['typeCondition'] =  typeCondition
                            side['heatConditionType'] = ""
                            side['data'] = temperature
                except:
                    msg = QMessageBox(win)
                    msg.setWindowTitle("Warning")
                    msg.setText("Tempererature is wrong, try again")
                    msg.exec_()
            if typeCondition == "Heat Flux":
                heatTypeCondition = win.cmbConditionType.currentText()
                # General inward heat flux
                if heatTypeCondition == "General inward heat flux":
                    # print("General inward heat flux")
                    try:
                        q0 = int(win.lEditHeatFlux.text())
                        for side in self.sidesData:
                            if self.currentSide == side['side']:
                                side['typeCondition'] =  typeCondition
                                side['heatConditionType'] = ""
                                side['data'] = q0
                    except:
                        msg = QMessageBox(win)
                        msg.setWindowTitle("Warning")
                        msg.setText("Heat flux is wrong, try again")
                        msg.exec_()
                if heatTypeCondition == "Convective heat flux":
                    # print("Convective heat flux")
                    try:
                        h = int(win.lEditHeatTransfer.text())
                        text = int(win.lEditExternalTemperature.text())
                        for side in self.sidesData:
                            if self.currentSide == side['side']:
                                side['typeCondition'] =  typeCondition
                                side['heatConditionType'] = ""
                                side['data'] = [h, text]
                    except:
                        msg = QMessageBox(win)
                        msg.setWindowTitle("Warning")
                        msg.setText("Heat flux is wrong, try again")
                        msg.exec_()
        if conditionsSelection == "All boundarys":
            print("All boundarys")
            if typeCondition == "Thermal Insulation":
                print("Thermal Insulation")
            if typeCondition == "Temperature":
                print("Temperature")
            if typeCondition == "Heat Flux":
                heatTypeCondition = win.cmbConditionType.currentText()
                if heatTypeCondition == "General inward heat flux":
                    print("General inward heat flux")
                if heatTypeCondition == "Convective heat flux":
                    print("Convective heat flux")
    def changeSelectionCondition(self, win):
        text = win.cmbConditionsSelection.currentText()
        lines = win.canvas.getEdges()

        if text == "All boundarys":
            # paint = QBrush(QColor(255,0,0,50))
            # Si existen lineas
            if lines:
                win.lWBoundarys.setEnabled(False)
                win.lblTypeConditionTitle.show()
                win.cmbTypeCondition.show()
                win.toolBoxTypeOfCondition.show()
                win.btnConditionsHelp.show()
                win.btnConditionsReset.show()
                win.btnConditionsApply.show()
                win.toolBoxInitialValuesConditions.show()
                win.lblFigureSelected.setText("All boundarys")

            redColor = QPen(Qt.red)
            redColor.setWidth(5)

            for line in lines:
                line.setPen(redColor)

        if text == "Manual":
            #Si existen lineas
            if lines:
                win.lWBoundarys.setEnabled(True)
                win.lblTypeConditionTitle.hide()
                win.cmbTypeCondition.hide()
                win.toolBoxTypeOfCondition.hide()
                win.btnConditionsHelp.hide()
                win.btnConditionsReset.hide()
                win.btnConditionsApply.hide()
                win.toolBoxInitialValuesConditions.hide()
                win.lblFigureSelected.setText("")

            LUBronze = QColor(156, 87, 20)
            defaultColor = QPen(LUBronze)
            defaultColor.setWidth(3)
            for line in lines:
                line.setPen(defaultColor)

    def selectedChangeTypeOfCondition(self, win, condition):
        if condition == "Thermal Insulation":
            for i in range(win.toolBoxTypeOfCondition.count()):
                win.toolBoxTypeOfCondition.setItemEnabled(i, False)
                toolBoxWidget = win.toolBoxTypeOfCondition.widget(i)
                toolBoxWidget.setEnabled(False)
        if condition == "Temperature":
            win.toolBoxTypeOfCondition.setCurrentIndex(0)
            for i in range(win.toolBoxTypeOfCondition.count()):
                toolBoxWidget = win.toolBoxTypeOfCondition.widget(i)
                if i == 0:
                    win.toolBoxTypeOfCondition.setItemEnabled(i, True)
                    toolBoxWidget.setEnabled(True)
                else:
                    win.toolBoxTypeOfCondition.setItemEnabled(i, False)
                    toolBoxWidget.setEnabled(False)
        if condition == "Heat Flux":
            win.toolBoxTypeOfCondition.setCurrentIndex(1)
            for i in range(win.toolBoxTypeOfCondition.count()):
                toolBoxWidget = win.toolBoxTypeOfCondition.widget(i)
                if i == 0:
                    win.toolBoxTypeOfCondition.setItemEnabled(i, False)
                    toolBoxWidget.setEnabled(False)
                else:
                    win.toolBoxTypeOfCondition.setItemEnabled(i, True)
                    toolBoxWidget.setEnabled(True)

    def selectedCurrentHeatFluxConditionType(self, win, conditionType):
        if conditionType == "General inward heat flux":
            win.lEditHeatFlux.setEnabled(True)
            win.lEditHeatTransfer.setEnabled(False)
            win.lEditExternalTemperature.setEnabled(False)
        if conditionType == "Convective heat flux":
            win.lEditHeatFlux.setEnabled(False)
            win.lEditHeatTransfer.setEnabled(True)
            win.lEditExternalTemperature.setEnabled(True)
    
    def selectedCurrentHeatFluxConditionType(self, win, conditionType):
        if conditionType == "General inward heat flux":
            win.lEditHeatFlux.setEnabled(True)
            win.lEditHeatTransfer.setEnabled(False)
            win.lEditExternalTemperature.setEnabled(False)
        if conditionType == "Convective heat flux":
            win.lEditHeatFlux.setEnabled(False)
            win.lEditHeatTransfer.setEnabled(True)
            win.lEditExternalTemperature.setEnabled(True)

    def changeTypeOfCondition(self, win, cmbTypeCondition):
        typeOfCondition = cmbTypeCondition.currentText()

        if typeOfCondition == "Thermal Insulation":
            for i in range(win.toolBoxTypeOfCondition.count()):
                win.toolBoxTypeOfCondition.setItemEnabled(i, False)
                toolBoxWidget = win.toolBoxTypeOfCondition.widget(i)
                toolBoxWidget.setEnabled(False)
        if typeOfCondition == "Temperature":
            win.toolBoxTypeOfCondition.setCurrentIndex(0)
            for i in range(win.toolBoxTypeOfCondition.count()):
                toolBoxWidget = win.toolBoxTypeOfCondition.widget(i)
                if i == 0:
                    win.toolBoxTypeOfCondition.setItemEnabled(i, True)
                    toolBoxWidget.setEnabled(True)
                else:
                    win.toolBoxTypeOfCondition.setItemEnabled(i, False)
                    toolBoxWidget.setEnabled(False)
        if typeOfCondition == "Heat Flux":
            self.currentHeatFluxConditionType(win)
            win.toolBoxTypeOfCondition.setCurrentIndex(1)
            for i in range(win.toolBoxTypeOfCondition.count()):
                toolBoxWidget = win.toolBoxTypeOfCondition.widget(i)
                if i == 0:
                    win.toolBoxTypeOfCondition.setItemEnabled(i, False)
                    toolBoxWidget.setEnabled(False)
                else:
                    win.toolBoxTypeOfCondition.setItemEnabled(i, True)
                    toolBoxWidget.setEnabled(True)
    
    

    def currentHeatFluxConditionType(self, win):
        conditionType = win.cmbConditionType.currentText()
        if conditionType == "General inward heat flux":
            win.lEditHeatFlux.setEnabled(True)
            win.lEditHeatTransfer.setEnabled(False)
            win.lEditHeatTransfer.setText("")
            win.lEditExternalTemperature.setEnabled(False)
            win.lEditExternalTemperature.setText("")

        if conditionType == "Convective heat flux":
            win.lEditHeatFlux.setEnabled(False)
            win.lEditHeatFlux.setText("")
            win.lEditHeatTransfer.setEnabled(True)
            win.lEditExternalTemperature.setEnabled(True)
