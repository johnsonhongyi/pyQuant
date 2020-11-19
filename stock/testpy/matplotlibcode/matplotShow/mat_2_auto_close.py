# -*- coding: utf-8 -*-
# @Author: xiaodong
# @Date:   2017-03-07 19:45:53
# @Last Modified by:   xiaodong
# @Last Modified time: 2017-03-07 20:04:07
from time import sleep
from threading import Thread
from matplotlib import pyplot as plt


def show():
    plt.plot(range(10))
    plt.show()

def close(time):
    sleep(time)
    plt.close()

thread1 = Thread(target=close, args=(5,))

thread1.start()
show()