# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pyspy.ui'
#
# Created: Sun May 02 00:43:05 2010
#      by: PyQt4 UI code generator 4.4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_SpyDialog(object):
    def setupUi(self, SpyDialog):
        SpyDialog.setObjectName("SpyDialog")
        SpyDialog.setEnabled(True)
        SpyDialog.resize(400, 292)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(SpyDialog.sizePolicy().hasHeightForWidth())
        SpyDialog.setSizePolicy(sizePolicy)
        SpyDialog.setMinimumSize(QtCore.QSize(400, 292))
        SpyDialog.setMaximumSize(QtCore.QSize(400, 292))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/res/finderf.bmp"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        SpyDialog.setWindowIcon(icon)
        SpyDialog.setModal(False)
        self.textEditInformation = QtGui.QTextEdit(SpyDialog)
        self.textEditInformation.setGeometry(QtCore.QRect(30, 70, 341, 161))
        self.textEditInformation.setObjectName("textEditInformation")
        self.label = QtGui.QLabel(SpyDialog)
        self.label.setGeometry(QtCore.QRect(290, 250, 91, 21))
        self.label.setTextFormat(QtCore.Qt.RichText)
        self.label.setOpenExternalLinks(True)
        self.label.setObjectName("label")

        self.retranslateUi(SpyDialog)
        QtCore.QMetaObject.connectSlotsByName(SpyDialog)

    def retranslateUi(self, SpyDialog):
        SpyDialog.setWindowTitle(QtGui.QApplication.translate("SpyDialog", "PySpy++", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("SpyDialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'宋体\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">By <a href=\"http://www.cnblogs.com/coderzh\"><span style=\" font-size:12pt; text-decoration: underline; color:#0000ff;\">CoderZh</span></a></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))

import pyspy_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    SpyDialog = QtGui.QDialog()
    ui = Ui_SpyDialog()
    ui.setupUi(SpyDialog)
    SpyDialog.show()
    sys.exit(app.exec_())

