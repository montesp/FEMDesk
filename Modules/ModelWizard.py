from Modules.Tabs import *

class ModelWizard:
    def hideInitialTabs(tabs, tabMenu):
        Tabs.hideElementsTab(tabs, tabMenu)

    def currentTreeItem(item, indexTree, tabs, tabMenu):
        if item.text(indexTree) == "Heat Transfer":
            Tabs.addTabElement(tabs, tabMenu)
            Tabs.hideElementTab(1 , tabMenu)

        elif item.text(indexTree) == "Mathematics":
            Tabs.addTabElement(tabs , tabMenu )

