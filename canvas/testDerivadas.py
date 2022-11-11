import numpy as np
def deri(coord):
    dxdy = []
    val = [np.random.randint(100), np.random.randint(100), np.random.randint(100)]
    dividendo = coord[0][0]*coord[1][1] - coord[1][0]*coord[0][1] - coord[0][0]*coord[2][1] + coord[2][0]*coord[0][1] + coord[1][0]*coord[2][1] - coord[2][0]*coord[1][1]

    dy = val[0]*coord[1][1] - val[1]*coord[0][1] - val[0]*coord[2][1] + val[2]*coord[0][1] + val[1]*coord[2][1] - val[2]*coord[1][1]
    dx = val[0]*coord[1][0] - val[1]*coord[0][0] - val[0]*coord[2][0] + val[2]*coord[0][0] + val[1]*coord[2][0] - val[2]*coord[1][0]

    dy = dy / dividendo
    dx = dx / dividendo

    dxdy.append([dx,dy])
    return dxdy

