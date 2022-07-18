

def DC00(elements):
            for i, item in enumerate(elements):
                if i > 0:
                    elements[i].setEnabled(False)
def DC01(elements):
            DC00(elements)
            elements[1].setEnabled(True)
def DC02(elements):
            DC00(elements)
            elements[1].setEnabled(True)
            elements[2].setEnabled(True)   
def DC10(elements):
            DC00(elements)
            elements[3].setEnabled(True)
def DC11(elements):
            DC00(elements)
            elements[1].setEnabled(True)
            elements[3].setEnabled(True)
            elements[4].setEnabled(True)        
def DC12(elements):
            DC00(elements)
            elements[1].setEnabled(True)
            elements[2].setEnabled(True)
            elements[3].setEnabled(True)
            elements[4].setEnabled(True)
            elements[5].setEnabled(True)
def DC20(elements):
            DC00(elements)
            elements[3].setEnabled(True)
            elements[6].setEnabled(True)
def DC21(elements):
            DC00(elements)
            elements[1].setEnabled(True)
            elements[3].setEnabled(True)
            elements[4].setEnabled(True)
            elements[6].setEnabled(True)
            elements[7].setEnabled(True)
def DC22(elements):
            for i, item in enumerate(elements):
                if i > 0:
                    elements[i].setEnabled(True)