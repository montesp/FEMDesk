class Conditions():
    def currentTypeCondition(comb, tbox): 
        tbox.widget(0).hide()
        tbox.setItemEnabled(0, False)
        tbox.widget(1).hide()
        tbox.setItemEnabled(1, False)
         

        if comb.currentIndex() == 1:
            tbox.setItemEnabled(0, True)
            tbox.widget(0).show()
        if comb.currentIndex() == 2:
            tbox.setItemEnabled(1, True)
            tbox.widget(1).show()