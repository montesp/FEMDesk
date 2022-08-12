class Geometry():
    def currentCheckedComboBoxItem(section, comb, array):
        section.show()

        for i in range(section.count()):
            section.removeItem(section.currentIndex())

        if comb.currentIndex() <= 4:
            section.insertItem(0, array[comb.currentIndex()], str(comb.currentText()))
            #array[comb.currentIndex()].move(10,100)
            #section.setItemEnabled(comb.currentIndex(), True)
            #section.widget(comb.currentIndex()).show()#