class Geometry():
    def currentCheckedComboBoxItem(section, comb):
        for i in range(section.count()):
            section.widget(i).hide()
            section.setItemEnabled(i, False)
        if comb.currentIndex() <= 4:
            section.setItemEnabled(comb.currentIndex(), True)
            section.widget(comb.currentIndex()).show()