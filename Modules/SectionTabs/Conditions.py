from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPen, QColor, QBrush

class Conditions():
    def __init__(self):
        self.sidesData = None

    def reloadEdges(self, canvas, listWid):
        edges = canvas.getEdges()
        listOfPolys = []

        if listWid.count() != 0:
            listWid.clear()

        for i in range(len(edges)):
            polygon = str(i+1)
            listOfPolys.append({'edge':edges[i], 'text':polygon, 'indice':i })
            listWid.addItem(polygon)


    def currentElementSelectListWidgets(self, win, element, canvas, lblFigureSelected):
        index = int(element.text())
        edges = canvas.getEdges()
        line = edges[index-1]
        print(line)
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

        self.changeTypeOfCondition(win, win.cmbTypeCondition)
        self.currentHeatFluxConditionType(win)

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
            win.lEditExternalTemperature.setEnabled(False)
        if conditionType == "Convective heat flux":
            win.lEditHeatFlux.setEnabled(False)
            win.lEditHeatTransfer.setEnabled(True)
            win.lEditExternalTemperature.setEnabled(True)

