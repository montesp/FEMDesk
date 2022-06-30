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
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QCloseEvent
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsView, QButtonGroup, QMessageBox
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets

app = None
       
class EditorWindow(QMainWindow):
    """MainWindow-klass som hanterar vårt huvudfönster"""

    def __init__(self):
        super(QMainWindow, self).__init__()
        self.app = app
        root = os.path.dirname(os.path.realpath(__file__))
        loadUi(os.path.join(root, 'Interfaz.ui'), self)
            
def init_app():
    app = QApplication.instance()

    if app is None:
        print("No QApplication instance found. Creating one.")
        # if it does not exist then a QApplication is created
        app = QApplication(sys.argv)
    else:
        print("QApplication instance found.")

    return app

if __name__ == '__main__':
    app = init_app()

    widget = EditorWindow()
    widget.show()
 
    sys.exit(app.exec_())