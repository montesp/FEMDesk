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
