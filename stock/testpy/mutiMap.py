# -*- coding:utf-8 -*-
# !/usr/bin/env python
import sys
# import multiprocessing
# import time

# import tushare as ts


# start = time.time()

# # import realdatajson as rl

# gold = {}
# goldl = []
# df = ts.get_today_all()
# top = df[df['changepercent'] > 10]
# print "top:", len(top['code'])
# # for code in top['code']:
# #     ave=sl.get_single_ave_compare(code)


# # Make the Pool of workers
# # pool = ThreadPool(4)
# pool = multiprocessing.Pool(processes=8)
# # Open the urls in their own threads
# # and return the results
# # print urllib2.urlopen('http://www.baidu.com')
# results = []
# for code in top['code']:
#     # msg = "hello %d" %(i)
#     # results.append(pool.apply_async(sl.get_today_tick_ave(code)))
#     results.append(pool.map(sl.get_today_tick_ave(code)))
# #close the pool and wait for the work to finish
# pool.close()
# pool.join()
# elapsed_per = (time.time() - start)
from functools import partial
import multiprocessing

def print_it(x=1,y=2):
    print x,y

xs = [0,1,2,3,4,5,6]
y = 0
# z = 2
func = partial(print_it,y=y)

cores = multiprocessing.cpu_count()
# pool = multiprocessing.Pool(processes=cores)
pool = multiprocessing.Pool(processes=3)
pool.map(func, xs)

pool.close()
pool.join()

# sys.exit()


import time
def f(x):
    return x * x

cores = multiprocessing.cpu_count()
pool = multiprocessing.Pool(processes=cores)
xs = range(300)

# method 1: map
results = pool.map_async(f, xs).get()
# print results
# print pool.map(f, xs)  # prints [0, 1, 4, 9, 16]

# method 2: imap
# for y in pool.imap(f, xs):
#     print y            # 0, 1, 4, 9, 16, respectively

# method 3: imap_unordered
# for y in pool.imap_unordered(f, xs):
#     print(y)           # may be in any order
results = []
from tqdm import tqdm
# for y in tqdm(pool.imap_unordered(f, xs),unit='%',unit_scale=False,total=len(xs),ncols=2):
try:
    # for y in tqdm(pool.apply_async(f, args=(xs,)),unit='%',unit_scale=False,total=len(xs),ncols=2):
     # [x.get() for x in [pool.apply_async(f, (x,)) for x in xs]]
    time_s = time.time()
    # for y in tqdm(pool.map_async(f, xs).get(),unit='%',unit_scale=True,total=len(xs),ncols=2):
    for y in tqdm(pool.map(f, xs),unit='%',mininterval=2,unit_scale=True,total=len(xs),ncols=3):
    # for y in tqdm([x.get() for x in [pool.apply_async(f, (x,)) for x in xs]],unit='%',unit_scale=False,total=len(xs),ncols=2):
        time.sleep(0.001)
        results.append(y)
except Exception as e:
    print e
else:
    pass
finally:
    pass
pool.close()
pool.join()
print "t:%s"%(time.time()-time_s)
print results[:10]
# print(results) 
#!/usr/bin/env python
# import itertools
# import logging
# import multiprocessing
# import time

# def compute(i):
#     time.sleep(.5)
#     return i**2

# if __name__ == "__main__":
#     logging.basicConfig(format="%(asctime)-15s %(levelname)s %(message)s",
#                         datefmt="%F %T", level=logging.DEBUG)
#     pool = multiprocessing.Pool()
#     try:
#         for square in pool.imap_unordered(compute, itertools.count(), chunksize=10):
#             logging.debug(square) # report progress by printing the result
#     except KeyboardInterrupt:
#         logging.warning("got Ctrl+C")
#     finally:
#         pool.terminate()
#         pool.join()


sys.exit()
import multiprocessing
from threading import Lock, Thread
from queue import Queue
import time
import sys

q = Queue()

# numTag和Lock用来演示多线程同步
numTag = 0
lock = Lock()

"""
    用来演示输出
"""
def print_num(item):
    # time.sleep(0.01)
    # 声明numTag是全局变量，所有的线程都可以对其进行修改
    global numTag
    with lock:
        numTag += 1
        # 输出的时候加上'\r'可以让光标退到当前行的开始处，进而实现显示进度的效果
        sys.stdout.write('\rQueue Item: {0}\tNumTag:{1}%'.format(str(item), str(numTag)))

"""
    worker是一个中间件，把Queue接收到的值传给对应的功能函数进行处理
"""
def worker():
    while True:
        item = q.get()
        if item is None:
            break
        print_num(item)
        q.task_done()

if __name__ == '__main__':
    # 根据CPU的数量创建对应数量的线程
    threadCount = multiprocessing.cpu_count()
    for i in range(threadCount):
        t = Thread(target=worker)
        # 设置daemon为True, 可以让线程在主线程退出的时候一起结束
        # 否则线程还会继续等待
        t.daemon = True
        t.start()

    # 通过Queue给线程传值
    for i in range(100):
        q.put(i)

    q.join()
    print('')