from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import numpy as np

# Open(and close)Both Files and read info, similarly formatted datasets
f = open('winequality-red.csv', 'r')
data = np.genfromtxt(f, delimiter=';', skip_header=1,
                     names=["fixed acidity", "volatile acidity", "citric acid",
                            "residual sugar", "chlorides", "free sulfur dioxide",
                            "total sulfur dioxide", "density",
                            "pH", "sulphates", "alcohol", "quality"])
f.close()
f2 = open('winequality-white.csv', 'r')
data2 = np.genfromtxt(f2, delimiter=';', skip_header=1,
                      names=["fixed acidity", "volatile acidity", "citric acid",
                             "residual sugar", "chlorides", "free sulfur dioxide",
                             "total sulfur dioxide", "density",
                             "pH", "sulphates", "alcohol", "quality"])
f2.close
# initialize the PyQt Gui
app = QtGui.QApplication([])
mw = QtGui.QMainWindow()
mw.resize(800, 800)
view = pg.GraphicsLayoutWidget()
mw.setCentralWidget(view)
mw.show()
mw.setWindowTitle('Wine Plots')

# create four areas to add plots
w1 = view.addPlot(title="pH vs alcohol in red Wines")
w2 = view.addPlot(title="pH vs alcohol in white Wines")
view.nextRow()
w3 = view.addPlot(title="residual Sugar vs Density in red Wines")
w4 = view.addPlot(title="residual Sugar vs Density in white Wines")
print("Generating data, this takes a few seconds...")

# 1: pH vs Alcohol red wines  (color = quality)
s1 = pg.ScatterPlotItem(size=10, pxMode=True)
spots1 = []
n = len(data['alcohol'])
x_var1 = data['alcohol']
y_var1 = data['pH']
scale = data['quality']
for i in range(n):
    spots1.append({'pos': (x_var1[i], y_var1[i]),
                   'brush': pg.intColor(scale[i] * 10, 100)})
s1.addPoints(spots1)
w1.addItem(s1)

# 2: pH vs Alcohol  white(color = quality)
s2 = pg.ScatterPlotItem(size=10, pxMode=True)
spots2 = []
n = len(data2['alcohol'])
x_var2 = data2['alcohol']
y_var2 = data2['pH']
scale2 = data2['quality']
for i in range(n):
    spots2.append({'pos': (x_var2[i], y_var2[i]),
                   'brush': pg.intColor(scale2[i] * 10, 100)})
s2.addPoints(spots2)
w2.addItem(s2)

# 3: pH vs Alcohol  red(color = quality)
s3 = pg.ScatterPlotItem(size=10, pxMode=True)
spots3 = []
n = len(data['residual_sugar'])
x_var3 = data['density']
y_var3 = data['residual_sugar']
scale3 = data['quality']
for i in range(n):
    spots3.append({'pos': (x_var3[i], y_var3[i]),
                   'brush': pg.intColor(scale3[i] * 10, 100)})
s3.addPoints(spots3)
w3.addItem(s3)

# 4: pH vs Alcohol  whites(color = quality)
s4 = pg.ScatterPlotItem(size=10, pxMode=True)
spots4 = []
n = len(data2['residual_sugar'])
x_var4 = data2['density']
y_var4 = data2['residual_sugar']
scale4 = data2['quality']
for i in range(n):
    spots4.append({'pos': (x_var4[i], y_var4[i]),
                   'brush': pg.intColor(scale4[i] * 10, 100)})
s4.addPoints(spots4)
w4.addItem(s4)
gl = pg.GradientLegend((10, 100), (300, 10))
gl.setIntColorScale(0, 100)
gl.scale(1, -1)
w4.addItem(gl)

# Start Qt event loop unless running in interactive mode.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
