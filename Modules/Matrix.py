import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QVBoxLayout, QLabel, QGridLayout
from PyQt5 import QtCore

class MatrixDiffusionCoef1X1(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Matriz')

        mainLayout = QVBoxLayout()

        self.lEdit11 = QLineEdit()
        self.lEdit11.setFixedSize(50,50)
        self.lEdit11.setAlignment(QtCore.Qt.AlignCenter)
        mainLayout.addWidget(self.lEdit11, alignment=QtCore.Qt.AlignCenter)

        self.setLayout(mainLayout)


class MatrixDiffusionCoef2X2(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Matriz')

        mainLayout = QGridLayout()

        self.lEdit11 = QLineEdit()
        self.lEdit11.setFixedSize(70,70)
        self.lEdit11.setAlignment(QtCore.Qt.AlignCenter)

        self.lEdit12 = QLineEdit()
        self.lEdit12.setFixedSize(70,70)
        self.lEdit12.setAlignment(QtCore.Qt.AlignCenter)

        self.lEdit21 = QLineEdit()
        self.lEdit21.setFixedSize(70,70)
        self.lEdit21.setAlignment(QtCore.Qt.AlignCenter)

        self.lEdit22 = QLineEdit()
        self.lEdit22.setFixedSize(70,70)
        self.lEdit22.setAlignment(QtCore.Qt.AlignCenter)

        mainLayout.addWidget(self.lEdit11)
        mainLayout.addWidget(self.lEdit12, 0 , 1)
        mainLayout.addWidget(self.lEdit21, 1 , 0)
        mainLayout.addWidget(self.lEdit22, 1 , 1)

        self.setLayout(mainLayout)

class MatrixDiffusionCoef3X3(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Matriz')

        mainLayout = QGridLayout()

        self.lEdit11 = QLineEdit()
        self.lEdit11.setFixedSize(70,70)
        self.lEdit11.setAlignment(QtCore.Qt.AlignCenter)

        self.lEdit12 = QLineEdit()
        self.lEdit12.setFixedSize(70,70)
        self.lEdit12.setAlignment(QtCore.Qt.AlignCenter)

        self.lEdit21 = QLineEdit()
        self.lEdit21.setFixedSize(70,70)
        self.lEdit21.setAlignment(QtCore.Qt.AlignCenter)

        self.lEdit22 = QLineEdit()
        self.lEdit22.setFixedSize(70,70)
        self.lEdit22.setAlignment(QtCore.Qt.AlignCenter)

        mainLayout.addWidget(self.lEdit11)
        mainLayout.addWidget(self.lEdit12, 0 , 1)
        mainLayout.addWidget(self.lEdit21, 1 , 0)
        mainLayout.addWidget(self.lEdit22, 1 , 1)

        self.setLayout(mainLayout)