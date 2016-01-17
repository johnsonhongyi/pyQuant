# -*- coding:utf-8 -*-
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
        self.xzoom = True
        self.yzoom = True
        self.cidBP = None
        self.cidBR = None
        self.cidBM = None
        self.cidKeyP = None
        self.cidKeyR = None
        self.cidScroll = None
        self.cidbuttonP = None
        self.butto_status = False
        self.lock = False

    def zoom_factory(self, ax, base_scale=2.):
        def zoom(event):
            if not self.lock and location_status(event):
                self.lock = True
                cur_xlim = ax.get_xlim()
                cur_ylim = ax.get_ylim()
                # print "cur-mouse:",cur_xlim,cur_ylim
                xdata = event.xdata  # get event x location
                ydata = event.ydata  # get event y location
                if (xdata is None):
                    return ()
                if (ydata is None):
                    return ()

                if event.button == 'down':
                    # deal with zoom in
                    scale_factor = 1 / base_scale
                elif event.button == 'up':
                    # deal with zoom out
                    scale_factor = base_scale
                else:
                    # deal with something that should never happen
                    scale_factor = 1
                    # print(event.button)

                new_width = (cur_xlim[1] - cur_xlim[0]) * scale_factor
                new_height = (cur_ylim[1] - cur_ylim[0]) * scale_factor

                relx = (cur_xlim[1] - xdata) / (cur_xlim[1] - cur_xlim[0])
                rely = (cur_ylim[1] - ydata) / (cur_ylim[1] - cur_ylim[0])

                if (self.xzoom):
                    ax.set_xlim([xdata - new_width * (1 - relx), xdata + new_width * (relx)])
                if (self.yzoom):
                    ax.set_ylim([ydata - new_height * (1 - rely), ydata + new_height * (rely)])
                ax.figure.canvas.draw()
                ax.figure.canvas.flush_events()
                self.lock = False

        def onKeyPress(event):
            if event.key == 'x':
                self.xzoom = True
                self.yzoom = False
            if event.key == 'y':
                self.xzoom = False
                self.yzoom = True

        def onKeyRelease(event):
            self.xzoom = True
            self.yzoom = True

        def location_status(event):
            x, y = event.x, event.y
            xAxes, yAxes = ax.transAxes.inverted().transform([x, y])
            # print "xAxes:", xAxes, yAxes, round(xAxes, 1), round(yAxes, 1)
            # f = lambda x: int(x) - 1 if int(x) < 0 else int(x) + 1
            # print int(xAxes), f(xAxes)
            # print int(yAxes), f(yAxes)
            if (xAxes < 1) and (0 < xAxes) and (yAxes < 1) and (0 < yAxes):
                return True
            else:
                return False

                # def on_press(event):
                # global g_size
                # print ax.transAxes.inverted()
                # print "trans:",ax.transData.inverted().transform([x, y])

                # if (-0.02 < xAxes < 0) | (1 < xAxes < 1.02):
                #     print "just outside x-axis"
                # if (-0.02 < yAxes < 0) | (1 < yAxes < 1.02):
                #     print "just outside y-axis"

                # if (xAxes < int(xAxes)) | (int(xAxes)+1 < xAxes):
                #     print "just outside x-axis"
                # if (yAxes < int(yAxes)) | (int(yAxes)+1 < yAxes):
                #     print "just outside y-axis"

                # print ax.transAxes.inverted()
                # x, y = event.x, event.y
                # xAxes, yAxes = ax.transAxes.inverted().transform([x, y])
                # print "xAxes:", xAxes, yAxes, round(xAxes, 1), round(yAxes, 1)
                # if ((xAxes < 1) and (0 < xAxes)) and ((yAxes < 1) and (0 < yAxes)):
                #     print("in")
                #     self.butto_status = True
                # else:
                #     print("out")
                #     self.butto_status = False

                # cur_xlim = ax.get_xlim()
                # cur_ylim = ax.get_ylim()
                # print "cur-mouse:",cur_xlim,cur_ylim
                # print dir(event)
                # newx = event.xdata
                # newy = event.ydata
                # print newx
                # print newy
                # 不合理的鼠标点击，直接返回，不绘制
                # if newx == None or newy == None or event.dblclick == True:
                #     self.butto_status = None
                #     return None
                # # 不合理的鼠标点击，直接返回，不绘制
                # if event.button == 1:  # button ==1 代表鼠标左键按下， 是放大图像
                #     self.butto_status = True
                #     # g_size =1
                #     # print "zoom out:%s"%g_size
                # elif event.button == 3:  # button == 3 代表鼠标右键按下， 是缩小图像
                #     self.butto_status = True
                #     # print "zoom in:%s"%g_size
                #
                # else:
                #     # print "other key:%s"%g_size
                #     self.butto_status = None
                #     return None

        fig = ax.get_figure()  # get the figure of interest
        self.cidScroll = fig.canvas.mpl_connect('scroll_event', zoom)
        self.cidKeyP = fig.canvas.mpl_connect('key_press_event', onKeyPress)
        self.cidKeyR = fig.canvas.mpl_connect('key_release_event', onKeyRelease)
        # self.cidbuttonP = fig.canvas.mpl_connect('button_press_event', on_press)
        # self.cidbuttonR = fig.canvas.mpl_connect('button_release_event', on_press)
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
            ax.figure.canvas.flush_events()

        fig = ax.get_figure()  # get the figure of interest

        self.cidBP = fig.canvas.mpl_connect('button_press_event', onPress)
        self.cidBR = fig.canvas.mpl_connect('button_release_event', onRelease)
        self.cidBM = fig.canvas.mpl_connect('motion_notify_event', onMotion)
        # attach the call back

        # return the function
        return onMotion


if __name__ == "__main__":
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

    # def new_modi():
    #     This is a suggestion for a slight modification to the code above - it makes keeping the zoom centred more manageable.
    #     cur_xrange = (cur_xlim[1] - cur_xlim[0])*.5
    #     cur_yrange = (cur_ylim[1] - cur_ylim[0])*.5
    #     xmouse = event.xdata # get event x location
    #     ymouse = event.ydata # get event y location
    #     cur_xcentre = (cur_xlim[1] + cur_xlim[0])*.5
    #     cur_ycentre = (cur_ylim[1] + cur_ylim[0])*.5
    #     xdata = cur_xcentre+ 0.25*(xmouse-cur_xcentre)
    #     ydata = cur_ycentre+ 0.25*(ymouse-cur_ycentre)
