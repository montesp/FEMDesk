import numpy as np
def deri(triangle, values):
    dxdy = []
    val = [np.random.randint(100), np.random.randint(100), np.random.randint(100)]
    dividendo = triangle[0][0]*triangle[1][1] - triangle[1][0]*triangle[0][1] - triangle[0][0]*triangle[2][1] + triangle[2][0]*triangle[0][1] + triangle[1][0]*triangle[2][1] - triangle[2][0]*triangle[1][1]

    dy = val[0]*triangle[1][1] - val[1]*triangle[0][1] - val[0]*triangle[2][1] + val[2]*triangle[0][1] + val[1]*triangle[2][1] - val[2]*triangle[1][1]
    dx = val[0]*triangle[1][0] - val[1]*triangle[0][0] - val[0]*triangle[2][0] + val[2]*triangle[0][0] + val[1]*triangle[2][0] - val[2]*triangle[1][0]

    dy = dy / dividendo
    dx = dx / dividendo

    dxdy.append([dx,dy])
    return dxdy
