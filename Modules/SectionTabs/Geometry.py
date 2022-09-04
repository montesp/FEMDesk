from ast import Pass
from cmath import log
from operator import index
from xml.dom.expatbuilder import CDATA_SECTION_NODE
import numpy as np
from PyQt5.QtWidgets import QLineEdit, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import QPointF
from PyQt5.QtGui import QPolygonF


class Geometry():
    def currentTypeDrawing(section, combType, combFigure, array):
        section.show()

        for i in range(section.count()):
            section.removeItem(section.currentIndex())

        if (combType.currentText() == "Data"):
            # if combFigure.currentIndex() <= 4:
            section.insertItem(0, array[combFigure.currentIndex()], str(
                combFigure.currentText()))

    def getData(sectionWidget, comb):
        widgetElements = []
        widgetElements = sectionWidget.findChildren(QLineEdit)

        if comb.currentIndex() == 0:
            try:
            #! Temp code because order is screwed up
            # waiting on @montesp

                uoValues = np.array([]) #: Unordered values from QLineEdits
                order = np.array([1,2,4,0,3])
                
                for element in widgetElements:
                    #! Unordered values: y,w,h,r,x
                    uoValues = np.append(uoValues, int(element.text()))

                #! Ordered values: w,h,x,y,r
                oValues = uoValues[order]

                width,height = oValues[0], oValues[1]
                x1,y1 = oValues[2] - (width / 2), oValues[3] - (height / 2) #* Top left corner
                x2,y2 = x1 + width, y1 + height #* Bottom right corner

                tempPoly = QPolygonF()
                tempPoly << QPointF(x1,y1)
                tempPoly << QPointF(x2,y1)
                tempPoly << QPointF(x2,y2)
                tempPoly << QPointF(x1,y2)

                return tempPoly

            except ValueError:
                return QPolygonF()

        if comb.currentIndex() == 1:
            widgetElements += sectionWidget.findChildren(QTableWidget)
            poly = QPolygonF()

            try:
                value = int(widgetElements[0].text())
                table = widgetElements[1]
                for i in range(value):
                    xValue = None
                    yValue = None

                    for j in range(2):
                        if table.item(i, j) is not None:
                            if j == 0:
                                xValue = float(table.item(i, j).text())
                            else:
                                yValue = float(table.item(i, j).text())
                                poly << QPointF(xValue, yValue)

                        else:
                            raise ValueError("Espacio vacio en: ", i, j)

                return poly

            except ValueError:
                print("Error al aplicar cambios. Espacios vacÃ­os en coordenadas")
                return QPolygonF()

    def updateTable(sectionWidget, comb):
        widgetElements = []
        widgetElements = sectionWidget.findChildren(QLineEdit)
        widgetElements += sectionWidget.findChildren(QTableWidget)

        try:
            if widgetElements[0].text() == "":
                print("No puedes dejar este espacio vacio")
            else:
                value = int(widgetElements[0].text())
                table = widgetElements[1]

                # Quitar elementos de la tabla
                table.setRowCount(0)

                for i in range(value):
                    table.insertRow(i)
                    table.setItem(i, i+1, QTableWidgetItem())

        except ValueError:
            print('Solo se aceptan numeros')
