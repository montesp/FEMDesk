from PyQt5.QtWidgets import QMessageBox
from Base import *

class SaveMaterial():
    def click_btnSaveMaterial(self):
        reviews = [0,0,0] #review each variable before saving
        reName = 0 #review material name

        dato = self.edtNameMaterial.text()
        if not (dato.isspace() or len(dato) == 0):
            mat = select_material(self.conn,dato)
            if len(mat) == 0:
                reName = 1
        
        if self.cmbTypeHeatConductionSolid.currentIndex() == 0 : #isotropic
            if self.DataProperties.kappa[0][0] != -1.0:
                reviews[0] = 1       
        elif self.cmbTypeHeatConductionSolid.currentIndex() == 1 : #diagonal
            if self.DataProperties.kappa[0][0] != -1.0 and self.DataProperties.kappa[1][1] != -1.0 :   
                reviews[0] = 1
        elif self.cmbTypeHeatConductionSolid.currentIndex() == 2 : #symmetric
            if self.DataProperties.kappa[0][0] != -1.0 and self.DataProperties.kappa[0][1] != -1.0 and self.DataProperties.kappa[1][0] != -1.0 and self.DataProperties.kappa[1][1] != -1.0:    
                reviews[0] = 1
        elif self.cmbTypeHeatConductionSolid.currentIndex() == 3 : #full
            if self.DataProperties.kappa[0][0] != -1.0 and self.DataProperties.kappa[0][1] != -1.0 and self.DataProperties.kappa[1][0] != -1.0 and self.DataProperties.kappa[1][1] != -1.0:    
                reviews[0] = 1

        if self.DataProperties.rho != -1.0:
            reviews[1] = 1 

        if self.DataProperties.Cp != -1.0:
            reviews[2] = 1 

        if self.statusLibrary == 1 :
            if sum(reviews) == 3 and reName == 1:
                material = (self.edtNameMaterial.text(),self.DataProperties.kappa[0][0],self.DataProperties.kappa[0][1],self.DataProperties.kappa[1][0],self.DataProperties.kappa[1][1],self.DataProperties.Cp,self.DataProperties.rho,self.cmbTypeHeatConductionSolid.currentIndex())
                add_material(self.conn, material)
                self.materialsDataBase = select_all_materials(self.conn)
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
                self.cmbTypeHeatConductionSolid.setEnabled(False)
                self.cmbTypeHeatConductionSolid.setCurrentIndex (0)
                self.edtTermalConductivityIsotropicProperties.setEnabled(False)
                self.edtTermalConductivityIsotropicProperties.setText("")
                self.edtTermalConductivityAnisotropicPropertiesA11.setEnabled(False)
                self.edtTermalConductivityAnisotropicPropertiesA12.setEnabled(False)
                self.edtTermalConductivityAnisotropicPropertiesA21.setEnabled(False)
                self.edtTermalConductivityAnisotropicPropertiesA22.setEnabled(False)
                self.edtTermalConductivityAnisotropicPropertiesA11.setText("")
                self.edtTermalConductivityAnisotropicPropertiesA12.setText("")
                self.edtTermalConductivityAnisotropicPropertiesA21.setText("")
                self.edtTermalConductivityAnisotropicPropertiesA22.setText("")
                self.edtRhoProperties.setEnabled(False)
                self.edtRhoProperties.setText("")
                self.edtCpProperties.setEnabled(False)
                self.edtCpProperties.setText("")
                self.addMaterials()
                QMessageBox.information(self, "Important message", "Material registered in the database")               
            else:
                QMessageBox.critical(self, "Important message", "Null values ​​exist, please check")
        elif self.statusLibrary == 2:
            if reName == 1:
                material = (self.edtNameMaterial.text(),self.DataProperties.kappa[0][0],self.DataProperties.kappa[0][1],self.DataProperties.kappa[1][0],self.DataProperties.kappa[1][1],self.DataProperties.Cp,self.DataProperties.rho,self.cmbTypeHeatConductionSolid.currentIndex())
                add_material(self.conn, material)
                self.materialsDataBase = select_all_materials(self.conn)
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
                self.cmbTypeHeatConductionSolid.setEnabled(False)
                self.cmbTypeHeatConductionSolid.setCurrentIndex (0)
                self.edtTermalConductivityIsotropicProperties.setEnabled(False)
                self.edtTermalConductivityIsotropicProperties.setText("")
                self.edtTermalConductivityAnisotropicPropertiesA11.setEnabled(False)
                self.edtTermalConductivityAnisotropicPropertiesA12.setEnabled(False)
                self.edtTermalConductivityAnisotropicPropertiesA21.setEnabled(False)
                self.edtTermalConductivityAnisotropicPropertiesA22.setEnabled(False)
                self.edtTermalConductivityAnisotropicPropertiesA11.setText("")
                self.edtTermalConductivityAnisotropicPropertiesA12.setText("")
                self.edtTermalConductivityAnisotropicPropertiesA21.setText("")
                self.edtTermalConductivityAnisotropicPropertiesA22.setText("")
                self.edtRhoProperties.setEnabled(False)
                self.edtRhoProperties.setText("")
                self.edtCpProperties.setEnabled(False)
                self.edtCpProperties.setText("")
                self.addMaterials()
                QMessageBox.information(self, "Important message", "Material registered in the database")
            else:
                QMessageBox.critical(self, "Important message", "Null values ​​exist, please check")
        elif self.statusLibrary == 3 :
            if sum(reviews) == 3 :
                # display(self.materialsDataBase[self.cmbNameMaterials.currentIndex()][0])
                material = (self.edtNameMaterial.text(),self.DataProperties.kappa[0][0],self.DataProperties.kappa[0][1],self.DataProperties.kappa[1][0],self.DataProperties.kappa[1][1],self.DataProperties.Cp,self.DataProperties.rho,self.cmbTypeHeatConductionSolid.currentIndex(),self.materialsDataBase[self.cmbNameMaterials.currentIndex()][0])
                update_material(self.conn, material)
                self.materialsDataBase = select_all_materials(self.conn)
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
                self.cmbTypeHeatConductionSolid.setEnabled(False)
                self.cmbTypeHeatConductionSolid.setCurrentIndex(0)
                self.edtTermalConductivityIsotropicProperties.setEnabled(False)
                self.edtTermalConductivityIsotropicProperties.setText("")
                self.edtTermalConductivityAnisotropicPropertiesA11.setEnabled(False)
                self.edtTermalConductivityAnisotropicPropertiesA12.setEnabled(False)
                self.edtTermalConductivityAnisotropicPropertiesA21.setEnabled(False)
                self.edtTermalConductivityAnisotropicPropertiesA22.setEnabled(False)
                self.edtTermalConductivityAnisotropicPropertiesA11.setText("")
                self.edtTermalConductivityAnisotropicPropertiesA12.setText("")
                self.edtTermalConductivityAnisotropicPropertiesA21.setText("")
                self.edtTermalConductivityAnisotropicPropertiesA22.setText("")
                self.edtRhoProperties.setEnabled(False)
                self.edtRhoProperties.setText("")
                self.edtCpProperties.setEnabled(False)
                self.edtCpProperties.setText("")
                self.addMaterials()
                QMessageBox.information(self, "Important message", "material registered in the database")               
            else:
                QMessageBox.critical(self, "Important message", "Null values ​​exist, please check")    
        self.statusLibrary = 0