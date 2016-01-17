import numpy
from matplotlib.pyplot import figure, show


class ZoomPan:
    def __init__(self):
        self.press = None
        self.cur_xlim = None
        self.cur_ylim = None
        self.x0 = None
        self.y0 = None
        self.x1 = None
        self.y1 = None
        self.xpress = None
        self.ypress = None

    def zoom_factory(self, ax, base_scale=2.):
        def zoom(event):
            cur_xlim = ax.get_xlim()
            cur_ylim = ax.get_ylim()

            xdata = event.xdata  # get event x location
            ydata = event.ydata  # get event y location

            if event.button == 'down':
                # deal with zoom in
                scale_factor = 1 / base_scale
            elif event.button == 'up':
                # deal with zoom out
                scale_factor = base_scale
            else:
                # deal with something that should never happen
                scale_factor = 1
                print event.button

            new_width = (cur_xlim[1] - cur_xlim[0]) * scale_factor
            new_height = (cur_ylim[1] - cur_ylim[0]) * scale_factor

            relx = (cur_xlim[1] - xdata) / (cur_xlim[1] - cur_xlim[0])
            rely = (cur_ylim[1] - ydata) / (cur_ylim[1] - cur_ylim[0])

            ax.set_xlim([xdata - new_width * (1 - relx), xdata + new_width * (relx)])
            ax.set_ylim([ydata - new_height * (1 - rely), ydata + new_height * (rely)])
            ax.figure.canvas.draw()

        fig = ax.get_figure()  # get the figure of interest
        fig.canvas.mpl_connect('scroll_event', zoom)

        return zoom

    def pan_factory(self, ax):
        def onPress(event):
            if event.inaxes != ax: return
            self.cur_xlim = ax.get_xlim()
            self.cur_ylim = ax.get_ylim()
            self.press = self.x0, self.y0, event.xdata, event.ydata
            self.x0, self.y0, self.xpress, self.ypress = self.press

        def onRelease(event):
            self.press = None
            ax.figure.canvas.draw()

        def onMotion(event):
            if self.press is None: return
            if event.inaxes != ax: return
            dx = event.xdata - self.xpress
            dy = event.ydata - self.ypress
            self.cur_xlim -= dx
            self.cur_ylim -= dy
            ax.set_xlim(self.cur_xlim)
            ax.set_ylim(self.cur_ylim)

            ax.figure.canvas.draw()

        fig = ax.get_figure()  # get the figure of interest

        # attach the call back
        fig.canvas.mpl_connect('button_press_event', onPress)
        fig.canvas.mpl_connect('button_release_event', onRelease)
        fig.canvas.mpl_connect('motion_notify_event', onMotion)

        # return the function
        return onMotion


fig = figure()

ax = fig.add_subplot(111, xlim=(0, 1), ylim=(0, 1), autoscale_on=False)

ax.set_title('Click to zoom')
x, y, s, c = numpy.random.rand(4, 200)
s *= 200

ax.scatter(x, y, s, c)
scale = 1.1
zp = ZoomPan()
figZoom = zp.zoom_factory(ax, base_scale=scale)
figPan = zp.pan_factory(ax)
show()


# other zoom
def zoom(self, event, factor):
    curr_xlim = self.ax.get_xlim()
    curr_ylim = self.ax.get_ylim()

    new_width = (curr_xlim[1] - curr_ylim[0]) * factor
    new_height = (curr_xlim[1] - curr_ylim[0]) * factor

    relx = (curr_xlim[1] - event.xdata) / (curr_xlim[1] - curr_xlim[0])
    rely = (curr_ylim[1] - event.ydata) / (curr_ylim[1] - curr_ylim[0])

    self.ax.set_xlim([event.xdata - new_width * (1 - relx),
                      event.xdata + new_width * (relx)])
    self.ax.set_ylim([event.ydata - new_width * (1 - rely),
                      event.ydata + new_width * (rely)])
    self.draw()


# third zoom

def zoom(self, event):
    '''This function zooms the image upon scrolling the mouse wheel.
    Scrolling it in the plot zooms the plot. Scrolling above or below the
    plot scrolls the x axis. Scrolling to the left or the right of the plot
    scrolls the y axis. Where it is ambiguous nothing happens.
    NOTE: If expanding figure to subplots, you will need to add an extra
    check to make sure you are not in any other plot. It is not clear how to
    go about this.
    Since we also want this to work in loglog plot, we work in axes
    coordinates and use the proper scaling transform to convert to data
    limits.'''

    x = event.x
    y = event.y

    # convert pixels to axes
    tranP2A = self.ax.transAxes.inverted().transform
    # convert axes to data limits
    tranA2D = self.ax.transLimits.inverted().transform
    # convert the scale (for log plots)
    tranSclA2D = self.ax.transScale.inverted().transform

    if event.button == 'down':
        # deal with zoom in
        scale_factor = self.zoom_scale
    elif event.button == 'up':
        # deal with zoom out
        scale_factor = 1 / self.zoom_scale
    else:
        # deal with something that should never happen
        scale_factor = 1

    # get my axes position to know where I am with respect to them
    xa, ya = tranP2A((x, y))
    zoomx = False
    zoomy = False
    if (ya < 0):
        if (xa >= 0 and xa <= 1):
            zoomx = True
            zoomy = False
    elif (ya <= 1):
        if (xa < 0):
            zoomx = False
            zoomy = True
        elif (xa <= 1):
            zoomx = True
            zoomy = True
        else:
            zoomx = False
            zoomy = True
    else:
        if (xa >= 0 and xa <= 1):
            zoomx = True
            zoomy = False

    new_alimx = (0, 1)
    new_alimy = (0, 1)
    if (zoomx):
        new_alimx = (np.array([1, 1]) + np.array([-1, 1]) * scale_factor) * .5
    if (zoomy):
        new_alimy = (np.array([1, 1]) + np.array([-1, 1]) * scale_factor) * .5

    # now convert axes to data
    new_xlim0, new_ylim0 = tranSclA2D(tranA2D((new_alimx[0], new_alimy[0])))
    new_xlim1, new_ylim1 = tranSclA2D(tranA2D((new_alimx[1], new_alimy[1])))

    # and set limits
    self.ax.set_xlim([new_xlim0, new_xlim1])
    self.ax.set_ylim([new_ylim0, new_ylim1])
    self.redraw()
