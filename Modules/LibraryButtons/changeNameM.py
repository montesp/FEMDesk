from Base import *
#Poner descripcion 
class changeNameMaterials():
    def change_cmbNameMaterials(self):
        if self.cmbNameMaterials.currentIndex() != -1 :
            if self.materialsDataBase[self.cmbNameMaterials.currentIndex()][6] == 0:  #isotropic
                self.cmbTypeHeatConductionSolid.setCurrentIndex(0)
                self.edtTermalConductivityIsotropicProperties.setText(str(self.materialsDataBase[self.cmbNameMaterials.currentIndex()][2]))  
                self.edtTermalConductivityAnisotropicPropertiesA11.setText("")
                self.edtTermalConductivityAnisotropicPropertiesA12.setText("")
                self.edtTermalConductivityAnisotropicPropertiesA21.setText("")
                self.edtTermalConductivityAnisotropicPropertiesA22.setText("")    
                self.edtCpProperties.setText(str(self.materialsDataBase[self.cmbNameMaterials.currentIndex()][7]))
                self.edtRhoProperties.setText(str(self.materialsDataBase[self.cmbNameMaterials.currentIndex()][8]))
                dato = self.edtTermalConductivityIsotropicProperties.text()
                self.DataProperties.kappa[0][0] = float(dato)
                self.DataProperties.kappa[0][1] = -1.0
                self.DataProperties.kappa[1][0] = -1.0
                self.DataProperties.kappa[1][1] = -1.0
            elif self.materialsDataBase[self.cmbNameMaterials.currentIndex()][6] == 1 : #diagonal  
                self.cmbTypeHeatConductionSolid.setCurrentIndex(1)
                self.edtTermalConductivityIsotropicProperties.setText("")  
                self.edtTermalConductivityAnisotropicPropertiesA11.setText(str(self.materialsDataBase[self.cmbNameMaterials.currentIndex()][2]))
                self.edtTermalConductivityAnisotropicPropertiesA12.setText("0")
                self.edtTermalConductivityAnisotropicPropertiesA21.setText("0")
                self.edtTermalConductivityAnisotropicPropertiesA22.setText(str(self.materialsDataBase[self.cmbNameMaterials.currentIndex()][5]))    
                self.edtCpProperties.setText(str(self.materialsDataBase[self.cmbNameMaterials.currentIndex()][7]))
                self.edtRhoProperties.setText(str(self.materialsDataBase[self.cmbNameMaterials.currentIndex()][8]))
                dato = self.edtTermalConductivityAnisotropicPropertiesA11.text()
                self.DataProperties.kappa[0][0] = float(dato)
                self.DataProperties.kappa[0][1] = 0.0
                self.DataProperties.kappa[1][0] = 0.0
                dato = self.edtTermalConductivityAnisotropicPropertiesA22.text()
                self.DataProperties.kappa[1][1] = float(dato)
            elif self.materialsDataBase[self.cmbNameMaterials.currentIndex()][6] == 2 : #symmetric   
                self.cmbTypeHeatConductionSolid.setCurrentIndex(2)
                self.edtTermalConductivityIsotropicProperties.setText("")  
                self.edtTermalConductivityAnisotropicPropertiesA11.setText(str(self.materialsDataBase[self.cmbNameMaterials.currentIndex()][2]))
                self.edtTermalConductivityAnisotropicPropertiesA12.setText(str(self.materialsDataBase[self.cmbNameMaterials.currentIndex()][3]))
                self.edtTermalConductivityAnisotropicPropertiesA21.setText(str(self.materialsDataBase[self.cmbNameMaterials.currentIndex()][4]))
                self.edtTermalConductivityAnisotropicPropertiesA22.setText(str(self.materialsDataBase[self.cmbNameMaterials.currentIndex()][5]))
                dato = self.edtTermalConductivityAnisotropicPropertiesA11.text()
                self.DataProperties.kappa[0][0] = float(dato)
                dato = self.edtTermalConductivityAnisotropicPropertiesA12.text()
                self.DataProperties.kappa[0][1] = float(dato)
                self.DataProperties.kappa[1][0] = float(dato)
                dato = self.edtTermalConductivityAnisotropicPropertiesA22.text()
                self.DataProperties.kappa[1][1] = float(dato)
            elif self.materialsDataBase[self.cmbNameMaterials.currentIndex()][6] == 3 : #full
                self.cmbTypeHeatConductionSolid.setCurrentIndex(3)
                self.edtTermalConductivityIsotropicProperties.setText("")  
                self.edtTermalConductivityAnisotropicPropertiesA11.setText(str(self.materialsDataBase[self.cmbNameMaterials.currentIndex()][2]))
                self.edtTermalConductivityAnisotropicPropertiesA12.setText(str(self.materialsDataBase[self.cmbNameMaterials.currentIndex()][3]))
                self.edtTermalConductivityAnisotropicPropertiesA21.setText(str(self.materialsDataBase[self.cmbNameMaterials.currentIndex()][4]))
                self.edtTermalConductivityAnisotropicPropertiesA22.setText(str(self.materialsDataBase[self.cmbNameMaterials.currentIndex()][5]))
                dato = self.edtTermalConductivityAnisotropicPropertiesA11.text()
                self.DataProperties.kappa[0][0] = float(dato)
                dato = self.edtTermalConductivityAnisotropicPropertiesA12.text()
                self.DataProperties.kappa[0][1] = float(dato)
                dato = self.edtTermalConductivityAnisotropicPropertiesA21.text()
                self.DataProperties.kappa[1][0] = float(dato)
                dato = self.edtTermalConductivityAnisotropicPropertiesA22.text()
            self.edtCpProperties.setText(str(self.materialsDataBase[self.cmbNameMaterials.currentIndex()][7]))
            self.edtRhoProperties.setText(str(self.materialsDataBase[self.cmbNameMaterials.currentIndex()][8]))
            dato = self.edtRhoProperties.text()
            self.DataProperties.rho = float(dato)
            dato = self.edtCpProperties.text()
            self.DataProperties.Cp = float(dato)
            self.edtTermalConductivityIsotropicProperties.setEnabled(False)
            self.edtTermalConductivityAnisotropicPropertiesA11.setEnabled(False)
            self.edtTermalConductivityAnisotropicPropertiesA12.setEnabled(False)
            self.edtTermalConductivityAnisotropicPropertiesA21.setEnabled(False)
            self.edtTermalConductivityAnisotropicPropertiesA22.setEnabled(False)
            self.edtCpProperties.setEnabled(False)
            self.edtRhoProperties.setEnabled(False)
