#!/usr/bin/env python
#coding:utf-8
#
# Copyright 2009 CoderZh.com.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

__author__ = 'CoderZh'

import win32gui
import win32con
import win32api
from ui_pyspy import Ui_SpyDialog
from PyQt4 import QtCore, QtGui

class SpyLabel(QtGui.QLabel):
    def __init__(self, parent = None):
        QtGui.QLabel.__init__(self, parent)
        self.parent = parent
        self.spying = False
        self.rectanglePen = win32gui.CreatePen(win32con.PS_SOLID, 3, win32api.RGB(255, 0, 0))
        self.prevWindow = None
        self.setCursor(QtCore.Qt.SizeAllCursor)

    def output(self, message):
        self.parent.output(message)
        
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.spying = True

    def mouseMoveEvent(self, event):
        if self.spying:
            curX, curY = win32gui.GetCursorPos()
            hwnd = win32gui.WindowFromPoint((curX, curY))

            if self.checkWindowValidity(hwnd):                
                if self.prevWindow:
                    self.refreshWindow(self.prevWindow)
                    
                self.prevWindow = hwnd
                self.highlightWindow(hwnd)
                self.displayWindowInformation(hwnd)

    def mouseReleaseEvent(self, event):
        if self.spying:
            if self.prevWindow:
                self.refreshWindow(self.prevWindow)

            win32gui.ReleaseCapture()
            self.spying = False

    def highlightWindow(self, hwnd):
        left, top, right, bottom = win32gui.GetWindowRect(hwnd)
        windowDc = win32gui.GetWindowDC(hwnd)
        if windowDc:
            prevPen = win32gui.SelectObject(windowDc, self.rectanglePen)
            prevBrush = win32gui.SelectObject(windowDc, win32gui.GetStockObject(win32con.HOLLOW_BRUSH))

            win32gui.Rectangle(windowDc, 0, 0, right - left, bottom - top)

            win32gui.SelectObject(windowDc, prevPen)
            win32gui.SelectObject(windowDc, prevBrush)
            win32gui.ReleaseDC(hwnd, windowDc)

    def refreshWindow(self, hwnd):
        win32gui.InvalidateRect(hwnd, None, True)
        win32gui.UpdateWindow(hwnd)
        win32gui.RedrawWindow(hwnd, None, None, win32con.RDW_FRAME|win32con.RDW_INVALIDATE|win32con.RDW_UPDATENOW|win32con.RDW_ALLCHILDREN)

    def checkWindowValidity(self, hwnd):
        if not hwnd:
            return False
        if not win32gui.IsWindow(hwnd):
            return False
        if self.prevWindow == hwnd:
            return False
        if self.parent == hwnd:
            return False
        return True

    def displayWindowInformation(self, hwnd):
        className = win32gui.GetClassName(hwnd)
        buf_size = 1 + win32gui.SendMessage(hwnd, win32con.WM_GETTEXTLENGTH, 0, 0)
        buffer = win32gui.PyMakeBuffer(buf_size)
        win32gui.SendMessage(hwnd, win32con.WM_GETTEXT, buf_size, buffer)
        windowText = buffer[:buf_size]

        try:
            windowText = unicode(windowText, 'gbk')
        except:
            pass

        message = ['Handle:\t' + str(hwnd),
                   'Class Name:\t' + className,
                   'Window Text:\t' + windowText]
        
        self.output('\r\n'.join(message))


class SpyDialog(QtGui.QDialog, Ui_SpyDialog):
    def __init__(self, parent = None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.spyLabel = SpyLabel(self)
        self.spyLabel.setGeometry(QtCore.QRect(170, 20, 41, 41))
        self.spyLabel.setPixmap(QtGui.QPixmap(":/res/finderf.bmp"))
        self.spyLabel.setObjectName("spyLabel")

    def output(self, message):
        self.textEditInformation.setText(message)

        
if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    dlg = SpyDialog()
    dlg.show()
    sys.exit(app.exec_())

