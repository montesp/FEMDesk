class SaveAsMaterial():
    def click_btnSaveAsMaterial(self):
        self.btnNewMaterial.setEnabled(False)
        self.btnDeleteMaterial.setEnabled(False)
        self.btnSaveMaterial.setEnabled(True)
        self.btnSaveAsMaterial.setEnabled(False)
        self.btnOpenMaterial.setEnabled(False)
        self.btnResetLibrary.setEnabled(True)
        self.btnHelpLibrary.setEnabled(True)
        self.cmbNameMaterials.setEnabled(False)
        self.edtNameMaterial.setEnabled(True)
        self.edtNameMaterial.setText("Copy"+self.cmbNameMaterials.currentText())
        self.statusLibrary = 2