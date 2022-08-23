from cmath import log
from ctypes import sizeof
import itertools
from functools import cmp_to_key
from operator import length_hint

import sys
import PyQt5
import numpy as np
from PyQt5.QtCore import QPointF, QLineF, QRectF, QRegExp, Qt, QRect
from PyQt5.QtGui import QPen, QColor, QBrush, QPolygonF, QFont, QRegExpValidator
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QFileDialog, QGraphicsScene, \
    QGraphicsItem, QGraphicsPolygonItem, QToolButton, QLabel, \
    QGraphicsEllipseItem, QLineEdit, QFormLayout, QGraphicsLineItem, QGraphicsTextItem, QGridLayout, QPushButton, QGraphicsItem, QGraphicsView, \
    QVBoxLayout, QMessageBox, QSlider

import matplotlib as mpl
mpl.use('Qt5Agg')

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

import geometry as cfg
import mesh as cfm
import vis_mpl as cfv

class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=5, dpi=100):
        fig = Figure(figsize=(width,height), dpi=dpi)
        super(MplCanvas, self).__init__(fig)

class Canvas(QWidget):
    def __init__(self, parentScene, parentt):
        super(Canvas, self).__init__()
        self.parentScene = parentScene
        self.parentt = parentt
        # Referencia a la escena padre. Permite acceder a las funciones de dibujo
        #! Esto no es necesario
        #! self.scene = QGraphicsScene(parent)
        #self.mplLayout = helper.mplLayout

        # Brushes y Pens
        self.greenBrush = QBrush(Qt.green)
        self.blackPen = QPen(Qt.black)
        self.blackPen.setWidth(5)

        # Variables de seguimiento
        self.newPoly = True
        self.firstPoint = None
        self.prevPoint = None
        self.currentPoly = None

        # Listas y variables de seguimiento
        self.polyList = []
        self.edgeList = []
        self.holeList = []
        self.labelsList = []

        self.potentialEdgeSplitters = []
        
        self.pointCoordList = np.zeros((1, 2))
        self.connectingRect = None
        self.connectingLine = None
        self.connectingLineList = []
        self.drawingPoly = QPolygonF()
        self.drawingPoints = []
        self.drawingPointsCoords = []
        self.drawingRect = QPolygonF()
        self.holeMode = False

        # Standard Mesh settings
        self.elType = 2
        self.dofsPerNode = 1
        self.elSizeFactor = 25

        # Colores de polígono
        self.LUBlue = QColor(0, 0, 128)
        self.LUBronze = QColor(156, 97, 20)
        self.LUBronzeDark = QColor(146, 87, 10)

        # Modo de operación dentro del programa
        # :Modos disponibles:
        #-> Arrow, Draw Poly, Draw Rect
        self.mode = "Draw poly"

        # Permitir el seguimiento del puntero dentro del canvas
        self.setMouseTracking(True)


        self.fig = cfv.figure()
        self.figureCanvas = cfv.figure_widget(self.fig)

    def mouseReleaseEvent(self, event):
        super(Canvas, self).mouseReleaseEvent(event)
        # If a point or polygon is selected releasing the mouse will de-select the object and add the
        # current coordinates back to the global coordinate list to update to the new position
        if self.mode == "Arrow":
            self.parentScene.clearSelection() 

    def popupButton(self, i):
        self.overlapWarningChoice = i.text()

    def intersectionError(self): 
        msg = QMessageBox()
        msg.setWindowTitle("Error")
        msg.setText("Hay un poligono que esta encimado consigo mismo")
        msg.setIcon(QMessageBox.Critical)
        msg.setStandardButtons(QMessageBox.Cancel)

        msg.exec_()

    def overlapWarning(self):
        msg = QMessageBox()
        msg.setWindowTitle("Advertencia")
        msg.setText("Hay figuras que se sobreponen")
        msg.setIcon(QMessageBox.Warning)
        msg.setStandardButtons(QMessageBox.Cancel | QMessageBox.Ignore)

        msg.buttonClicked.connect(self.popupButton)
        msg.exec_()
        return self.overlapWarningChoice
            
    def mouseDoubleClickEvent(self, event, layout, widget):
        if self.mode == "Arrow":
            super(Canvas, self).mouseDoubleClickEvent(event)
            # If in the surface view highlight the polygon to allow updating exact values of the corner points
            if self.parentScene.selectedItems():
                for label in  self.labelsList:
                    label.setVisible(False);
                self.labelsList = [];
                if isinstance(self.parentScene.selectedItems()[0], PyQt5.QtWidgets.QGraphicsPolygonItem):
                    index = 0
                    poly = self.parentScene.selectedItems()[0]

                    grid = layout
                    for i in reversed(range(layout.count())): 
                        grid.itemAt(i).widget().deleteLater()

                    widget.setGeometry(10, 250, 200, len(self.polyToList(poly, "Global"))*50)
                    # Add a x- and y- editor for each point of the polygon
                    for point in self.polyToList(poly, "Global"):
                        self.labelsList.append(self.parentScene.addText("Punto "+str(index+1)))
                        self.labelsList[index].setPos(QPointF(point.x()-10, point.y()-10) - self.labelsList[index].boundingRect().center())

                        validator = QRegExpValidator(QRegExp("\\-*\\d*\\.\\d+"))
                        labelX = QLineEdit(str(point.x()))
                        labelX.setValidator(validator)
                        labelY = QLineEdit(str(-point.y()))
                        labelY.setValidator(validator)
                        grid.addWidget(labelX, index, 0)
                        grid.addWidget(labelY, index, 1)
                        label1 = QLabel()
                        text = ("Punto "+ str((index+1)))
                        label1.setText(text)    
                        layout.addWidget(label1, index, 2)
                        index += 1

                    def update():
                        # Update the polygon with the new edited values
                        labelIndex = 0
                        i = 0
                        for childItem in poly.childItems():
                            if isinstance(childItem, PyQt5.QtWidgets.QGraphicsEllipseItem):
                                if childItem.localIndex == i:
                                    x = float(grid.itemAtPosition(i, 0).widget().text())
                                    y = -float(grid.itemAtPosition(i, 1).widget().text())
                                    circ = childItem
                                    self.moveNode(circ, poly, x, y)
                                    point = circ.scenePos()
                                    self.labelsList[labelIndex].setPos(QPointF(point.x()-10, point.y()-10) - self.labelsList[labelIndex].boundingRect().center())
                                    self.pointCoordList = np.append(self.pointCoordList,
                                                                        [[point.x(), point.y()]], axis=0)
                                    i += 1
                                labelIndex += 1
                        
                    updateButton = (QPushButton("Update"))
                    updateButton.setStyleSheet("border: 3px solid rgb(0,0,128);")
                    grid.addWidget(updateButton, index + 1, 1)
                    updateButton.clicked.connect(update)


    def mousePressEvent(self, e):
        #: Evento de un click del mouse
        x = e.pos().x()
        y = e.pos().y()

        if self.mode == "Arrow":
            super(Canvas, self).mousePressEvent(e)

            # Si el botón presionado es otro al izquierdo del mouse
            if e.button() != 1:
                return

        if self.mode == "Draw poly":
            if e.button() == 2:
                # Si un polígono está siendo dibujado, terminar el polígono presionando el botón derecho del mouse.
                # Esto cerrará el polígono y removerá las lineas de soporte iniciales,
                # dejando únicamente las líneas y puntos del polígono terminado.

                # Si el polígono a dibujar contiene 2 o menos puntos no se dibujará
                if self.newPoly or self.currentPoly.__len__() <= 2:
                    return
                
                self.addPoly(self.currentPoly, holeMode=self.holeMode)
                self.removeDrawingPoly()

                # Resetear variables a su estado inicial
                self.currentPoly = None
                self.newPoly = True
                self.firstPoint = None
                self.prevPoint = None

            elif e.button() == 1:
                # Si se está dibujando un nuevo polígono
                if self.newPoly:
                    # Inicializar nuevo poligono como objeto de tipo QPolygonF()
                    self.currentPoly = QPolygonF()

                    point = self.parentScene.addEllipse(
                        x - 3, y - 3, 6, 6, self.blackPen, self.greenBrush)

                    # Guardamos coordenadas del punto inicial del nuevo polígono    
                    self.firstPoint = QPointF(x, y)
                    self.prevPoint = QPointF(x, y)

                    # Pasar el punto inicial al poligono a construir
                    self.currentPoly << self.firstPoint
                    self.newPoly = False

                    self.drawingPoints.append(point)
                    self.drawingPointsCoords.append([x, y])
                else:
                    point = self.parentScene.addEllipse(
                        x - 3, y - 3, 6, 6, self.blackPen, self.greenBrush)

                    # Dibujamos linea entre punto actual y el anterior
                    line = self.parentScene.addLine(
                        QLineF(self.prevPoint, QPointF(x, y)), self.blackPen)

                    # Guardamos coordenada del punto recién dibujado
                    self.prevPoint = QPointF(x, y)

                    # Pasar el punto previo al Poligono a construir
                    self.currentPoly << self.prevPoint

                    self.connectingLineList.append(line)
                    self.drawingPoints.append(point)
                    self.drawingPointsCoords.append([x, y])

        if self.mode == "Draw rect":
            # Si se está dibujando un nuevo polígono
            if self.newPoly:
                # Guardar coordenada del punto recién dibujado
                self.prevPoint = QPointF(x, y)
                self.newPoly = False
            # Catch para evitar crear un rectángulo donde los puntos estén sobrepuestos
            elif self.prevPoint.x() == x or self.prevPoint.y() == y:
                pass  
            else:
                r = self.connectingRect.rect()
                x1 = r.x()
                x2 = r.x() + r.width()
                y1 = r.y()
                y2 = r.y() + r.height()
                self.drawingRect << QPointF(x1, y1)
                self.drawingRect << QPointF(x2, y1)
                self.drawingRect << QPointF(x2, y2)
                self.drawingRect << QPointF(x1, y2)

                self.addPoly(self.drawingRect, holeMode=self.holeMode)
                self.removeDrawingRect()

    def addPoly(self, polygon, holeMode):
        """ Agrega un polígono a la escena padre. Regresa QPolygonF"""
        # Si el modo de dibujo es de agujero
        if holeMode:
            poly = self.parentScene.addPolygon(polygon, QPen(QColor(0, 0, 0, 0)), QBrush(QColor(255, 255, 255)))
            poly.setZValue(1)
            self.polyList.append(poly)
            self.holeList.append(poly)
        else:
            poly = self.parentScene.addPolygon(polygon, QPen(QColor(0, 0, 0, 0)), QBrush(QColor(0, 0, 0, 50)))
            self.polyList.append(poly)
        self.addPolyCorners(poly)
        self.addPolyEdges(poly)
        return poly

    def addPolyCorners(self, polyItem):
        """ Agrega puntos/vertices del polígono dibujado"""
        poly = polyItem.polygon()

        for i in range(poly.size()):
            point = poly.at(i)
            p = self.parentScene.addEllipse(-4, -4, 8, 8, self.LUBronze, self.LUBronze)
            p.setZValue(2)  # Make sure corners always in front of polygon surfaces
            p.setParentItem(polyItem)
            p.__setattr__("localIndex", int(i))
            p.setPos(point.x(), point.y())
            self.pointCoordList = np.append(self.pointCoordList, [[p.x(), p.y()]], axis=0)

    def addPolyEdges(self, polyItem):
        """ Agrega líneas/caras del polígono dibujado"""
        poly = polyItem.polygon()

        for i in range(1, poly.size() + 1):
            if i == poly.size():
                p1 = poly.at(i - 1)
                p2 = poly.at(0)
                index = -poly.size()

            else:
                p1 = poly.at(i - 1)
                p2 = poly.at(i)
                index = i

            line = self.parentScene.addLine(QLineF(p1, p2))
            line.setZValue(-1)
            displayLine = self.parentScene.addLine(QLineF(p1, p2), QPen(self.LUBronze, 3))
            line.__setattr__("localIndex", index)
            line.setParentItem(polyItem)
            displayLine.setParentItem(line)
            self.edgeList.append(line)

    def removeDrawingPoly(self):
        """Hace invisble el polígono auxiliar. Deja solo visible el polígono terminado"""
        self.currentPoly = QPolygonF()
        self.drawingPointsCoords = []

        for p in self.drawingPoints:
            p.setVisible(False)

        for line in self.connectingLineList:
            line.setVisible(False)

        if self.connectingLine:
            self.connectingLine.setVisible(False)

        self.connectingLine = None
        self.newPoly = True

    def removeDrawingRect(self):
        """Hace invisible el rectángulo auxiliar. Deja visible el rectángulo terminado"""
        self.drawingRect = QPolygonF()
        if self.connectingRect:
            self.connectingRect.setVisible(False)
        self.connectingRect = None
        self.newPoly = True
    
    def moveNode(self, circ, poly, newX, newY):
        # En teoria se utiliza para actualizar los puntos, las coodenadas de los puntos en las listas
        polyList = self.polyToList(poly,
                                      "Local")
        # Extrae las posicion de los puntos del poligono antes de mover el punto

        tempPoint = QGraphicsEllipseItem()
        tempPoint.setPos(newX, newY)
        if tempPoint.pos() in self.polyToList(poly, "Global"):
            return
        # No permite que se sobrepongan dos puntos en el mismo poligono

        index = polyList.index(circ.pos())  
        # Consigue el index del circulo seleccionado

        circ.setPos(newX - poly.scenePos().x(), newY - poly.scenePos().y())  
        # Mueve el circulo seleccionado

        polyList[index] = circ.pos()  
        # Actualiza las coordenadas del punto en la lista de poligonos

        poly.setPolygon(QPolygonF(polyList))  
        # Actualiza el poligono con la nueva lista

        # Hace loop a todos los bordes del poligono para determinar que dos lineas estan conectadas al punto que movimos
        # actualiza esos bordes con el nuevo punto
        # las lineas que lo se conectan con este punto son: la que tiene el mismo index que el punto y la que tiene el index-1
        # excepcion 1: cuando seleccionamos el index 0, en este caso utilizamos el ultimo borde indexandalo con un indice negativo
        # excepcion 2: cuando escogemos el borde con el index mayor, el ultimo inex esta indexado con un simbolo negativo
        # en este caso lo atrapamos con un if
        for item in poly.childItems():
            if isinstance(item, PyQt5.QtWidgets.QGraphicsLineItem):
                if circ.localIndex == 0:
                    if item.localIndex < 0:
                        line = item.line()
                        line.setP2(circ.pos())
                        item.setLine(line)
                        item.childItems()[0].setLine(line)
                        if item.childItems()[0].childItems():
                            text = item.childItems()[0].childItems()[0]
                            text.setPos((item.line().x1() + item.line().x2()) / 2,
                                        (item.line().y1() + item.line().y2()) / 2)
                if item.localIndex == circ.localIndex:
                    line = item.line()
                    line.setP2(circ.pos())
                    item.setLine(line)
                    item.childItems()[0].setLine(line)
                    if item.childItems()[0].childItems():
                        text = item.childItems()[0].childItems()[0]
                        text.setPos((item.line().x1() + item.line().x2()) / 2,
                                    (item.line().y1() + item.line().y2()) / 2)
                if item.localIndex == circ.localIndex + 1:
                    line = item.line()
                    line.setP1(circ.pos())
                    item.setLine(line)
                    item.childItems()[0].setLine(line)
                    if item.childItems()[0].childItems():
                        text = item.childItems()[0].childItems()[0]
                        text.setPos((item.line().x1() + item.line().x2()) / 2,
                                    (item.line().y1() + item.line().y2()) / 2)
                if circ.localIndex == poly.polygon().size() - 1:
                    if item.localIndex < 0:
                        line = item.line()
                        line.setP1(circ.pos())
                        item.setLine(line)
                        item.childItems()[0].setLine(line)
                        if item.childItems()[0].childItems():
                            text = item.childItems()[0].childItems()[0]
                            text.setPos((item.line().x1() + item.line().x2()) / 2,
                                        (item.line().y1() + item.line().y2()) / 2)

    def mouseMoveEvent(self, event):
        # Conseguimos las coordenadas X y Y del mouse cada vez que se mueve
        x = event.pos().x()
        y = event.pos().y() 

        if self.mode == "Draw poly":
            # Esto muestra la linea desde el punto anterior a la posicion del mouse
            if self.newPoly:
                pass  # No dibuja nada si el primer punto no ha sido dibujado
            else:

                # Si ya existe un punto hay dos casos:
                
                if self.connectingLine:
                    self.connectingLine.setLine(QLineF(self.prevPoint, QPointF(x, y)))
                    # Caso 1: si ya existe una linea, actualiza las coordenadas finales con la posicion del mouse
                else:
                    self.connectingLine = self.parentScene.addLine(QLineF(self.prevPoint, QPointF(x, y)))
                    # caso 2: si no hay una linea creada, crea una con el punto inicial en 
                    # slas coordenadas del punto anterior y la coordenada final 
                    # en la posicion del mouse.

        if self.mode == "Draw rect":
            # Muestra el rectangulo de ayuda desde el punto anterior hasta la posicion actual del mouse
            if self.newPoly:
                pass  # Si el primer punto no ha sido dibujado, no dibuja nada
            else:
                # Si el primer punto ya fue dibujado
                if self.connectingRect:
                    # Si existe un rectangulo lo actualiza con la posicion actual del mouse
                    if self.prevPoint.x() > x and self.prevPoint.y() > y:
                        self.connectingRect.setRect(QRectF(QPointF(x, y), self.prevPoint))
                    elif self.prevPoint.x() > x:
                        self.connectingRect.setRect(
                            QRectF(QPointF(x, self.prevPoint.y()), QPointF(self.prevPoint.x(), y)))
                    elif self.prevPoint.y() > y:
                        self.connectingRect.setRect(
                            QRectF(QPointF(self.prevPoint.x(), y), QPointF(x, self.prevPoint.y())))
                    else:
                        self.connectingRect.setRect(QRectF(self.prevPoint, QPointF(x, y)))
                else:
                    #Si no existe un rectangulo crea uno nuevo
                    self.connectingRect = self.parentScene.addRect(QRectF(self.prevPoint, QPointF(x, y)))

    def polyToList(self, poly, scope: str):
        # Extrae lo puntos de un QGraphicsPolygonItem o un QPolygonF y regresa una lista de todos los QPointF que contiene
        # si el scoope es global regresa las coordenadas de la escena, si no regresa las coordenadas locales
        innerList = []
        x = 0
        y = 0

        # Para que pueda manejar QGraphicsPolygonItem y QPolygonF como inputs
        if isinstance(poly, PyQt5.QtWidgets.QGraphicsPolygonItem):
            if scope == "Global":
                x = poly.x()
                y = poly.y()
            poly = poly.polygon()

        for i in range(poly.size()):
            innerList.append(QPointF(poly.at(i).x() + x, poly.at(i).y() + y))
        return innerList

    def enablePolygonSelect(self, enabled=True):
        # Cambia la etiqueta del poligono para que pueda ser seleccionado o no
        for poly in self.polyList:
            if isinstance(poly, QGraphicsPolygonItem):
                if enabled:
                    poly.setFlag(
                        QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
                else:
                    poly.setFlag(
                        QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, enabled)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_F5:
            self.mode = "Arrow"
            self.enablePolygonSelect()

        elif e.key() == Qt.Key_F6:
            self.mode = "Draw poly"
            self.enablePolygonSelect(False)
        elif e.key() == Qt.Key_F7:
            self.mode = "Draw rect"
            self.enablePolygonSelect(False)

        if e.key() == Qt.Key_F1:
            self.holeMode = True
        elif e.key() == Qt.Key_F2:
            self.holeMode = False
        if e.key() == Qt.Key_F10:
            self.showMesh()
        print(self.mode)
        print(self.holeMode)

    def polygonContains(self, polyOuter, polyInner):
        # Revisa si un poligono interno esta totalmente contenido por un poligono exterior
        # resgresa una lista de boorleanos con los valores de todos los puntos en el triangulo interior que contiene
        # True si esta contenido False si no
        # los valores de los bordes no son contados como contenidos
        
        innerList = self.polyToList(polyInner, "Global")
        containList = []

        #Hace loop a todos los puntos en el poligono interior para ver si estan contenidos por el poligono exterior
        for point in innerList:
            # Los puntos estan definidos con coordenadas locales, los movemos para que ambos tengan las 
            # coordenadas locales del poligono exterior
            pX = point.x() - polyOuter.x()
            pY = point.y() - polyOuter.y()
            point.setX(pX)
            point.setY(pY)

            # Revisar si el poligono exterior contiene ninguno, alguno o todos los puntos
            if polyOuter.contains(point):
                trueContain = []
                
                # Revisar un area cuadrada alrededor del punto para ver si todo el cuadrado esta contenido, 
                # si no esta en un borde y no debe ser incluido
                for i, j in itertools.product(range(-1, 2), range(-1, 2)):
                    point.setX(pX + i)
                    point.setY(pY + j)
                    if polyOuter.contains(point):
                        trueContain.append(True)
                    else:
                        trueContain.append(False)

                # Lo agrega al containList si toda el area cuadrada esta dentro del poligono exterior
                if all(trueContain):
                    containList.append(True)
                else:
                    containList.append(False)
            else:
                containList.append(False)
        return containList

    def polygonContainsHoles(self, outerPoly):
        # Revisa si el poligono contiene un objeto de tipo hoyo, regresa una lista de los objetos tipo agujeros que estan contenidos
        containList = []
        for holePolygon in self.holeList:
            if all(self.polygonContains(outerPoly, holePolygon)):
                containList.append(holePolygon)
        return containList

    def polygonContainsOtherPolygon(self, outerPoly):
        # Revisa si el poligono contiene totalmente cualquier otro poligono, regresa una lista de los objetos de tipo poligono que 
        #estan contenidos
        containList = []
        for innerPoly in self.polyList:
            if outerPoly == innerPoly:
                pass
            elif all(self.polygonContains(outerPoly, innerPoly)):
                containList.append(innerPoly)
        return containList

    def polygonOverlapsOtherPolygon(self, outerPoly):
        # Revisa si un poligono esta transpuest con algun otro poligono en la escena
        containList = []
        for innerPoly in self.polyList:
            if outerPoly == innerPoly:
                pass
            elif all(self.polygonContains(outerPoly, innerPoly)):
                pass
            elif any(self.polygonContains(outerPoly, innerPoly)):
                containList.append(innerPoly)
        return containList
    
    def buildGmsh(self):
        g = cfg.Geometry()
        pointIndex = 0
        lineIndex = 0
        addedPoints = []
        addedLines = []
        pointmarkerList = []
        edgeMarkerList = []
        surfaceIndex = 0
        ignoreWarning = False

        # Loop first one time to sort the list in order of polygons containing each other to ensure that polygons which
        # contain other polygons are added first
        for poly in self.polyList:
            if self.polygonContainsOtherPolygon(poly):
                pass
            else:
                self.polyList.append(self.polyList.pop(self.polyList.index(poly)))

        # Loop through all polygons again to add them to the gmsh object
        for poly in self.polyList:
            if poly in self.holeList:
                continue

            # Check for polygons overlapping eachother and warn user if any
            if self.polygonOverlapsOtherPolygon(poly) and not ignoreWarning:
                if self.overlapWarning is not None:
                    userChoice = self.overlapWarning()
                    if userChoice == "Cancel":
                        return None
                    elif userChoice == "Ignore":
                        ignoreWarning = True

            # Check if polygon intersects itself and warn user if true
            lines = []
            for item in poly.childItems():
                if isinstance(item, QGraphicsLineItem):
                    lines.append(item)

            for a, b in itertools.combinations(lines, 2):
                if a.collidesWithItem(b):
                    if a.line().p1() == b.line().p1() or a.line().p1() == b.line().p2():
                        pass
                    elif a.line().p2() == b.line().p1() or a.line().p2() == b.line().p2():
                        pass
                    else:
                        self.intersectionError()
                        return None

            surfaceTot = []
            pointIndex, lineIndex, addedPoints, addedLines, surface = self.addPolyGmsh(poly, g, pointIndex,
                                                                                                   pointmarkerList,
                                                                                                   lineIndex,
                                                                                                   addedPoints,
                                                                                                   addedLines,
                                                                                                   edgeMarkerList)
            surfaceTot.append(surface)
            surfaceHoles = []

            # Check if there are any holes inside the polygon
            for hole in self.polygonContainsHoles(poly):
                pointIndex, lineIndex, addedPoints, addedLines, surfaceHole = self.addPolyGmsh(hole, g,
                                                                                                            pointIndex,
                                                                                                            pointmarkerList,
                                                                                                            lineIndex,
                                                                                                            addedPoints,
                                                                                                            addedLines,
                                                                                                            edgeMarkerList)

            for innerPoly in self.polygonContainsOtherPolygon(poly):
                pointIndex, lineIndex, addedPoints, addedLines, surfaceInner = self.addPolyGmsh(innerPoly,
                                                                                                             g,
                                                                                                             pointIndex,
                                                                                                             pointmarkerList,
                                                                                                             lineIndex,
                                                                                                             addedPoints,
                                                                                                             addedLines,
                                                                                                             edgeMarkerList)
                surfaceHoles.append(surfaceInner)
                surfaceTot.append(surfaceInner)
            # Create a surface from the added lines, give the surface a number index
            g.surface(surface, holes=surfaceHoles, marker=surfaceIndex)
            surfaceIndex += 1
        self.g = g
        return g

    def addPolyGmsh(self, poly, g, pointIndex, pointmarkerList, lineIndex, addedPoints, addedLines,
                            edgeMarkerList):
        first = True
        firstIndex = pointIndex
        prevIndex = pointIndex
        polyList = self.polyToListWithOverlap(poly)
        surface = []

        for point in polyList:  # loop over all points in the polygon
            pointmarker = None

            if [point.x(), -point.y()] in addedPoints:  # if the point already exists don't add again
                if first:  # If it is the first point of the poly set existing point as firstIndex
                    first = False
                    currentindex = addedPoints.index([point.x(), -point.y()])
                    firstIndex = currentindex
                elif prevIndex == addedPoints.index([point.x(), -point.y()]):
                    # To avoid occurrence of adding zero length line from point to self
                    pass
                else:

                    currentindex = addedPoints.index([point.x(), -point.y()])
                    # Check if the line from previous point already exists, in that case don't att a new one
                    if [prevIndex, currentindex] in addedLines:
                        surface.append( addedLines.index([prevIndex, currentindex]))

                    elif [currentindex, prevIndex] in addedLines:
                        surface.append( addedLines.index([currentindex, prevIndex]))

                    else:  # else add a line from the previous point to the current pre-existing one
                        # If the coordinates is in the edgeMarkerList also add the marker for that edge

                        if [addedPoints[prevIndex], addedPoints[currentindex]] in edgeMarkerList:
                            i = edgeMarkerList.index([addedPoints[prevIndex], addedPoints[currentindex]])
                            lineMarker = self.lineMarkerList[i].marker
                            g.addSpline([prevIndex, currentindex], marker=lineMarker)

                        elif [addedPoints[currentindex], addedPoints[prevIndex]] in edgeMarkerList:
                            i = edgeMarkerList.index([addedPoints[currentindex], addedPoints[prevIndex]])
                            lineMarker = self.lineMarkerList[i].marker
                            g.addSpline([prevIndex, currentindex], marker=lineMarker)

                        else:
                            g.addSpline([prevIndex, currentindex])

                        surface.append(lineIndex)
                        lineIndex += 1
                        addedLines.append([prevIndex, currentindex])
            else:
                # Else add a new point, if the point has a marker also add the marker
                if pointmarker:
                    g.addPoint([point.x(), -point.y()], pointIndex, marker=pointmarker)
                else:
                    g.addPoint([point.x(), -point.y()],
                               pointIndex)  # Negative y since the Graphicsscene has inverted y-axis
                currentindex = pointIndex
                pointIndex += 1
                addedPoints.append([point.x(), -point.y()])

                if first:
                    # If it is the first added point do nothing as there is no other point to connect a line to
                    first = False
                else:
                    # Else add a new line between the previous point and the current, if those coordinates
                    # correspond with a marker also add the marker to the line
                    if [addedPoints[prevIndex], addedPoints[currentindex]] in edgeMarkerList:
                        i = edgeMarkerList.index([addedPoints[prevIndex], addedPoints[currentindex]])
                        lineMarker = self.lineMarkerList[i].marker
                        g.addSpline([prevIndex, currentindex], marker=lineMarker)

                    elif [addedPoints[currentindex], addedPoints[prevIndex]] in edgeMarkerList:
                        i = edgeMarkerList.index([addedPoints[currentindex], addedPoints[prevIndex]])
                        lineMarker = self.lineMarkerList[i].marker
                        g.addSpline([prevIndex, currentindex], marker=lineMarker)

                    else:
                        g.addSpline([prevIndex, currentindex])

                    surface.append(lineIndex)
                    lineIndex += 1
                    addedLines.append([prevIndex, currentindex])

            prevIndex = currentindex

        # Finally do the procedure again but add the line from the last index to the first index to close the
        # surface, also here add a line marker if there is one
        if [currentindex, firstIndex] in addedLines:
            surface.append(addedLines.index([currentindex, firstIndex]))

        elif [firstIndex, currentindex] in addedLines:
            surface.append(addedLines.index([firstIndex, currentindex]))

        else:
            if [addedPoints[firstIndex], addedPoints[currentindex]] in edgeMarkerList:
                i = edgeMarkerList.index([addedPoints[firstIndex], addedPoints[currentindex]])
                lineMarker = self.lineMarkerList[i].marker
                g.addSpline([currentindex, firstIndex], marker=lineMarker)

            elif [addedPoints[currentindex], addedPoints[firstIndex]] in edgeMarkerList:
                i = edgeMarkerList.index([addedPoints[currentindex], addedPoints[firstIndex]])
                lineMarker = self.lineMarkerList[i].marker
                g.addSpline([currentindex, firstIndex], marker=lineMarker)

            else:
                g.addSpline([currentindex, firstIndex])

            surface.append(lineIndex)
            lineIndex += 1
            addedLines.append([currentindex, firstIndex])
        return pointIndex, lineIndex, addedPoints, addedLines, surface

    def polyToListWithOverlap(self, polygon):
        """
            Creates a polygon list but includes checking of overlapping points on edges, in case of overlap adds a extra
            point in the list where the overlap occurs.
        """
        added = 0
        polygonitem = polygon.polygon()
        polygonitem.translate(polygon.x(), polygon.y())

        # Comparator to determine which x value of two points is the highest
        def compareX(item1, item2):
            if item1.x() < item2.x():
                return -1
            elif item1.x() > item2.x():
                return 1
            else:
                return 0

        # Comparator to determine which y value of two points is the highest
        def compareY(item1, item2):
            if item1.y() < item2.y():
                return -1
            elif item1.y() > item2.y():
                return 1
            else:
                return 0

        # Create two lists, one sorted by ascending x-values, one by ascending y-values
        xList = sorted(self.potentialEdgeSplitters, key=cmp_to_key(compareX))
        yList = sorted(self.potentialEdgeSplitters, key=cmp_to_key(compareY))

        # Loop over all children to the polygon
        for item in polygon.childItems():
            # Look only at edges (overlapping of points is handled elsewhere)
            if isinstance(item, PyQt5.QtWidgets.QGraphicsLineItem):
                edge = item

                p1 = edge.line().p1()
                p2 = edge.line().p2()
                addedThis = 0

                # Choose the direction with the largest disparity (to avoid scenario of straight lines)
                # then use the sorted list for that direction
                if abs(p1.x() - p2.x()) > abs(p1.y() - p2.y()):
                    mode = "X"
                    circList = xList
                else:
                    mode = "Y"
                    circList = yList

                for circ in circList:
                    poly = circ.parentItem()
                    p = circ.scenePos()

                    # tempP needed since edge.contains does not account for the edge being moved in the canvas
                    tempP = circ.scenePos()
                    tempP.setX(tempP.x() - edge.scenePos().x())
                    tempP.setY(tempP.y() - edge.scenePos().y())

                    # Find the edges to split which contain tempP, if the edge contains decide the orientation (in x-
                    # or y-direction decided earlier) of p1 and p2, based on this insert the new point in the polygon
                    # in the correct position
                    if edge.contains(tempP):
                        if edge in poly.childItems():
                            pass  # Ignore if the edge is in the same polygon as the point
                        else:
                            if tempP == p1 or tempP == p2:
                                pass  # Don't compare if it contains an edge point, instead handled later by the overlapping points
                            elif mode == "Y":
                                if p1.y() < p2.y():  # Left to right
                                    index = abs(edge.localIndex)
                                    polygonitem.insert(index + added, p)
                                    added += 1
                                elif p1.y() > p2.y():  # Right to left
                                    index = abs(edge.localIndex)
                                    polygonitem.insert(index + added - addedThis, p)
                                    addedThis += 1
                                    added += 1
                            else:
                                if p1.x() < p2.x():  # Left to right
                                    index = abs(edge.localIndex)
                                    polygonitem.insert(index + added, p)
                                    added += 1
                                elif p1.x() > p2.x():  # Right to left
                                    index = abs(edge.localIndex)
                                    polygonitem.insert(index + added - addedThis, p)
                                    addedThis += 1
                                    added += 1

        return self.polyToList(polygonitem, "Global")

    def showMesh(self):
        """Update the CALFEM vis figure with the CALFEM mesh description of the currently drawn geometry"""
        g = self.buildGmsh()
        if g:
            mesh = cfm.GmshMesh(g)
            mesh.elType = self.elType

            mesh.dofs_per_node = self.dofsPerNode
            mesh.el_size_factor = self.elSizeFactor
            self.mesh = mesh

            coords, edof, dofs, bdofs, elementmarkers = mesh.create()
            cfv.clf()

            cfv.draw_mesh(
                coords = coords,
                edof = edof,
                dofs_per_node = mesh.dofs_per_node,
                el_type = mesh.elType,
                filled = True
            )
            if self.figureCanvas is not None:
                if self.mplLayout.count() == 0:
                    sizeFactorInput = QLineEdit(str(self.elSizeFactor))
                    sizeFactorInput.setStyleSheet("background-color: white;")
                    self.mplLayout.addWidget(self.figureCanvas)
                    self.mplLayout.addWidget(sizeFactorInput)
                    updateButton = (QPushButton("Update"))
                    updateButton.setStyleSheet("border: 3px solid rgb(0,0,128);")
                    def update():
                        self.elSizeFactor = float(sizeFactorInput.text())
                        self.showMesh()
                        slider.setValue(float(sizeFactorInput.text()))
                    updateButton.clicked.connect(update)
                    self.mplLayout.addWidget(updateButton)
                    slider = QSlider(Qt.Horizontal)
                    slider.setFocusPolicy(Qt.StrongFocus)
                    slider.setTickPosition(QSlider.TicksBothSides)
                    slider.setTickInterval(10)
                    slider.setSingleStep(1)
                    slider.setValue(self.elSizeFactor)
                    slider.setMinimum(1)
                    slider.setMaximum(100)
                    def changeValue(value):
                        self.elSizeFactor = str(value)
                        sizeFactorInput.setText(str(value))
                    slider.valueChanged[int].connect(changeValue)
                    self.mplLayout.addWidget(slider)
                self.figureCanvas.draw()
            else:
                cfv.show_and_wait()
            return None
        else:
            return "Canceled"

class MainView(QGraphicsView):
    def __init__(self, win):
        super(MainView, self).__init__()

        # Crear escena para los items dentro del View
        self.scene = QGraphicsScene(win)
        self.setScene(self.scene)

        # Matplotlib widget
        self.mplWidget = QWidget(self)
        self.mplWidget.setGeometry(0,0,300,300)
        self.mplLayout = QVBoxLayout(self.mplWidget)
        self.mplWidget.setLayout(self.mplLayout)
        self.mplWidget.setStyleSheet("background-color: grey;")

        # Agregar el componente Canvas a la escena
        self.canvas = Canvas(self)
        self.scene.addWidget(self.canvas)

        self.widget = QWidget(self)
        self.widget.setGeometry(10,310,150, 100)


        #Aqui agregan los labels 
        # Layout Label Widget Container
        self.layoutWid = QGridLayout(self.widget)
        self.widget.setLayout(self.layoutWid)
        
        self.widget.setStyleSheet("background-color: yellow;")

    def mouseDoubleClickEvent(self, event):
        self.canvas.mouseDoubleClickEvent(event, self.layoutWid, self.widget)

class Window(QMainWindow):
    # * Main Application Window
    def __init__(self, screenSize=None):
        super(QMainWindow, self).__init__()
        self.setWindowTitle("Pyside2 QGraphic View - Draw Test")
        self.resize(800,600)

        self.view = MainView(self)
        # Add central widget
        self.setCentralWidget(self.view)

        # Centrar en pantalla
        if screenSize is not None:
            center = (screenSize.width()/2, screenSize.height()/2)
            self.setGeometry(int(center[0]), int(center[1]), 1100, 800)
        else:
            self.setGeometry(0, 0, 1100, 800)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    screen = app.primaryScreen()

    # Crear ventana
    window = Window(screen.size())
    # Mostrar ventana
    window.show()

    sys.exit(app.exec_())