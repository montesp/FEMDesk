class Materials():
    def currentHeatConduction(comb, ar):
        for i, item in enumerate(ar):
            ar[i].clear()
            ar[i].setEnabled(False)

        if comb.currentIndex() == 0:
            ar[0].setEnabled(True)
        if comb.currentIndex() == 1:
            ar[1].setEnabled(True)
            ar[4].setEnabled(True)
            ar[2].insert("0")
            ar[3].insert("0")
        if comb.currentIndex() == 2:
            ar[1].setEnabled(True)
            ar[2].setEnabled(True)
            ar[4].setEnabled(True)
        if comb.currentIndex() == 3:
            ar[1].setEnabled(True)
            ar[2].setEnabled(True)
            ar[3].setEnabled(True)
            ar[4].setEnabled(True)

    def currentTextSimmetry(comb, ar):
        if comb.currentIndex() == 2:
            ar[3].clear()
            ar[3].insert(ar[1].text())

    def currentDomains(lwDomains, canvas):
        polys, edges = canvas.getAll()

        if lwDomains.count() != 0:
            lwDomains.clear()

        if len(polys) != 0:
            for indexPoly in range(len(polys)):
                text = 'figura ' + str(indexPoly + 1)
                lwDomains.addItem(text)
