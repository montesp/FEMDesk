from PyQt5.QtWidgets import QMessageBox

class MeshSettings():
    def __init__(self):
        self.meshSettingsData = []

    def currentShowMeshTab(self, text, win):
        if(text == "Mesh and Setting Study"):
            win.show()
            win.setEnabled(True)
        else:
            win.hide()
            win.setEnabled(False)

    def completeDataStudiesValue(self, win):
        meshAndSettingStudy = win.toolBoxMeshAndSettingStudy

        try:
            unit = win.cmbTypeUnit.currentText()
            start = float(win.lEditStart.text())
            step = float(win.lEditStep.text())
            stop = float(win.lEditStop.text())
            meshAndSettingStudy.setItemEnabled(1, True)
            
            # Si la informacion ya existe, la vuelve a escribir
            if self.meshSettingsData:
                print("Ya existe informacion")
                self.meshSettingsData = []
                self.meshSettingsData.append({'unit':unit, 'start':start, 'step':step, 'stop':stop})
            else:
                print("No existen datos")
                self.meshSettingsData.append({'unit':unit, 'start':start, 'step':step, 'stop':stop})

        except:
            QMessageBox.warning(win, "Important message", "You can only enter numeric values")
        
    def showMeshData(self):
        print(self.meshSettingsData)