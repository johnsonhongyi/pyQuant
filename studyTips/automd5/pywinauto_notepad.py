#! /usr/bin/env python
#coding=gbk
 
# http://my.oschina.net/yangyanxing/blog/167042
import time,sys
from pywinauto import application,timings
from pywinauto import win32defines

import logging
logger = logging.getLogger('pywinauto')
# logger.level = logging.WARNING # or higher
logger.level = logging.DEBUG # or higher
# pywinauto.Timings.window_find_timeout = 10
timings.Timings.window_find_timeout = 0.1

App = application.Application()
# app = App.Connect(class_name='Notepad')
# app = App.start('notepad.exe')

# app.notepad.TypeKeys("%FX")
# time.sleep(.5)
# sys.exit(0)
app.Notepad.MenuSelect('帮助->关于记事本'.decode('gb2312'))
# time.sleep(.5)
 
#这里有两种方法可以进行定位“关于记事本”的对话框
#top_dlg = app.top_window_() 不推荐这种方式，因为可能得到的并不是你想要的
# about_dlg = app.window_(title_re = u"关于", class_name = "#32770",found_index=1)#这里可以进行正则匹配title
about_dlg = app.window_(title_re = u"关于", class_name = "#32770")#这里可以进行正则匹配title
# about_dlg.print_control_identifiers()
# app.window_(title_re = u'关于“记事本”').window_(title_re = u'确定').Click()
# app.Notepad.MenuSelect('帮助->关于记事本'.decode('gb2312'))
# time.sleep(.5) #停0.5s 否则你都看不出来它是否弹出来了！
ABOUT = u'关于“记事本”'
OK = u'确定'
# lp=''
# app[ABOUT][OK].SendMessage(win32defines.WM_GETTEXT, wparam = 100, lparam = lp)
# about_dlg[OK].Click()
# app[u'关于“记事本”'][u'确定'].Click()
# print about_dlg.Children()
print "App Focus:%s"%(App.notepad.GetFocus())

if about_dlg.Exists():
    # reboot_dlg.No.Click()
    app[ABOUT][OK].Click()
    about_dlg.WaitNot('visible')  
notetitle=u"无标题"    
# app[notetitle].SetFocus() 
print "App Focus:%s"%(App.notepad.GetFocus())

app.Notepad.TypeKeys(u"杨彦星")
dig = app.Notepad.MenuSelect("编辑(E)->替换(R)".decode('gb2312'))
Replace = u'替换'
Cancle = u'取消'
Find = u'查找内容'
rep_dlg = app[Replace]
print rep_dlg.Exists()
print "App Focus:%s"%(App.notepad.GetFocus())
if rep_dlg.Exists():
    print "App Focus:%s"%(App.notepad.GetFocus())
    app[Replace][Cancle].SetFocus() 
    # rep_dlg[Cancle].click()
    # app[Replace][Find].Click()
    app[Replace][Cancle].CloseClick()
    # app.TypeKeys("{ENTER}")ff
    rep_dlg.WaitNot('visible')
    
app.Notepad.TypeKeys("%FX")
dotSave=u"不保存"
Savename=u"记事本"
app[Savename][dotSave].Click()
# time.sleep(.5)
# about_dlg.ChildWindow(title_re=Replace).Click()
# app.window_(title_re = Replace).window_(title_re = Cancle).Click()
# app[Replace][Cancle].Click()
# dialogs = app.windows_()
# app.Notepad.不保存