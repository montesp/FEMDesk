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
        print(comb.currentIndex())
        widgetElements = []
        widgetElements = sectionWidget.findChildren(QLineEdit)

        
        # print(widgetElement.text())


        if comb.currentIndex() <= 3:
            print('First Elements')
            for widgetElement in widgetElements:
                try:
                    valor = float(widgetElement.text())
                    print(valor)
                except ValueError:
                    print('Solo se aceptan numeros')
                
            
        else :
            print('Polygon')
            widgetElements += sectionWidget.findChildren(QTableWidget)
            for indexElement in range(len(widgetElements)):
                if indexElement == 0:
                    # print(widgetElements[indexElement].text())
                    pass
                else:
                    pass
                    # print(indexElement)
                    # print(widgetElements[indexElement])
