class MeshSettings():
    def currentShowMeshTab(text, win):
        if(text == "Mesh and Setting Study"):
            win.show()
        else:
            win.hide()

    def do_something(wid):
        if(wid.cmbConstructionBy.currentText() == "Data"):
            wid.canvas.mode = "Arrow"
        else:
            if(wid.cmbGeometricFigure.currentText() == "Polygon"):
                wid.canvas.mode = "Draw poly"
            elif(wid.cmbGeometricFigure.currentText() == "Square"):
                wid.canvas.mode = "Draw rect"

    def changeDrawMode(wid):
        if(wid.cmbGeometricFigure.currentText() == "Polygon"):
            wid.canvas.mode = "Draw poly"
        elif(wid.cmbGeometricFigure.currentText() == "Square"):
           wid.canvas.mode = "Draw rect"

    def changeMode(wid):
        if(wid.cmbTypeOfConstruction.currentText() == "Solid"):
            wid.canvas.holeMode = False
        else:
           wid.canvas.holeMode = True
           
    def changeTab(wid):
        if(wid.tabWidgetMenu.tabText(wid.tabWidgetMenu.currentIndex())) == "Geometry":
            if(wid.cmbConstructionBy.currentText() == "Data"):
                wid.canvas.mode = "Arrow"
            else:
                if(wid.cmbGeometricFigure.currentText() == "Polygon"):
                    wid.canvas.mode = "Draw poly"
                elif(wid.cmbGeometricFigure.currentText() == "Square"):
                    wid.canvas.mode = "Draw rect"

    def meshSettings(wid):
        if(wid.cmbElementType.currentText()=="Triangle"):
            wid.canvas.elType = 2
        elif(wid.cmbElementType.currentText()=="Quadrangle"):
            wid.canvas.elType = 3
        
        if(wid.cmbElementSize.currentText()=="Finer"):
            wid.canvas.elSizeFactor = 5
        elif(wid.cmbElementSize.currentText()=="Fine"):
            wid.canvas.elSizeFactor = 15
        elif(wid.cmbElementSize.currentText()=="Normal"):
            wid.canvas.elSizeFactor = 25
        elif(wid.cmbElementSize.currentText()=="Coarse"):
            wid.canvas.elSizeFactor = 35
        elif(wid.cmbElementSize.currentText()=="Coarser"):
            wid.canvas.elSizeFactor = 45

        wid.canvas.showMesh()