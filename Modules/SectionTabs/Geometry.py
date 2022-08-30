from ast import Pass
from operator import index
from PyQt5.QtWidgets import QLineEdit, QTableWidget

class Geometry():
    def currentCheckedComboBoxItem(section, comb, array):
        section.show()
        for i in range(section.count()):
            section.removeItem(section.currentIndex())

        if comb.currentIndex() <= 4:
            section.insertItem(0, array[comb.currentIndex()], str(comb.currentText()))

    def getData(sectionWidget, comb):
        widgetElements = []
        widgetElements = sectionWidget.findChildren(QLineEdit)

        if comb.currentIndex() <= 3:
            print('First Elements')
            for widgetElement in widgetElements:
                try:

                    if widgetElement.text() == "":
                        print("No puedes dejar espacio vacio")
                    else:
                        widgetValue = float(widgetElement.text())
                        print(widgetValue)
                except ValueError:
                    print('Solo se aceptan numeros')

        else :
            print('Polygon')
            widgetElements += sectionWidget.findChildren(QTableWidget)
            try:
                if widgetElements[0].text() == "":
                        print("No puedes dejar espacio vacio")
                else:
                    widgetValue = int(widgetElements[0].text())
                    widgetTable = widgetElements[1]
                    
                    print('Wigget value')
                    print(widgetValue)
                    print('--------------------')
                    indexPastTable = widgetTable.rowCount()

                    print(indexPastTable)

                    for i in range(indexPastTable): #Quitar los elementos de la tabla
                        widgetTable.removeRow(1)

                    for indexTable in range(widgetValue): #Poner los elementos 
                        widgetTable.insertRow(indexTable)

                    print(widgetTable)
                    print(widgetTable.rowCount())


            except ValueError:
                print('Solo se aceptan numeros')
