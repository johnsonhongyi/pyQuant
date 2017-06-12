# -*- coding:utf-8 -*-
import multiprocessing
from multiprocessing import Process, Queue
import time
import signal
import signal
import os
import sys
import statsmodels.api as sm
# from statsmodels import regression

def set_ctrl_handler():
    import win32api, thread
    # def doSaneThing(sig, func=None):
    # '''忽略所有KeyCtrl'''
    # return True
    # win32api.SetConsoleCtrlHandler(doSaneThing, 1)
    def handler(dwCtrlType, hook_sigint=thread.interrupt_main):
        # print ("ctrl:%s"%(dwCtrlType))
        p = multiprocessing.current_process()
        # q_display = Queue()
        # print q_display.get()
        print "pm:",p.pid
        if dwCtrlType == 0:  # CTRL_C_EVENT
            # hook_sigint()
            os.kill(p.pid,signal.CTRL_C_EVENT)
            # raise KeyboardInterrupt("CTRL-C!")
            return 1  # don't chain to the next handler
        return 0  # chain to the next handler

    win32api.SetConsoleCtrlHandler(handler, 1)
set_ctrl_handler()
    
def handler(signal, frame):
    print("handler!!!")
    sys.exit(10)

def worker(): 
    p = multiprocessing.current_process()
    try:
        signal.signal(signal.SIGINT,handler)  
        print("[PID:{}] acquiring resources".format(p.pid))
        while(True):           
            #working...
            print "#",
            time.sleep(3)
    except (KeyboardInterrupt, SystemExit) as e:
        print "KeyboardInterrupt",e
    finally:
        print("[PID:{}] releasing resources".format(p.pid))

if __name__ == "__main__":
    lst = []
    for i in range(1):
        p = multiprocessing.Process(target=worker)
        p.start()
        lst.append(p)
    print "pid:%s"%lst
    time.sleep(3)    
    # q_display = Queue()
    for p in lst:        
        # os.kill(p.pid,signal.SIGINT)
        # data = q_display.get(True, timeout=0.1)
        # print data
        print "p.id end:",p.pid
        # os.kill(p.pid,signal.CTRL_C_EVENT)
        # os.kill(p.pid,signal.CTRL_BREAK_EVENT)
        p.join()
        print(p)
        print(p.exitcode)
    print("joined all processes")