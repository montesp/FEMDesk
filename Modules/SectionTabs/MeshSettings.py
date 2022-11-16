class MeshSettings():
    def currentShowMeshTab(text, win):
        if(text == "Mesh and Setting Study"):
            win.show()
            win.setEnabled(True)
        else:
            win.hide()
            win.setEnabled(False)