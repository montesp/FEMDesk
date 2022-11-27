from Modules.Postprocesing.Global import resolverEq as motor
class PostPro():
    def click_btnResult(canvas, datapost):
        motor(canvas.nodes, canvas.tabl, canvas.bound, datapost)
