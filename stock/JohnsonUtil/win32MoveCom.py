#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-03-25 15:33:21
# @Author  : Johnson (5208115@qq.com)
# @Link    : ${link}
# @Version : $Id$

import ctypes
from ctypes.wintypes import *
 
def get_current_size(hwnd):
    try:
        f = ctypes.windll.dwmapi.DwmGetWindowAttribute
    except WindowsError:
        f = None
    if f:
        rect = ctypes.wintypes.RECT()
        DWMWA_EXTENDED_FRAME_BOUNDS = 9
        f(ctypes.wintypes.HWND(hwnd),
          ctypes.wintypes.DWORD(DWMWA_EXTENDED_FRAME_BOUNDS),
          ctypes.byref(rect),
          ctypes.sizeof(rect)
          )
        size = (rect.right - rect.left, rect.bottom - rect.top)        
        return size

def get_window_rect(hwnd):
    try:
        f = ctypes.windll.dwmapi.DwmGetWindowAttribute
    except WindowsError:
        f = None
    if f:
        rect = ctypes.wintypes.RECT()
        DWMWA_EXTENDED_FRAME_BOUNDS = 9
        f(ctypes.wintypes.HWND(hwnd),
          ctypes.wintypes.DWORD(DWMWA_EXTENDED_FRAME_BOUNDS),
          ctypes.byref(rect),
          ctypes.sizeof(rect)
          )
        return rect.left, rect.top, rect.right, rect.bottom
# pos = get_window_rect(hwnd1)


# import win32api, win32gui, win32print
# import win32con
# from win32api import GetSystemMetrics

# def get_real_resolution():
#     """获取真实的分辨率"""
#     hDC = win32gui.GetDC(0)
#     # 横向分辨率
#     w = win32print.GetDeviceCaps(hDC, win32con.DESKTOPHORZRES)
#     # 纵向分辨率
#     h = win32print.GetDeviceCaps(hDC, win32con.DESKTOPVERTRES)
#     return w, h


# def get_screen_size():
#     """获取缩放后的分辨率"""
#     w = GetSystemMetrics (0)
#     h = GetSystemMetrics (1)
#     return w, h

# real_resolution = get_real_resolution()
# screen_size = get_screen_size()
# print(real_resolution)
# print(screen_size)
# screen_scale_rate = round(real_resolution[0] / screen_size[0], 2)
# print(screen_scale_rate)
# # 版权声明：本文为CSDN博主「frostime」的原创文章，遵循 CC 4.0 BY-SA 版权协议，转载请附上原文出处链接及本声明。
# # 原文链接：https://blog.csdn.net/frostime/article/details/104798061



import win32gui,win32print
import win32con
from win32api import GetSystemMetrics

def get_system_disp():
    #获取系统分辨率
    return GetSystemMetrics(0), GetSystemMetrics(1)

def get_dpi():
    hDC = win32gui.GetDC(0)
    # dpi = win32print.GetDeviceCaps(hDC, win32con.LOGPIXELSX)
    w = win32print.GetDeviceCaps(hDC, win32con.DESKTOPHORZRES)
    h = win32print.GetDeviceCaps(hDC, win32con.DESKTOPVERTRES)
    return w,h

def get_system_zoom():
    dpi = get_dpi()
    screen = get_system_disp()
    return get_dpi()[0]/get_system_disp()[0]

# print "zoom:%s"%(get_system_zoom())

def get_window_pos(targetTitle):  
    hWndList = []  
    win32gui.EnumWindows(lambda hWnd, param: param.append(hWnd), hWndList)  
    for hwnd in hWndList:
        clsname = win32gui.GetClassName(hwnd)
        title = win32gui.GetWindowText(hwnd)
        if (title.find(targetTitle) >= 0):    #调整目标窗口到坐标(600,300),大小设置为(600,600)
            rect1 = win32gui.GetWindowRect(hwnd)
            rect2 = get_window_rect(hwnd)
            print("targetTitle:%s rect1:%s rect2:%s"%(title,rect1,rect2))
            # win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 330,678,600,600, win32con.SWP_SHOWWINDOW)
            # win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 330,678,600,600, win32con.SWP_SHOWWINDOW)
            # win32gui.MoveWindow(hwnd,1026, 699, 900, 360,True)  #108,19

def reset_window_pos(targetTitle,posx=1026,posy=699,width=900,height=360):

    hWndList = []  
    win32gui.EnumWindows(lambda hWnd, param: param.append(hWnd), hWndList)  
    for hwnd in hWndList:
        clsname = win32gui.GetClassName(hwnd)
        title = win32gui.GetWindowText(hwnd)
        if (title.find(targetTitle) >= 0):    #调整目标窗口到坐标(600,300),大小设置为(600,600)
            rect1 = win32gui.GetWindowRect(hwnd)
            rect2 = get_window_rect(hwnd)
            print("targetTitle:%s rect1:%s rect2:%s"%(title,rect1,rect2))
            # win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 330,678,600,600, win32con.SWP_SHOWWINDOW)
            # win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 330,678,600,600, win32con.SWP_SHOWWINDOW)
            win32gui.MoveWindow(hwnd,posx, posy, width, height,True)  #108,19

# reset_window_pos("single",width=900,height=360)

# import sys
# sys.exit(0)

# # 没有直接修改窗口大小的方式，但可以曲线救国，几个参数
# # 分别表示句柄,起始点坐标,宽,高度,是否重绘界面 ，如果想改变窗口大小，就必须指定起始点的坐标，没果对起始点坐标没有要求，随便写就可以；如果还想要放在原先的位置，就需要先获取之前的边框位置，再调用该方法即可
# win32gui.MoveWindow(hwnd,20,20,405,756,True)

# # 指定句柄设置为前台，也就是激活
# win32gui.SetForegroundWindow(hwnd)
# # 设置为后台
# win32gui.SetBkMode(hwnd, win32con.TRANSPARENT)



# import win32gui, win32con, win32api
# import time, math, random
  
# def _MyCallback( hwnd, extra ):
#     windows = extra
#     temp=[]
#     temp.append(hex(hwnd))
#     temp.append(win32gui.GetClassName(hwnd))
#     temp.append(win32gui.GetWindowText(hwnd))
#     windows[hwnd] = temp
  
# def TestEnumWindows():
#     windows = {}
#     win32gui.EnumWindows(_MyCallback, windows)
#     print "Enumerated a total of  windows with %d classes" ,(len(windows))
#     print '------------------------------'
#     #print classes
#     print '-------------------------------'
#     for item in windows :
#         print  windows[item]
 
# print "Enumerating all windows..."
# h=win32gui.FindWindow(None,'\xba\xec\xce\xe5')
# print hex(h)
# #TestEnumWindows()
# print "All tests done!"

# import ipdb;ipdb.set_trace()



# '''
# pythonwin中win32gui的用法
# 本文件演如何使用win32gui来遍历系统中所有的顶层窗口，
# 并遍历所有顶层窗口中的子窗口
# '''
 
# import win32gui
# from pprint import pprint
 
# def gbk2utf8(s):
#     return s.decode('gbk').encode('utf-8')
 
# def show_window_attr(hWnd):
#     '''
#     显示窗口的属性
#     :return:
#     '''
#     if not hWnd:
#         return
 
#     #中文系统默认title是gb2312的编码
#     title = win32gui.GetWindowText(hWnd)
#     title = gbk2utf8(title)
#     clsname = win32gui.GetClassName(hWnd)
 
#     # 窗口句柄:264230 
#     # 窗口标题:singleAnalyseUtil.py B:91760-91760 V:1.0 ZL: 61.9 To:13 D:54 Sh: 2.17%  Vr:2931.9-3069.0-1.1%  MR: 0.5 ZL: 61.9
#     # 窗口类名:ConsoleWindowClass

#     print '窗口句柄:%s ' % (hWnd)
#     print '窗口标题:%s' % (title)
#     print '窗口类名:%s' % (clsname)
#     print ''
 
# def show_windows(hWndList):
#     for h in hWndList:
#         show_window_attr(h)
 
# def demo_top_windows():
#     '''
#     演示如何列出所有的顶级窗口
#     :return:
#     '''
#     hWndList = []
#     win32gui.EnumWindows(lambda hWnd, param: param.append(hWnd), hWndList)
#     show_windows(hWndList)
 
#     return hWndList
 
# def demo_child_windows(parent):
#     '''
#     演示如何列出所有的子窗口
#     :return:
#     '''
#     if not parent:
#         return
 
#     hWndChildList = []
#     win32gui.EnumChildWindows(parent, lambda hWnd, param: param.append(hWnd),  hWndChildList)
#     show_windows(hWndChildList)
#     return hWndChildList
 
 
# hWndList = demo_top_windows()
# assert len(hWndList)
 
# parent = hWndList[20]
# #这里系统的窗口好像不能直接遍历，不知道是否是权限的问题
# hWndChildList = demo_child_windows(parent)
 
# print('-----top windows-----')
# pprint(hWndList)
 
# print('-----sub windows:from %s------' % (parent))
# pprint(hWndChildList)

# # 窗口句柄:264230 
# # 窗口标题:singleAnalyseUtil.py B:91760-91760 V:1.0 ZL: 61.9 To:13 D:54 Sh: 2.17%  Vr:2931.9-3069.0-1.1%  MR: 0.5 ZL: 61.9
# # 窗口类名:ConsoleWindowClass


# # import win32api,win32gui,win32con

# # label = 'single' #此处假设主窗口名为tt

# # hld = win32gui.FindWindow('single', label)

# # if hld > 0:

# #     dlg = win32api.FindWindowEx(hld, None, 'Edit', None)#获取hld下第一个为edit控件的句柄

# #     buffer = '0' *50

# #     len = win32gui.SendMessage(dlg, win32con.WM_GETTEXTLENGTH)+1 #获取edit控件文本长度

# #     win32gui.SendMessage(dlg, win32con.WM_GETTEXT, len, buffer) #读取文本

# #     print buffer[:len-1]

# #     #虚拟鼠标点击按钮(或者回车)

# #     btnhld = win32api.FindWindowEx(hld, None,'Button', None)

# #     # win32gui.PostMessage(btnhld, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)

# #     # win32gui.PostMessage(btnhld, win32con.WM_KEYUP, win32con.VK_RETURN, 0)

# #     win32gui.PostMessage(btnhld, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, 0)

# #     win32gui.PostMessage(btnhld, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, 0)

# #     #获取显示器屏幕大小

# #     width = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)

# #     height = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)