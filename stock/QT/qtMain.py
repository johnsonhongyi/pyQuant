# -*- coding: utf-8 -*-
__author__ = 'djstava@gmail.com'

import sys

# from PyQt5.QtWidgets import QApplication , QMainWindow
from PyQt5 import QtWidgets
class mywindow(QtWidgets.QWidget):

    def __init__(self):
        super(mywindow,self).__init__()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    windows = mywindow()
    windows.show()
    sys.exit(app.exec_())