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

    def addTabElement2(tabs, tabMenu, sig):
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

    def addTabElement3(tabs, tabMenu):
        tabMenu.insertTab(0, tabs[0]['widget'], tabs[0]['title'])
        tabMenu.insertTab(1, tabs[1]['widget'], tabs[1]['title'])
        tabMenu.insertTab(2, tabs[2]['widget'], tabs[2]['title'])
        tabMenu.insertTab(3, tabs[3]['widget'], tabs[3]['title'])
        tabMenu.setCurrentIndex(2)