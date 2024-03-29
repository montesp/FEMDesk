class ResetLibrary():
    def click_btnResetLibrary(self):
        self.btnNewMaterial.setEnabled(True)
        self.btnDeleteMaterial.setEnabled(True)
        self.btnSaveMaterial.setEnabled(False)
        self.btnSaveAsMaterial.setEnabled(True)
        self.btnOpenMaterial.setEnabled(True)
        self.btnResetLibrary.setEnabled(False)
        self.btnHelpLibrary.setEnabled(True)
        self.cmbNameMaterials.setEnabled(True)
        self.edtNameMaterial.setEnabled(False)
        self.edtNameMaterial.setText("")
        self.cmbTypeHeatConductionSolid.setCurrentIndex (0)
        self.edtTermalConductivityIsotropicProperties.setEnabled(False)
        self.edtTermalConductivityIsotropicProperties.setText("")
        self.edtRhoProperties.setEnabled(False)
        self.edtRhoProperties.setText("")
        self.edtCpProperties.setEnabled(False)
        self.edtCpProperties.setText("")
        self.addMaterials()