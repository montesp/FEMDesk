from ast import Pass
from operator import index, methodcaller
from unittest import findTestCases
from xml.dom.expatbuilder import CDATA_SECTION_NODE
import math
import numpy as np
from PyQt5.QtWidgets import QLineEdit, QTableWidget, QTableWidgetItem, QSpinBox, QGraphicsPolygonItem, QGraphicsItem, QMessageBox
from PyQt5.QtCore import QPointF, QRectF
from PyQt5.QtGui import QPolygonF, QColor

from Modules.Graphics.PP import Canvas


class Geometry():
    def currentTypeDrawing(section, combType, combFigure, array):
        section.show()

        for i in range(section.count()):
            section.removeItem(section.currentIndex())

        if (combType.currentText() == "Data"):
            section.insertItem(0, array[combFigure.currentIndex()], str(
                combFigure.currentText()))
            Geometry.resetData(section, combFigure)

    def resetData(sectionWidget, comb):
        """Reinicia los valores dentro del modo Data"""
        if comb.currentIndex() == 0:
            lineEditWidgets = sectionWidget.findChildren(QLineEdit)
            for lineEdit in lineEditWidgets:
                lineEdit.clear()
        
        if comb.currentIndex() == 1:
            spinBox = sectionWidget.findChild(QSpinBox, 'sbNumPoints')
            tableWidget = sectionWidget.findChild(QTableWidget, 'tbwPolygon')
            
            spinBox.setValue(spinBox.minimum())
            tableWidget.clearContents()
            tableWidget.setRowCount(spinBox.minimum())            

            for r in range(tableWidget.rowCount()):
                for c in range(2):
                    tableWidget.setCellWidget(r,c, QLineEdit())

    def setData(sectionWidget, comb, polygon:QPolygonF):
        """Recibe un QPolygonF y mete los valores en la tabla"""
        tableWidget = None
        spinBoxWidget = None
        tableCells = []

        #* Revisa si el objeto contiene un atributo qRectObj
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
            for r in range(tableWidget.rowCount()):
                for c in range(2):
                    tableWidget.setCellWidget(r, c, QLineEdit())
                    tableCells.append(tableWidget.cellWidget(r,c))
                    
            try:
                index = 0   
                for point in polygon:
                    tableCells[index].setText(str(point.x()))
                    tableCells[index+1].setText(str(point.y()))
                    index += 2
            except:
                pass

    def getData(sectionWidget, comb, selectedItems, canvas:Canvas):
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
                    if element.text().strip() == "":
                        raise ValueError("Una o más casillas vacías")

                    values.append(float(element.text()))
                    element.clear()

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

            except ValueError as e:
                canvas.warning(f"Error",
                f"No es posible crear la figura con los valores ingresados.\nCausa: {e}",
                level=2)
                return

        #* Polygon
        if comb.currentIndex() == 1:
            widgetElements.append(sectionWidget.findChild(QSpinBox, 'sbNumPoints'))
            widgetElements.append(sectionWidget.findChild(QTableWidget, 'tbwPolygon'))

            try:
                value = int(widgetElements[0].value())
                tableWidget = widgetElements[1]
                for r in range(value):
                    xValue = None
                    yValue = None

                    for c in range(2):
                        cellText = tableWidget.cellWidget(r, c).text() if tableWidget.cellWidget(r, c).text().strip() != "" else None
                        
                        if cellText is None:
                            col = "x" if c == 0 else "y"
                            raise ValueError(f"Casilla vacía para '{col}{r+1}'")

                        if c == 0:
                            xValue = float(cellText) 
                        else:
                            yValue = float(cellText)
                            tempPoly << QPointF(xValue, yValue)
                
                if selectedItems:
                    item = selectedItems[0]
                    canvas.deletePolygon(item)

                tableWidget.clearContents()
                tableWidget.setRowCount(widgetElements[0].minimum())
                widgetElements[0].setValue(widgetElements[0].minimum())

            except ValueError as e:
                canvas.warning(f"Error",
                f"No es posible crear la figura con los valores ingresados.\nCausa: {e}",
                level=2)
                return

        canvas.addPoly(tempPoly, holeMode = canvas.holeMode)
        canvas.enablePolygonSelect(False)

    def updateTable(sectionWidget, canvas:Canvas):
        """Permite insertar y remover filas de la tabla en el modo Data"""
        widgetElements = []
        widgetElements = sectionWidget.findChildren(QSpinBox)
        widgetElements += sectionWidget.findChildren(QTableWidget)

        value = int(widgetElements[0].value())
        tableWidget = widgetElements[1]

        tableWidget.setRowCount(value)

        for r in range(tableWidget.rowCount()):
            for c in range(2):
                tableWidget.setCellWidget(r,c, QLineEdit())

    def unionClicked(win):
        win.canvas.mode = "Union"
        win.btnDeletePolygon.setEnabled(False)
        win.btnIntersection.setEnabled(False)
        win.btnDifference.setEnabled(False)

    def intersectionClicked(win):
        win.canvas.mode = "Interseccion"
        win.btnDeletePolygon.setEnabled(False)
        win.btnUnion.setEnabled(False)
        win.btnDifference.setEnabled(False)

    def diferenceClicked(win):
        win.canvas.mode = "Diferencia"
        win.btnDeletePolygon.setEnabled(False)
        win.btnIntersection.setEnabled(False)
        win.btnUnion.setEnabled(False)

    def borrar(win):
        win.canvas.mode = "Borrado"
        win.btnUnion.setEnabled(False)
        win.btnIntersection.setEnabled(False)
        win.btnDifference.setEnabled(False)

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
        msg.setText("In the contruction by means there are three modes, Data, Mouse and Combination.\nIn Data you have to specify the number of points and their coordinates in the canvas, when you doble click in a polygon the coordinates of the poins are loaded to the table and you can modify them.\nIn Mouse you have to left click in the canvas to add a point, when you finished your figure press right click to close the figure.\nIn Combination you can draw a figure like in Mouse, but this figure can be adjacent and share a vertix with another.")
        msg.setIcon(QMessageBox.Warning)
        msg.setStandardButtons(QMessageBox.Cancel)

        msg.exec_()

    def funct( win, funct):
        if win.canvas.polyG == None:
            pass
        elif(funct == "bor"):
            win.canvas.mode = "Arrow"
            win.canvas.enablePolygonSelect()
            win.canvas.deletePolygon(win.canvas.polyG)
        else:
            #Movemos los objetos QPolygonF a las coordenadas globales y los unimos (mergeamos)
            p1 = win.canvas.polyG.polygon().translated(win.canvas.polyG.x(), win.canvas.polyG.y())
            p2 = win.canvas.polyN.polygon().translated(win.canvas.polyN.x(), win.canvas.polyN.y())
            if funct == "uni":
                uni = p1.united(p2)
            if funct == "int":
                uni = p1.intersected(p2)
            if funct == "dif":
                uni = p1.subtracted(p2)

            #Unite agrega el punto inicial como punto final asi que removemos este punto final
            uni = win.canvas.polyToList(uni, "Global")
            uni = uni[:-1]

            #Agregamos el nuevo poligono y removemos los viejor de la vista y las listas
            win.canvas.addPoly(QPolygonF(uni),False)
            win.canvas.deletePolygon(win.canvas.polyG, True)
            win.canvas.deletePolygon(win.canvas.polyN, True)
            
            #Vaciamos las variables de seguimiento
            win.canvas.polyG = None
            win.canvas.polyN = None
            
        win.canvas.mode = "Arrow"
        win.canvas.enablePolygonSelect()
        win.btnUnion.setEnabled(True)
        win.btnDeletePolygon.setEnabled(True)
        win.btnIntersection.setEnabled(True)
        win.btnDifference.setEnabled(True)
        win.resetConstructionBy()

    def mode2( win):
        if(win.canvas.mode == "Union"):
            Geometry.funct(win, "uni")
        if(win.canvas.mode == "Interseccion"):
            Geometry.funct(win, "int")
        if(win.canvas.mode == "Diferencia"):
            Geometry.funct(win, "dif")
        if(win.canvas.mode == "Borrado"):
            Geometry.funct(win,"bor")

    def mode2Cancel(win):
        win.canvas.mode = "Arrow"
        if (win.canvas.polyG == None):
            pass
        elif (win.canvas.polyN == None):
            win.canvas.polyG.setBrush(QColor(0,0,0,50))
        else:
            win.canvas.polyG.setBrush(QColor(0,0,0,50))
            win.canvas.polyN.setBrush(QColor(0,0,0,50))
        win.canvas.polyG = None
        win.canvas.polyN = None
        win.btnUnion.setEnabled(True)
        win.btnDeletePolygon.setEnabled(True)
        win.btnIntersection.setEnabled(True)
        win.btnDifference.setEnabled(True)