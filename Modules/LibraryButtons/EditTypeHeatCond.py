from PyQt5.QtWidgets import QMessageBox
from Base import *

class TypeHeatConductionSolid():
 def change_cmbTypeHeatConductionSolid(self):
        if self.cmbTypeHeatConductionSolid.currentIndex() == 0 : #isotropic
            self.edtTermalConductivityIsotropicProperties.setEnabled(True)
            self.edtTermalConductivityIsotropicProperties.setText("")
            self.edtTermalConductivityAnisotropicPropertiesA11.setEnabled(False)
            self.edtTermalConductivityAnisotropicPropertiesA11.setText("")
            self.edtTermalConductivityAnisotropicPropertiesA12.setEnabled(False)
            self.edtTermalConductivityAnisotropicPropertiesA12.setText("")
            self.edtTermalConductivityAnisotropicPropertiesA21.setEnabled(False)
            self.edtTermalConductivityAnisotropicPropertiesA21.setText("")
            self.edtTermalConductivityAnisotropicPropertiesA22.setEnabled(False)
            self.edtTermalConductivityAnisotropicPropertiesA22.setText("")
        elif self.cmbTypeHeatConductionSolid.currentIndex() == 1 : #diagonal
            self.edtTermalConductivityIsotropicProperties.setEnabled(False)
            self.edtTermalConductivityIsotropicProperties.setText("")
            self.edtTermalConductivityAnisotropicPropertiesA11.setEnabled(True)
            self.edtTermalConductivityAnisotropicPropertiesA11.setText("")
            self.edtTermalConductivityAnisotropicPropertiesA12.setEnabled(False)
            self.edtTermalConductivityAnisotropicPropertiesA12.setText("0")
            self.edtTermalConductivityAnisotropicPropertiesA21.setEnabled(False)
            self.edtTermalConductivityAnisotropicPropertiesA21.setText("0")
            self.edtTermalConductivityAnisotropicPropertiesA22.setEnabled(True)
            self.edtTermalConductivityAnisotropicPropertiesA22.setText("")
        elif self.cmbTypeHeatConductionSolid.currentIndex() == 2 : #symmetric
            self.edtTermalConductivityIsotropicProperties.setEnabled(False)
            self.edtTermalConductivityIsotropicProperties.setText("")
            self.edtTermalConductivityAnisotropicPropertiesA11.setEnabled(True)
            self.edtTermalConductivityAnisotropicPropertiesA11.setText("")
            self.edtTermalConductivityAnisotropicPropertiesA12.setEnabled(True)
            self.edtTermalConductivityAnisotropicPropertiesA12.setText("")
            self.edtTermalConductivityAnisotropicPropertiesA21.setEnabled(False)
            self.edtTermalConductivityAnisotropicPropertiesA21.setText("")
            self.edtTermalConductivityAnisotropicPropertiesA22.setEnabled(True)
            self.edtTermalConductivityAnisotropicPropertiesA22.setText("")
        elif self.cmbTypeHeatConductionSolid.currentIndex() == 3 : #full
            self.edtTermalConductivityIsotropicProperties.setEnabled(False)
            self.edtTermalConductivityIsotropicProperties.setText("")
            self.edtTermalConductivityAnisotropicPropertiesA11.setEnabled(True)
            self.edtTermalConductivityAnisotropicPropertiesA11.setText("")
            self.edtTermalConductivityAnisotropicPropertiesA12.setEnabled(True)
            self.edtTermalConductivityAnisotropicPropertiesA12.setText("")
            self.edtTermalConductivityAnisotropicPropertiesA21.setEnabled(True)
            self.edtTermalConductivityAnisotropicPropertiesA21.setText("")
            self.edtTermalConductivityAnisotropicPropertiesA22.setEnabled(True)
            self.edtTermalConductivityAnisotropicPropertiesA22.setText("")

 def exit_edtTermalConductivityIsotropicProperties(self):
        dato = self.edtTermalConductivityIsotropicProperties.text()
        if not (dato.isspace() or len(dato) ==0):
            if float(dato) >= 0:
                self.DataProperties.kappa[0][0] = float(dato)
                self.DataProperties.kappa[0][1] = -1.0
                self.DataProperties.kappa[1][0] = -1.0
                self.DataProperties.kappa[1][1] = -1.0
            else:
                QMessageBox.critical(self, "Important message", "The value must be greater than or equal to zero")
                self.edtTermalConductivityIsotropicProperties.setText("")

 def exit_edtTermalConductivityAnisotropicPropertiesA11(self):
        dato = self.edtTermalConductivityAnisotropicPropertiesA11.text()
        if not (dato.isspace() or len(dato) ==0):
            if float(dato) >= 0:
                self.DataProperties.kappa[0][0] = float(dato)
                if self.cmbTypeHeatConductionSolid.currentIndex () == 1 : #diagonal
                    self.DataProperties.kappa[0][1] = 0.0
                    self.DataProperties.kappa[1][0] = 0.0
            else:
                QMessageBox.critical(self, "Important message", "The value must be greater than or equal to zero")
                self.edtTermalConductivityAnisotropicPropertiesA11.setText("")

 def exit_edtTermalConductivityAnisotropicPropertiesA12(self):
        dato = self.edtTermalConductivityAnisotropicPropertiesA12.text()
        if not (dato.isspace() or len(dato) ==0):
            if float(dato) >= 0:
                self.DataProperties.kappa[0][1] = float(dato)
                if self.cmbTypeHeatConductionSolid.currentIndex () == 2 : #symmetric
                    self.DataProperties.kappa[1][0] = float(dato)
                    self.edtTermalConductivityAnisotropicPropertiesA21.setText(dato)
            else:
                QMessageBox.critical(self, "Important message", "The value must be greater than or equal to zero")
                self.edtTermalConductivityAnisotropicPropertiesA12.setText("")


 def exit_edtTermalConductivityAnisotropicPropertiesA21(self):
        dato = self.edtTermalConductivityAnisotropicPropertiesA21.text()
        if not (dato.isspace() or len(dato) ==0):
            if float(dato) >= 0:
                self.DataProperties.kappa[1][0] = float(dato)
            else:
                QMessageBox.critical(self, "Important message", "The value must be greater than or equal to zero")
                self.edtTermalConductivityAnisotropicPropertiesA21.setText("")

 def exit_edtTermalConductivityAnisotropicPropertiesA22(self):
        dato = self.edtTermalConductivityAnisotropicPropertiesA22.text()
        if not (dato.isspace() or len(dato) ==0):
            if float(dato) >= 0:
                self.DataProperties.kappa[1][1] = float(dato)
                if self.cmbTypeHeatConductionSolid.currentIndex () == 1 : #diagonal
                    self.DataProperties.kappa[0][1] = 0.0
                    self.DataProperties.kappa[1][0] = 0.0   
            else:
                QMessageBox.critical(self, "Important message", "The value must be greater than or equal to zero")
                self.edtTermalConductivityAnisotropicPropertiesA22.setText("")

 def exit_edtRhoProperties(self):
        dato = self.edtRhoProperties.text()
        if not (dato.isspace() or len(dato) ==0):
            if float(dato) > 0:
                self.DataProperties.rho = float(dato)
            else:
                QMessageBox.critical(self, "Important message", "The value must be greater than zero")
                self.edtRhoProperties.setText("")  

 def exit_edtCpProperties(self) :
        dato = self.edtCpProperties.text()
        if not (dato.isspace() or len(dato) ==0):
            if float(dato) > 0:
                self.DataProperties.Cp = float(dato)
            else:
                QMessageBox.critical(self, "Important message", "The value must be greater than zero")
                self.edtCpProperties.setText("")      
