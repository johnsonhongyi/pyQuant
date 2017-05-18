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

log = LoggerFactory.log

class SafeHDFStore(HDFStore):
    # def __init__(self, *args, **kwargs):
    def __init__(self, *args, **kwargs):
        probe_interval = kwargs.pop("probe_interval", 1)
        lock = cct.get_ramdisk_path(args[0],lock=True)
        fname = cct.get_ramdisk_path(args[0])
        self._lock = lock
        while True:
            try:
                self._flock = os.open(self._lock, os.O_CREAT |os.O_EXCL |os.O_WRONLY)
                log.info("SafeHDF:%s lock:%s"%(lock,self._flock))
                break
            # except FileExistsError:
#            except FileExistsError as e:
            except (IOError, EOFError, Exception) as e:
                # time.sleep(probe_interval)
                # print ("Error:%s"%(e))
                time.sleep(probe_interval)

        # HDFStore.__init__(self, *args, **kwargs)
        HDFStore.__init__(self, fname, **kwargs)

    def __exit__(self, *args, **kwargs):
        HDFStore.__exit__(self, *args, **kwargs)
        os.close(self._flock)
        os.remove(self._lock)

# with SafeHDFStore('example.hdf') as store:
#     # Only put inside this block the code which operates on the store
#     store['result'] = result

# def write_lock(fname):
#     fpath = cct.get_ramdisk_path(fname,lock=True)

def get_hdf5_file(fpath,wr_mode='r',complevel=9,complib='zlib'):
    # store=pd.HDFStore(fpath,wr_mode, complevel=complevel, complib=complib)
    fpath = cct.get_ramdisk_path(fpath)
    if fpath is None:
        # print ("don't exists %s"%(fpath))
        return None

    if os.path.exists(fpath):
        if wr_mode == 'w':
            store=pd.HDFStore(fpath,complevel=None, complib=None, fletcher32=False)
        else:
            store=pd.HDFStore(fpath, mode=wr_mode, complevel=None, complib=None, fletcher32=False)
    else:
#        store = pd.HDFStore(fpath,complevel=9,complib='zlib')
        return None
        # store = pd.HDFStore(fpath, mode=wr_mode,complevel=9,complib='zlib')
    # store.put("Year2015", dfMinutes, format="table", append=True, data_columns=['dt','code'])
    return store
    # fp='/Volumes/RamDisk/top_now.h5'
    # get_hdf5_file(fp)
    # def hdf5_read_file(file):
        # store.select("Year2015", where=['dt<Timestamp("2015-01-07")','code=="000570"'])
        # return store

def write_hdf_db(fname,df,table='all',index=False,baseCount=500):
    # if 'code' in df.columns:
        # df = df.set_index('code')
#    dd = df.copy()
    if 'code' in df.columns:
        df = df.set_index('code')
    df['timel'] =  time.time()
#    h5=top_hdf_api(fname, table=table, df=dd,index=index)
#def top_hdf_api(fname='tdx',table=None,df=None,index=index):
    time_t = time.time()
#    h5 = get_hdf5_file(fname,wr_mode='r')
    if df is not None and not df.empty and table is not None:
        with SafeHDFStore(fname) as h5:
            if h5 is not None:
                dd = df.dtypes.to_frame()
                if 'object' in dd.values:
                    dd = dd[dd == 'object'].dropna()
                    col = dd.index.tolist()
                df.index = df.index.astype(str)
                df[col] = df[col].astype(str)
                if index:
#                    df.index = df.index.apply(lambda x:str(int(x)+700000) if x.startswith('0') else x)
                    df.index = map((lambda x:str(1000000-int(x)) if x.startswith('0') else x),df.index)

                if '/'+table in h5.keys():
                    tmpdf = h5[table]
                    if 'code' in tmpdf.columns:
                        tmpdf = tmpdf.set_index('code')
                    if 'code' in df.columns:
                        df = df.set_index('code')
                    diff_columns = set(df.columns) - set(tmpdf.columns)
                    if len(diff_columns) <> 0:
                        log.error("columns diff:%s"%(diff_columns))
#                        dif_co = list(set(df.index) - set(tmpdf.index))
#                        if len(dif_co) > 0:
                    df=cct.combine_dataFrame(tmpdf, df, col=None,append=True)
                    h5.remove(table)
                    h5[table] = df
                else:
                    h5[table] = df
                return df
            else:
                log.error("HDFile is None,Pls check:%s"%(fname))
#    else:
#        h5 = get_hdf5_file(fname,wr_mode='r')
#        if table is None and df is None and h5 is not None:
#            df = h5.copy()
#            if h5.is_open:
#                h5.close()
#            return df
#        if h5 is not None:
#            if table is not None:
#                if '/'+table in h5.keys():
#                    df = h5[table]
#                    if h5.is_open:
#                        h5.close()
#                    return df
#                log.error("%s is not find %s"%(fname,table))
#            if h5.is_open:
#                h5.close()
    log.info("wr hdf time:%0.2f"%(time.time()-time_t))
    return None

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
    df = None
    if code_l is not None:
        h5 = get_hdf5_file(fname,wr_mode='r')
        if h5 is not None:
            if table is not None:
                if '/'+table in h5.keys():
                    if index:
                        code_l = map((lambda x:str(1000000-int(x)) if x.startswith('0') else x),code_l)
                    dd = h5[table]
                    dif_co = list(set(dd.index) & set(code_l))
                    dratio = (float(len(code_l)) - float(len(dif_co)))/float(len(code_l))
                    if dratio < 0.1 and len(dd) > 0:
                        log.info("find all:%s :%s %0.2f"%(len(code_l),len(code_l)-len(dif_co),dratio))
                        if timelimit:
                            dd = dd.loc[dif_co]
                            o_time = dd[dd.timel <> 0].timel
                            if len(o_time) > 0:
                                o_time = o_time[0]
                                l_time = time.time() - o_time
                                if cct.get_work_day_status() and not cct.get_work_time() or (not (915 < cct.get_now_time_int() < 930) and l_time < limit_time):
                                    df = dd
                                    log.info("load time hdf ok:%s"%(len(df)))
                            log.info('l_time:%s'%(l_time))
                        else:
                             df = dd.loc[dif_co]
                    else:
                        log.info("don't find :%s"%(len(code_l)-len(dif_co)))
            else:
                log.error("%s is not find %s"%(fname,table))
    else:
        h5 = get_hdf5_file(fname,wr_mode='r')
        dd=None
        if h5 is not None:
            if table is None:
                dd = h5
            else:
                if table is not None:
                    if '/'+table in h5.keys():
                        dd = h5[table]
                    else:
                        log.error("%s is not find %s"%(fname,table))
            if timelimit:
                if dd is not None and len(dd)>0:
                    o_time = dd[dd.timel <> 0].timel
                    if len(o_time) > 0:
                        o_time = o_time[0]
                        l_time = time.time() - o_time
                        if cct.get_work_day_status() and not cct.get_work_time() or (not (915 < cct.get_now_time_int() < 930) and l_time < limit_time):
                            df = dd
                            log.info("load time hdf ok:%s"%(len(df)))
                    log.info('l_time:%s'%(l_time))
            else:
                 df = dd

    if h5 is not None and h5.is_open:
        h5.close()
    log.info("read_hdf_time:%s"%(time.time()-time_t))
    return df




if __name__ == "__main__":

    import tushare as ts
    df=ts.get_k_data('300334',start='2017-04-01')
    with SafeHDFStore('example.h5') as store:
        # Only put inside this block the code which operates on the store
        store['result'] = df