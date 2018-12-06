import interface
import sys
import pygame
import time
from PyQt5.QtWidgets import QApplication, QMainWindow
class CommonHelper:
    def __init__(self):
        pass

    @staticmethod
    def readQss(style):
        with open(style, 'r') as f:
            return f.read()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    # MainWindow.setStyleSheet('q.qss')
    ui = interface.Ui_MainWindow()
    ui.setupUi(MainWindow)
    styleFile = './q.qss'
    qssStyle = CommonHelper.readQss(styleFile)
    MainWindow.setStyleSheet(qssStyle)
    MainWindow.show()
    sys.exit(app.exec_())
