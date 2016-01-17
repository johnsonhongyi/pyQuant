#!/usr/bin/env python

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import ConnectionPatch


def f1(t):
    return np.exp(-t) * np.cos(2 * np.pi * t)


def f11(t):
    return np.exp(-t) * np.cos(2 * np.pi * t + 0.2)


def f111(t):
    return np.exp(-t + 0.2) * np.cos(2 * np.pi * t)


t = np.arange(0.0, 5.0, 0.02)

plt.figure(figsize=(16, 8), dpi=98)
p1 = plt.subplot(121, aspect=5 / 2.5)
p2 = plt.subplot(122, aspect=0.5 / 0.05)

label_f0 = r"$f(t)=e^{-t+\alpha} \cos (2 \pi t+\beta)$"
label_f1 = r"$\alpha=0,\beta=0$"
label_f11 = r"$\alpha=0,\beta=0.2$"
label_f111 = r"$\alpha=0.2,\beta=0$"

p1.plot(t, f1(t), "g", label=label_f1, linewidth=2)
p1.plot(t, f11(t), "r-.", label=label_f11, linewidth=2)
p1.plot(t, f111(t), "b:", label=label_f111, linewidth=2)
p2.plot(t, f1(t), "g", label=label_f1, linewidth=2)
p2.plot(t, f11(t), "r-.", label=label_f11, linewidth=2)
p2.plot(t, f111(t), "b:", label=label_f111, linewidth=2)

# p1.plot(t,f1(t),"g",linewidth=2)
# p1.plot(t,f11(t),"r-.",linewidth=2)
# p1.plot(t,f111(t),"b:",linewidth=2)
# p2.plot(t,f1(t),"g",linewidth=2)
# p2.plot(t,f11(t),"r-.",linewidth=2)
# p2.plot(t,f111(t),"b:",linewidth=2)

p1.axis([0.0, 5.01, -1.0, 1.5])

p1.set_ylabel("v", fontsize=14)
p1.set_xlabel("t", fontsize=14)
# p1.set_title("A simple example",fontsize=18)
p1.grid(True)
p1.legend()

tx = 0.5
ty = 0.9
# p1.text(tx,ty,label_f0,fontsize=15,verticalalignment="top",horizontalalignment="left")

p2.axis([4, 4.5, -0.02, 0.03])
p2.set_ylabel("v", fontsize=14)
p2.set_xlabel("t", fontsize=14)
p2.grid(True)
p2.legend()

# plot the box
tx0 = 4
tx1 = 4.5
ty0 = -0.1
ty1 = 0.1
sx = [tx0, tx1, tx1, tx0, tx0]
sy = [ty0, ty0, ty1, ty1, ty0]
p1.plot(sx, sy, "purple")

# plot patch lines
xy = (4.45, 0.09)
xy2 = (4.02, 0.026)
con = ConnectionPatch(xyA=xy2, xyB=xy, coordsA="data", coordsB="data",
                      axesA=p2, axesB=p1)
p2.add_artist(con)

xy = (4.45, -0.09)
xy2 = (4.02, -0.018)
con = ConnectionPatch(xyA=xy2, xyB=xy, coordsA="data", coordsB="data",
                      axesA=p2, axesB=p1)
p2.add_artist(con)

plt.show()
