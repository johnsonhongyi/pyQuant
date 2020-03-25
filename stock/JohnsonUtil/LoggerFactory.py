# -*- coding: UTF-8 -*-
'''
Created on 2015-3-11
@author: Casey
'''
import logging
import sys,os
# from logging.handlers import RotatingFileHandler
from LoggerFactoryMultiprocess import MultiprocessHandler
# sys.path.append("..")
import ipykernel.iostream 
# from logbook import StderrHandler
# from commonTips import RamBaseDir as rbd
# print sys.modules
# try:
#     from commonTips import *
#     print "imp",commonTips.get_os_system()
# except ImportError:
#     print "a"
#     cct = sys.modules['/Users/Johnson/Documents/Quant/pyQuant/stock/JohnsonUtil/' + 'commonTips']
#     print cct.get_os_system()
    
# Hack to import something without circular import issue
# def load_module(name):
#     """Load module using imp.find_module"""
#     import imp
#     names = name.split(".")
#     path = None
#     for name in names:
#         print name,path
#         f, path, info = imp.find_module(name, path)
#         path = [path]
#     return imp.load_module(name, f, path[0], info)
# constants = load_module("commonTips")    
# print constants    

win10_ramdisk_triton = r'E:'
win10_ramdisk_root = r'R:'
mac_ramdisk_root = r'/Volumes/RamDisk' 
path_sep = os.path.sep
ramdisk_rootList = [win10_ramdisk_triton,win10_ramdisk_root, mac_ramdisk_root]

def get_log_file(log_n='stock.log'):
    basedir = None
    for root in ramdisk_rootList:
        basedir = root.replace('/', path_sep).replace('\\', path_sep)
        if os.path.exists(basedir):
            break
    if os.path.exists(basedir):
        path = basedir + os.path.sep
        # print basedir,path
    else:
        # path = os.getcwd()
        path = os.path.split(os.path.abspath(sys.argv[0]))[0]
        alist = path.split('stock')
        if len(alist) > 0:
            path = alist[0]
            # os_sep=get_os_path_sep()
            path = path + 'stock' + os.path.sep
        else:
            print "error"
            raise TypeError('log path error.')

    path = path + log_n
    return path

'''
传入名称
'''
#global log_path
#print get_run_path()
# log_path = get_run_path() + 'stock.log'
#print log_path
CRITICAL = 50
FATAL = CRITICAL
ERROR = 40
WARNING = 30
WARN = WARNING
INFO = 20
DEBUG = 10
NOTSET = 0

# print(log_path)

# http://blog.sina.com.cn/s/blog_411fed0c0100wkvj.html


def testlog():
    #logging.basicConfig(filename="test.log",level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # create file handler which logs even debug messages
    fh = logging.FileHandler('test.log')
    fh.setLevel(logging.DEBUG)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)

def getLogger(name=None,logpath=None,writemode='a',show_detail=True):

    if logpath is None:
        log_f = get_log_file(log_n='stock.log')
    else:
        log_f = logpath
    # logging.basicConfig(
    #         level=logging.ERROR,
    #         format=_logformat,
    #         datefmt='%m-%d %H:%M',
    #         filename=log_f,
    #         filemode=writemode);
    logger = logging.getLogger(name)
    '''
    #jupyter Notebook
    if len(logger.handlers) > 0:
        print "name:%s handlers:%s stdout:%s"%(name,logger.handlers,sys.stdout)
        logger.handlers.pop()
    else:
        logger.propagate = False
        print "name:%s no handlers,stdout:%s"%(name,sys.stdout)
    if isinstance(type(sys.stderr),ipykernel.iostream.OutStream):
        print 'ipython'
        stdout = sys.stdout
        stderr = sys.stderr
    '''
    logger.setLevel(logging.ERROR)
    # create file handler which logs even debug messages
    
    # handler = logging.FileHandler(log_f)
    # handler.setLevel(logging.DEBUG)
    # create console handler with a higher log level
    '''
    if len(logger.handlers) > 0:
        ch = logger.handlers[0].stream
        # print "name:%s handlers:%s stdout:%s"%(name,logger.handlers[0],sys.stdout)
    else:
        ch = logging.StreamHandler()
    '''
    ch = logging.StreamHandler()
    # ch.setLevel(logging.ERROR)
    # create formatter and add it to the handlers
    # print "handeer",len(logger.handlers)
    # formatter = logging.Formatter(name + ': LINE %(lineno)-4d : %(levelname)-8s %(message)s');
    # formatter = logging.Formatter( '%(levelname)-5s %(message)s');



    # handler = RotatingFileHandler(log_f, maxBytes=2*1000*1000, 
    #                              backupCount=1, encoding=None, delay=0)
    
     # handler = RotatingFileHandler(log_f, maxBytes=2*1000*1000, 
     #                             backupCount=1, encoding=None, delay=0)

    handler = MultiprocessHandler(log_f, when='D')
    # handler = MultiprocessHandler(log_f, when='S')


    # fh_formatter = logging.Formatter( '%(filename)s(%(funcName)s:%(lineno)s):%(levelname)-5s %(message)s');
    if show_detail:
        handler_logformat = logging.Formatter("[%(asctime)s] %(levelname)s:%(filename)s(%(funcName)s:%(lineno)s): %(message)s")
        ch_formatter = logging.Formatter("[%(asctime)s] %(levelname)s:%(filename)s(%(funcName)s:%(lineno)s): %(message)s");
    else:
        handler_logformat = logging.Formatter("(%(funcName)s:%(lineno)s): %(message)s")
        ch_formatter = logging.Formatter("%(funcName)s:%(lineno)s): %(message)s");
    
    handler.setFormatter(handler_logformat)
    ch.setFormatter(ch_formatter)
    logger.addHandler(ch)
    logger.addHandler(handler)
    return logger

log = getLogger(show_detail=True)
# sys.stdout = log.handlers[0].stream
# sys.stderr = log.handlers[0].stream
# def log_format(record, handler):
#     handler = StderrHandler()
#     # handler.format_string = '{record.channel}: {record.message}'
#     handler.format_string = '{record.channel}: {record.message) [{record.extra[cwd]}]'
#     return record.message
#
#     # from logbook import FileHandler
#     # log_handler = FileHandler('application.log')
#     # log_handler.push_application()


def set_log_file(console, level_s='DEBUG'):
    console = logging.StreamHandler()
    console.setLevel(eval('logging.%s' % level_s))
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)


class JohnsonLoger(logging.Logger):
    """
    Custom logger class with additional levels and methods
    """
    # WARNPFX = logging.WARNING+1
    # CRITICAL = 50
    # FATAL = CRITICAL
    # ERROR = 40
    # WARNING = 30
    # WARN = WARNING
    # INFO = 20
    # DEBUG = 10
    # NOTSET = 0

    def __init__(self, name):
        # now = time.strftime('%Y-%m-%d %H:%M:%S')
        # path_sep = get_os_path_sep()
        self.name=name
        log_path = get_run_path() + 'stock.log'
        logging.basicConfig(
            # level    =eval('logging.%s'%(level_s)),
            # level=DEBUG,
            # format   = now +":" + name + ' LINE %(lineno)-4d  %(levelname)-8s %(message)s',
            format="[%(asctime)s] %(name)s:%(levelname)s: %(message)s",
            datefmt='%m-%d %H:%M',
            filename=log_path,
#            filemode='w');
            filemode='a');
        self.console=logging.StreamHandler();
        self.console.setLevel(logging.DEBUG);
        formatter = logging.Formatter(self.name + ': LINE %(lineno)-4d :%(levelname)-8s %(message)s');
        self.console.setFormatter(formatter);
        self.logger = logging.getLogger(self.name)
        self.logger.addHandler(self.console);
        self.setLevel(ERROR)

        # return self.logger

    def warnpfx(self, msg, *args, **kw):
        self.log(self.WARNPFX, "! PFXWRN %s" % msg, *args, **kw)

    def setLevel(self, level):
        self.logger.setLevel(level)
        return self.logger

    def debug(self,message):
        self.logger.debug(message)

    def info(self,message):
        self.logger.info(message)

    def warn(self,message):
        self.logger.warn(message)

    def error(self,message):
        self.logger.error(message)

    def cri(self,message):
        self.logger.critical(message)
    # logging.setLoggerClass(CheloExtendedLogger)
    # rrclogger = logging.getLogger("rrcheck")
    # rrclogger.setLevel(logging.INFO)

# def set_log_format():
#     console = logging.StreamHandler()
#     console.setLevel(logging.WARNING)
#     formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
#     console.setFormatter(formatter)
#     logging.getLogger('').addHandler(console)

if __name__ == '__main__':
    getLogger("www").debug("www")
#    log=JohnsonLoger("www").setLevel(DEBUG)
#   pass