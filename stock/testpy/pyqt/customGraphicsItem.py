import pyqtgraph as pg
from pyqtgraph import QtCore, QtGui
import numpy as np
# os.chdir(sys.path.append(".."))
import os,sys  
os.chdir('../../')
# print os.getcwd()
sys.path.append(".")
# print sys.path
from JSONData import tdx_data_Day as tdd

class CandlestickItem(pg.GraphicsObject):
    def __init__(self, data):
        pg.GraphicsObject.__init__(self)
        self.data = data  ## data must have fields: time, open, close, min, max
        self.generatePicture()
    
    def generatePicture(self):
         ## pre-computing a QPicture object allows paint() to run much more quickly, 
        ## rather than re-drawing the shapes every time.
        self.picture = QtGui.QPicture()
        p = QtGui.QPainter(self.picture)
        p.setPen(pg.mkPen('w'))
        # import ipdb;ipdb.set_trace()

        # w = (self.data[1][0] - self.data[0][0]) / 3.
        # # w = (self.data[1][0] - self.data[0][0]) 
        # print self.data[1][0] , self.data[0][0]
        # print self.data[1] , self.data[0]

        for (t, open, close, low, high) in self.data:
            # p.drawLine(QtCore.QPointF(t, low), QtCore.QPointF(t, high))
            p.drawLine(QtCore.QPointF(t, low), QtCore.QPointF(t, high))
            if open > close:
                p.setBrush(pg.mkBrush('r'))
            else:
                p.setBrush(pg.mkBrush('g'))
            # p.drawRect(QtCore.QRectF(t-w, open, w*2, close-open))
            p.drawRect(QtCore.QRectF(t, open, 0.66, close-open))
        p.end()
    
    def paint(self, p, *args):
        p.drawPicture(0, 0, self.picture)
    
    def boundingRect(self):
        return QtCore.QRectF(self.picture.boundingRect())


def getCandlesData(bars):
    from matplotlib import dates
    # bars.index = dates.date2num(bars.index.to_datetime().to_pydatetime())

    # bars['datet'] = bars.index
    # bars['datet'] = bars['datet'].apply(lambda x:x.replace('-',''))
    # date = bars.datet

    # date = dates.date2num(bars.index.to_datetime().to_pydatetime())
    # date = bars.index.to_datetime()

    date = bars.index
    openp = bars['open']
    closep = bars['close']
    highp = bars['high']
    lowp = bars['low']
    # volume = bars['volume']
    # data = np.array([[1.0, 1.0, 1.0, 1.0, 1.0]])
    data = np.array([[1.0, 1.0, 1.0, 1.0, 1.0]])
    for i in range(len(bars)):
        # print date[i],float(highp[i])
        data = np.append(
            # data, [[float(date[i]), float(highp[i]), float(lowp[i]), float(closep[i]), ]], axis=0)
            data, [[(date[i]), float(openp[i]), float(highp[i]), float(lowp[i]), float(closep[i]), ]], axis=0)
            # data, [[float(date[i]), float(openp[i]), float(highp[i]), float(lowp[i]), float(closep[i]), ]], axis=0)
    data = np.delete(data, 0, 0)
    return data

#simple data    
data = [  ## fields are (time, open, close, min, max).
    (20190101., 10, 13, 5, 15),
    (20190102., 13, 17, 9, 20),
    (20190103., 17, 14, 11, 23),
    (20190104., 14, 15, 5, 19),
    (20190105., 15, 9, 8, 22),
    (20190106., 9, 15, 8, 16),
    ]
start='2020-01-01'
code='000002'
df=tdd.get_tdx_append_now_df_api(code,start=start).sort_index(ascending=True)
data=getCandlesData(df)
print data
item = CandlestickItem(data)
plt = pg.plot()
plt.addItem(item)
QtGui.QApplication.exec_()