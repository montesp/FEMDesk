from ast import Pass
from operator import index, methodcaller
from unittest import findTestCases
from xml.dom.expatbuilder import CDATA_SECTION_NODE
import math
import numpy as np
from PyQt5.QtWidgets import QLineEdit, QTableWidget, QTableWidgetItem, QSpinBox, QGraphicsPolygonItem, QGraphicsItem
from PyQt5.QtCore import QPointF
from PyQt5.QtGui import QPolygonF, QTransform


class Geometry():
    def currentTypeDrawing(section, combType, combFigure, array):
        section.show()

        for i in range(section.count()):
            section.removeItem(section.currentIndex())

        if (combType.currentText() == "Data"):
            section.insertItem(0, array[combFigure.currentIndex()], str(
                combFigure.currentText()))
    
    def currentTypeCheckBox(combType , chkElement):
        if (combType.currentText() == "Data"):
            chkElement.show()
        else:
            chkElement.hide()
    

    def setTableData(sectionWidget, comb, polygon:QPolygonF):
        tableWidget = None
        spinBoxWidget = None
        tableCells = []

        if comb.currentIndex() == 1:
            spinBoxWidget = sectionWidget.findChild(QSpinBox, 'sbNumPoints')
            tableWidget = sectionWidget.findChild(QTableWidget, 'tbwPolygon')
            tableWidget.setRowCount(len(polygon))

            spinBoxWidget.setValue(tableWidget.rowCount())
            for i in range(tableWidget.rowCount()):
                for j in range(2):
                    tableWidget.setCellWidget(i, j, QLineEdit())
                    tableCells.append(tableWidget.cellWidget(i,j))
                    
            try:
                index = 0   
                for point in polygon:
                    tableCells[index].setText(str(point.x()))
                    tableCells[index+1].setText(str(point.y()))
                    index += 2
            except:
                pass



    def getTableData(sectionWidget, comb, selectedItem:QGraphicsPolygonItem, deletePolygon):
        widgetElements = []
        # Rectangle
        if comb.currentIndex() == 0:
            try:
                # Guarda los elementos de los ledit
                nameElements = ["lEditWidthRectangle", "lEditHeightRectangle", "lEditXRectangle", "lEditYRectangle", "lEditRotationRectangle"]
                for i in range(len(nameElements)):
                    widgetElements.append(sectionWidget.findChild(QLineEdit, nameElements[i]))

                def rotatePoint(cx, cy, deg, point:QPointF):
                    rads = math.pi/180
                    sin = math.sin(-deg*rads)
                    cos = math.cos(-deg*rads)

                    tempX = point.x() - cx
                    tempY = point.y() - cy

                    #->Rotation
                    newX = tempX * cos - tempY * sin
                    newY = tempX * sin + tempY * cos

                    point.setX(newX + cx)
                    point.setY(newY + cy)

                    return point


                values = []
                # Se acomodan los valores de los lEdits
                for element in widgetElements:
                    values.append(float(element.text()))

                width,height =values[0],values[1]
                cx, cy =values[2],values[3]
                x1,y1 = cx - (width / 2), cy - (height / 2) #* Top left corner
                x2,y2 = x1 + width, y1 + height #* Bottom right corner
                degrees =values[4]

                tempPoly = QPolygonF()
                tempPoly << rotatePoint(cx, cy, degrees, QPointF(x1,y1))
                tempPoly << rotatePoint(cx, cy, degrees, QPointF(x2,y1))
                tempPoly << rotatePoint(cx, cy, degrees, QPointF(x2,y2))
                tempPoly << rotatePoint(cx, cy, degrees, QPointF(x1,y2))

                return tempPoly

            except ValueError:
                print("Error al aplicar cambios. Por favor llenar todos los campos")
                return QPolygonF()

        # Polygon
        if comb.currentIndex() == 1:
            widgetElements.append(sectionWidget.findChild(QSpinBox, 'sbNumPoints'))
            widgetElements.append(sectionWidget.findChild(QTableWidget, 'tbwPolygon'))

            poly = QPolygonF()
            try:
                value = int(widgetElements[0].text())
                tableWidget = widgetElements[1]
                for i in range(value):
                    xValue = None
                    yValue = None

                    for j in range(2):
                        if tableWidget.cellWidget(i, j) is not None:
                            if j == 0:
                                xValue = float(tableWidget.cellWidget(i, j).text())
                            else:
                                yValue = float(tableWidget.cellWidget(i, j).text())
                                poly << QPointF(xValue, yValue)

                        else:
                            raise ValueError("Espacio vacio en:" , i, j)
                
                if selectedItem:
                    deletePolygon(selectedItem)

            except ValueError as e:
                print(e)
                print("Error al aplicar cambios.")
                return QPolygonF()
                
            return poly

    def updateTable(sectionWidget, comb):
        widgetElements = []
        widgetElements = sectionWidget.findChildren(QSpinBox)
        widgetElements += sectionWidget.findChildren(QTableWidget)

        try:
            if widgetElements[0].text() == "":
                print("No puedes dejar este espacio vacio")
            else:
                value = int(widgetElements[0].value())
                print(value)
                table = widgetElements[1]

                # Quitar elementos de la tabla
                table.setRowCount(0)

                for i in range(value):
                    table.insertRow(i)
                    table.setItem(i, i+1, QTableWidgetItem())

        except ValueError as e:
            print(e)
