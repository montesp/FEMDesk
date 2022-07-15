class Materials():
     def currentHeatConduction(comb, ar):
        
        if comb.currentIndex() == 0:
            ar[0].setEnabled(True)
            ar[1].setEnabled(False)
            ar[2].setEnabled(False)
            ar[3].setEnabled(False)
            ar[4].setEnabled(False)
        if comb.currentIndex() == 3:
            ar[0].setEnabled(False)
            ar[1].setEnabled(True)
            ar[2].setEnabled(True)
            ar[3].setEnabled(True)
            ar[4].setEnabled(True)