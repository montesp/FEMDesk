from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPen, QColor

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

