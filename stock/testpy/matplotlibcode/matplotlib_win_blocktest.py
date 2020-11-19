from math import *
from matplotlib import pyplot as plt
print plt.get_backend()
def main():
    x = range(-50, 51, 1)
    for pow in range(1,5):   # plot x^1, x^2, ..., x^4
        y = [Xi**pow for Xi in x]
        print y
        plt.plot(x, y)
        plt.draw()
        #plt.show()             #this plots correctly, but blocks execution.
        plt.show(block=False)   #this creates an empty frozen window.
        _ = raw_input("Press [enter] to continue.")


# if __name__ == '__main__':
#     main()


import numpy as np
from matplotlib import pyplot as plt

def main2():
    plt.axis([-50,50,0,10000])
    plt.ion()
    plt.show()

    x = np.arange(-50, 51)
    for pow in range(1,5):   # plot x^1, x^2, ..., x^4
        y = [Xi**pow for Xi in x]
        plt.plot(x, y)
        plt.draw()
        plt.pause(0.001)
        raw_input("Press [enter] to continue.")

import numpy as np
import matplotlib.pyplot as plt

def realtime():
    plt.axis([0, 10, 0, 1])

    for i in range(10):
        y = np.random.random()
        plt.scatter(i, y)
        plt.pause(0.05)

    plt.show()


# if __name__ == '__main__':
#     # main()
#     print("main2-------------")
#     # main2()
#     realtime()

import numpy as np
import time
import matplotlib
matplotlib.use('GTKAgg')
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

    plt.show(block=False)
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
    # run(doblit=False)
    run(doblit=True)