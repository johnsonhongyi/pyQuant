import wx
import functools
import threading
import subprocess
import time

class Frame(wx.Frame):
    def __init__(self):
        super(Frame, self).__init__(None, -1, 'Threading Example')
        # add some buttons and a text control
        panel = wx.Panel(self, -1)
        sizer = wx.BoxSizer(wx.VERTICAL)
        for i in range(3):
            name = 'Button %d' % (i+1)
            button = wx.Button(panel, -1, name)
            func = functools.partial(self.on_button, button=name)
            button.Bind(wx.EVT_BUTTON, func)
            sizer.Add(button, 0, wx.ALL, 5)
        text = wx.TextCtrl(panel, -1, style=wx.TE_MULTILINE|wx.TE_READONLY)
        self.text = text
        sizer.Add(text, 1, wx.EXPAND|wx.ALL, 5)
        panel.SetSizer(sizer)
    def on_button(self, event, button):
        # create a new thread when a button is pressed
        thread = threading.Thread(target=self.run, args=(button,))
        thread.setDaemon(True)
        thread.start()
    def on_text(self, text):
        self.text.AppendText(text)
    def run(self, button):
        cmd = ['ls', '-lta']
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for line in proc.stdout:
            wx.CallAfter(self.on_text, line)
import traceback
def show_error():
    message = ''.join(traceback.format_exception(*sys.exc_info()))
    dialog = wx.MessageDialog(None, message, 'Error!', wx.OK|wx.ICON_ERROR)
    dialog.ShowModal()

if __name__ == '__main__':
#    app = wx.PySimpleApp()
    app = wx.App()
    try:
        frame = Frame()
        frame.Show()
        frame.cause_error()
        app.MainLoop()
    except:
        show_error()
##    app = wx.App(redirect=True,filename="mylogfile.txt")
#    frame = wx.Frame(parent=None)
##    frame.Show(True)
##    frame = Frame()
#    frame.Show()
    app.MainLoop()