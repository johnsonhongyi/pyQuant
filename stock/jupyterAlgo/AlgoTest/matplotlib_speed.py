# -*- coding:utf-8 -*-
# from pylab import *
# import time

# ion()
# fig = figure()
# ax1 = fig.add_subplot(611)
# ax2 = fig.add_subplot(612)
# ax3 = fig.add_subplot(613)
# ax4 = fig.add_subplot(614)
# ax5 = fig.add_subplot(615)
# ax6 = fig.add_subplot(616)

# x = arange(0,2*pi,0.01)
# y = sin(x)
# line1, = ax1.plot(x, y, 'r-')
# line2, = ax2.plot(x, y, 'g-')
# line3, = ax3.plot(x, y, 'y-')
# line4, = ax4.plot(x, y, 'm-')
# line5, = ax5.plot(x, y, 'k-')
# line6, = ax6.plot(x, y, 'p-')

# # turn off interactive plotting - speeds things up by 1 Frame / second
# plt.ioff()


# tstart = time.time()               # for profiling
# for i in arange(1, 200):
#     line1.set_ydata(sin(x+i/10.0))  # update the data
#     line2.set_ydata(sin(2*x+i/10.0))
#     line3.set_ydata(sin(3*x+i/10.0))
#     line4.set_ydata(sin(4*x+i/10.0))
#     line5.set_ydata(sin(5*x+i/10.0))
#     line6.set_ydata(sin(6*x+i/10.0))
#     draw()                         # redraw the canvas

# print 'FPS:' , 200/(time.time()-tstart)

#2 speed 10fps
# import matplotlib.pyplot as plt
# import numpy as np
# import time

# x = np.arange(0, 2*np.pi, 0.01)
# y = np.sin(x)

# fig, axes = plt.subplots(nrows=6)
# styles = ['r-', 'g-', 'y-', 'm-', 'k-', 'c-']
# lines = [ax.plot(x, y, style)[0] for ax, style in zip(axes, styles)]

# fig.show()

# tstart = time.time()
# for i in xrange(1, 20):
#     for j, line in enumerate(lines, start=1):
#         line.set_ydata(np.sin(j*x + i/10.0))
#     fig.canvas.draw()

# print 'FPS:' , 20/(time.time()-tstart)


#3 speed
# import matplotlib.pyplot as plt
# import numpy as np
# import time

# x = np.arange(0, 2*np.pi, 0.1)
# y = np.sin(x)

# fig, axes = plt.subplots(nrows=6)

# fig.show()

# # We need to draw the canvas before we start animating...
# fig.canvas.draw()

# styles = ['r-', 'g-', 'y-', 'm-', 'k-', 'c-']
# def plot(ax, style):
#     return ax.plot(x, y, style, animated=True)[0]
# lines = [plot(ax, style) for ax, style in zip(axes, styles)]

# # Let's capture the background of the figure
# backgrounds = [fig.canvas.copy_from_bbox(ax.bbox) for ax in axes]

# tstart = time.time()
# for i in xrange(1, 2000):
#     items = enumerate(zip(lines, axes, backgrounds), start=1)
#     for j, (line, ax, background) in items:
#         fig.canvas.restore_region(background)
#         line.set_ydata(np.sin(j*x + i/10.0))
#         ax.draw_artist(line)
#         fig.canvas.blit(ax.bbox)
# plt.show()
# print 'FPS:' , 2000/(time.time()-tstart) 
# 


# 4 speed

# import matplotlib.pyplot as plt
# import matplotlib.animation as animation
# import numpy as np

# x = np.arange(0, 2*np.pi, 0.1)
# y = np.sin(x)

# fig, axes = plt.subplots(nrows=6)

# styles = ['r-', 'g-', 'y-', 'm-', 'k-', 'c-']
# def plot(ax, style):
#     return ax.plot(x, y, style, animated=True)[0]
# lines = [plot(ax, style) for ax, style in zip(axes, styles)]

# def animate(i):
#     for j, line in enumerate(lines, start=1):
#         line.set_ydata(np.sin(j*x + i/10.0))
#     return lines

# # We'd normally specify a reasonable "interval" here...
# ani = animation.FuncAnimation(fig, animate, xrange(1, 200), interval=0, blit=True)
# # ani = animation.FuncAnimation(fig, animate, xrange(1, 200),interval=50, blit=False)
# plt.show()
# 


#!/usr/bin/env python

import numpy as np
import time
import matplotlib
# matplotlib.use('GTKAgg')
from matplotlib import pyplot as plt


def randomwalk(dims=(256, 256), n=20, sigma=5, alpha=0.95, seed=1):
    """ A simple random walk with memory """

    r, c = dims
    gen = np.random.RandomState(seed)
    pos = gen.rand(2, n) * ((r,), (c,))
    old_delta = gen.randn(2, n) * sigma

    while True:
        delta = (1. - alpha) * gen.randn(2, n) * sigma + alpha * old_delta
        pos += delta
        for ii in xrange(n):
            if not (0. <= pos[0, ii] < r):
                pos[0, ii] = abs(pos[0, ii] % r)
            if not (0. <= pos[1, ii] < c):
                pos[1, ii] = abs(pos[1, ii] % c)
        old_delta = delta
        yield pos


def run(niter=1000, doblit=True):
    """
    Display the simulation using matplotlib, optionally using blit for speed
    """

    fig, ax = plt.subplots(1, 1)
    ax.set_aspect('equal')
    ax.set_xlim(0, 255)
    ax.set_ylim(0, 255)
    ax.hold(True)
    rw = randomwalk()
    x, y = rw.next()

    plt.ion()
    # plt.show(False)
    plt.draw()

    if doblit:
        # cache the background
        background = fig.canvas.copy_from_bbox(ax.bbox)

    points = ax.plot(x, y, 'o')[0]
    tic = time.time()

    for ii in xrange(niter):

        # update the xy data
        x, y = rw.next()
        points.set_data(x, y)

        if doblit:
            # restore background
            fig.canvas.restore_region(background)

            # redraw just the points
            ax.draw_artist(points)

            # fill in the axes rectangle
            fig.canvas.blit(ax.bbox)

        else:
            # redraw everything
            fig.canvas.draw()

    plt.close(fig)
    print "Blit = %s, average FPS: %.2f" % (
        str(doblit), niter / (time.time() - tic))

if __name__ == '__main__':
    run(doblit=False)
    run(doblit=True)

import sys
sys.exit(0)
#实时显示随机数据
#
import numpy as np 
import matplotlib.pyplot as plt 
from matplotlib.widgets import Slider, Button, RadioButtons 
  
fig, ax = plt.subplots() 
plt.subplots_adjust(left=0.25, bottom=0.25) 
t = np.arange(0.0, 1.0, 0.001) 
a0 = 5 
f0 = 3 
s = a0*np.sin(2*np.pi*f0*t) 
l, = plt.plot(t, s, lw=2, color='red') 
plt.axis([0, 1, -10, 10]) 
  
axcolor = 'lightgoldenrodyellow' 
axfreq = plt.axes([0.25, 0.1, 0.65, 0.03], axisbg=axcolor) 
axamp = plt.axes([0.25, 0.15, 0.65, 0.03], axisbg=axcolor) 
  
sfreq = Slider(axfreq, 'Freq', 0.1, 30.0, valinit=f0) 
samp = Slider(axamp, 'Amp', 0.1, 10.0, valinit=a0) 

def update(val): 
     amp = samp.val 
     freq = sfreq.val 
     l.set_ydata(amp*np.sin(2*np.pi*freq*t)) 
     fig.canvas.draw_idle() 
sfreq.on_changed(update) 
samp.on_changed(update) 
  
resetax = plt.axes([0.8, 0.025, 0.1, 0.04]) 
button = Button(resetax, 'Reset', color=axcolor, hovercolor='0.975') 

def reset(event): 
     sfreq.reset() 
     samp.reset() 
button.on_clicked(reset) 
  
rax = plt.axes([0.025, 0.5, 0.15, 0.15], axisbg=axcolor) 
radio = RadioButtons(rax, ('red', 'blue', 'green'), active=0) 

def colorfunc(label): 
     l.set_color(label) 
     fig.canvas.draw_idle() 
radio.on_clicked(colorfunc) 
  
plt.show()

import sys
sys.exit(0)

import matplotlib.pyplot as plt
import numpy as np

t = np.arange(0.01, 5.0, 0.01)
s1 = np.sin(2*np.pi*t)
s2 = np.exp(-t)
s3 = np.sin(4*np.pi*t)

ax1 = plt.subplot(311)
plt.plot(t, s1)
plt.setp(ax1.get_xticklabels(), fontsize=6)

# share x only
ax2 = plt.subplot(312, sharex=ax1)
plt.plot(t, s2)
# make these tick labels invisible
plt.setp(ax2.get_xticklabels(), visible=False)

# share x and y
ax3 = plt.subplot(313, sharex=ax1, sharey=ax1)
plt.plot(t, s3)
plt.xlim(0.01, 5.0)
import sys
sys.path.append('../../')
from JohnsonUtil import zoompan
zp = zoompan.ZoomPan()
figZoom = zp.zoom_factory(ax1, base_scale=1.1)
figPan = zp.pan_factory(ax1)
plt.show()