import matplotlib.patches as patches
import numpy as np
from matplotlib.pylab import plt


def press_zoom(self, event):
    if event.button == 1:
        self._button_pressed = 1
    elif event.button == 3:
        self._button_pressed = 3
    else:
        self._button_pressed = None
        return

    x, y = event.x, event.y

    # push the current view to define home if stack is empty
    if self._views.empty(): self.push_current()

    self._xypress = []
    for i, a in enumerate(self.canvas.figure.get_axes()):
        if (x is not None and y is not None and a.in_axes(event) and
                a.get_navigate() and a.can_zoom()):
            self._xypress.append((x, y, a, i, a.viewLim.frozen(),
                                  a.transData.frozen()))

    id1 = self.canvas.mpl_connect('motion_notify_event', self.drag_zoom)

    id2 = self.canvas.mpl_connect('key_press_event',
                                  self._switch_on_zoom_mode)
    id3 = self.canvas.mpl_connect('key_release_event',
                                  self._switch_off_zoom_mode)

    self._ids_zoom = id1, id2, id3

    self._zoom_mode = event.key

    self.press(event)


def is_just_outside(fig, event):
    x, y = event.x, event.y
    print "x:", x, y
    for ax in fig.axes:
        xAxes, yAxes = ax.transAxes.inverted().transform([x, y])
        print "xAxes:", xAxes, yAxes
        # if (-0.02 < xAxes < 0) | (1 < xAxes < 1.02):
        #     print "just outside x-axis"
        # if (-0.02 < yAxes < 0) | (1 < yAxes < 1.02):
        #     print "just outside y-axis"
        if (xAxes < 0) | (1 < xAxes):
            print "just outside x-axis"
        if (yAxes < 0) | (1 < yAxes):
            print "just outside y-axis"


x = np.linspace(-np.pi, np.pi, 100)
y = np.sin(x)
fig = plt.figure()
plt.plot(x, y)
ax = fig.add_subplot(111)
fig.canvas.mpl_connect('button_press_event', lambda e: is_just_outside(fig, e))
circ = patches.Circle((0.6, 0.5), 0.25, transform=ax.transAxes,
                      facecolor='yellow', alpha=0.5)
ax.add_patch(circ)
plt.show()
