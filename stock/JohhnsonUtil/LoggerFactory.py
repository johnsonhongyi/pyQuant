# -*- coding: UTF-8 -*-
'''
Created on 2015-3-11
@author: Casey
'''
import logging
import sys
sys.path.append("..")
import commonTips as cct

# from logbook import StderrHandler

'''
传入名称
'''
log_path = cct.get_run_path() + 'stock.log'

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
def getLogger(name):
    # now = time.strftime('%Y-%m-%d %H:%M:%S')
    # path_sep = cct.get_os_path_sep()
    logging.basicConfig(
        # level    =eval('logging.%s'%(level_s)),
        # level=logging.DEBUG,
        # format   = now +":" + name + ' LINE %(lineno)-4d  %(levelname)-8s %(message)s',
        format="[%(asctime)s] %(name)s:%(levelname)s: %(message)s",
        datefmt='%m-%d %H:%M',
        filename=log_path,
        filemode='w');

    console = logging.StreamHandler();
    console.setLevel(logging.DEBUG);
    formatter = logging.Formatter(name + ': LINE %(lineno)-4d : %(levelname)-8s %(message)s');
    console.setFormatter(formatter);
    logger = logging.getLogger(name)
    logger.addHandler(console);
    return logger


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


class CheloExtendedLogger(logging.Logger):
    """
    Custom logger class with additional levels and methods
    """
    WARNPFX = logging.WARNING+1

    def __init__(self, name):
        logging.Logger.__init__(self, name, logging.DEBUG)

        logging.addLevelName(self.WARNPFX, 'WARNING')

        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG)
        # create formatter and add it to the handlers
        formatter = logging.Formatter("%(asctime)s [%(funcName)s: %(filename)s,%(lineno)d] %(message)s")
        console.setFormatter(formatter)

        # add the handlers to logger
        self.addHandler(console)

        return

    def warnpfx(self, msg, *args, **kw):
        self.log(self.WARNPFX, "! PFXWRN %s" % msg, *args, **kw)


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
