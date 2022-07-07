from EF import *
from interfaz import *

def currentPolygon(self):

    figuresSection = self.findChild(QtWidgets.QToolBox, "figuresSection")
    cmbGeometricFigure = self.findChild(QtWidgets.QComboBox, "cmbGeometricFigure")

    figuresSection.setItemEnabled(0, False)
    figuresSection.setItemEnabled(1, False)
    figuresSection.setItemEnabled(2, False)
    figuresSection.setItemEnabled(3, False)
    figuresSection.setItemEnabled(4, False)

    figuresSection.setItemEnabled(cmbGeometricFigure.currentIndex(), True)

  
    
