class Conditions():
    def currentTypeCondition(comb, tbox, array): 
        
        for i in range(tbox.count()):
            tbox.removeItem(tbox.currentIndex())
         
        if comb.currentIndex() == 1:
            tbox.insertItem(0, array[0], str(comb.currentText()))
        if comb.currentIndex() == 2:
            tbox.insertItem(0, array[1], str(comb.currentText()))

    def reloadEdges(canvas, listWid):
        polygons , edges = canvas.getAll()
        # print(polygons)
        # print(edges)
        listOfEdges = []
        listOfPolys = []

        if listWid.count() != 0:
            listWid.clear()
        
        for i in range(len(polygons)):
            # print("Figura " + str(i+1))
            polygon = "Figura " + str(i+1)
            listOfPolys.append({'polygon':polygons[i], 'text':polygon })
            # listWid.addItem(polygon)

        for poly in listOfPolys:
            # print(poly['text'])
            listWid.addItem(poly['text'])
            for i in range(len(poly['polygon'][0])):
                # print(i)
                text = "linea " + str(i+1)
            # listOfEdges.append([edges[i], text ])
                listWid.addItem(text)

        # print(listOfPolys)
    
    def currentElementSelectListWidgets(element):
        value = element.text()
        print(value)