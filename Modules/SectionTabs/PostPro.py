from Modules.Postprocesing.Global import resolverEq as motor
class PostPro():
    def click_btnResult(canvas, datapost):
        motor(canvas.nodes, canvas.bound, canvas.tabl, datapost)
        temp = []
        file1 = open('u.txt', 'r')
        for line in file1:
            temp.append(line.strip())
        file1.close()
        temp = list(map(float, temp))

        gradTx = []
        file1 = open('ux.txt', 'r')
        for line in file1:
            gradTx.append(line.strip())
        file1.close()
        gradTx = list(map(float, gradTx))

        gradTy = []
        file1 = open('ux.txt', 'r')
        for line in file1:
            gradTy.append(line.strip())
        file1.close()
        gradTy = list(map(float, gradTy))

        qx = []
        file1 = open('ux.txt', 'r')
        for line in file1:
            qx.append(line.strip())
        file1.close()
        qx = list(map(float, qx))

        qy = []
        file1 = open('ux.txt', 'r')
        for line in file1:
            qy.append(line.strip())
        file1.close()
        qy = list(map(float, qy))

        print("temp", temp)
        print("gradtx", gradTx)
        print("gradty", gradTy)
        print("qx", qx)
        print("qy", qy)

        canvas.showMeshPost(temp)