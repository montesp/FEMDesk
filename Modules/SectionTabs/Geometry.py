from ast import Pass
from cmath import log
from operator import index
from os import EX_CANTCREAT
from PyQt5.QtWidgets import QLineEdit, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import QPointF
from PyQt5.QtGui import QPolygonF


class Geometry():
    def currentCheckedComboBoxItem(section, comb, array):
        section.show()

        for i in range(section.count()):
            section.removeItem(section.currentIndex())

        if comb.currentIndex() <= 4:
            section.insertItem(
                0, array[comb.currentIndex()], str(comb.currentText()))
            # array[comb.currentIndex()].move(10,100)
            #section.setItemEnabled(comb.currentIndex(), True)
            #section.widget(comb.currentIndex()).show()#

    def getData(sectionWidget, comb):
        # ? Es el comb necesario?
        widgetElements = []
        widgetElements = sectionWidget.findChildren(QLineEdit)
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
                            xValue = float(table.item(i,j).text())
                        else: 
                            yValue = float(table.item(i,j).text())
                            poly << QPointF(xValue, yValue)
                            
                    else:
                        raise ValueError("Espacio vacio en: ", i, j)

            return poly 

        except ValueError:
            print("Error al aplicar cambios. Espacios vacíos en coordenadas")
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
