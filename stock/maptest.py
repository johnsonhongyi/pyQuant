from multiprocessing import cpu_count
from multiprocessing.dummy import Pool as ThreadPool

import tushare as ts
# print(cpu_count())
import datetime
import logging
import sys
logger = logging.getLogger(__name__)
#do something
import singleAnalyseUtil as sl
import threading_t as tt

urls = [
    'http://www.python.org', 
    'http://www.python.org/about/',
    'http://www.onlamp.com/pub/a/python/2003/04/17/metaclasses.html',
    'http://www.python.org/doc/',
    'http://www.python.org/download/',
    'http://www.python.org/getit/',
    'http://www.python.org/community/',
    'https://wiki.python.org/moin/',
    'http://planet.python.org/',
    'https://wiki.python.org/moin/LocalUserGroups',
    'http://www.python.org/psf/',
    'http://docs.python.org/devguide/',
    'http://www.python.org/community/awards/'
    # etc.. 
    ]


def div_list(ls,n):
    if not isinstance(ls,list) or not isinstance(n,int):
        return []
    ls_len = len(ls)
    if n<=0 or 0==ls_len:
        return []
    if n > ls_len:
        return []
    elif n == ls_len:
        return [[i] for i in ls]
    else:
        j = (ls_len/n)+1
        k = ls_len%n
        ls_return = []
        for i in xrange(0,(n-1)*j,j):
            ls_return.append(ls[i:i+j])
        ls_return.append(ls[(n-1)*j:])
        return ls_return

def get_all_top():
    gold = {}
    goldl = []
    df = ts.get_today_all()
    top = df[df['changepercent'] > 6]
    # top = df[df['changepercent'] < -2]
    top = top[top['changepercent'] <10]
    # logging.info("top:", len(top['code']))
    list =top['code'].tolist()
    print len(list)
    return list
# Make the Pool of workers
# print cpu_count()

def mainrun(codes=None):

    pool = ThreadPool(cpu_count())
    # pool.
    # pool = ThreadPool(1)
    # # Open the urls in their own threads
    # # and return the results
    # results = pool.map(urllib2.urlopen, urls)
    # #close the pool and wait for the work to finish
    # codes=['000030','601198','601608']
    # codes=['600476']
    if codes==None:
        codes=get_all_top()
    starttime = datetime.datetime.now()
    # results=pool.map(sl.get_multiday_ave_compare_silent,codes)
    # goldl = ['1', '2', '3', '4', '5', '6', '7', '8', '9','10','12','13','14']
    # for x in cpu_count():
    #     eval(pool+str(i))

    # c_num=cpu_count()
    # num=len(goldl)/c_num
    # print num
    # listall=[]
    # count_list=len(goldl)
    # list=div_list(goldl,c_num)
    # print list
    # sys.exit(0)

    # logger = multiprocessing.get_logger()
    # logger.setLevel(logging.INFO)
    # print type(codes)
    c_list=div_list(codes,cpu_count())

    # results=pool.map(sl.get_multiday_ave_compare_silent,codes)

    # results= pool.map(sl.get_multiday_ave_compare_silent_noreal,(codes,60))

    for code in codes:
        results=pool.apply_async(sl.get_multiday_ave_compare_silent_noreal,(code,60))
        # print results
    pool.close()
    pool.join()

    # print results

    # if c_list==[]:
    #     print "MuP"
    #     # pool.map(sl.get_multiday_ave_compare_silent,codes)
    #     for code in codes:
    #         pool.apply_async(sl.get_multiday_ave_compare_silent_noreal,(code,))
    #
    #     pool.close()
    #     pool.join()
    # else:
    #     print "All P"
    #     for code in c_list:
    #             # msg = "hello %d" %(i)
    #             # print code
    #             pool.apply_async(tt.main,(code,))
    #
    #     pool.close()
    #     pool.join()

    # for p in multiprocessing.active_children():
    #         print("child   p.name:" + p.name + "\tp.id" + str(p.pid))
    #         print "END!!!!!!!!!!!!!!!!!"

    endtime = datetime.datetime.now()
    interval=(endtime - starttime).seconds
    print ""
    print "interval:",interval
    # print results


if __name__ == '__main__':
    mainrun()

    sys.exit(0)
    pool = ThreadPool(cpu_count())
    # pool.
    # pool = ThreadPool(1)
    # # Open the urls in their own threads
    # # and return the results
    # results = pool.map(urllib2.urlopen, urls)
    # #close the pool and wait for the work to finish
    # codes=['000030','601198','601608']

    codes=get_all_top()
    starttime = datetime.datetime.now()
    # results=pool.map(sl.get_multiday_ave_compare_silent,codes)
    goldl = ['1', '2', '3', '4', '5', '6', '7', '8', '9','10','12','13','14']
    # for x in cpu_count():
    #     eval(pool+str(i))

    # c_num=cpu_count()
    # num=len(goldl)/c_num
    # print num
    # listall=[]
    # count_list=len(goldl)
    # list=div_list(goldl,c_num)
    # print list
    # sys.exit(0)

    # logger = multiprocessing.get_logger()
    # logger.setLevel(logging.INFO)
    # print type(codes)
    c_list=div_list(codes,cpu_count())

    # results=pool.map(sl.get_multiday_ave_compare_silent,codes)
    # pool.close()
    # pool.join()

    if c_list==[]:
        print "MuP"
        # pool.map(sl.get_multiday_ave_compare_silent,codes)
        for code in codes:
            pool.apply_async(sl.get_multiday_ave_compare_silent,(code,))

        pool.close()
        pool.join()
    else:
        print "All P"
        for code in c_list:
                # msg = "hello %d" %(i)
                # print code
                pool.apply_async(tt.main,(code,))

        pool.close()
        pool.join()

    # for p in multiprocessing.active_children():
    #         print("child   p.name:" + p.name + "\tp.id" + str(p.pid))
    #         print "END!!!!!!!!!!!!!!!!!"

    endtime = datetime.datetime.now()
    interval=(endtime - starttime).seconds
    print ""
    print "interval:",interval
    # print results
