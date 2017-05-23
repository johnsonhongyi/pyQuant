# -*- encoding: utf-8 -*-
# !/usr/bin/python
# from __future__ import division

import os
import sys
import time
import pandas as pd
from pandas import HDFStore
sys.path.append("..")
from JohhnsonUtil import LoggerFactory
from JohhnsonUtil import commonTips as cct
from JohhnsonUtil import johnson_cons as ct
import random

log = LoggerFactory.log

global RAMDISK_KEY
RAMDISK_KEY = 0
class SafeHDFStore(HDFStore):
    # def __init__(self, *args, **kwargs):
    def __init__(self, *args, **kwargs):
        self.probe_interval = kwargs.pop("probe_interval", 2)
        lock = cct.get_ramdisk_path(args[0],lock=True)
        baseDir=cct.ramdisk_root
        self.fname = cct.get_ramdisk_path(args[0])
        self._lock = lock
        self.countlock = 0
        self.write_status = False
        global RAMDISK_KEY
        if not os.path.exists(baseDir):
            if RAMDISK_KEY < 1:
                log.error("NO RamDisk Root:%s"%(baseDir))
                RAMDISK_KEY +=1
        else:
            self.write_status = True
            self.run(self.fname)
    def run(self,fname,**kwargs):
        while True:
            try:
                self._flock = os.open(self._lock, os.O_CREAT |os.O_EXCL |os.O_WRONLY)
                log.info("SafeHDF:%s lock:%s"%(self._lock,self._flock))
                break
            # except FileExistsError:
#            except FileExistsError as e:
            except (IOError, EOFError,Exception) as e:
                # time.sleep(probe_interval)
                log.error("IOError Error:%s"%(e))
                if self.countlock < 6:
                    time.sleep(random.randint(0, 3))
                    # time.sleep(random.randint(0,5))
                    self.countlock +=1
                else:
                    os.remove(self._lock)
                    log.error("count10 remove lock")
#            except (Exception) as e:
#                print ("Exception Error:%s"%(e))
#                log.info("safeHDF Except:%s"%(e))
#                time.sleep(probe_interval)
#                return None
#        HDFStore.__init__(self, *args, **kwargs)
        HDFStore.__init__(self,fname, **kwargs)

    def __enter__(self):
        if self.write_status:
            return self

    def __exit__(self, *args, **kwargs):
        if self.write_status:
            HDFStore.__exit__(self, *args, **kwargs)
            os.close(self._flock)
            os.remove(self._lock)

# with SafeHDFStore('example.hdf') as store:
#     # Only put inside this block the code which operates on the store
#     store['result'] = result

# def write_lock(fname):
#     fpath = cct.get_ramdisk_path(fname,lock=True)

def get_hdf5_file(fpath,wr_mode='r',complevel=9,complib='zlib',mutiindx=False):
    '''old outdata'''
    # store=pd.HDFStore(fpath,wr_mode, complevel=complevel, complib=complib)
    fpath = cct.get_ramdisk_path(fpath)
    if fpath is None:
        log.info("don't exists %s"%(fpath))
        return None

    if os.path.exists(fpath):
        if wr_mode == 'w':
            store=pd.HDFStore(fpath,complevel=None, complib=None, fletcher32=False)
        else:
            lock = cct.get_ramdisk_path(fpath,lock=True)
            while True:
                try:
#                    lock_s = os.open(lock, os.O_CREAT |os.O_EXCL |os.O_WRONLY)
                    lock_s = os.open(lock,os.O_CREAT| os.O_EXCL)
                    log.info("SafeHDF:%s read lock:%s"%(lock_s,lock))
                    break
                # except FileExistsError:
    #            except FileExistsError as e:
                except (IOError, EOFError,Exception) as e:
                    # time.sleep(probe_interval)
                    log.error("IOError READ ERROR:%s"%(e))
                    time.sleep(random.random())

            store=pd.HDFStore(fpath, mode=wr_mode, complevel=None, complib=None, fletcher32=False)
            os.remove(lock)
#            store = SafeHDFStore(fpath)
    else:
        if mutiindx:
            store = pd.HDFStore(fpath,complevel=9,complib='zlib')
        else:
            return None
        # store = pd.HDFStore(fpath, mode=wr_mode,complevel=9,complib='zlib')
    # store.put("Year2015", dfMinutes, format="table", append=True, data_columns=['dt','code'])
    return store
    # fp='/Volumes/RamDisk/top_now.h5'
    # get_hdf5_file(fp)
    # def hdf5_read_file(file):
        # store.select("Year2015", where=['dt<Timestamp("2015-01-07")','code=="000570"'])
        # return store

def write_hdf_db(fname,df,table='all',index=False,baseCount=500,append=False):
    if 'code' in df.columns:
        df = df.set_index('code')
    df['timel'] =  time.time()
#    write_status = False
    time_t = time.time()
#    if not os.path.exists(cct.ramdisk_root):
#        log.info("NO RamDisk")
#        return False
    global RAMDISK_KEY
    if not RAMDISK_KEY < 1:
        return df
    if df is not None and not df.empty and len(df) > 0:
        dd = df.dtypes.to_frame()
        if 'object' in dd.values:
            dd = dd[dd == 'object'].dropna()
            col = dd.index.tolist()
            log.info("col:%s"%(col))
            df[col] = df[col].astype(str)
        df.index = df.index.astype(str)
    if df is not None and not df.empty and table is not None:
        # h5 = get_hdf5_file(fname,wr_mode='r')
        tmpdf = []
        with SafeHDFStore(fname) as store:
            if store is not None:
                if '/'+table in store.keys():
                    tmpdf = store[table]
        if index:
            df.index = map((lambda x:str(1000000-int(x)) if x.startswith('0') else x),df.index)
        if tmpdf is not None and len(tmpdf) > 0:
            if 'code' in tmpdf.columns:
                tmpdf = tmpdf.set_index('code')
            if 'code' in df.columns:
                df = df.set_index('code')
            diff_columns = set(df.columns) - set(tmpdf.columns)
            if len(diff_columns) <> 0:
                log.error("columns diff:%s"%(diff_columns))
#                        dif_co = list(set(df.index) - set(tmpdf.index))
#                        if len(dif_co) > 0:
            df=cct.combine_dataFrame(tmpdf, df, col=None,append=append)
#            df=cct.combine_dataFrame(tmpdf, df, col=None,append=False)
            log.info("read hdf time:%0.2f"%(time.time()-time_t))
        else:
            # if index:
                # df.index = map((lambda x:str(1000000-int(x)) if x.startswith('0') else x),df.index)
            log.info("h5 None hdf reindex time:%0.2f"%(time.time()-time_t))
    time_t = time.time()
    if df is not None and not df.empty and table is not None:
        # df['timel'] =  time.time()
        with SafeHDFStore(fname) as h5:
            df = df.fillna(0)
            if h5 is not None:
                if '/'+table in h5.keys():
                    h5.remove(table)
                    h5[table] = df
                else:
                    h5[table] = df
            else:
                log.error("HDFile is None,Pls check:%s"%(fname))
    log.info("write hdf time:%0.2f"%(time.time()-time_t))

    return True

#def lo_hdf_db_old(fname,table='all',code_l=None,timelimit=True,index=False):
#    h_t = time.time()
#    h5=top_hdf_api(fname=fname, table=table, df=None,index=index)
#    if h5 is not None and code_l is not None:
#        if len(code_l) == 0:
#            return None
#        if h5 is not None:
#            diffcode = set(code_l) - set(h5.index)
#            if len(diffcode) > 10 and len(h5) <> 0 and float(len(diffcode))/float(len(code_l)) > ct.diffcode:
#                log.error("f:%s t:%s dfc:%s %s co:%s h5:%s"%(fname,table,len(diffcode),h5.index.values[0],code_l[:2],h5.index.values[:2]))
#                return None
#
#    if h5 is not None and not h5.empty and 'timel' in h5.columns:
#            o_time = h5[h5.timel <> 0].timel
#            if len(o_time) > 0:
#                o_time = o_time[0]
#    #            print time.time() - o_time
#                # if cct.get_work_hdf_status() and (not (915 < cct.get_now_time_int() < 930) and time.time() - o_time < ct.h5_limit_time):
#                if not cct.get_work_time() or (not timelimit or time.time() - o_time < ct.h5_limit_time):
#                    log.info("time hdf:%s %s"%(fname,len(h5))),
##                    if 'timel' in h5.columns:
##                        h5=h5.drop(['timel'],axis=1)
#                    if code_l is not None:
#                        if 'code' in h5.columns:
#                            h5 = h5.set_index('code')
#                        h5.drop([inx for inx in h5.index  if inx not in code_l], axis=0, inplace=True)
#                            # log.info("time in idx hdf:%s %s"%(fname,len(h5))),
#                    # if index == 'int' and 'code' not in h5.columns:
#                    #     h5=h5.reset_index()
#                    log.info("load hdf time:%0.2f"%(time.time()-h_t))
#                    return h5
#    else:
#        if h5 is not None:
#            return h5
#    return None

def load_hdf_db(fname,table='all',code_l=None,timelimit=True,index=False,limit_time=ct.h5_limit_time):
    time_t = time.time()
    global RAMDISK_KEY
    if not RAMDISK_KEY < 1:
        return None
    df = None
    dd = None
    if code_l is not None:
        if table is not None:
            with SafeHDFStore(fname) as store:
                if store is not None:
                    if '/'+table in store.keys():
                        dd = store[table]
            if dd is not None and len(dd) > 0:
                if index:
                    code_l = map((lambda x:str(1000000-int(x)) if x.startswith('0') else x),code_l)
                dif_co = list(set(dd.index) & set(code_l))
                dratio = (float(len(code_l)) - float(len(dif_co)))/float(len(code_l))
                if dratio < 0.1 and len(dd) > 0:
                    log.info("find all:%s :%s %0.2f"%(len(code_l),len(code_l)-len(dif_co),dratio))
                    if timelimit and len(dd) > 0:
                        dd = dd.loc[dif_co]
                        o_time = dd[dd.timel <> 0].timel
                        if len(o_time) > 0:
                            o_time = o_time[0]
                            l_time = time.time() - o_time
                            return_hdf_status = not cct.get_work_day_status()  or not cct.get_work_time() or (cct.get_work_day_status() and cct.get_work_time() and l_time < limit_time)
#                                if not cct.get_work_time() or not cct.get_work_day_status() or (cct.get_work_time() and l_time < limit_time):
                            if return_hdf_status:
                                df = dd
                                log.info("load %s time hdf ok:%s"%(fname,len(df)))

                        log.info('fname:%s l_time:None'%(fname))
                    else:
                         df = dd.loc[dif_co]
                else:
                    log.info("don't find :%s"%(len(code_l)-len(dif_co)))
        else:
            log.error("%s is not find %s"%(fname,table))
    else:
        # h5 = get_hdf5_file(fname,wr_mode='r')
        if table is not None:
            with SafeHDFStore(fname) as store:
                if store is not None:
                    if '/'+table in store.keys():
                        dd = store[table]
            if dd is not None and len(dd) > 0:
                if timelimit:
                    if dd is not None and len(dd)>0:
                        o_time = dd[dd.timel <> 0].timel
                        if len(o_time) > 0:
                            o_time = o_time[0]
                            l_time = time.time() - o_time
#                                    return_hdf_status = not cct.get_work_day_status()  or not cct.get_work_time() or (cct.get_work_day_status() and (cct.get_work_time() and l_time < limit_time))
                            return_hdf_status = not cct.get_work_day_status()  or not cct.get_work_time() or (cct.get_work_day_status() and cct.get_work_time() and l_time < limit_time)
                            log.info("return_hdf_status:%s time:%0.2f"%(return_hdf_status,l_time))
                            if  return_hdf_status:
                                log.info("return hdf5 data:%s"%(len(dd)))
                                df = dd
                            else:
                                log.info("no return time hdf5:%s"%(len(dd)))
                        log.info('fname:%s l_time:None'%(fname))
                else:
                     df = dd
            else:
                log.error("%s is not find %s"%(fname,table))
        else:
            log.error("% / table is Init None:%s"(fname,table))

    if df is not None and len(df) > 0:
        df = df.fillna(0)
        if 'timel' in df.columns:
            time_list = df.timel.tolist()
            time_list = sorted(set(time_list),key = time_list.index)
            if time_list is not None and len(time_list) > 0:
                df['timel'] = time_list[0]
                log.info("load hdf times:%s"%(time_list))

    log.info("load_hdf_time:%0.2f"%(time.time()-time_t))
    return df

# def load_hdf_db_old_outdate(fname,table='all',code_l=None,timelimit=True,index=False,limit_time=ct.h5_limit_time):
#     time_t = time.time()
#     df = None
#     global RAMDISK_KEY
#     # print RAMDISK_KEY
#     if not RAMDISK_KEY < 1:
#         return df
#     if code_l is not None:
#         h5 = get_hdf5_file(fname,wr_mode='r')
#         if h5 is not None:
#             if table is not None:
#                 if '/'+table in h5.keys():
#                     if index:
#                         code_l = map((lambda x:str(1000000-int(x)) if x.startswith('0') else x),code_l)
#                     dd = h5[table]
#                     dif_co = list(set(dd.index) & set(code_l))
#                     dratio = (float(len(code_l)) - float(len(dif_co)))/float(len(code_l))
#                     if dratio < 0.1 and len(dd) > 0:
#                         log.info("find all:%s :%s %0.2f"%(len(code_l),len(code_l)-len(dif_co),dratio))
#                         if timelimit and len(dd) > 0:
#                             dd = dd.loc[dif_co]
#                             o_time = dd[dd.timel <> 0].timel
#                             if len(o_time) > 0:
#                                 o_time = o_time[0]
#                                 l_time = time.time() - o_time
#                                 return_hdf_status = not cct.get_work_day_status()  or not cct.get_work_time() or (cct.get_work_day_status() and cct.get_work_time() and l_time < ct.limit_time)
#                                 if return_hdf_status:
#                                     df = dd
#                                     log.info("load %s time hdf ok:%s"%(fname,len(df)))

#                             log.info('fname:%s l_time:None'%(fname))
#                         else:
#                              df = dd.loc[dif_co]
#                     else:
#                         log.info("don't find :%s"%(len(code_l)-len(dif_co)))
#             else:
#                 log.error("%s is not find %s"%(fname,table))
#     else:
#         h5 = get_hdf5_file(fname,wr_mode='r')
#         dd=None
#         if h5 is not None:
#             if table is None:
#                 dd = h5
#             else:
#                 if table is not None:
#                     if '/'+table in h5.keys():
#                         dd = h5[table]
#                         if timelimit and len(dd) > 0:
#                             if dd is not None and len(dd)>0:
#                                 o_time = dd[dd.timel <> 0].timel
#                                 if len(o_time) > 0:
#                                     o_time = o_time[0]
#                                     l_time = time.time() - o_time
#                                     return_hdf_status = not cct.get_work_day_status()  or not cct.get_work_time() or (cct.get_work_day_status() and cct.get_work_time() and l_time < ct.h5_limit_time)
#                                     log.info("return_hdf_status:%s time:%0.2f"%(return_hdf_status,l_time))
#                                     if  return_hdf_status:
#                                         log.info("return hdf5 data:%s"%(len(h5)))
#                                         df = dd
#                                     else:
#                                         log.info("no return time hdf5:%s"%(len(h5)))
#                                 log.info('fname:%s l_time:None'%(fname))
#                         else:
#                              df = dd
#                     else:
#                         log.error("%s is not find %s"%(fname,table))
#     if h5 is not None and h5.is_open:
#         h5.close()

#     if df is not None and len(df) > 0:
#         df = df.fillna(0)
#         if 'timel' in df.columns:
#             time_list = df.timel.tolist()
#             time_list = sorted(set(time_list),key = time_list.index)
#             if time_list is not None and len(time_list) > 0:
#                 df['timel'] = time_list[0]
#                 log.info("load hdf times:%s"%(time_list))

#     log.info("load_hdf_time:%0.2f"%(time.time()-time_t))
#     return df




if __name__ == "__main__":

    import tushare as ts
    df=ts.get_k_data('300334',start='2017-04-01')
    with SafeHDFStore('example.h5') as store:
        # Only put inside this block the code which operates on the store
        store['result'] = df