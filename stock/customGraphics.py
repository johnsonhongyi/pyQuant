import numpy as np
import pyqtgraph as pg
from pyqtgraph import QtCore, QtGui

from JSONData import tdx_data_Day as tdd


# import pyqtgraph.examples
# pyqtgraph.examples.run()

class CandlestickItem(pg.GraphicsObject):
    def __init__(self, data):
        pg.GraphicsObject.__init__(self)
        self.data = data  # data must have fields: time, open, close, min, max
        self.generatePicture()

    def generatePicture(self):
        self.picture = QtGui.QPicture()
        p = QtGui.QPainter(self.picture)
        p.setPen(pg.mkPen('w'))
        # print self.data[1] , self.data[0]
        w = (self.data[1][0] - self.data[0][0]) / 3.
        for (t, open, close, low, high) in self.data:
            p.drawLine(QtCore.QPointF(t, low), QtCore.QPointF(t, high))
            if open > close:
                p.setBrush(pg.mkBrush('g'))
            else:
                p.setBrush(pg.mkBrush('r'))
            p.drawRect(QtCore.QRectF(t - w, open, w * 2, close - open))
        p.end()

    def paint(self, p, *args):
        p.drawPicture(0, 0, self.picture)

    def boundingRect(self):
        return QtCore.QRectF(self.picture.boundingRect())


def getCandlesData2(bars):
    # date = date2num(bars.index.to_datetime().to_pydatetime())
    bars.reset_index(inplace=True)
    # date = map(lambda x:x.replace('-',''),df.index)
    date = bars.index
    openp = bars['open']
    closep = bars['close']
    highp = bars['high']
    lowp = bars['low']
    # volume = bars['volume']
    # data = np.array([[1.0, 1.0, 1.0, 1.0, 1.0]])
    data = []
    for i in range(len(bars)):
        data.append((date[i], openp[i], closep[i], lowp[i], highp[i]))
    return data


def getCandlesData(bars):
    # date = date2num(bars.index.to_datetime().to_pydatetime())
    # date = map(lambda x:int(x.replace('-','')),df.index)
    # bars.index = map(lambda x:int(x.replace('-','')),bars.index)
    bars.reset_index(inplace=True)
    # print bars.index
    # bars = bars.astype(float)
    date = bars.index
    openp = bars['open']
    closep = bars['close']
    highp = bars['high']
    lowp = bars['low']
    # volume = bars['volume']
    # data = np.array([[1.0, 1.0, 1.0, 1.0, 1.0]])
    data = np.array([[1.0, 1.0, 1.0, 1.0, 1.0]])
    for i in range(len(bars)):
        data = np.append(
            data, [[date[i], openp[i], closep[i], lowp[i], highp[i], ]], axis=0)
    data = np.delete(data, 0, 0)
    return data


# data = [  ## fields are (time, open, close, min, max).
#     (1., 10, 13, 5, 15),
#     (2., 13, 17, 9, 20),
#     (3., 17, 14, 11, 23),
#     (4., 14, 15, 5, 19),
#     (5., 15, 9, 8, 22),
#     (6., 9, 15, 8, 16),
# ]
start = '2016-01-01'
# start=None
code = '999999'
df = tdd.get_tdx_append_now_df_api(
    code, start=start).sort_index(ascending=True)
print df[-1:]
data = getCandlesData2(df)

item = CandlestickItem(data)
plt = pg.plot()
plt.addItem(item)

QtGui.QApplication.exec_()
