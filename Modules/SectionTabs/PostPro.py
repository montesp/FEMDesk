from Modules.Postprocesing.Global import resolverEq as motor
class PostPro():
    def click_btnResult(canvas):
        motor(canvas.nodes, canvas.tabl, canvas.bound)
