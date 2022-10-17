import calfem.core as cfc
import calfem.utils as cfu
from cmath import log
from ctypes import sizeof
import itertools
from functools import cmp_to_key
import math
from operator import length_hint

import sys
import PyQt5
import numpy as np
from PyQt5.QtCore import QEvent, QPointF, QLineF, QRectF, QRegExp, Qt, QRect
from PyQt5.QtGui import QPen, QColor, QBrush, QPolygonF, QFont, QRegExpValidator
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QFileDialog, QGraphicsScene, \
    QGraphicsItem, QGraphicsPolygonItem, QToolButton, QLabel, \
    QGraphicsEllipseItem, QLineEdit, QFormLayout, QGraphicsLineItem, QGraphicsTextItem, QGridLayout, QPushButton, QGraphicsItem, QGraphicsView, \
    QVBoxLayout, QMessageBox, QSlider

import random

import matplotlib as mpl
mpl.use('Qt5Agg')

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

import geometry as cfg
import mesh as cfm
import vis_mpl as cfv

setattr(cfg.Geometry, "marker_dict", None)
setattr(QGraphicsEllipseItem, "marker", None)
setattr(QGraphicsEllipseItem, "localIndex", None)
setattr(QGraphicsLineItem, "localIndex", None)


kx1 = 100
ky1 = 100
t = 1.0

# Gauss points or integration points

n = 2
ep = [t, n]

D = np.matrix([
    [kx1, 0.],
    [0., ky1]
])

g = cfg.Geometry()  # Create a GeoData object that holds the geometry.

g.point([0, 0]) #0
g.point([2, 0]) #1
g.point([2, 1]) #2
g.point([0, 1]) #3

g.point([0.5, 0.2]) #4
g.point([0.9, 0.2]) #5
g.point([1.8, 0.8]) #6
g.point([1.0, 0.9]) #7
g.point([0.5, 0.5]) #8

id_hole1 = 50
id_outer = 80

g.spline([4, 6, 7, 8, 4], marker=id_hole1)

g.spline([0, 1], marker=id_outer)
g.spline([2, 1], marker=id_outer)
g.spline([3, 2], marker=id_outer)
g.spline([3, 0], marker=id_outer)

g.surface([4, 3, 2, 1], [[0]]) # Esquinas y agujeros

mesh = cfm.GmshMesh(g)

mesh.el_type = 2
mesh.dofs_per_node = 1  # Degrees of freedom per node.
mesh.el_size_factor = 1  # Factor that changes element sizes.

coords, edof, dofs, bdofs, element_markers = mesh.create()

n_dofs = np.size(dofs)
ex, ey = cfc.coordxtr(edof, coords, dofs)

K = np.zeros([n_dofs, n_dofs])

for el_topo, elx, ely, marker in zip(edof, ex, ey, element_markers):

    # Calc element stiffness matrix: Conductivity matrix D is taken
    # from Ddict and depends on which region (which marker) the element is in.

    if mesh.el_type == 2:
        Ke = cfc.flw2te(elx, ely, ep, D)
    elif mesh.el_type == 3:
        Ke = cfc.flw2i4e(elx, ely, ep, D)
    elif mesh.el_type == 16:
        Ke = cfc.flw2i8e(elx, ely, ep, D)
    else:
        print("Element type not supported")

    cfc.assem(el_topo, K, Ke)

    f = np.zeros([n_dofs, 1])

bc = np.array([], 'i')
bc_val = np.array([], 'f')

bc, bc_val = cfu.applybc(bdofs, bc, bc_val, id_outer, 2.0)
bc, bc_val = cfu.applybc(bdofs, bc, bc_val, id_hole1, 10.0)

a, r = cfc.solveq(K, f, bc, bc_val)

ed = cfc.extract_eldisp(edof, a)

for i in range(np.shape(ex)[0]):
    if mesh.el_type == 2:
        es, et = cfc.flw2ts(ex[i, :], ey[i, :], D, ed[i, :])
    elif mesh.el_type == 3:
        es, et, eci = cfc.flw2i4s(ex[i, :], ey[i, :], ep, D, ed[i, :])
    elif mesh.el_type == 16:
        es, et, eci = cfc.flw2i8s(ex[i, :], ey[i, :], ep, D, ed[i, :])
    else:
        print("Element type not supported.")

plot = cfv.draw_nodal_values(a, coords, edof, title="Temperature", dofs_per_node=mesh.dofs_per_node, el_type=mesh.el_type, draw_elements=True, levels=16)
cfv.colorbar()
cfv.show_and_wait()