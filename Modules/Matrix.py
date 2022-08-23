import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QVBoxLayout, QLabel, QGridLayout
from PyQt5 import QtCore

class Matrix1X1(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Matriz')

        mainLayout = QGridLayout()

        self.lEdit11 = QLineEdit()
        self.lEdit11.setFixedSize(70,70)
        self.lEdit11.setAlignment(QtCore.Qt.AlignCenter)
        self.lEdit11.setEnabled(False)
        mainLayout.addWidget(self.lEdit11)

        self.setLayout(mainLayout)


class Matrix2X2(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Matriz')

        mainLayout = QGridLayout()

        self.lEdit11 = QLineEdit()
        self.lEdit11.setFixedSize(70,70)
        self.lEdit11.setAlignment(QtCore.Qt.AlignCenter)
        self.lEdit11.setEnabled(False)

        self.lEdit12 = QLineEdit()
        self.lEdit12.setFixedSize(70,70)
        self.lEdit12.setAlignment(QtCore.Qt.AlignCenter)
        self.lEdit12.setEnabled(False)

        self.lEdit21 = QLineEdit()
        self.lEdit21.setFixedSize(70,70)
        self.lEdit21.setAlignment(QtCore.Qt.AlignCenter)
        self.lEdit21.setEnabled(False)

        self.lEdit22 = QLineEdit()
        self.lEdit22.setFixedSize(70,70)
        self.lEdit22.setAlignment(QtCore.Qt.AlignCenter)
        self.lEdit22.setEnabled(False)

        mainLayout.addWidget(self.lEdit11)
        mainLayout.addWidget(self.lEdit12, 0 , 1)
        mainLayout.addWidget(self.lEdit21, 1 , 0)
        mainLayout.addWidget(self.lEdit22, 1 , 1)

        self.setLayout(mainLayout)

class Matrix3X3(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Matriz')

        mainLayout = QGridLayout()

        self.lEdit11 = QLineEdit()
        self.lEdit11.setFixedSize(70,70)
        self.lEdit11.setAlignment(QtCore.Qt.AlignCenter)
        self.lEdit11.setEnabled(False)

        self.lEdit12 = QLineEdit()
        self.lEdit12.setFixedSize(70,70)
        self.lEdit12.setAlignment(QtCore.Qt.AlignCenter)
        self.lEdit12.setEnabled(False)

        self.lEdit13 = QLineEdit()
        self.lEdit13.setFixedSize(70,70)
        self.lEdit13.setAlignment(QtCore.Qt.AlignCenter)
        self.lEdit13.setEnabled(False)

        self.lEdit21 = QLineEdit()
        self.lEdit21.setFixedSize(70,70)
        self.lEdit21.setAlignment(QtCore.Qt.AlignCenter)
        self.lEdit21.setEnabled(False)

        self.lEdit22 = QLineEdit()
        self.lEdit22.setFixedSize(70,70)
        self.lEdit22.setAlignment(QtCore.Qt.AlignCenter)
        self.lEdit22.setEnabled(False)

        self.lEdit23 = QLineEdit()
        self.lEdit23.setFixedSize(70,70)
        self.lEdit23.setAlignment(QtCore.Qt.AlignCenter)
        self.lEdit23.setEnabled(False)

        self.lEdit31 = QLineEdit()
        self.lEdit31.setFixedSize(70,70)
        self.lEdit31.setAlignment(QtCore.Qt.AlignCenter)
        self.lEdit31.setEnabled(False)

        self.lEdit32 = QLineEdit()
        self.lEdit32.setFixedSize(70,70)
        self.lEdit32.setAlignment(QtCore.Qt.AlignCenter)
        self.lEdit32.setEnabled(False)

        self.lEdit33 = QLineEdit()
        self.lEdit33.setFixedSize(70,70)
        self.lEdit33.setAlignment(QtCore.Qt.AlignCenter)
        self.lEdit33.setEnabled(False)

        mainLayout.addWidget(self.lEdit11)
        mainLayout.addWidget(self.lEdit12, 0 , 1)
        mainLayout.addWidget(self.lEdit13, 0 , 2)
        mainLayout.addWidget(self.lEdit21, 1 , 0)
        mainLayout.addWidget(self.lEdit22, 1 , 1)
        mainLayout.addWidget(self.lEdit23, 1 , 2)
        mainLayout.addWidget(self.lEdit31, 2 , 0)
        mainLayout.addWidget(self.lEdit32, 2 , 1)
        mainLayout.addWidget(self.lEdit33, 2 , 2)
        self.setLayout(mainLayout)

class Matrix2X1(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Matriz')

        mainLayout = QGridLayout()

        self.lEdit11 = QLineEdit()
        self.lEdit11.setFixedSize(70,70)
        self.lEdit11.setAlignment(QtCore.Qt.AlignCenter)
        self.lEdit11.setEnabled(False)

        self.lEdit21 = QLineEdit()
        self.lEdit21.setFixedSize(70,70)
        self.lEdit21.setAlignment(QtCore.Qt.AlignCenter)
        self.lEdit21.setEnabled(False)

        mainLayout.addWidget(self.lEdit11)
        mainLayout.addWidget(self.lEdit21, 1, 0)

        self.setLayout(mainLayout)

class Matrix3X1(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Matriz')

        mainLayout = QGridLayout()

        self.lEdit11 = QLineEdit()
        self.lEdit11.setFixedSize(70,70)
        self.lEdit11.setAlignment(QtCore.Qt.AlignCenter)
        self.lEdit11.setEnabled(False)

        self.lEdit21 = QLineEdit()
        self.lEdit21.setFixedSize(70,70)
        self.lEdit21.setAlignment(QtCore.Qt.AlignCenter)
        self.lEdit21.setEnabled(False)

        self.lEdit31 = QLineEdit()
        self.lEdit31.setFixedSize(70,70)
        self.lEdit31.setAlignment(QtCore.Qt.AlignCenter)
        self.lEdit31.setEnabled(False)
        mainLayout.addWidget(self.lEdit11)
        mainLayout.addWidget(self.lEdit21, 1, 0)
        mainLayout.addWidget(self.lEdit31, 2, 0)

        self.setLayout(mainLayout)