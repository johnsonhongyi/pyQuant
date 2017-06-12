#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys
from OpFlow import * # 这是自己写的一个python文件，在github上
class LayoutDialog(QDialog):
    def __init__(self, parent=None):
        super(LayoutDialog, self).__init__(parent)
        self.setWindowTitle("Path Check")
        self.CreateControls()
        self.Layout()
        self.ConnectSignalSlot()
    def CreateControls(self):
        self.label_0 = QLabel(self.tr("src IP:"))
        self.label_1 = QLabel(self.tr("dst IP:"))
        self.label_2 = QLabel(self.tr("Path:"))
        self.srcip = QLineEdit()
        self.dstip = QLineEdit()
        self.path = QTextEdit()
        self.btn_check = QPushButton(self.tr("Check"))
        self.btn_check.clicked.connect(self.buttonClicked)
    def buttonClicked(self):
        srcip = self.srcip.text()
        dstip = self.dstip.text()
        res = control.getSwitchFlowPath(str(srcip), str(dstip))
        self.path.clear()
        for string in res:
            self.path.append(string)
    def Layout(self):
        self.LeftLayout()
        mainLayout = QGridLayout(self)
        mainLayout.setMargin(10)
        mainLayout.setSpacing(10)
        mainLayout.addLayout(self.leftLayout, 0, 0)
        mainLayout.setSizeConstraint(QLayout.SetFixedSize)
    def LeftLayout(self):
        self.leftLayout = QGridLayout()
        self.leftLayout.addWidget(self.label_0, 0, 0)
        self.leftLayout.addWidget(self.label_1, 1, 0)
        self.leftLayout.addWidget(self.label_2, 3, 0)
        self.leftLayout.addWidget(self.srcip, 0, 1)
        self.leftLayout.addWidget(self.dstip, 1, 1)
        self.leftLayout.addWidget(self.path, 3, 1)
        self.leftLayout.setColumnStretch(0, 1)
        self.leftLayout.setColumnStretch(1, 3)
        self.leftLayout.addWidget(self.btn_check)
    def ConnectSignalSlot(self):
        pass
control = Controller()
app = QApplication(sys.argv)
dialog = LayoutDialog()
dialog.show()
app.exec_()