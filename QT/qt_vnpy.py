# -*- coding: gbk -*-
import pyQt
class LogMonitor(QtGui.QTableWidget):
    """用于显示日志"""
    signal = QtCore.pyqtSignal(type(Event()))

    #----------------------------------------------------------------------
    def __init__(self, eventEngine, parent=None):
        """Constructor"""
        super(LogMonitor, self).__init__(parent)
        self.__eventEngine = eventEngine

        self.initUi()
        self.registerEvent()

    #----------------------------------------------------------------------
    def initUi(self):
        """初始化界面"""
        self.setWindowTitle(u'日志')

        self.setColumnCount(2)                     
        self.setHorizontalHeaderLabels([u'时间', u'日志'])

        self.verticalHeader().setVisible(False)                 # 关闭左边的垂直表头
        self.setEditTriggers(QtGui.QTableWidget.NoEditTriggers) # 设为不可编辑状态

        # 自动调整列宽
        self.horizontalHeader().setResizeMode(0, QtGui.QHeaderView.ResizeToContents)
        self.horizontalHeader().setResizeMode(1, QtGui.QHeaderView.Stretch)        

    #----------------------------------------------------------------------
    def registerEvent(self):
        """注册事件监听"""
        # Qt图形组件的GUI更新必须使用Signal/Slot机制，否则有可能导致程序崩溃
        # 因此这里先将图形更新函数作为Slot，和信号连接起来
        # 然后将信号的触发函数注册到事件驱动引擎中
        self.signal.connect(self.updateLog)
        self.__eventEngine.register(EVENT_LOG, self.signal.emit)

    #----------------------------------------------------------------------
    def updateLog(self, event):
        """更新日志"""
        # 获取当前时间和日志内容
        t = time.strftime('%H:%M:%S',time.localtime(time.time()))   
        log = event.dict_['log']                                    

        # 在表格最上方插入一行
        self.insertRow(0)              

        # 创建单元格
        cellTime = QtGui.QTableWidgetItem(t)    
        cellLog = QtGui.QTableWidgetItem(log)

        # 将单元格插入表格
        self.setItem(0, 0, cellTime)            
        self.setItem(0, 1, cellLog)