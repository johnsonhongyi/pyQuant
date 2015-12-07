####
# This sample is published as part of the blog article at www.toptal.com/blog
# Visit www.toptal.com/blog and subscribe to our newsletter to read great posts
####

import logging
import os
import Queue
from threading import Thread
from time import time
import maptest as mp

# from download import setup_download_dir, get_links, download_link
import singleAnalyseUtil as sl
import tushare as ts

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)

counter = 0
class DownloadWorker(Thread):

    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        global counter
        counter += 1
        # while True:
            # Get the work from the queue and expand the tuple
        code = self.queue.get()
        print "I am %s, set counter:%s" % (self.name, counter)
        sl.get_multiday_ave_compare_silent(code)
        self.queue.task_done()


from multiprocessing.dummy import Pool as ThreadPool


def main(codes):
    print "start thread"
    ts = time()
    # codes=sl.get_all_toplist()


    # pool = ThreadPool()


    # client_id = os.getenv('IMGUR_CLIENT_ID')
    # if not client_id:
    #     raise Exception("Couldn't find IMGUR_CLIENT_ID environment variable!")
    # download_dir = setup_download_dir()
    # links = [l for l in get_links(client_id) if l.endswith('.jpg')]
    # Create a queue to communicate with the worker threads
    queue = Queue.Queue()
    if len(codes) >=8:
        thread_n=8
    else:
        thread_n=len(codes)
    # Create 8 worker threads
    print "thread is ::::",thread_n
    print ""
    for x in range(thread_n):
        worker = DownloadWorker(queue)
        # Setting daemon to True will let the main thread exit even though the workers are blocking
        worker.daemon = True
        worker.start()
    # Put the tasks into the queue as a tuple
    for code in codes:
        logger.info('Queueing {}'.format(code))
        queue.put((code))
    # Causes the main thread to wait for the queue to finish processing all the tasks
    queue.join()
    logging.info('Took %s', time() - ts)
    # print('Took %s', time() - ts)

if __name__ == '__main__':
    # codes=mp.get_all_top()
    # main(codes)
    df = ts.get_sina_dd('601198','2015-11-20')
    print df
