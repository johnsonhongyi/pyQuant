#coding=utf-8
import sys
import time
import multiprocessing
# from multiprocessloghandler import MultiprocessHandler
from LoggerFactoryMultiprocess import MultiprocessHandler

# 定义日志输出格式
formattler = '%(levelname)s - %(name)s - %(asctime)s - %(message)s'
fmt = logging.Formatter(formattler)

# 获得logger，默认获得root logger对象
# 设置logger级别 debug
# root logger默认的级别是warning级别。
# 不设置的话 只能发送 >= warning级别的日志
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
# 设置handleer日志处理器，日志具体怎么处理都在日志处理器里面定义
# SteamHandler 流处理器，输出到控制台,输出方式为stdout
#   StreamHandler默认输出到sys.stderr
# 设置handler所处理的日志级别。
#   只能处理 >= 所设置handler级别的日志
# 设置日志输出格式
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setLevel(logging.DEBUG)
stream_handler.setFormatter(fmt)

# 使用我们写的多进程版Handler理器，定义日志输出到mylog.log文件内
#   文件打开方式默认为 a
#   按分钟进行日志切割
file_handler = MultiprocessHandler('mylog', when='M')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(fmt)

# 对logger增加handler日志处理器
logger.addHandler(stream_handler)
logger.addHandler(file_handler)


# 发送debug级别日志消息
def test(num):
    time.sleep(3)
    logger.debug('日志测试' + str(num))

if __name__ == '__main__':

    pool = multiprocessing.Pool(processes=10)

    for i in range(10):
        pool.apply_async(func=test, args=(i,))
    pool.close()
    pool.join()
    print '完毕'
