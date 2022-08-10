class Tabs:
    def hideElementTab(index, tabMenu):
        tabMenu.removeTab(index)
    def addTabElement(index, tabs, tabMenu):
        tabMenu.insertTab(index, tabs[index], 'Nuevo')