from Modules.Tabs import *

class ModelWizard:
    def currentTreeItem(item, indexTree, tabs, tabMenu):
        if item.text(indexTree) == "Heat Transfer":
            for i in range(len(tabs)):
                if i != 0:
                    print(i)
                    Tabs.hideElementTab(i, tabMenu)
        elif item.text(indexTree) == "Mathematics":
             for i in range(len(tabs)):
                if i != 0:
                    Tabs.addTabElement( i , tabs , tabMenu )

