from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPen, QColor

class Conditions():
    def currentTypeCondition(comb, tbox, array): 
        
        for i in range(tbox.count()):
            tbox.removeItem(tbox.currentIndex())
         
        if comb.currentIndex() == 1:
            tbox.insertItem(0, array[0], str(comb.currentText()))
        if comb.currentIndex() == 2:
            tbox.insertItem(0, array[1], str(comb.currentText()))

    def reloadEdges(canvas, listWid):
        edges = canvas.getEdges()
        listOfPolys = []

        if listWid.count() != 0:
            listWid.clear()
        
        for i in range(len(edges)):
            polygon = str(i+1)
            listOfPolys.append({'edge':edges[i], 'text':polygon, 'indice':i })
            listWid.addItem(polygon)

    
    def currentElementSelectListWidgets(element, canvas):
        index = int(element.text())
        edges = canvas.getEdges()
        line = edges[index-1]
        LUBronze = QColor(156, 87, 20)
        defaultColor = QPen(LUBronze)
        defaultColor.setWidth(3)
        for elem in edges:
            elem.setPen(defaultColor)

        paint = QPen(Qt.red)
        paint.setWidth(5)
        line.setPen(paint)
