class OpenMaterial():
    def click_btnOpenMaterial(self):
        self.btnNewMaterial.setEnabled(False)
        self.btnDeleteMaterial.setEnabled(False)
        self.btnSaveMaterial.setEnabled(True)
        self.btnSaveAsMaterial.setEnabled(False)
        self.btnOpenMaterial.setEnabled(False)
        self.btnResetLibrary.setEnabled(True)
        self.btnHelpLibrary.setEnabled(True)
        self.cmbNameMaterials.setEnabled(False)
        self.edtNameMaterial.setEnabled(False)
        self.edtNameMaterial.setText(self.cmbNameMaterials.currentText())
        self.cmbTypeHeatConductionSolid.setEnabled(True)

        if self.cmbTypeHeatConductionSolid.currentIndex() == 0 : #isotropic
            self.edtTermalConductivityIsotropicProperties.setEnabled(True)
            self.edtTermalConductivityAnisotropicPropertiesA11.setEnabled(False)
            self.edtTermalConductivityAnisotropicPropertiesA12.setEnabled(False)
            self.edtTermalConductivityAnisotropicPropertiesA21.setEnabled(False)
            self.edtTermalConductivityAnisotropicPropertiesA22.setEnabled(False)                  
        elif self.cmbTypeHeatConductionSolid.currentIndex() == 1 : #diagonal
            self.edtTermalConductivityIsotropicProperties.setEnabled(False)
            self.edtTermalConductivityAnisotropicPropertiesA11.setEnabled(True)
            self.edtTermalConductivityAnisotropicPropertiesA12.setEnabled(False)
            self.edtTermalConductivityAnisotropicPropertiesA21.setEnabled(False)
            self.edtTermalConductivityAnisotropicPropertiesA22.setEnabled(True)
        elif self.cmbTypeHeatConductionSolid.currentIndex() == 2 : #symmetric
            self.edtTermalConductivityIsotropicProperties.setEnabled(False)
            self.edtTermalConductivityAnisotropicPropertiesA11.setEnabled(True)
            self.edtTermalConductivityAnisotropicPropertiesA12.setEnabled(True)
            self.edtTermalConductivityAnisotropicPropertiesA21.setEnabled(False)
            self.edtTermalConductivityAnisotropicPropertiesA22.setEnabled(True)
        elif self.cmbTypeHeatConductionSolid.currentIndex() == 3 : #full
            self.edtTermalConductivityIsotropicProperties.setEnabled(True)
            self.edtTermalConductivityAnisotropicPropertiesA11.setEnabled(True)
            self.edtTermalConductivityAnisotropicPropertiesA12.setEnabled(True)
            self.edtTermalConductivityAnisotropicPropertiesA21.setEnabled(True)
            self.edtTermalConductivityAnisotropicPropertiesA22.setEnabled(True)
        self.edtCpProperties.setEnabled(True)
        self.edtRhoProperties.setEnabled(True)         
        self.statusLibrary = 3