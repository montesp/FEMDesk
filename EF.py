#-*- coding: utf-8 -*-
"""
Created on Wed May 11 13:39:55 2022

@author: ruben.castaneda
"""

#-*- coding: utf-8 -*-
"""
Created on Tue May 10 14:30:09 2022

@author: ruben.castaneda
"""

import os, sys
import imagen_rc
from PyQt5.QtCore import Qt, QObject
from PyQt5.QtGui import QPainter, QCloseEvent, QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsView, QButtonGroup, QMessageBox, QTabWidget
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from interfaz import *
from module import *

app = None
class EditorWindow(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()
        self.app = app
        with open('styles.qss', 'r', encoding='utf-8') as file:
            str = file.read()
        self.setStyleSheet(str)
        root = os.path.dirname(os.path.realpath(__file__))
        loadUi(os.path.join(root, 'Interfaz.ui'), self)
        #cmbGeometricFigure = self.findChild(QtWidgets.QComboBox, "cmbGeometricFigure")
        #cmbGeometricFigure.activated.connect(currentPolygon)
        currentPolygon(self)
            

def init_app():
    app = QApplication.instance()
    app = QApplication(sys.argv)

    return app

def main():
    app = init_app()
    
    widget = EditorWindow()
    widget.setWindowIcon(QIcon("icon-temperature.png"))
    widget.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
