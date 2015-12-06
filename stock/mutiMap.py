import urllib2
from multiprocessing.dummy import Pool as ThreadPool
import time
import multiprocessing
import stock.emacount as ema
import stock.singleAnalyseUtil as sl
import tushare as ts
start = time.time()


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
