from ast import Pass
from operator import index, methodcaller
from unittest import findTestCases
from xml.dom.expatbuilder import CDATA_SECTION_NODE
import math
import numpy as np
from PyQt5.QtWidgets import QLineEdit, QTableWidget, QTableWidgetItem, QSpinBox, QGraphicsPolygonItem, QGraphicsItem, QMessageBox
from PyQt5.QtCore import QPointF, QRectF
from PyQt5.QtGui import QPolygonF

from canvas.PP import Canvas


class Geometry():
    def currentTypeDrawing(section, combType, combFigure, array):
        section.show()

        for i in range(section.count()):
            section.removeItem(section.currentIndex())

        if (combType.currentText() == "Data"):
            section.insertItem(0, array[combFigure.currentIndex()], str(
                combFigure.currentText()))
    
    # def currentTypeCheckBox(combType , chkElement):
    #     if (combType.currentText() == "Data"):
    #         chkElement.show()
    #     else:
    #         chkElement.hide()
    

    def setTableData(sectionWidget, comb, polygon:QPolygonF):
        """Recibe un QPolygonF y mete los valores en la tabla"""
        tableWidget = None
        spinBoxWidget = None
        tableCells = []

        if hasattr(polygon, "qRectObj"):
            if comb.currentIndex() != 0:
                comb.setCurrentIndex(0)
                return

            lineEditWidgets = []
            nameElements = ["lEditWidthRectangle", "lEditHeightRectangle", "lEditXRectangle", "lEditYRectangle", "lEditRotationRectangle"]
            for i in range(len(nameElements)):
                lineEditWidgets.append(sectionWidget.findChild(QLineEdit, nameElements[i]))

            rect = polygon.qRectObj

            width, height = rect.width(), rect.height()            
            c = rect.center()
            x,y = c.x(), c.y()
            rot = polygon.rotation

            lineEditWidgets[0].setText(str(width))
            lineEditWidgets[1].setText(str(height))
            lineEditWidgets[2].setText(str(x))
            lineEditWidgets[3].setText(str(y))
            lineEditWidgets[4].setText(str(rot))

        else:
            if comb.currentIndex() != 1: 
                comb.setCurrentIndex(1)
                return
           
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

    def getTableData(sectionWidget, comb, selectedItems, canvas:Canvas):
        """
        Agrega un nuevo QPolygonF al QGraphicsScene

        Regresa los datos de la tabla en forma de QPolygonF
        """
        tempPoly = QPolygonF()
        widgetElements = []
        #* Rectangle
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

                #! Unrotated values
                width,height =values[0],values[1]
                cx, cy = values[2],values[3]
                x1,y1 = cx - (width / 2), cy - (height / 2) #* Top left corner
                x2,y2 = x1 + width, y1 + height #* Bottom right corner
                degrees = values[4]

                qRectObj = QRectF(x1, y1, width, height)

                tempPoly << rotatePoint(cx, cy, degrees, QPointF(x1,y1))
                tempPoly << rotatePoint(cx, cy, degrees, QPointF(x2,y1))
                tempPoly << rotatePoint(cx, cy, degrees, QPointF(x2,y2))
                tempPoly << rotatePoint(cx, cy, degrees, QPointF(x1,y2))
                
                tempPoly.__setattr__("qRectObj", qRectObj)
                tempPoly.__setattr__("rotation", degrees)

                if selectedItems:
                    item = selectedItems[0]
                    canvas.deletePolygon(item)

            except ValueError:
                print("Error al aplicar cambios. Por favor llenar todos los campos")
                tempPoly = QPolygonF()

        #* Polygon
        if comb.currentIndex() == 1:
            widgetElements.append(sectionWidget.findChild(QSpinBox, 'sbNumPoints'))
            widgetElements.append(sectionWidget.findChild(QTableWidget, 'tbwPolygon'))

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
                                tempPoly << QPointF(xValue, yValue)
                        else:
                            raise ValueError("Espacio vacio en:" , i, j)
                
                if selectedItems:
                    item = selectedItems[0]
                    canvas.deletePolygon(item)

            except ValueError as e:
                print(e)
                print("Error al aplicar cambios.")
                tempPoly = QPolygonF()

        canvas.addPoly(tempPoly, holeMode = canvas.holeMode)
        canvas.enablePolygonSelect()

        return tempPoly

    def updateTable(sectionWidget, comb):
        widgetElements = []
        widgetElements = sectionWidget.findChildren(QSpinBox)
        widgetElements += sectionWidget.findChildren(QTableWidget)

        try:
            if widgetElements[0].text() == "":
                print("No puedes dejar este espacio vacio")
            else:
                value = int(widgetElements[0].value())
                table = widgetElements[1]

                # Quitar elementos de la tabla
                table.setRowCount(0)

                for i in range(value):
                    table.insertRow(i)
                    table.setItem(i, i+1, QTableWidgetItem())

        except ValueError as e:
            print(e)

    def unionClicked(win):
        win.canvas.mode = "Union"

    def intersectionClicked(win):
        win.canvas.mode = "Interseccion"

    def diferenceClicked(win):
        win.canvas.mode = "Diferencia"

    def resetClicked(self):
        print('reset')

    def helpClicked(self):
        msg = QMessageBox()
        msg.setWindowTitle("Information union, subtraction and intersection")
        msg.setText("Select two polygons:\nUnion: adds the polygon that is the union of the selected polygons\n Intersection: adds the intersecion of the two and removes the two polygons\n Substraction: removes the intersection of the first polygon with the second")
        msg.setIcon(QMessageBox.Warning)
        msg.setStandardButtons(QMessageBox.Cancel)

        msg.exec_()

    def helpClicked2(self):
        msg = QMessageBox()
        msg.setWindowTitle("Information Data, Mouse and Combination")
        msg.setText("In the contruction by means there are three modes, Data, Mouse and Combination.\nIn Data you have to specify the number of points and their coordinates in the canvas.\nIn Mouse you have to left click in the canvas to add a point, when you finished your figure press right click to close the figure.\nIn Combination you can draw a figure like in Mouse, but this figure can be adjacent and share a vertix with another.")
        msg.setIcon(QMessageBox.Warning)
        msg.setStandardButtons(QMessageBox.Cancel)

        msg.exec_()