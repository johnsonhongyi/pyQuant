#-*- coding: UTF-8 -*-
'''
Created on 2015-3-11
@author: Casey
'''
import logging
import time
'''
传入名称
'''
# http://blog.sina.com.cn/s/blog_411fed0c0100wkvj.html
def getLogger(name):
        now = time.strftime('%Y-%m-%d %H:%M:%S')

        logging.basicConfig(
            level    = logging.DEBUG,
            format   = now +":" + name + ' LINE %(lineno)-4d  %(levelname)-8s %(message)s',
            datefmt  = '%m-%d %H:%M',
            filename =  "stock.log",
            filemode = 'a');

        console = logging.StreamHandler();
        console.setLevel(logging.DEBUG);
        formatter = logging.Formatter(name + ': LINE %(lineno)-4d : %(levelname)-8s %(message)s');
        console.setFormatter(formatter);

        logger = logging.getLogger(name)
        logger.addHandler(console);
        return logger

if __name__ == '__main__':
    getLogger("www").debug("www")