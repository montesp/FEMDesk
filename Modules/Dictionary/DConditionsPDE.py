

domainsConditions = {
    'domain' : 0,
}

coordinates = {
    'coordinateDirichlet': 0,
    'coordinateBoundary' : [0] * 2,
}

def DC00(elements):
            for i in range(len(elements)):
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


#Index Alpha-----------------------------------------------------

def IndexA00(ax, ay):
        for i in range(len(ax)):
            if i > 0:
                ax[i].setEnabled(False)
                ay[i].setEnabled(False)
def IndexA01(ax, ay):
            IndexA00(ax, ay)
            ax[1].setEnabled(True)
            ay[1].setEnabled(True)
def IndexA02(ax, ay):
            IndexA00(ax, ay)
            ax[1].setEnabled(True)
            ay[1].setEnabled(True)
            ax[2].setEnabled(True)
            ay[2].setEnabled(True)
def IndexA10(ax, ay):
            IndexA00(ax, ay)
            ax[3].setEnabled(True)
            ay[3].setEnabled(True)
def IndexA11(ax, ay):
            IndexA00(ax, ay)
            ax[1].setEnabled(True)
            ay[1].setEnabled(True)
            ax[3].setEnabled(True)
            ay[3].setEnabled(True)
            ax[4].setEnabled(True)
            ay[4].setEnabled(True)  
def IndexA12(ax, ay):
            IndexA00(ax, ay)
            for i in range(6):
             if i > 0:
                ax[i].setEnabled(True)
                ay[i].setEnabled(True)
def IndexA20(ax, ay):
            IndexA00(ax, ay)
            ax[3].setEnabled(True)
            ay[3].setEnabled(True)
            ax[6].setEnabled(True)
            ay[6].setEnabled(True)
def IndexA21(ax, ay):
            IndexA00(ax, ay)
            ax[1].setEnabled(True)
            ay[1].setEnabled(True)
            ax[3].setEnabled(True)
            ay[3].setEnabled(True)
            ax[4].setEnabled(True)
            ay[4].setEnabled(True)
            ax[6].setEnabled(True)
            ay[6].setEnabled(True)
            ax[7].setEnabled(True)
            ay[7].setEnabled(True)
def IndexA22(ax, ay):
            for i in range(len(ax)):
             if i > 0:
                ax[i].setEnabled(True)
                ay[i].setEnabled(True)