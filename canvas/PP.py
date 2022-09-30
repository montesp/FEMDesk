from cmath import log
from ctypes import sizeof
import itertools
from functools import cmp_to_key
import math
from operator import length_hint

import sys
import PyQt5
import numpy as np
from PyQt5.QtCore import QEvent, QPointF, QLineF, QRectF, QRegExp, Qt, QRect
from PyQt5.QtGui import QPen, QColor, QBrush, QPolygonF, QFont, QRegExpValidator
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QFileDialog, QGraphicsScene, \
    QGraphicsItem, QGraphicsPolygonItem, QToolButton, QLabel, \
    QGraphicsEllipseItem, QLineEdit, QFormLayout, QGraphicsLineItem, QGraphicsTextItem, QGridLayout, QPushButton, QGraphicsItem, QGraphicsView, \
    QVBoxLayout, QMessageBox, QSlider

import random

import matplotlib as mpl
mpl.use('Qt5Agg')

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

import canvas.geometry as cfg
import canvas.mesh as cfm
import canvas.vis_mpl as cfv

setattr(cfg.Geometry, "marker_dict", None)
setattr(QGraphicsEllipseItem, "marker", None)
setattr(QGraphicsEllipseItem, "localIndex", None)
setattr(QGraphicsLineItem, "localIndex", None)

class Canvas(QWidget):
    def __init__(self, parentView:QGraphicsView):
        super(Canvas, self).__init__()
        self.parentView = parentView

        # Referencia a la escena de dibujo. Permite acceder a las funciones de dibujo
        self.scene = self.parentView.scene()
        self.mplWidget = self.scene.mplWidget

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


        self.grid_on = True
        self.grid_built = False
        self.grid = []
        self.grid_snap = False
        self.grid_snap_last_x = 0
        self.grid_snap_last_y = 0
        self.grid_spacing = 20
        self.grid_max_scale = 10
        self.grid_min_scale = 0.2
        self.create_grid()

        # Modo de operación dentro del programa
        # :Modos disponibles:
        #-> Arrow, Draw Poly, Draw Rect
        self.mode = "Arrow"

        # Permitir el seguimiento del puntero dentro del canvas
        #self.setMouseTracking(True)


        self.fig = cfv.figure()
        self.figureCanvas = cfv.figure_widget(self.fig)

        # Matplotlib widget
        self.mplWidget = self.scene.mplWidget
        self.mplLayout = QVBoxLayout(self.mplWidget)
        self.mplWidget.setLayout(self.mplLayout)
        self.mplWidget.setStyleSheet("background-color: grey;")

        self.nodeSplitter = self.scene.addEllipse(-3, -3, 6, 6)
        self.nodeSplitter.setVisible(False)
        self.splitEdge = None

        self.splice=False
        self.polySplice=None
        self.polySplice2=None

        self.polyG=None
        self.polyN=None

        self.marker_dict = {}
        self.reversed_marker_dict = {}
        self.line_marker_index = 1

        self.point_marker_list = []
        self.line_marker_list = []

        self.marker_removal_warning = None

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

    def overlapWarningHolePoly(self): 
        msg = QMessageBox()
        msg.setWindowTitle("Error")
        msg.setText("Hay agujeros encimados con poligonos")
        msg.setIcon(QMessageBox.Critical)
        msg.setStandardButtons(QMessageBox.Cancel)

        msg.exec_()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_F5:
            self.merge()
        # if e.key() == Qt.Key_F6:
        #     self.mode = "Splice poly right"
        # if e.key() == Qt.Key_F7:
        #     self.mode = "Splice poly left"
        # if e.key() == Qt.Key_F8:
        #     self.mode = "Splice poly up"
        # if e.key() == Qt.Key_F9:
        #     self.mode = "Splice poly down"
        if e.key() == Qt.Key_F2:
            self.mode = "Match points"
        if e.key() == Qt.Key_F3:
            self.mode = "Union 3"
        if e.key() == Qt.Key_F4:
            self.mode = "Union"
        if e.key() == Qt.Key_F1:
            data = self.getAll()
            for val in data:
                print(val)
        if e.key() == Qt.Key_F6:
            self.getEdges()               
        print(self.mode)

    def getAll(self):
        polyEdges = []
        edges = []
        for edge in self.edgeList:
            edges.append(edge.line())
        for edge in edges:
            polyEdges.append([edge.x1(), edge.y1(),edge.x2(), edge.y2()])

        polys = []
        i = 0
        holeMode = []
        pp = []
        dom = []
        for poly in self.polyList:
            polys.append(poly.polygon())
            if poly in self.holeList:
                holeMode.append([2])
            else:
                holeMode.append([1])
        for poly in polys:
            i+=1
            polyPoints = []
            for point in poly:
                polyPoints.append([point.x(),point.y()])
            dom.append([i])
            pp.append(polyPoints)
            
        print(polyEdges)
        data = zip(pp, dom, holeMode)
                        
        return data

    def getEdges(self):
        allEdges = []
        for edge in self.edgeList:
            allEdges.append(edge)

        polyEdges = []
        edges = []
        for edge in self.edgeList:
            edges.append(edge.line())
        for edge in edges:
            polyEdges.append([edge.x1(), edge.y1(),edge.x2(), edge.y2()])

        temp = []
        for x in polyEdges:
            if x not in temp:
                temp.append(x)
        polyEdges = temp

        print(polyEdges)

        return allEdges

    def merge(self):
        #Si estamos en modo Draw Poly eliminamos el poligono de dibujo
        if self.mode == "Draw Poly":
            self.removeDrawingPoly()

        #Si estamos en modo Draw Rect eliminamos el rectangulo de dibujo
        elif self.mode == "Draw Rect":
            self.removeDrawingRect()

        # Recorre todos los poligonos y los compara entre si, si dos poligonos son mergeados se remueven de la lista
        for poly_outer in self.polyList:
            for poly_inner in self.polyList:
                if poly_outer == poly_inner:
                    continue  # Ignora la comparación consigo mismo

                contain_list = self.polygonContains(poly_outer, poly_inner)
                
                if all(contain_list):
                    # Si todos los puntos estan dentro del poligono exterior no hacer merge (quitaria el poligono interno)
                    pass
                elif any(contain_list):
                    # Si algunos de los puntos (no todos) de un poligono estan dentro del poligono exterior los dos poligonos son mergeados

                    # Si el agujero interno es un agujero y el externo no es un agujero eliminamos el interno
                    # ya que esta por fuera del poligono externo
                    if poly_inner in self.holeList and poly_outer not in self.holeList:
                        self.overlapWarningHolePoly()
                        self.deletePolygon(poly_inner)
                        
                    # Si el agujero interno es un agujero y el externo no es un agujero eliminamos el interno
                    # ya que esta por fuera del poligono externo
                    elif poly_inner not in self.holeList and poly_outer in self.holeList:
                        self.overlapWarningHolePoly()
                        self.deletePolygon(poly_outer)

                    #Si ambos poligonos son agujeros
                    elif poly_inner in self.holeList and poly_outer in self.holeList:
                        # Mueve los objetos QPolygonF a las coordenadas globales y unirlas (mergear)
                        p1 = poly_outer.polygon().translated(poly_outer.x(), poly_outer.y())
                        p2 = poly_inner.polygon().translated(poly_inner.x(), poly_inner.y())
                        uni = p1.united(p2)

                        # Unite agrega el punto inicial de nuevo como punto final, removemos este punto duplicado
                        uni = self.polyToList(uni, "Global")
                        uni = uni[:-1]

                        # Agregamos el nuevo poligono mergeado como agujero, removemos los dos anteriores de la vista y de las listas
                        self.addPoly(QPolygonF(uni),True)
                        self.deletePolygon(poly_inner, True)
                        self.deletePolygon(poly_outer, True)

                    #Si ambos poligonos son solidos
                    elif poly_inner in self.polyList and poly_outer in self.polyList:
                        # Mueve los objetos QPolygonF a las coordenadas globales y unirlas (mergear)
                        p1 = poly_outer.polygon().translated(poly_outer.x(), poly_outer.y())
                        p2 = poly_inner.polygon().translated(poly_inner.x(), poly_inner.y())
                        uni = p1.united(p2)

                        # Unite agrega el punto inicial de nuevo como punto final, removemos este punto duplicado
                        uni = self.polyToList(uni, "Global")
                        uni = uni[:-1]

                        # Agregamos el nuevo poligono mergeado como solido, removemos los dos anteriores de la vista y de las listas
                        self.addPoly(QPolygonF(uni),False)
                        self.deletePolygon(poly_inner, True)
                        self.deletePolygon(poly_outer, True)

    def deletePolygon(self, poly: QGraphicsPolygonItem, delete_from_coord_list=False):
        """Metodo para remover poligonos existentes de la escena y si se necesita 
        se borran los puntos correspondientes de la lista de coordenadas"""
        print(self.polyList)

        if poly in self.holeList:
            self.holeList.remove(poly)

            self.polyList.remove(poly)

            for item in poly.childItems():
                if isinstance(item, PyQt5.QtWidgets.QGraphicsLineItem):
                    self.edgeList.remove(item)

            if delete_from_coord_list:
                for point in self.polyToList(poly, "Global"):
                    self.pointCoordList = np.delete(self.pointCoordList, np.where(
                        np.all(self.pointCoordList == [[point.x(), point.y()]], axis=1))[0][0], axis=0)
        else:
            self.polyList.remove(poly)

            for item in poly.childItems():
                if isinstance(item, PyQt5.QtWidgets.QGraphicsLineItem):
                    self.edgeList.remove(item)

            if delete_from_coord_list:
                for point in self.polyToList(poly, "Global"):
                    self.pointCoordList = np.delete(self.pointCoordList, np.where(
                        np.all(self.pointCoordList == [[point.x(), point.y()]], axis=1))[0][0], axis=0)

        poly.hide()

    def mouseMoveEvent(self, event):
        # Conseguimos las coordenadas X y Y del mouse cada vez que se mueve
        x = event.pos().x()
        y = event.pos().y()

        #Redondeamos las variables que guardan las coordenadas para que se unan al grid
        x = round(x / self.grid_spacing) * self.grid_spacing
        y = round(y / self.grid_spacing) * self.grid_spacing

        # if self.mode == "Splice poly right" or self.mode == "Splice poly left" or self.mode == "Splice poly up" or self.mode == "Splice poly down":
        #     # Esto muestra la linea desde el punto anterior a la posicion del mouse
        #     if self.newPoly:
        #         x_closest = None
        #         y_closest = None
        #         edge_closest = None

        #         # Check a area around the mouse point to search for any edges to snap to
        #         edge_point_list = []
        #         # Check a square area with width 10 if there is any edge that contains the point, store all edges
        #         # that contains a point
        #         # Most inefficient part of the code, noticeable lag when creating many edges in the canvas
        #         for i, j in itertools.product(range(-10, 10), range(-10, 10)):
        #             for edge in self.edgeList:
        #                 p = QPointF(0, 0)
        #                 p.setX(x + i - edge.scenePos().x())
        #                 p.setY(y + j - edge.scenePos().y())
        #                 if [x + i - edge.scenePos().x(), y + j - edge.scenePos().y()] in self.pointCoordList.tolist():
        #                     pass
        #                 elif edge.contains(p):
        #                     edge_point_list.append([x + i, y + j, edge])

        #         smallest = np.inf
        #         edge_point_list = np.array(edge_point_list)
        #         # Loop through all potential points, if they exist, and choose the one closest to the mouse pointer
        #         # as the point to snap to
        #         for row in edge_point_list:
        #             coords = np.array([row[0], row[1]])
        #             dist = np.linalg.norm(coords - np.array([event.pos().x(), event.pos().y()]))
        #             if dist < smallest:
        #                 smallest = dist
        #                 x_closest = coords[0]
        #                 y_closest = coords[1]
        #                 edge_closest = row[2]

        #         # If there is a edge close to the pointer place the pointer there else hide it
        #         # Both cases required to handle moving along the axes

        #         # If there is a edge close to the pointer place the pointer there else hide it
        #         # Both cases required to handle moving along the axes
        #         if x_closest:
        #             self.nodeSplitter.setPos(x_closest, y_closest)
        #             self.nodeSplitter.setVisible(True)
        #             self.splitEdge = edge_closest
        #         elif y_closest:
        #             self.nodeSplitter.setPos(x_closest, y_closest)
        #             self.nodeSplitter.setVisible(True)
        #             self.splitEdge = edge_closest
        #         else:
        #             self.nodeSplitter.setVisible(False)
        #             self.splitEdge = None
        #     else:
        #         # Si ya existe un punto hay dos casos:

        #         x_closest = None
        #         y_closest = None
        #         edge_closest = None

        #         # Check a area around the mouse point to search for any edges to snap to
        #         edge_point_list = []
        #         # Check a square area with width 10 if there is any edge that contains the point, store all edges
        #         # that contains a point
        #         # Most inefficient part of the code, noticeable lag when creating many edges in the canvas
        #         for i, j in itertools.product(range(-10, 10), range(-10, 10)):
        #             for edge in self.edgeList:
        #                 p = QPointF(0, 0)
        #                 p.setX(x + i - edge.scenePos().x())
        #                 p.setY(y + j - edge.scenePos().y())
        #                 if [x + i - edge.scenePos().x(), y + j - edge.scenePos().y()] in self.pointCoordList.tolist():
        #                     pass
        #                 elif edge.contains(p):
        #                     edge_point_list.append([x + i, y + j, edge])

        #         smallest = np.inf
        #         edge_point_list = np.array(edge_point_list)
        #         # Loop through all potential points, if they exist, and choose the one closest to the mouse pointer
        #         # as the point to snap to
        #         for row in edge_point_list:
        #             coords = np.array([row[0], row[1]])
        #             dist = np.linalg.norm(coords - np.array([event.pos().x(), event.pos().y()]))
        #             if dist < smallest:
        #                 smallest = dist
        #                 x_closest = coords[0]
        #                 y_closest = coords[1]
        #                 edge_closest = row[2]

        #         # If there is a edge close to the pointer place the pointer there else hide it
        #         # Both cases required to handle moving along the axes
        #         if x_closest:
        #             self.nodeSplitter.setPos(x_closest, y_closest)
        #             self.nodeSplitter.setVisible(True)
        #             self.splitEdge = edge_closest
        #             if self.connectingLine:
        #                 self.connectingLine.setLine(QLineF(self.prevPoint, QPointF(x_closest, y_closest)))
        #                 # Caso 1: si ya existe una linea, actualiza las coordenadas finales con la posicion del mouse
        #             else:
        #                 self.connectingLine = self.scene.addLine(QLineF(self.prevPoint, QPointF(x_closest, y_closest)))
        #                 # caso 2: si no hay una linea creada, crea una con el punto inicial en 
        #                 # slas coordenadas del punto anterior y la coordenada final 
        #                 # en la posicion del mouse.
        #         elif y_closest:
        #             self.nodeSplitter.setPos(x_closest, y_closest)
        #             self.nodeSplitter.setVisible(True)
        #             self.splitEdge = edge_closest
        #             if self.connectingLine:
        #                 self.connectingLine.setLine(QLineF(self.prevPoint, QPointF(x_closest, y_closest)))
        #                 # Caso 1: si ya existe una linea, actualiza las coordenadas finales con la posicion del mouse
        #             else:
        #                 self.connectingLine = self.scene.addLine(QLineF(self.prevPoint, QPointF(x_closest, y_closest)))
        #                 # caso 2: si no hay una linea creada, crea una con el punto inicial en 
        #                 # slas coordenadas del punto anterior y la coordenada final 
        #                 # en la posicion del mouse.
        #         else:
        #             self.nodeSplitter.setVisible(False)
        #             self.splitEdge = None
        #             if self.connectingLine:
        #                 self.connectingLine.setLine(QLineF(self.prevPoint, QPointF(x, y)))
        #                 # Caso 1: si ya existe una linea, actualiza las coordenadas finales con la posicion del mouse
        #             else:
        #                 self.connectingLine = self.scene.addLine(QLineF(self.prevPoint, QPointF(x, y)))
        #                 # caso 2: si no hay una linea creada, crea una con el punto inicial en 
        #                 # slas coordenadas del punto anterior y la coordenada final 
        #                 # en la posicion del mouse.

        if self.mode == "Match points":
            #Revisa si es un poligono nuevo
            if self.newPoly:
                #Creamos tres variables de seguimiento
                x_closest = None
                y_closest = None
                edge_closest = None

                #Revisamos un area alrededor del mouse para revisar si hay alguna linea a la que juntarse
                edge_point_list = []
                # Check a square area with width 10 if there is any edge that contains the point, store all edges
                # that contains a point
                #Revisar un area cuadrada de 10 por lado, si hay alguna linea que contenga el punto, guardar todas las linas que contienen un punto 
                for i, j in itertools.product(range(-10, 10), range(-10, 10)):
                    for edge in self.edgeList:
                        p = QPointF(0, 0)
                        p.setX(x + i - edge.scenePos().x())
                        p.setY(y + j - edge.scenePos().y())
                        if [x + i - edge.scenePos().x(), y + j - edge.scenePos().y()] in self.pointCoordList.tolist():
                            pass
                        elif edge.contains(p):
                            edge_point_list.append([x + i, y + j, edge])

                smallest = np.inf
                edge_point_list = np.array(edge_point_list)
                #Hacer loop a todos los puntos potenciales, si existen, y se selecciona el mas cercano al mouse como punto para hacer snap
                for row in edge_point_list:
                    coords = np.array([row[0], row[1]])
                    dist = np.linalg.norm(coords - np.array([event.pos().x(), event.pos().y()]))
                    if dist < smallest:
                        smallest = dist
                        x_closest = coords[0]
                        y_closest = coords[1]
                        edge_closest = row[2]

                #Si hay una linea cerca al pointer poner el pointer en la linea, si no esconderlo
                if x_closest:
                    #Ponemos las coordenadas al pointer y lo volvemos visible
                    self.nodeSplitter.setPos(x_closest, y_closest)
                    self.nodeSplitter.setVisible(True)
                    #Guardamos la linea donde esta el pointer
                    self.splitEdge = edge_closest
                elif y_closest:
                    #Ponemos las coordenadas al pointer y lo volvemos visible
                    self.nodeSplitter.setPos(x_closest, y_closest)
                    self.nodeSplitter.setVisible(True)
                    #Guardamos la linea donde esta el pointer
                    self.splitEdge = edge_closest
                #Si no hay una linea cercana
                else:
                    #Volvemos invisible al pointer
                    self.nodeSplitter.setVisible(False)
                    #Borramos la variable de la linea
                    self.splitEdge = None
            else:
                # Si ya existe un punto hay dos casos:

                #Creamos tres variables de seguimiento
                x_closest = None
                y_closest = None
                edge_closest = None

                #Revisamos un area alrededor del mouse para revisar si hay alguna linea a la que juntarse
                edge_point_list = []
                # Check a square area with width 10 if there is any edge that contains the point, store all edges
                # that contains a point
                #Revisar un area cuadrada de 10 por lado, si hay alguna linea que contenga el punto, guardar todas las linas que contienen un punto 
                for i, j in itertools.product(range(-10, 10), range(-10, 10)):
                    for edge in self.edgeList:
                        p = QPointF(0, 0)
                        p.setX(x + i - edge.scenePos().x())
                        p.setY(y + j - edge.scenePos().y())
                        if [x + i - edge.scenePos().x(), y + j - edge.scenePos().y()] in self.pointCoordList.tolist():
                            pass
                        elif edge.contains(p):
                            edge_point_list.append([x + i, y + j, edge])

                smallest = np.inf
                edge_point_list = np.array(edge_point_list)
                #Hacer loop a todos los puntos potenciales, si existen, y se selecciona el mas cercano al mouse como punto para hacer snap
                for row in edge_point_list:
                    coords = np.array([row[0], row[1]])
                    dist = np.linalg.norm(coords - np.array([event.pos().x(), event.pos().y()]))
                    if dist < smallest:
                        smallest = dist
                        x_closest = coords[0]
                        y_closest = coords[1]
                        edge_closest = row[2]

                #Si hay una linea cerca al pointer poner el pointer en la linea, si no esconderlo                       
                if x_closest:
                    #Ponemos las coordenadas al pointer y lo volvemos visible
                    self.nodeSplitter.setPos(x_closest, y_closest)
                    self.nodeSplitter.setVisible(True)
                    #Guardamos la linea donde esta el pointer
                    self.splitEdge = edge_closest
                    if self.connectingLine:
                        self.connectingLine.setLine(QLineF(self.prevPoint, QPointF(x_closest, y_closest)))
                        # Caso 1: si ya existe una linea, actualiza las coordenadas finales con la posicion del mouse
                    else:
                        self.connectingLine = self.scene.addLine(QLineF(self.prevPoint, QPointF(x_closest, y_closest)))
                        # caso 2: si no hay una linea creada, crea una con el punto inicial en 
                        # slas coordenadas del punto anterior y la coordenada final 
                        # en la posicion del mouse.
                elif y_closest:
                    #Ponemos las coordenadas al pointer y lo volvemos visible
                    self.nodeSplitter.setPos(x_closest, y_closest)
                    self.nodeSplitter.setVisible(True)
                    #Guardamos la linea donde esta el pointer
                    self.splitEdge = edge_closest
                    if self.connectingLine:
                        self.connectingLine.setLine(QLineF(self.prevPoint, QPointF(x_closest, y_closest)))
                        # Caso 1: si ya existe una linea, actualiza las coordenadas finales con la posicion del mouse
                    else:
                        self.connectingLine = self.scene.addLine(QLineF(self.prevPoint, QPointF(x_closest, y_closest)))
                        # caso 2: si no hay una linea creada, crea una con el punto inicial en 
                        # slas coordenadas del punto anterior y la coordenada final 
                        # en la posicion del mouse.
                else:
                    #Volvemos invisible el pointer
                    self.nodeSplitter.setVisible(False)
                    #Vaciamos la variable de seguimiento
                    self.splitEdge = None
                    if self.connectingLine:
                        self.connectingLine.setLine(QLineF(self.prevPoint, QPointF(x, y)))
                        # Caso 1: si ya existe una linea, actualiza las coordenadas finales con la posicion del mouse
                    else:
                        self.connectingLine = self.scene.addLine(QLineF(self.prevPoint, QPointF(x, y)))
                        # caso 2: si no hay una linea creada, crea una con el punto inicial en 
                        # slas coordenadas del punto anterior y la coordenada final 
                        # en la posicion del mouse.                        

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
                    self.connectingLine = self.scene.addLine(QLineF(self.prevPoint, QPointF(x, y)))
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
                    self.connectingRect = self.scene.addRect(QRectF(self.prevPoint, QPointF(x, y)))

    def mousePressEvent(self, e):
        #: Evento de un click del mouse
        x = e.pos().x()
        y = e.pos().y()
        
        
        #Redondeamos las variables que guardan las coordenadas para que se unan al grid
        x = round(x / self.grid_spacing) * self.grid_spacing
        y = round(y / self.grid_spacing) * self.grid_spacing

        if self.mode == "Union":
            #Si damos click izquierdo
            if e.button() == 1:
                #Revisamos si la variable de seguimiento self.polyG no esta vacia y se esta seleccionando algo de la escena    
                if self.polyG != None and self.scene.selectedItems():
                    #Revisamos si lo que se selecciono es un QGraphicsPolygonItem
                    if isinstance(self.scene.selectedItems()[0], PyQt5.QtWidgets.QGraphicsPolygonItem):
                        #Guardamos ese QGraphicsPolygonItem en la variable de seguimiento self.polyN
                        self.polyN = self.scene.selectedItems()[0]
                        #Revisamos si las variables de seguimiento no estan vacias y no son el mismo poligono
                        if self.polyG != None and self.polyN!=None and self.polyG != self.polyN:

                            #Movemos los objetos QPolygonF a las coordenadas globales y los unimos (mergeamos)
                            p1 = self.polyG.polygon().translated(self.polyG.x(), self.polyG.y())
                            p2 = self.polyN.polygon().translated(self.polyN.x(), self.polyN.y())
                            uni = p1.united(p2)

                            #Unite agrega el punto inicial como punto final asi que removemos este punto final
                            uni = self.polyToList(uni, "Global")
                            uni = uni[:-1]

                            #Agregamos el nuevo poligono y removemos los viejor de la vista y las listas
                            self.addPoly(QPolygonF(uni),False)
                            self.deletePolygon(self.polyG, True)
                            self.deletePolygon(self.polyN, True)
                            
                            #Vaciamos las variables de seguimiento
                            self.polyG = None
                            self.polyN = None
                #Si la variable de seguimiento self.polyG esta vacia y se esta seleccionando algo de la escena
                elif self.scene.selectedItems():
                    #Si lo que se selecciona es un QGraphicsPolygonItem
                    if isinstance(self.scene.selectedItems()[0], PyQt5.QtWidgets.QGraphicsPolygonItem):
                        #Guardamos este poligono en la variable de seguimiento self.polyG
                        self.polyG = self.scene.selectedItems()[0]

        if self.mode == "Match points":
            if e.button() == 2:
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
                    self.splice=False
                    self.polySplice=None
                    self.polySplice2=None
                    
            if e.button() == 1:
                if self.splitEdge:
                    self.splice=True
                    edge = self.splitEdge
                    self.polySplice = edge.parentItem()
                    poly = edge.parentItem()
                    line2 = edge.line()
                    self.polyG = poly
                    polyList = self.polyToList(self.polySplice, "Global")

                    if self.newPoly:
                    # Inicializar nuevo poligono como objeto de tipo QPolygonF()
                        self.currentPoly = QPolygonF()

                        point = self.scene.addEllipse(
                            self.nodeSplitter.pos().x() - 3, self.nodeSplitter.pos().y() - 3, 6, 6, self.blackPen, self.greenBrush)

                        # Guardamos coordenadas del punto inicial del nuevo polígono    
                        self.firstPoint = QPointF(self.nodeSplitter.pos().x(), self.nodeSplitter.pos().y())
                        self.prevPoint = QPointF(self.nodeSplitter.pos().x(), self.nodeSplitter.pos().y())

                        # Pasar el punto inicial al poligono a construir
                        self.currentPoly << self.firstPoint
                        self.newPoly = False

                        self.drawingPoints.append(point)
                        self.drawingPointsCoords.append([self.nodeSplitter.pos().x(), self.nodeSplitter.pos().y()])

                        line2.translate(edge.scenePos())  # Move line to global coordinates
                        p1_index = polyList.index(line2.p1())
                        p2_index = polyList.index(line2.p2())

                        # Determine between which point index to insert the new point
                        if abs(p1_index - p2_index) > 1:  # If difference is larger than one means the split occurs between the first and last point
                            if p1_index > p2_index:
                                insert_index = p1_index
                            else:
                                insert_index = p2_index
                        else:
                            if p1_index < p2_index:
                                insert_index = p1_index
                            else:
                                insert_index = p2_index
                        insert_index += 1

                        # Insert a new the new point and create a new poilygon
                        polyList.insert(insert_index, self.nodeSplitter.scenePos())
                        new_poly = QPolygonF()
                        for p in polyList:
                            new_poly << p

                        self.polyN=new_poly

                        self.deletePolygon(self.polyG, True)
                        self.addPoly(self.polyN, holeMode=False)

                    else:
                        point = self.scene.addEllipse(
                            self.nodeSplitter.pos().x() - 3, self.nodeSplitter.pos().y() -3, 6, 6, self.blackPen, self.greenBrush)

                        # Dibujamos linea entre punto actual y el anterior
                        line = self.scene.addLine(
                            QLineF(self.prevPoint, QPointF(self.nodeSplitter.pos().x(), self.nodeSplitter.pos().y())), self.blackPen)

                        # Guardamos coordenada del punto recién dibujado
                        self.prevPoint = QPointF(self.nodeSplitter.pos().x(), self.nodeSplitter.pos().y())

                        # Pasar el punto previo al Poligono a construir
                        self.currentPoly << self.prevPoint

                        self.connectingLineList.append(line)
                        self.drawingPoints.append(point)
                        self.drawingPointsCoords.append([self.nodeSplitter.pos().x(), self.nodeSplitter.pos().y()])

                        line2.translate(edge.scenePos())  # Move line to global coordinates
                        p1_index = polyList.index(line2.p1())
                        p2_index = polyList.index(line2.p2())

                        # Determine between which point index to insert the new point
                        if abs(p1_index - p2_index) > 1:  # If difference is larger than one means the split occurs between the first and last point
                            if p1_index > p2_index:
                                insert_index = p1_index
                            else:
                                insert_index = p2_index
                        else:
                            if p1_index < p2_index:
                                insert_index = p1_index
                            else:
                                insert_index = p2_index
                        insert_index += 1

                        # Insert a new the new point and create a new poilygon
                        polyList.insert(insert_index, self.nodeSplitter.scenePos())
                        new_poly = QPolygonF()
                        for p in polyList:
                            new_poly << p

                        self.polyN=new_poly
                        self.deletePolygon(self.polyG, True)
                        self.addPoly(self.polyN, holeMode=False)

                # Si se está dibujando un nuevo polígono
                elif self.newPoly:
                    # Inicializar nuevo poligono como objeto de tipo QPolygonF()
                    self.currentPoly = QPolygonF()

                    point = self.scene.addEllipse(
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
                    point = self.scene.addEllipse(
                        x - 3, y - 3, 6, 6, self.blackPen, self.greenBrush)

                    # Dibujamos linea entre punto actual y el anterior
                    line = self.scene.addLine(
                        QLineF(self.prevPoint, QPointF(x, y)), self.blackPen)

                    # Guardamos coordenada del punto recién dibujado
                    self.prevPoint = QPointF(x, y)

                    # Pasar el punto previo al Poligono a construir
                    self.currentPoly << self.prevPoint

                    self.connectingLineList.append(line)
                    self.drawingPoints.append(point)
                    self.drawingPointsCoords.append([x, y])

        # if self.mode == "Union rect":
        #     if self.splitEdge:
        #         self.splice=True
        #         edge = self.splitEdge
        #         self.polySplice = edge.parentItem()
        #         poly = edge.parentItem()
        #         self.polyG = poly
        #         polyList = self.polyToList(poly, "Global")
        #         line = edge.line()

        #         if self.newPoly:
        #         # Inicializar nuevo poligono como objeto de tipo QPolygonF()
        #             line.translate(edge.scenePos())  # Move line to global coordinates
        #             p1_index = polyList.index(line.p1())
        #             p2_index = polyList.index(line.p2())
        #             # Determine between which point index to insert the new point
        #             if abs(p1_index - p2_index) > 1:  # If difference is larger than one means the split occurs between the first and last point
        #                 if p1_index > p2_index:
        #                     insert_index = p1_index
        #                 else:
        #                     insert_index = p2_index
        #             else:
        #                 if p1_index < p2_index:
        #                     insert_index = p1_index
        #                 else:
        #                     insert_index = p2_index
        #             insert_index += 1

        #             # Insert a new the new point and create a new poilygon
        #             polyList.insert(insert_index, self.nodeSplitter.scenePos())
        #             new_poly = QPolygonF()
        #             for p in polyList:
        #                 new_poly << p

        #             self.polyN=new_poly

        #             self.currentPoly = QPolygonF()

        #             point = self.scene.addEllipse(
        #                 self.nodeSplitter.pos().x() - 3, self.nodeSplitter.pos().y() - 3, 6, 6, self.blackPen, self.greenBrush)

        #             # Guardamos coordenadas del punto inicial del nuevo polígono    
        #             self.firstPoint = QPointF(self.nodeSplitter.pos().x(), self.nodeSplitter.pos().y())
        #             self.prevPoint = QPointF(self.nodeSplitter.pos().x(), self.nodeSplitter.pos().y())

        #             # Pasar el punto inicial al poligono a construir
        #             self.currentPoly << self.firstPoint
        #             self.newPoly = False

        #             self.drawingPoints.append(point)
        #             self.drawingPointsCoords.append([self.nodeSplitter.pos().x(), self.nodeSplitter.pos().y()])

        #         elif self.prevPoint.x() == x or self.prevPoint.y() == y:
        #             pass

        #         else:
        #             r = self.connectingRect.rect()
        #             x1 = r.x()
        #             x2 = r.x() + r.width()
        #             y1 = r.y()
        #             y2 = r.y() + r.height()
        #             self.drawingRect << QPointF(x1, y1)
        #             self.drawingRect << QPointF(x2, y1)
        #             self.drawingRect << QPointF(x2, y2)
        #             self.drawingRect << QPointF(x1, y2)

        #             self.addPoly(self.drawingRect, holeMode=self.holeMode)
        #             self.deletePolygon(self.polyG, True)
        #             self.addPoly(self.polyN, hole_mode=False)
        #             self.removeDrawingRect()
        #             self.currentPoly = None
        #             self.newPoly = True
        #             self.firstPoint = None
        #             self.prevPoint = None
        #             self.splice=False
        #             self.polyG=None
        #             self.polyN=None
                
        #     # Si se está dibujando un nuevo polígono
        #     elif self.newPoly:
        #         # Guardar coordenada del punto recién dibujado
        #         self.prevPoint = QPointF(x, y)
        #         self.newPoly = False
        #     # Catch para evitar crear un rectángulo donde los puntos estén sobrepuestos
        #     elif self.prevPoint.x() == x or self.prevPoint.y() == y:
        #         pass  

        #     else:
        #         r = self.connectingRect.rect()
        #         x1 = r.x()
        #         x2 = r.x() + r.width()
        #         y1 = r.y()
        #         y2 = r.y() + r.height()
        #         self.drawingRect << QPointF(x1, y1)
        #         self.drawingRect << QPointF(x2, y1)
        #         self.drawingRect << QPointF(x2, y2)
        #         self.drawingRect << QPointF(x1, y2)

        #         self.addPoly(self.drawingRect, holeMode=self.holeMode)
        #         self.deletePolygon(self.polyG, True)
        #         self.addPoly(self.polyN, holeMode=False)
        #         self.removeDrawingRect()

        #         self.currentPoly = None
        #         self.newPoly = True
        #         self.firstPoint = None
        #         self.prevPoint = None
        #         self.splice=False
        #         self.polyG=None
        #         self.polyN=None

                
        # if self.mode == "Splice poly right":
        #     if e.button() == 2:
        #         # Si el polígono a dibujar contiene 2 o menos puntos no se dibujará
        #         if self.newPoly or self.currentPoly.__len__() <= 2:
        #             return
                    
        #         if self.splice:
        #             self.polySplice2 = self.addPoly(self.currentPoly, holeMode=self.holeMode)
        #             p1 = self.polySplice.polygon().translated(self.polySplice.x(), self.polySplice.y())
        #             p2 = self.polySplice2.polygon().translated(self.polySplice.x(), self.polySplice.y())
        #             uni = p1.united(p2)

        #             # Unite adds the starting point again as endpoint so we have to remove this duplicate point
        #             # to avoid future problems
        #             uni = self.polyToList(uni, "Global")
        #             uni = uni[:-1]

        #             # Add the new merged polygon, remove the old polygons from the view and lists
        #             self.addPoly(QPolygonF(uni),False)
        #             self.deletePolygon(self.polySplice2, True)
        #             self.deletePolygon(self.polySplice, True)
        #             self.removeDrawingPoly()
        #             # break
        #         else:    
        #             # Si un polígono está siendo dibujado, terminar el polígono presionando el botón derecho del mouse.
        #             # Esto cerrará el polígono y removerá las lineas de soporte iniciales,
        #             # dejando únicamente las líneas y puntos del polígono terminado.
                    
        #             self.addPoly(self.currentPoly, holeMode=self.holeMode)
        #             self.removeDrawingPoly()

        #         # Resetear variables a su estado inicial
        #         self.currentPoly = None
        #         self.newPoly = True
        #         self.firstPoint = None
        #         self.prevPoint = None
        #         self.splice=False
        #         self.polySplice=None
        #         self.polySplice2=None

        #     elif e.button() == 1:
        #         if self.splitEdge:
        #             self.splice=True
        #             edge = self.splitEdge
        #             self.polySplice = edge.parentItem()
        #             if self.newPoly:
        #             # Inicializar nuevo poligono como objeto de tipo QPolygonF()
        #                 self.currentPoly = QPolygonF()

        #                 point = self.scene.addEllipse(
        #                     self.nodeSplitter.pos().x() - 3, self.nodeSplitter.pos().y() - 3, 6, 6, self.blackPen, self.greenBrush)

        #                 # Guardamos coordenadas del punto inicial del nuevo polígono    
        #                 self.firstPoint = QPointF(self.nodeSplitter.pos().x() - 5, self.nodeSplitter.pos().y())
        #                 self.prevPoint = QPointF(self.nodeSplitter.pos().x() - 5, self.nodeSplitter.pos().y())

        #                 # Pasar el punto inicial al poligono a construir
        #                 self.currentPoly << self.firstPoint
        #                 self.newPoly = False

        #                 self.drawingPoints.append(point)
        #                 self.drawingPointsCoords.append([self.nodeSplitter.pos().x() - 3, self.nodeSplitter.pos().y()])
        #             else:
        #                 point = self.scene.addEllipse(
        #                     self.nodeSplitter.pos().x() - 3, self.nodeSplitter.pos().y() -3, 6, 6, self.blackPen, self.greenBrush)

        #                 # Dibujamos linea entre punto actual y el anterior
        #                 line = self.scene.addLine(
        #                     QLineF(self.prevPoint, QPointF(self.nodeSplitter.pos().x(), self.nodeSplitter.pos().y())), self.blackPen)

        #                 # Guardamos coordenada del punto recién dibujado
        #                 self.prevPoint = QPointF(self.nodeSplitter.pos().x() -5, self.nodeSplitter.pos().y())

        #                 # Pasar el punto previo al Poligono a construir
        #                 self.currentPoly << self.prevPoint

        #                 self.connectingLineList.append(line)
        #                 self.drawingPoints.append(point)
        #                 self.drawingPointsCoords.append([self.nodeSplitter.pos().x() - 5, self.nodeSplitter.pos().y()])

        #         # Si se está dibujando un nuevo polígono
        #         elif self.newPoly:
        #             # Inicializar nuevo poligono como objeto de tipo QPolygonF()
        #             self.currentPoly = QPolygonF()

        #             point = self.scene.addEllipse(
        #                 x - 3, y - 3, 6, 6, self.blackPen, self.greenBrush)

        #             # Guardamos coordenadas del punto inicial del nuevo polígono    
        #             self.firstPoint = QPointF(x, y)
        #             self.prevPoint = QPointF(x, y)

        #             # Pasar el punto inicial al poligono a construir
        #             self.currentPoly << self.firstPoint
        #             self.newPoly = False

        #             self.drawingPoints.append(point)
        #             self.drawingPointsCoords.append([x, y])
        #         else:
        #             point = self.scene.addEllipse(
        #                 x - 3, y - 3, 6, 6, self.blackPen, self.greenBrush)

        #             # Dibujamos linea entre punto actual y el anterior
        #             line = self.scene.addLine(
        #                 QLineF(self.prevPoint, QPointF(x, y)), self.blackPen)

        #             # Guardamos coordenada del punto recién dibujado
        #             self.prevPoint = QPointF(x, y)

        #             # Pasar el punto previo al Poligono a construir
        #             self.currentPoly << self.prevPoint

        #             self.connectingLineList.append(line)
        #             self.drawingPoints.append(point)
        #             self.drawingPointsCoords.append([x, y])

        # if self.mode == "Splice poly left":
        #     if e.button() == 2:
        #         # Si el polígono a dibujar contiene 2 o menos puntos no se dibujará
        #         if self.newPoly or self.currentPoly.__len__() <= 2:
        #             return
                    
        #         if self.splice:
        #             self.polySplice2 = self.addPoly(self.currentPoly, holeMode=self.holeMode)
        #             p1 = self.polySplice.polygon().translated(self.polySplice.x(), self.polySplice.y())
        #             p2 = self.polySplice2.polygon().translated(self.polySplice.x(), self.polySplice.y())
        #             uni = p1.united(p2)

        #             # Unite adds the starting point again as endpoint so we have to remove this duplicate point
        #             # to avoid future problems
        #             uni = self.polyToList(uni, "Global")
        #             uni = uni[:-1]

        #             # Add the new merged polygon, remove the old polygons from the view and lists
        #             self.addPoly(QPolygonF(uni),False)
        #             self.deletePolygon(self.polySplice2, True)
        #             self.deletePolygon(self.polySplice, True)
        #             self.removeDrawingPoly()
        #             # break
        #         else:    
        #             # Si un polígono está siendo dibujado, terminar el polígono presionando el botón derecho del mouse.
        #             # Esto cerrará el polígono y removerá las lineas de soporte iniciales,
        #             # dejando únicamente las líneas y puntos del polígono terminado.
                    
        #             self.addPoly(self.currentPoly, holeMode=self.holeMode)
        #             self.removeDrawingPoly()

        #         # Resetear variables a su estado inicial
        #         self.currentPoly = None
        #         self.newPoly = True
        #         self.firstPoint = None
        #         self.prevPoint = None
        #         self.splice=False
        #         self.polySplice=None
        #         self.polySplice2=None

        #     elif e.button() == 1:
        #         if self.splitEdge:
        #             self.splice=True
        #             edge = self.splitEdge
        #             self.polySplice = edge.parentItem()
        #             if self.newPoly:
        #             # Inicializar nuevo poligono como objeto de tipo QPolygonF()
        #                 self.currentPoly = QPolygonF()

        #                 point = self.scene.addEllipse(
        #                     self.nodeSplitter.pos().x() - 3, self.nodeSplitter.pos().y() -3, 6, 6, self.blackPen, self.greenBrush)

        #                 # Guardamos coordenadas del punto inicial del nuevo polígono    
        #                 self.firstPoint = QPointF(self.nodeSplitter.pos().x() + 3, self.nodeSplitter.pos().y())
        #                 self.prevPoint = QPointF(self.nodeSplitter.pos().x() + 3, self.nodeSplitter.pos().y())

        #                 # Pasar el punto inicial al poligono a construir
        #                 self.currentPoly << self.firstPoint
        #                 self.newPoly = False

        #                 self.drawingPoints.append(point)
        #                 self.drawingPointsCoords.append([self.nodeSplitter.pos().x() + 3, self.nodeSplitter.pos().y()])
        #             else:
        #                 point = self.scene.addEllipse(
        #                     self.nodeSplitter.pos().x() - 3, self.nodeSplitter.pos().y() - 3, 6, 6, self.blackPen, self.greenBrush)

        #                 # Dibujamos linea entre punto actual y el anterior
        #                 line = self.scene.addLine(
        #                     QLineF(self.prevPoint, QPointF(self.nodeSplitter.pos().x(), self.nodeSplitter.pos().y())), self.blackPen)

        #                 # Guardamos coordenada del punto recién dibujado
        #                 self.prevPoint = QPointF(self.nodeSplitter.pos().x() + 3, self.nodeSplitter.pos().y())

        #                 # Pasar el punto previo al Poligono a construir
        #                 self.currentPoly << self.prevPoint

        #                 self.connectingLineList.append(line)
        #                 self.drawingPoints.append(point)
        #                 self.drawingPointsCoords.append([self.nodeSplitter.pos().x() + 3, self.nodeSplitter.pos().y()])

        #         # Si se está dibujando un nuevo polígono
        #         elif self.newPoly:
        #             # Inicializar nuevo poligono como objeto de tipo QPolygonF()
        #             self.currentPoly = QPolygonF()

        #             point = self.scene.addEllipse(
        #                 x - 3, y - 3, 6, 6, self.blackPen, self.greenBrush)

        #             # Guardamos coordenadas del punto inicial del nuevo polígono    
        #             self.firstPoint = QPointF(x, y)
        #             self.prevPoint = QPointF(x, y)

        #             # Pasar el punto inicial al poligono a construir
        #             self.currentPoly << self.firstPoint
        #             self.newPoly = False

        #             self.drawingPoints.append(point)
        #             self.drawingPointsCoords.append([x, y])
        #         else:
        #             point = self.scene.addEllipse(
        #                 x - 3, y - 3, 6, 6, self.blackPen, self.greenBrush)

        #             # Dibujamos linea entre punto actual y el anterior
        #             line = self.scene.addLine(
        #                 QLineF(self.prevPoint, QPointF(x, y)), self.blackPen)

        #             # Guardamos coordenada del punto recién dibujado
        #             self.prevPoint = QPointF(x, y)

        #             # Pasar el punto previo al Poligono a construir
        #             self.currentPoly << self.prevPoint

        #             self.connectingLineList.append(line)
        #             self.drawingPoints.append(point)
        #             self.drawingPointsCoords.append([x, y])
    
        # if self.mode == "Splice poly down":
        #     if e.button() == 2:
        #         # Si el polígono a dibujar contiene 2 o menos puntos no se dibujará
        #         if self.newPoly or self.currentPoly.__len__() <= 2:
        #             return
                    
        #         if self.splice:
        #             self.polySplice2 = self.addPoly(self.currentPoly, holeMode=self.holeMode)
        #             p1 = self.polySplice.polygon().translated(self.polySplice.x(), self.polySplice.y())
        #             p2 = self.polySplice2.polygon().translated(self.polySplice.x(), self.polySplice.y())
        #             uni = p1.united(p2)

        #             # Unite adds the starting point again as endpoint so we have to remove this duplicate point
        #             # to avoid future problems
        #             uni = self.polyToList(uni, "Global")
        #             uni = uni[:-1]

        #             # Add the new merged polygon, remove the old polygons from the view and lists
        #             self.addPoly(QPolygonF(uni),False)
        #             self.deletePolygon(self.polySplice2, True)
        #             self.deletePolygon(self.polySplice, True)
        #             self.removeDrawingPoly()
        #             # break
        #         else:    
        #             # Si un polígono está siendo dibujado, terminar el polígono presionando el botón derecho del mouse.
        #             # Esto cerrará el polígono y removerá las lineas de soporte iniciales,
        #             # dejando únicamente las líneas y puntos del polígono terminado.
                    
        #             self.addPoly(self.currentPoly, holeMode=self.holeMode)
        #             self.removeDrawingPoly()

        #         # Resetear variables a su estado inicial
        #         self.currentPoly = None
        #         self.newPoly = True
        #         self.firstPoint = None
        #         self.prevPoint = None
        #         self.splice=False
        #         self.polySplice=None
        #         self.polySplice2=None

        #     elif e.button() == 1:
        #         if self.splitEdge:
        #             self.splice=True
        #             edge = self.splitEdge
        #             self.polySplice = edge.parentItem()
        #             if self.newPoly:
        #             # Inicializar nuevo poligono como objeto de tipo QPolygonF()
        #                 self.currentPoly = QPolygonF()

        #                 point = self.scene.addEllipse(
        #                     self.nodeSplitter.pos().x() - 3, self.nodeSplitter.pos().y() - 3, 6, 6, self.blackPen, self.greenBrush)

        #                 # Guardamos coordenadas del punto inicial del nuevo polígono    
        #                 self.firstPoint = QPointF(self.nodeSplitter.pos().x(), self.nodeSplitter.pos().y() - 5)
        #                 self.prevPoint = QPointF(self.nodeSplitter.pos().x(), self.nodeSplitter.pos().y() - 5)

        #                 # Pasar el punto inicial al poligono a construir
        #                 self.currentPoly << self.firstPoint
        #                 self.newPoly = False

        #                 self.drawingPoints.append(point)
        #                 self.drawingPointsCoords.append([self.nodeSplitter.pos().x(), self.nodeSplitter.pos().y() - 5])
        #             else:
        #                 point = self.scene.addEllipse(
        #                     self.nodeSplitter.pos().x() - 3, self.nodeSplitter.pos().y() - 3, 6, 6, self.blackPen, self.greenBrush)

        #                 # Dibujamos linea entre punto actual y el anterior
        #                 line = self.scene.addLine(
        #                     QLineF(self.prevPoint, QPointF(self.nodeSplitter.pos().x(), self.nodeSplitter.pos().y())), self.blackPen)

        #                 # Guardamos coordenada del punto recién dibujado
        #                 self.prevPoint = QPointF(self.nodeSplitter.pos().x() - 3, self.nodeSplitter.pos().y() - 5)

        #                 # Pasar el punto previo al Poligono a construir
        #                 self.currentPoly << self.prevPoint

        #                 self.connectingLineList.append(line)
        #                 self.drawingPoints.append(point)
        #                 self.drawingPointsCoords.append([self.nodeSplitter.pos().x(), self.nodeSplitter.pos().y() - 5])

        #         # Si se está dibujando un nuevo polígono
        #         elif self.newPoly:
        #             # Inicializar nuevo poligono como objeto de tipo QPolygonF()
        #             self.currentPoly = QPolygonF()

        #             point = self.scene.addEllipse(
        #                 x - 3, y - 3, 6, 6, self.blackPen, self.greenBrush)

        #             # Guardamos coordenadas del punto inicial del nuevo polígono    
        #             self.firstPoint = QPointF(x, y)
        #             self.prevPoint = QPointF(x, y)

        #             # Pasar el punto inicial al poligono a construir
        #             self.currentPoly << self.firstPoint
        #             self.newPoly = False

        #             self.drawingPoints.append(point)
        #             self.drawingPointsCoords.append([x, y])
        #         else:
        #             point = self.scene.addEllipse(
        #                 x - 3, y - 3, 6, 6, self.blackPen, self.greenBrush)

        #             # Dibujamos linea entre punto actual y el anterior
        #             line = self.scene.addLine(
        #                 QLineF(self.prevPoint, QPointF(x, y)), self.blackPen)

        #             # Guardamos coordenada del punto recién dibujado
        #             self.prevPoint = QPointF(x, y)

        #             # Pasar el punto previo al Poligono a construir
        #             self.currentPoly << self.prevPoint

        #             self.connectingLineList.append(line)
        #             self.drawingPoints.append(point)
        #             self.drawingPointsCoords.append([x, y])

        # if self.mode == "Splice poly up":
        #     if e.button() == 2:
        #         # Si el polígono a dibujar contiene 2 o menos puntos no se dibujará
        #         if self.newPoly or self.currentPoly.__len__() <= 2:
        #             return
                    
        #         if self.splice:
        #             self.polySplice2 = self.addPoly(self.currentPoly, holeMode=self.holeMode)
        #             p1 = self.polySplice.polygon().translated(self.polySplice.x(), self.polySplice.y())
        #             p2 = self.polySplice2.polygon().translated(self.polySplice.x(), self.polySplice.y())
        #             uni = p1.united(p2)

        #             # Unite adds the starting point again as endpoint so we have to remove this duplicate point
        #             # to avoid future problems
        #             uni = self.polyToList(uni, "Global")
        #             uni = uni[:-1]

        #             # Add the new merged polygon, remove the old polygons from the view and lists
        #             self.addPoly(QPolygonF(uni),False)
        #             self.deletePolygon(self.polySplice2, True)
        #             self.deletePolygon(self.polySplice, True)
        #             self.removeDrawingPoly()
        #             # break
        #         else:    
        #             # Si un polígono está siendo dibujado, terminar el polígono presionando el botón derecho del mouse.
        #             # Esto cerrará el polígono y removerá las lineas de soporte iniciales,
        #             # dejando únicamente las líneas y puntos del polígono terminado.
                    
        #             self.addPoly(self.currentPoly, holeMode=self.holeMode)
        #             self.removeDrawingPoly()

        #         # Resetear variables a su estado inicial
        #         self.currentPoly = None
        #         self.newPoly = True
        #         self.firstPoint = None
        #         self.prevPoint = None
        #         self.splice=False
        #         self.polySplice=None
        #         self.polySplice2=None

        #     elif e.button() == 1:
        #         if self.splitEdge:
        #             self.splice=True
        #             edge = self.splitEdge
        #             self.polySplice = edge.parentItem()
        #             if self.newPoly:
        #             # Inicializar nuevo poligono como objeto de tipo QPolygonF()
        #                 self.currentPoly = QPolygonF()

        #                 point = self.scene.addEllipse(
        #                     self.nodeSplitter.pos().x() - 3, self.nodeSplitter.pos().y() - 3, 6, 6, self.blackPen, self.greenBrush)

        #                 # Guardamos coordenadas del punto inicial del nuevo polígono    
        #                 self.firstPoint = QPointF(self.nodeSplitter.pos().x(), self.nodeSplitter.pos().y() + 5)
        #                 self.prevPoint = QPointF(self.nodeSplitter.pos().x(), self.nodeSplitter.pos().y() + 5)

        #                 # Pasar el punto inicial al poligono a construir
        #                 self.currentPoly << self.firstPoint
        #                 self.newPoly = False

        #                 self.drawingPoints.append(point)
        #                 self.drawingPointsCoords.append([self.nodeSplitter.pos().x(), self.nodeSplitter.pos().y() + 5])
        #             else:
        #                 point = self.scene.addEllipse(
        #                     self.nodeSplitter.pos().x() - 3, self.nodeSplitter.pos().y() - 3, 6, 6, self.blackPen, self.greenBrush)

        #                 # Dibujamos linea entre punto actual y el anterior
        #                 line = self.scene.addLine(
        #                     QLineF(self.prevPoint, QPointF(self.nodeSplitter.pos().x(), self.nodeSplitter.pos().y())), self.blackPen)

        #                 # Guardamos coordenada del punto recién dibujado
        #                 self.prevPoint = QPointF(self.nodeSplitter.pos().x(), self.nodeSplitter.pos().y() + 5)

        #                 # Pasar el punto previo al Poligono a construir
        #                 self.currentPoly << self.prevPoint

        #                 self.connectingLineList.append(line)
        #                 self.drawingPoints.append(point)
        #                 self.drawingPointsCoords.append([self.nodeSplitter.pos().x(), self.nodeSplitter.pos().y() + 5])

        #         # Si se está dibujando un nuevo polígono
        #         elif self.newPoly:
        #             # Inicializar nuevo poligono como objeto de tipo QPolygonF()
        #             self.currentPoly = QPolygonF()

        #             point = self.scene.addEllipse(
        #                 x - 3, y - 3, 6, 6, self.blackPen, self.greenBrush)

        #             # Guardamos coordenadas del punto inicial del nuevo polígono    
        #             self.firstPoint = QPointF(x, y)
        #             self.prevPoint = QPointF(x, y)

        #             # Pasar el punto inicial al poligono a construir
        #             self.currentPoly << self.firstPoint
        #             self.newPoly = False

        #             self.drawingPoints.append(point)
        #             self.drawingPointsCoords.append([x, y])
        #         else:
        #             point = self.scene.addEllipse(
        #                 x - 3, y - 3, 6, 6, self.blackPen, self.greenBrush)

        #             # Dibujamos linea entre punto actual y el anterior
        #             line = self.scene.addLine(
        #                 QLineF(self.prevPoint, QPointF(x, y)), self.blackPen)

        #             # Guardamos coordenada del punto recién dibujado
        #             self.prevPoint = QPointF(x, y)

        #             # Pasar el punto previo al Poligono a construir
        #             self.currentPoly << self.prevPoint

        #             self.connectingLineList.append(line)
        #             self.drawingPoints.append(point)
        #             self.drawingPointsCoords.append([x, y])


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

                    point = self.scene.addEllipse(
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
                    point = self.scene.addEllipse(
                        x - 3, y - 3, 6, 6, self.blackPen, self.greenBrush)

                    # Dibujamos linea entre punto actual y el anterior
                    line = self.scene.addLine(
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

    def mouseReleaseEvent(self, event):
        # If a point or polygon is selected releasing the mouse will de-select the object and add the
        # current coordinates back to the global coordinate list to update to the new position
        
        if self.mode == "Arrow":
            if self.scene.selectedItems():
                if isinstance(self.scene.selectedItems()[0], PyQt5.QtWidgets.QGraphicsPolygonItem):
                    for point in self.polyToList(self.scene.selectedItems()[0], "Global"):
                        self.pointCoordList = np.append(self.pointCoordList, [[point.x(), point.y()]], axis=0)
            self.scene.clearSelection()                

    def addPoly(self, polygon, point_marker_dict=None, curve_marker_dict=None, holeMode = False):
        """ Agrega un polígono a la escena padre. Regresa QPolygonF"""
        # Si el modo de dibujo es de agujero
        if holeMode:
            poly = self.scene.addPolygon(polygon, QPen(QColor(0, 0, 0, 0)), QBrush(QColor(255, 255, 255)))
            poly.setZValue(1)
            self.polyList.append(poly)
            self.holeList.append(poly)
        else:
            poly = self.scene.addPolygon(polygon, QPen(QColor(0, 0, 0, 0)), QBrush(QColor(0, 0, 0, 50)))
            self.polyList.append(poly)
        self.addPolyCorners(poly, point_marker_dict)
        self.addPolyEdges(poly, curve_marker_dict)
        return poly

    def addPolyCorners(self, polyItem, marker_dict=None):
        """ Agrega puntos/vertices del polígono dibujado"""
        poly = polyItem.polygon()

        for i in range(poly.size()):
            point = poly.at(i)
            p = self.scene.addEllipse(-4, -4, 8, 8, self.LUBronze, self.LUBronze)
            p.setZValue(2)  # Make sure corners always in front of polygon surfaces
            p.setParentItem(polyItem)
            p.setFlag(QGraphicsItem.ItemIsSelectable)
            p.setFlag(QGraphicsItem.ItemIsMovable)
            p.__setattr__("localIndex", int(i))
            p.setPos(point.x(), point.y())
            self.pointCoordList = np.append(self.pointCoordList, [[p.x(), p.y()]], axis=0)
            
            # Used to pass markers when loading a g
            if marker_dict:
                if i in marker_dict:
                    self.add_marker(p, marker_dict[i])
                    text = p.childItems()[0]
                    text.setVisible(True)
                    print(text)

    def addPolyEdges(self, polyItem, marker_dict=None):
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

            line = self.scene.addLine(QLineF(p1, p2))
            line.setZValue(-1)
            displayLine = self.scene.addLine(QLineF(p1, p2), QPen(self.LUBronze, 3))
            line.__setattr__("localIndex", index)
            line.setParentItem(polyItem)
            displayLine.setParentItem(line)
            self.edgeList.append(line)

            # Used to pass markers when loading a g
            if marker_dict:
                print("a")
                if i - 1 in marker_dict:
                    self.add_marker(displayLine, marker_dict[i - 1])
                    displayLine.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, False)
                    text = displayLine.childItems()[0]
                    text.setVisible(True)

    def add_marker(self, item, marker_text):
        """Add a marker to a line or a point, updates the marker dictionary and a reversed one to handle MATLAB
        interactions, also changes the display of the targeted edge or point"""

        if marker_text in self.marker_dict:
            index = self.marker_dict[marker_text]
        else:
            index = self.line_marker_index
        item.__setattr__("marker", index)
        self.marker_dict[marker_text] = index
        self.reversed_marker_dict[index] = marker_text
        self.line_marker_index += 1

        if isinstance(item, PyQt5.QtWidgets.QGraphicsEllipseItem):
            self.point_marker_list.append(item)
            item.setBrush(QColor("Red"))

            # If there is an old marker remove it and remove as child item
            if item.childItems():
                item.childItems()[0].setVisible(False)
                item.childItems()[0].setParentItem(None)

            text = self.addText(str(marker_text), QFont("Helvetica", 8, QFont.Bold))
            text.setParentItem(item)
            text.setPos(-5, 5)

        if isinstance(item, PyQt5.QtWidgets.QGraphicsLineItem):
            self.line_marker_list.append(item)
            item.setPen(QPen(QColor("Red"), 2))

            # If there is an old marker remove it and remove as child item
            if item.childItems():
                item.childItems()[0].setVisible(False)
                item.childItems()[0].setParentItem(None)

            text = self.addText(str(marker_text), QFont("Helvetica", 8, QFont.Bold))
            text.setParentItem(item)
            text.setPos((item.line().x1() + item.line().x2()) / 2 - 15, (item.line().y1() + item.line().y2()) / 2 - 15)


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

        for edge in self.edgeList:
            edge.childItems()[0].setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, enabled)
            if edge.childItems()[0].childItems():
                text = edge.childItems()[0].childItems()[0]
                text.setVisible(True)
                
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
                self.polyG = outerPoly
                self.polyN = innerPoly
                containList.append(innerPoly)
        return containList
    
    def buildGmsh(self):
        g = cfg.Geometry()
        g.marker_dict = self.reversed_marker_dict
        pointIndex = 0
        lineIndex = 0
        addedPoints = []
        addedLines = []
        pointmarkerList = []
        edgeMarkerList = []
        surfaceIndex = 0
        ignoreWarning = False

        # Create a list of all coordinates where a point has a marker
        for point in self.point_marker_list:
            pointmarkerList.append(point.scenePos())

        # Create a list with coordinates of the points of a edge which has a marker
        for edge in self.line_marker_list:
            l = edge.line()
            x = edge.scenePos().x()
            y = edge.scenePos().y()
            edgeMarkerList.append([[l.p1().x() + x, -l.p1().y() - y], [l.p2().x() + x, - l.p2().y() - y]])

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

            # If the point is in the marker list store the marker text in point_marker
            if point in pointmarkerList:
                i = pointmarkerList.index(point)
                pointmarker = self.point_marker_list[i].marker

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
        if len(self.polyList) != 0:
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

                a = []
                for i in coords:
                    a.append(random.randrange(100,300))
                
                cfv.plt.set_cmap("jet")
                cfv.plt.ion()

                if self.figureCanvas is not None:
                    if self.mplLayout.count() == 0:
                        self.mplLayout.addWidget(self.figureCanvas)
    
                    # Ejemplo de color y de tiempo equisde
                    for phase in np.linspace(1,100,10):
                        if phase == 1:
                            changedValues = [val * phase for val in a]
                            cfv.draw_nodal_values_contourf(changedValues, coords, edof, title="Temperature", dofs_per_node=mesh.dofs_per_node, el_type=mesh.el_type, draw_elements=True)    
                            cfv.colorbar()
                            self.figureCanvas.draw()
                            self.figureCanvas.flush_events()
                        else:
                            changedValues = [val * phase for val in a]
                            cfv.draw_nodal_values_contourf(changedValues, coords, edof, title="Temperature", dofs_per_node=mesh.dofs_per_node, el_type=mesh.el_type, draw_elements=True)    
                            self.figureCanvas.draw()
                            self.figureCanvas.flush_events()
                        
                else:
                    cfv.show_and_wait()
                return None
            else:
                return "Canceled"

        else:
            self.noPoly()

    def noPoly(self):
        msg = QMessageBox()
        msg.setWindowTitle("Advertencia")
        msg.setText("No hay figuras")
        msg.setIcon(QMessageBox.Warning)
        msg.setStandardButtons(QMessageBox.Cancel | QMessageBox.Ignore)

        msg.buttonClicked.connect(self.popupButton)
        msg.exec_()
        return self.overlapWarningChoice

    def create_grid(self):
        """
        Create the grid for the graphics scene
        """

        # If called when a grid already exists create a new grid
        if self.grid:
            self.grid = []

        grid_pen = QPen(QColor(215, 215, 215), 1)
        w = 1020
        h = 760
        self.scene.addLine(0, 380, 1020, 380, QPen(QColor(0, 0, 0), 2))
        self.scene.addLine(500, 760, 500, 0, QPen(QColor(0, 0, 0), 2))

        w = int(w / self.grid_spacing) * self.grid_spacing
        h = int(h / self.grid_spacing) * self.grid_spacing
        for i in range(0, w, self.grid_spacing):
            if i == 0:
                pass
            else:
                line = self.scene.addLine(i, 0, i, h, grid_pen)
                line.setZValue(-1)
                self.grid.append(line)
        for i in range(0, h, self.grid_spacing):
            if i == 0:
                pass
            else:
                line = self.scene.addLine(0, i, w, i, grid_pen)
                line.setZValue(-1)
                self.grid.append(line)

        self.grid_built = True