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

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

x = np.arange(0, 2*np.pi, 0.1)
y = np.sin(x)

fig, axes = plt.subplots(nrows=6)

styles = ['r-', 'g-', 'y-', 'm-', 'k-', 'c-']
def plot(ax, style):
    return ax.plot(x, y, style, animated=True)[0]
lines = [plot(ax, style) for ax, style in zip(axes, styles)]

def animate(i):
    for j, line in enumerate(lines, start=1):
        line.set_ydata(np.sin(j*x + i/10.0))
    return lines

# We'd normally specify a reasonable "interval" here...
ani = animation.FuncAnimation(fig, animate, xrange(1, 200), interval=0, blit=True)
# ani = animation.FuncAnimation(fig, animate, xrange(1, 200),interval=50, blit=False)
plt.show()