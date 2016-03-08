#-*-coding:utf-8-*-
import os
import time
import win32gui
import win32api
import win32con
from PIL import ImageGrab

#os.startfile("D:\\artcut6\\Prog\\Artcut6.exe")
#time.sleep(1)

# wdname1=r"文泰刻绘2009[] - [无标题-1]"
wdname1=r'Hash'
w1hd=win32gui.FindWindow(wdname1,None)
print "w1hd",w1hd
w2hd=win32gui.FindWindowEx(w1hd,None,None,None)
print "w2hd",w2hd

def aotohelper_wt(i):
    #获取窗口焦点
    win32gui.SetForegroundWindow(w2hd)
    #快捷键Alt+F
    win32api.keybd_event(18,0,0,0)      # Alt
    win32api.keybd_event(70,0,0,0)     # F
    win32api.keybd_event(70,0,win32con.KEYEVENTF_KEYUP,0)  #释放按键
    win32api.keybd_event(18,0,win32con.KEYEVENTF_KEYUP,0)

    #快捷键I
    win32api.keybd_event(73,0,0,0)     # I
    win32api.keybd_event(73,0,win32con.KEYEVENTF_KEYUP,0)

    time.sleep(0.2)
    wdname3=r"打开"
    w3hd=win32gui.FindWindow(None,wdname3)  #”打开“ 窗口句柄  
    #print w3hd

    #win32gui.MoveWindow(w3hd, 50, 50, 300, 200, True)
    if i<=9:
        msg="YC-00"+str(i)
    elif 10<=i<=99:
        msg="YC-0"+str(i)
    else:
        msg="YC-"+str(i)
    edithd=win32gui.FindWindowEx(w3hd,None,"Edit",None)
    win32api.SendMessage(edithd,win32con.WM_SETTEXT,None,msg)
    time.sleep(0.1)
    #btnhd=win32gui.FindWindowEx(w3hd,None,"BUTTON",None)
    #print btnhd
    #模拟快捷键Alt+O
    win32api.keybd_event(18,0,0,0)      # Alt
    win32api.keybd_event(79,0,0,0)     # O
    win32api.keybd_event(79,0,win32con.KEYEVENTF_KEYUP,0)  #释放按键
    win32api.keybd_event(18,0,win32con.KEYEVENTF_KEYUP,0)
    time.sleep(0.1)
    #模拟鼠标操作
    win32api.SetCursorPos([30,150])    #为鼠标焦点设定一个位置
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0,0,0)
    win32api.SetCursorPos([500,500])
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0,0,0)
    time.sleep(0.1)
    #模拟快捷键F7(极限观察)
    win32api.keybd_event(118,0,0,0)     # F7
    win32api.keybd_event(118,0,win32con.KEYEVENTF_KEYUP,0)  #释放按键
    time.sleep(0.2)
    #利用PIL截屏
    # path="C:\\Users\\LY\\Desktop\\pic\\"
    # filename="YC-"+str(i)+".jpg"
    # im=ImageGrab.grab()
    # im.save(path+filename)

    #模拟快捷键F8(回到原页面大小)
    win32api.keybd_event(119,0,0,0)     # F8
    win32api.keybd_event(119,0,win32con.KEYEVENTF_KEYUP,0)  #释放按键

    #模拟键盘事件delete
    win32api.keybd_event(46,0,0,0)     # Delete
    win32api.keybd_event(46,0,win32con.KEYEVENTF_KEYUP,0)  #释放按键
    time.sleep(1)

# for i in range(2,85):
    # aotohelper_wt(i)
    # print i
raw_input("pause")
print "work done!"