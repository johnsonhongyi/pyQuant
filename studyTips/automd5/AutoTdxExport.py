#! /usr/bin/env python
#coding=utf8
import os
import time
import win32gui
import win32api
import win32con
# http://www.orangecube.net/articles/python-win32-example.html
def find_idxSubHandle(pHandle, winClass, index=0):
    """
    已知子窗口的窗体类名
    寻找第index号个同类型的兄弟窗口
    """
    assert type(index) == int and index >= 0
    handle = win32gui.FindWindowEx(pHandle, 0, winClass, None)
    while index > 0:
        handle = win32gui.FindWindowEx(pHandle, handle, winClass, None)
        index -= 1
    return handle

def find_subHandle(pHandle, winClassList):
    """
    递归寻找子窗口的句柄
    pHandle是祖父窗口的句柄
    winClassList是各个子窗口的class列表，父辈的list-index小于子辈
    """
    assert type(winClassList) == list
    if len(winClassList) == 1:
        return find_idxSubHandle(pHandle, winClassList[0][0], winClassList[0][1])
    else:
        pHandle = find_idxSubHandle(pHandle, winClassList[0][0], winClassList[0][1])
        return find_subHandle(pHandle, winClassList[1:])    

handle = find_subHandle(self.Mhandle, [("ComboBoxEx32", 1), ("ComboBox", 0), ("Edit", 0)])
print "%x" % (handle)


# win32gui.PostMessage(self.Mhandle, win32con.WM_COMMAND, open_ID, 0)
    """
    打开菜单
    """
class FaceGenWindow(object):
    def __init__(self, fgFilePath=None):
        self.Mhandle = win32gui.FindWindow("FaceGenMainWinClass", None)
        self.menu = win32gui.GetMenu(self.Mhandle)
        self.menu = win32gui.GetSubMenu(self.menu, 0)
        print "FaceGen initialization compeleted"
    def menu_command(self, command):
        """
        菜单操作
        返回弹出的打开或保存的对话框的句柄 dig_handle
        返回确定按钮的句柄 confBTN_handle
        """
        command_dict = {  # [目录的编号, 打开的窗口名]
            "open": [2, u"打开"],
            "save_to_image": [5, u"另存为"],
        }
        cmd_ID = win32gui.GetMenuItemID(self.menu, command_dict[command][0])
        win32gui.PostMessage(self.Mhandle, win32con.WM_COMMAND, cmd_ID, 0)
        for i in range(10):
            if win32gui.FindWindow(None, command_dict[command][1]):
                break
            else:
                win32api.Sleep(200)
        dig_handle = win32gui.FindWindow(None, command_dict[command][1])
        confBTN_handle = win32gui.FindWindowEx(dig_handle, 0, "Button", None)
        return dig_handle, confBTN_handle
    def open_fg(self, fgFilePath):
        """打开fg文件"""
        Mhandle, confirmBTN_handle = self.menu_command('open')
        handle = find_subHandle(Mhandle, [("ComboBoxEx32", 0), ("ComboBox", 0), ("Edit", 0)])
        if win32api.SendMessage(handle, win32con.WM_SETTEXT, 0, os.path.abspath(fgFilePath).encode('gbk')) == 1:
            return win32api.SendMessage(Mhandle, win32con.WM_COMMAND, 1, confirmBTN_handle)
        raise Exception("File opening path set failed")
        
        # handle = find_subHandle(Mhandle, [("ComboBoxEx32", 0), ("ComboBox", 0), ("Edit", 0)]) #文本框 
        # win32api.SendMessage(handle, win32con.WM_SETTEXT, 0, os.path.abspath(fgFilePath).encode('gbk'))#带返回信息
        #win32api.SendMessage(Mhandle, win32con.WM_COMMAND, 1, confirmBTN_handle) #确认键
    '''
    buf_size = win32gui.SendMessage(hwnd, win32con.WM_GETTEXTLENGTH, 0, 0) + 1 # 要加上截尾的字节
    str_buffer = win32gui.PyMakeBuffer(buf_size) # 生成buffer对象
    win32api.SendMessage(hwnd, win32con.WM_GETTEXT, buf_size, str_buffer) # 获取buffer
    str = str(str_buffer[:-1]) # 转为字符串
    '''
    
    #下拉确认通知Main
    # if win32api.SendMessage(CB_handle, win32con.CB_SETCURSEL, format_dict[format], 0) == format_dict[format]:
        # win32api.SendMessage(PCB_handle, win32con.WM_COMMAND, win32con.CBN_SELENDOK&lt;&lt;16+0, CB_handle)  # 控件的ID是0，所以低位直接加0
        # win32api.SendMessage(PCB_handle, win32con.WM_COMMAND, win32con.CBN_SELCHANGE&lt;&lt;16+0, CB_handle)
    # else:
        # raise Exception("Change saving type failed")