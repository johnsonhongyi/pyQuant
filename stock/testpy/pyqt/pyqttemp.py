"""
Demonstrate creation of a custom graphic (a candlestick plot)

"""
import pyqtgraph as pg
from pyqtgraph import QtCore, QtGui
import random

## Create a subclass of GraphicsObject.
## The only required methods are paint() and boundingRect() 
## (see QGraphicsItem documentation)
class CandlestickItem(pg.GraphicsObject):
    def __init__(self):
        pg.GraphicsObject.__init__(self)
        self.flagHasData = False

    def set_data(self, data):
        self.data = data  ## data must have fields: time, open, close, min, max
        self.flagHasData = True
        self.generatePicture()
        self.informViewBoundsChanged()

    def generatePicture(self):
        ## pre-computing a QPicture object allows paint() to run much more quickly, 
        ## rather than re-drawing the shapes every time.
        self.picture = QtGui.QPicture()
        p = QtGui.QPainter(self.picture)
        p.setPen(pg.mkPen('w'))
        w = (self.data[1][0] - self.data[0][0]) / 3.
        for (t, open, close, min, max) in self.data:
            p.drawLine(QtCore.QPointF(t, min), QtCore.QPointF(t, max))
            if open > close:
                p.setBrush(pg.mkBrush('r'))
            else:
                p.setBrush(pg.mkBrush('g'))
            p.drawRect(QtCore.QRectF(t-w, open, w*2, close-open))
        p.end()

    def paint(self, p, *args):
        if self.flagHasData:
            p.drawPicture(0, 0, self.picture)

    def boundingRect(self):
        ## boundingRect _must_ indicate the entire area that will be drawn on
        ## or else we will get artifacts and possibly crashing.
        ## (in this case, QPicture does all the work of computing the bouning rect for us)
        return QtCore.QRectF(self.picture.boundingRect())

app = QtGui.QApplication([])

data = [  ## fields are (time, open, close, min, max).
    [1., 10, 13, 5, 15],
    [2., 13, 17, 9, 20],
    [3., 17, 14, 11, 23],
    [4., 14, 15, 5, 19],
    [5., 15, 9, 8, 22],
    [6., 9, 15, 8, 16],
]
item = CandlestickItem()
item.set_data(data)

plt = pg.plot()
plt.addItem(item)
plt.setWindowTitle('pyqtgraph example: customGraphicsItem')


def update():
    global item, data
    data_len = len(data)
    rand = random.randint(0, len(data)-1)
    new_bar = data[rand][:]
    new_bar[0] = data_len
    data.append(new_bar)
    item.set_data(data)
    app.processEvents()  ## force complete redraw for every plot

timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(100)

## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()