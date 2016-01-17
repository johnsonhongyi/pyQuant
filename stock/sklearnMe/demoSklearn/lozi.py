# -*- coding: utf-8 -*-

# 需要安装matplotlib、numpy等库才能运行
import time

import numpy as np
import pylab as pl
from matplotlib import cm


def iter_point2(x, y):
    # 初始化公式的参数，需要改的话，可以改参数
    a = 1
    b = 1.75
    iter = 0  # 初始化迭代次数
    for i in xrange(1, 10):
        iter = i
        dist = (x * x + y * y)  # 计算摸长，看是否超过最大限度
        dist *= dist
        # print "dist:" + str(dist)
        if dist > 200:  # 如果超出了最大长度，就跳出循环，返回这个迭代次数
            break
        # 临时保存一下x和y
        tempx = x
        tempy = y
        # 这里是公式 X = a-b|x| + y ; Y = 0.3x;
        x = a - b * abs(tempx) + tempy
        y = 0.3 * tempx
    return iter


# 绘制图形时，以cx，xy为中心，距离为d
def draw_lozi(cx, cy, d):
    size = 400
    x0, x1, y0, y1 = cx - d, cx + d, cy - d, cy + d
    y, x = np.ogrid[y1:y0:size * 1j, x0:x1:size * 1j]  # 使用范围生成数组，后面用这个进行迭代
    c = x + y * 1j
    x.shape = -1  # 转化成线性数组
    y.shape = -1

    start = time.clock()
    lozi = np.ones(c.shape)
    # 遍历每一个点，计算迭代次数，赋值给数组lozi
    for j in range(0, size):
        for i in range(0, size):
            lozi[j][i] = iter_point2(x[i], y[j])
            pass

    pl.cla()

    # 使用数组lozi，绘图， 使用蓝色调色板，显示到图上的坐标范围是x0,x1,y0,y1
    pl.imshow(lozi, cmap=cm.Blues_r, extent=[x0, x1, y0, y1])
    # 不显示横纵坐标
    # pl.gca().set_axis_off()
    # 刷新画布
    print "time:", time.clock() - start
    # pl.ion()
    # pl.show()
    pl.draw()


# 鼠标点击触发执行的函数
def on_press(event):
    global g_size
    print event
    print dir(event)
    newx = event.xdata
    newy = event.ydata
    print newx
    print newy

    # 不合理的鼠标点击，直接返回，不绘制
    if newx == None or newy == None or event.dblclick == True:
        return None
    # 不合理的鼠标点击，直接返回，不绘制
    if event.button == 1:  # button ==1 代表鼠标左键按下， 是放大图像
        g_size /= 2
        # g_size =1
        print "zoom out:%s" % g_size
    elif event.button == 3:  # button == 3 代表鼠标右键按下， 是缩小图像
        g_size *= 2
        print "zoom in:%s" % g_size

    else:
        print "other key:%s" % g_size
        return None
    print "g_size:", g_size

    draw_lozi(newx, newy, g_size)


fig, ax = pl.subplots(1)

g_size = 4.5
print ("init:", g_size)

# 注册鼠标事件
fig.canvas.mpl_connect('button_press_event', on_press)

# 初始绘制一个图
draw_lozi(0, 0, g_size)
pl.show()
# raw_input(">>")
