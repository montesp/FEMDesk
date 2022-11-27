from Modules.Postprocesing.Global import resolverEq as motor
class PostPro():
    def click_btnResult(canvas, datapost):
        motor(canvas.nodes, canvas.bound, canvas.tabl, datapost)
        results = []
        file1 = open('u.txt', 'r')
        for line in file1:
            results.append(line.strip())
        file1.close()
        results = list(map(float, results))
        canvas.showMeshPost(results)