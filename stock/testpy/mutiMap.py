import multiprocessing
import time

import tushare as ts

import pyQuant.stock.singleAnalyseUtil as sl

start = time.time()

# import realdatajson as rl

gold = {}
goldl = []
df = ts.get_today_all()
top = df[df['changepercent'] > 10]
print "top:", len(top['code'])
# for code in top['code']:
#     ave=sl.get_single_ave_compare(code)


# Make the Pool of workers
# pool = ThreadPool(4)
pool = multiprocessing.Pool(processes=8)
# Open the urls in their own threads
# and return the results
# print urllib2.urlopen('http://www.baidu.com')
results = []
for code in top['code']:
    # msg = "hello %d" %(i)
    # results.append(pool.apply_async(sl.get_today_tick_ave(code)))
    results.append(pool.map(sl.get_today_tick_ave(code)))
#close the pool and wait for the work to finish
pool.close()
pool.join()
elapsed_per = (time.time() - start)
# for x in results:
#     print x
# print elapsed_per
