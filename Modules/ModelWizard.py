from Modules.Tabs import *

class ModelWizard:
    def hideInitialTabs(tabs, tabMenu):
        Tabs.hideElementsTab(tabs, tabMenu)

    def currentTreeItem(self, item, indexTree, tabs, tabMenu):
        if item.text(indexTree) == "Heat Transfer":
            Tabs.addTabElement(tabs, tabMenu)
            Tabs.hideElementTab(1 , tabMenu)
            self.cmbGeneralStudie.hide()
            self.lblGeneralStudie.hide()
            self.tboxModelWizard.hide()

        elif item.text(indexTree) == "Mathematics":
            Tabs.addTabElement(tabs , tabMenu )
            self.cmbGeneralStudie.show()
            self.lblGeneralStudie.show()
            self.tboxModelWizard.show()

    

