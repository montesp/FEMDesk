import numpy as np
from PyQt5.QtCore import QPointF, QLineF, QRectF, QRegExp, Qt, QRect
from PyQt5.QtGui import QPen, QColor, QBrush, QPolygonF, QFont, QRegExpValidator
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QFileDialog, QGraphicsScene, \
    QGraphicsItem, QGraphicsPolygonItem, QToolButton, QLabel, \
    QGraphicsEllipseItem, QLineEdit, QFormLayout, QGraphicsLineItem, QGraphicsTextItem, QGridLayout, QPushButton, QGraphicsItem, QGraphicsView, \
    QVBoxLayout, QMessageBox, QSlider
import canvas

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
        self.canvas = canvas(self)
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