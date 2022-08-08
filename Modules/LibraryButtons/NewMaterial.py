class NewMaterial():
    def click_btnNewMaterial(self):
        self.cmbNameMaterials.setEnabled(False)
        self.edtNameMaterial.setEnabled(True)
        self.edtNameMaterial.setText("Material_Name")
        self.cmbTypeHeatConductionSolid.setEnabled(True)
        self.cmbTypeHeatConductionSolid.setCurrentIndex (0)
        self.edtTermalConductivityIsotropicProperties.setEnabled(True)
        self.edtTermalConductivityIsotropicProperties.setText("")
        self.edtRhoProperties.setEnabled(True)
        self.edtRhoProperties.setText("")
        self.edtCpProperties.setEnabled(True)
        self.edtCpProperties.setText("")
        self.btnNewMaterial.setEnabled(False)
        self.btnSaveMaterial.setEnabled(True)
        self.btnDeleteMaterial.setEnabled(False)
        self.btnSaveAsMaterial.setEnabled(False)
        self.btnOpenMaterial.setEnabled(False)
        self.btnResetLibrary.setEnabled(True)
        self.kappa = [[-1.0,-1.0],[-1.0,-1.0]]
        self.rho = -1.0
        self.Cp = -1.0
        self.statusLibrary = 1