
class UpdateData:
 def findCurrentInputMode(self, matrix):
    positionMatrix = matrix[self.cmbRowDiffusionCoef.currentIndex()][self.cmbColumnDiffusionCoef.currentIndex()]
    if positionMatrix == 'None' or positionMatrix == '':
        floatMatrix = 0
    else:
        positionMatrix = positionMatrix.replace(" ", "")
        positionMatrix = positionMatrix.strip('[]')
        positionMatrix = positionMatrix.split(',')
        floatMatrix = ['{0:g}'.format(float(i)) for i in positionMatrix]
        floatMatrix = int(floatMatrix[4])
    return floatMatrix

 def setInputSingle(self, floatMatrix, diffusionMatrix):
    self.cmbDiffusionCoef.setCurrentIndex(floatMatrix)   
    if diffusionMatrix[self.cmbRowDiffusionCoef.currentIndex()][self.cmbColumnDiffusionCoef.currentIndex()] == 'None' or diffusionMatrix[self.cmbRowDiffusionCoef.currentIndex()][self.cmbColumnDiffusionCoef.currentIndex()] == '':
     self.lEditDiffusionCoef.setText("")
    else: 
     strCell = diffusionMatrix[self.cmbRowDiffusionCoef.currentIndex()][self.cmbColumnDiffusionCoef.currentIndex()]
     strCell = strCell.strip("[]")
     strCell = strCell.split(',')
     floatCell = ['{0:g}'.format(float(i)) for i in strCell]
     self.lEditDiffusionCoef.setText(floatCell[0])

 def setInputDiagonal(self, floatMatrix, diffusionMatrix):
    self.cmbDiffusionCoef.setCurrentIndex(floatMatrix)   
    if diffusionMatrix[self.cmbRowDiffusionCoef.currentIndex()][self.cmbColumnDiffusionCoef.currentIndex()] == 'None' or diffusionMatrix[self.cmbRowDiffusionCoef.currentIndex()][self.cmbColumnDiffusionCoef.currentIndex()] == '':
      self.lEditDiffusionCoef11.setText("")
      self.lEditDiffusionCoef22.setText("")
    else:  
      strCell = diffusionMatrix[self.cmbRowDiffusionCoef.currentIndex()][self.cmbColumnDiffusionCoef.currentIndex()]
      strCell = strCell.strip("[]")
      strCell = strCell.split(',')
      floatCell = ['{0:g}'.format(float(i)) for i in strCell]
      self.lEditDiffusionCoef11.setText(floatCell[0])
      self.lEditDiffusionCoef22.setText(floatCell[3])

 def setInputSimmetryOrFull(self, floatMatrix, diffusionMatrix):
    self.cmbDiffusionCoef.setCurrentIndex(floatMatrix)  
    if diffusionMatrix[self.cmbRowDiffusionCoef.currentIndex()][self.cmbColumnDiffusionCoef.currentIndex()] == 'None' or diffusionMatrix[self.cmbRowDiffusionCoef.currentIndex()][self.cmbColumnDiffusionCoef.currentIndex()] == '':
      self.lEditDiffusionCoef11.setText("")
      self.lEditDiffusionCoef12.setText("")
      self.lEditDiffusionCoef21.setText("")
      self.lEditDiffusionCoef22.setText("")
    else:
      strCell = diffusionMatrix[self.cmbRowDiffusionCoef.currentIndex()][self.cmbColumnDiffusionCoef.currentIndex()]
      strCell = strCell.strip("[]")
      strCell = strCell.split(',')
      floatCell = ['{0:g}'.format(float(i)) for i in strCell]
      self.lEditDiffusionCoef11.setText(floatCell[0])
      self.lEditDiffusionCoef12.setText(floatCell[1])
      self.lEditDiffusionCoef21.setText(floatCell[2])
      self.lEditDiffusionCoef22.setText(floatCell[3])

 def setCurrentSingleData(self, coordinate, label):
    if coordinate == 'None' or coordinate == '':
        label.setText("")
    else:
        label.setText(str(coordinate))

 def setCurrentDoubleData(self, coordinate, label, label2):
    if coordinate == 'None' or coordinate == '':
        label.setText("")
        label2.setText("")
    else:
        strCell = coordinate
        strCell = strCell.strip("[]")
        strCell = strCell.split(',')
        label.setText(strCell[0])
        label2.setText(strCell[1])

 def setCurrentCoordinateConfig(self, coordinate, comb):
        strComb = coordinate
        strComb = strComb.strip("[]")
        strComb = strComb.split(',')
        intComb = [int(i) for i in strComb]
        print("Cordenada Diffusion")
        print(intComb)
        if len(intComb) == 1:
            comb[0].setCurrentIndex(intComb[0])
        else:    
            comb[0].setCurrentIndex(intComb[0])
            comb[1].setCurrentIndex(intComb[1])