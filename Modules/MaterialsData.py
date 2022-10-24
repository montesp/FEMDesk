
class MaterialsData:
    def __init__(self):
        self.__figureIndex = 0
        self.__thermalConductivity = []
        self.__density = 0
        self.__heatCapacity = 0
        self.__heatConvection = []
        self.__material = ""
        self.__headConductionType = ""

    def getFigureIndex(self):
        return self.__figureIndex

    def setFigureIndex(self, figureIndex):
        self.__figureIndex = figureIndex

    def getThermalConductivity(self):
        return self.__thermalConductivity

    def setThermalConductivity(self, thermalConductivity):
        self.__thermalConductivity = thermalConductivity

    def getDensity(self):
        return self.__density

    def setDensity(self, density):
        self.__density = density

    def getHeatCapacity(self):
        return self.__heatCapacity

    def setHeatCapacity(self, heatCapacity):
        self.__heatCapacity = heatCapacity

    def getHeatConvection(self):
        return self.__heatConvection

    def setHeatConvection(self, heatConvection):
        self.__heatConvection = heatConvection

    def getMaterial(self):
        return self.__material

    def setMaterial(self, material):
        self.__material = material

    def getHeadConductionType(self):
        return self.__headConductionType

    def setHeadConductionType(self):
        self.__headConductionType


