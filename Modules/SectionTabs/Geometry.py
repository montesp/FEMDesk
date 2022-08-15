from PyQt5.QtWidgets import QLineEdit, QTableWidget

class Geometry():
    def currentCheckedComboBoxItem(section, comb, array):
        section.show()

        for i in range(section.count()):
            section.removeItem(section.currentIndex())

        if comb.currentIndex() <= 4:
            section.insertItem(0, array[comb.currentIndex()], str(comb.currentText()))
            #array[comb.currentIndex()].move(10,100)
            #section.setItemEnabled(comb.currentIndex(), True)
            #section.widget(comb.currentIndex()).show()#

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
                        print(widgetElement)
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
                    widgetValue = float(widgetElements[0].text())
            except ValueError:
                print('Solo se aceptan numeros')
            print(widgetValue)