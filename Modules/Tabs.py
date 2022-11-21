class Tabs:
    def hideElementsTab(tabs ,tabMenu):
        for i in range(len(tabs)):
            if i != 0:
                # Borra siempre la posicion 1 porque se recorre los tabs al momento de eliminarse
                tabMenu.removeTab(1)

    def hideElementTab(index, tabMenu):
        tabMenu.removeTab(index)

    def addTabElement(tabs, tabMenu):
        for i in range(len(tabs)):
                if i != 0:
                    tabMenu.insertTab(i, tabs[i]['widget'], tabs[i]['title'])


    def addTabElement2(tabs, tabMenu, sig, win):
        if len(win.canvas.polyList) > 0:
            choice = win.geometryWarning("Are you sure?", "If you accept you will be unable to modify the geometry")
            if choice == "OK":
                edges = len(win.canvas.getEdges())
                win.conditions.createData(win, edges)
                if sig == 1:
                    tabMenu.insertTab(0, tabs[0]['widget'], tabs[0]['title'])
                    tabMenu.insertTab(1, tabs[1]['widget'], tabs[1]['title'])
                    tabMenu.insertTab(2, tabs[2]['widget'], tabs[2]['title'])
                    tabMenu.setCurrentIndex(1)
                elif sig == 2:
                    tabMenu.insertTab(0, tabs[0]['widget'], tabs[0]['title'])
                    tabMenu.insertTab(1, tabs[1]['widget'], tabs[1]['title'])
                    tabMenu.insertTab(4, tabs[4]['widget'], tabs[4]['title'])
                    tabMenu.setCurrentIndex(1)
                win.btnDoneGeometry.setEnabled(False)
                win.cmbConstructionBy.setEnabled(False)
                if win.cmbGeneralStudie.currentText() == "Stationary":
                    win.sectionStudySettings.setEnabled(False)
                elif win.cmbGeneralStudie.currentText() == "Time dependent":
                    win.sectionStudySettings.setEnabled(True)

    def addTabElement3(tabs, tabMenu):
        tabMenu.insertTab(0, tabs[0]['widget'], tabs[0]['title'])
        tabMenu.insertTab(1, tabs[1]['widget'], tabs[1]['title'])
        tabMenu.insertTab(2, tabs[2]['widget'], tabs[2]['title'])
        tabMenu.insertTab(3, tabs[3]['widget'], tabs[3]['title'])
        tabMenu.setCurrentIndex(2)

    def addTabElement4(tabs, tabMenu):
        tabMenu.insertTab(0, tabs[0]['widget'], tabs[0]['title'])
        tabMenu.insertTab(1, tabs[1]['widget'], tabs[1]['title'])
        tabMenu.insertTab(2, tabs[2]['widget'], tabs[2]['title'])
        tabMenu.insertTab(3, tabs[3]['widget'], tabs[3]['title'])
        tabMenu.insertTab(6, tabs[6]['widget'], tabs[6]['title'])
        tabMenu.setCurrentIndex(3)

    def addTabElement5(tabs, tabMenu):
        tabMenu.insertTab(0, tabs[0]['widget'], tabs[0]['title'])
        tabMenu.insertTab(1, tabs[1]['widget'], tabs[1]['title'])
        tabMenu.insertTab(4, tabs[4]['widget'], tabs[4]['title'])
        tabMenu.insertTab(5, tabs[5]['widget'], tabs[5]['title'])
        tabMenu.setCurrentIndex(2)

    def addTabElement6(tabs, tabMenu):
        tabMenu.insertTab(0, tabs[0]['widget'], tabs[0]['title'])
        tabMenu.insertTab(1, tabs[1]['widget'], tabs[1]['title'])
        tabMenu.insertTab(4, tabs[4]['widget'], tabs[4]['title'])
        tabMenu.insertTab(5, tabs[5]['widget'], tabs[5]['title'])
        tabMenu.insertTab(6, tabs[6]['widget'], tabs[6]['title'])
        tabMenu.setCurrentIndex(3)