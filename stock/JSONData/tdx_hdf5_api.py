# -*- encoding: utf-8 -*-
# !/usr/bin/python
# from __future__ import division

import os
import sys
import time
import pandas as pd
from pandas import HDFStore
sys.path.append("..")
from JohnsonUtil import LoggerFactory
# from JohnsonUtil.commonTips import get_ramdisk_dir
# print get_ramdisk_dir()
from JohnsonUtil import commonTips as cct
from JohnsonUtil import johnson_cons as ct
import random
import numpy as np
import subprocess
log = LoggerFactory.log
import gc
global RAMDISK_KEY, INIT_LOG_Error
RAMDISK_KEY = 0
INIT_LOG_Error = 0
# Compress_Count = 1
BaseDir = cct.get_ramdisk_dir()

#import fcntl linux
#lock：
# fcntl.flock(f,fcntl.LOCK_EX)
# unlock
# fcntl.flock(f,fcntl.LOCK_UN)

# for win
# with portalocker.Lock('some_file', 'rb+', timeout=60) as fh:
#     # do what you need to do
#     ...
 
#     # flush and sync to filesystem
#     fh.flush()
#     os.fsync(fh.fileno())

class SafeHDFStore(HDFStore):
    # def __init__(self, *args, **kwargs):

    def __init__(self, *args, **kwargs):
        self.probe_interval = kwargs.pop("probe_interval", 2)
        lock = cct.get_ramdisk_path(args[0], lock=True)
        baseDir = BaseDir
        self.fname_o = args[0]
        self.basedir = baseDir
        self.config_ini = baseDir + os.path.sep+ 'h5config.txt'
        if args[0] == cct.tdx_hd5_name or args[0].find('tdx_all_df') >=0:
            
            self.fname = cct.get_run_path_tdx(args[0])
            self.basedir = self.fname.split(self.fname_o)[0]
            log.info("tdx_hd5:%s"%(self.fname))
        else:
            self.fname = cct.get_ramdisk_path(args[0])
            self.basedir = self.fname.split(self.fname_o)[0]
            log.info("ramdisk_hd5:%s"%(self.fname))

        self._lock = lock
        self.countlock = 0
        self.write_status = False
        self.complevel = 9
        self.complib = 'zlib'
        # self.ptrepack_cmds = "ptrepack --chunkshape=auto --propindexes --complevel=9 --complib=%s %s %s"
        self.ptrepack_cmds = "ptrepack --overwrite-nodes --chunkshape=auto --complevel=9 --complib=%s %s %s"
        self.big_H5_Size_limit = ct.big_H5_Size_limit
        self.h5_size_org = 0
        # self.pt_lock_file = self.fname + '.txt'
        global RAMDISK_KEY
        if not os.path.exists(baseDir):
            if RAMDISK_KEY < 1:
                log.error("NO RamDisk Root:%s" % (baseDir))
                RAMDISK_KEY += 1
        else:
            self.temp_file = self.fname + '_tmp'
            self.write_status = True
            if os.path.exists(self.fname):
                self.h5_size_org = os.path.getsize(self.fname) / 1000 / 1000
            self.run(self.fname)
        # ptrepack --chunkshape=auto --propindexes --complevel=9 --complib=blosc in.h5 out.h5
        # subprocess.call(["ptrepack", "-o", "--chunkshape=auto", "--propindexes", --complevel=9,", ",--complib=blosc,infilename, outfilename])
        # os.system()

    '''def read_write_pt_File(self, f_size, mode='a+'):
        with open(self.pt_lock_file, mode) as f:
            f.seek(0)
            read_limit = f.read()
            limit_now = ((f_size / 10 + 1) * self.big_H5_Size_limit)
            # log.info("big_size:%s read_limit:%s" % (self.big_H5_Size_limit, f_size))
            if read_limit is not None and len(read_limit) > 0:
                if int(read_limit) > f_size:
                    log.info("f_size:%s < read_limit:%s" % (self.big_H5_Size_limit, f_size))
                    return False
                else:
                    f.seek(0)
                    log.error("f_size:%s > read_limit:%s" % (self.big_H5_Size_limit, f_size))
                    f.truncate()
                    f.write(str(limit_now))
                    return True
            else:
                f.seek(0)
                f.write(str(limit_now))
                return False
        # with open(fname, mode) as f:
        #     f.seek(0)
        #     model.input(f.read())
        #     model.compute()
        #     f.seek(0)
        #     f.truncate()
        #     f.write(model.output())'''

    def run(self, fname, *args, **kwargs):
        while True:
            try:
                self._flock = os.open(
                    self._lock, os.O_CREAT | os.O_EXCL)
                    # self._lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                log.info("SafeHDF:%s lock:%s" % (self._lock, self._flock))
                break
            # except FileExistsError:
#            except FileExistsError as e:
            except (IOError, EOFError, Exception) as e:
                # except (IOError, OSError) as e:
                # time.sleep(probe_interval)
                # import ipdb;ipdb.set_trace()
                # os.unlink(self._lock)
                # os.remove(self._lock)
                if self.countlock > 1:
                    log.error("IOError Error:%s" % (e))

                if self.countlock <= 8:
                    time.sleep(round(random.randint(3, 10) / 1.2, 2))
                    # time.sleep(random.randint(0,5))
                    self.countlock += 1
                else:
                    # os.close(self._flock)
                    # os.unlink(self._lock)
                    os.remove(self._lock)
                    # time.sleep(random.randint(15, 30))
                    log.error("count10 remove lock")
            except WindowsError:
                log.error('WindowsError')
            finally:
                pass

#            except (Exception) as e:
#                print ("Exception Error:%s"%(e))
#                log.info("safeHDF Except:%s"%(e))
#                time.sleep(probe_interval)
#                return None
        # HDFStore.__init__(self, fname, *args, **kwargs)
        HDFStore.__init__(self, fname, *args, **kwargs)
        # if not os.path.exists(cct.get_ramdisk_path(cct.tdx_hd5_name)):
        #     if os.path.exists(cct.tdx_hd5_path):
        #         tdx_size = os.path.getsize(cct.tdx_hd5_path)

        # HDFStore.__init__(self,fname,complevel=self.complevel,complib=self.complib, **kwargs)
        # HDFStore.__init__(self,fname,format="table",complevel=self.complevel,complib=self.complib, **kwargs)
        # ptrepack --complib=zlib --complevel 9 --overwrite sina_data.h5 out.h5

    def __enter__(self):
        if self.write_status:
            return self

    def __exit__(self, *args, **kwargs):
        if self.write_status:
            HDFStore.__exit__(self, *args, **kwargs)
            os.close(self._flock)
            h5_size = os.path.getsize(self.fname) / 1000 / 1000
            new_limit = ((h5_size / self.big_H5_Size_limit + 1) * self.big_H5_Size_limit)
            # global Compress_Count
           # if Compress_Count == 1 and self.h5_size_org > self.big_H5_Size_limit:
#                cct.get_config_value(self.config_ini,self.fname_o,h5_size,new_limit)
               # log.info("Compress_Count init:%s h5_size_org:%s" % (Compress_Count, self.h5_size_org))
            log.info("fname:%s h5_size:%s big:%s" % (self.fname,h5_size, self.big_H5_Size_limit))
            # if  h5_size >= self.big_H5_Size_limit:
            if cct.get_config_value(self.config_ini,self.fname_o,h5_size,new_limit):
                time_pt=time.time()
                if os.path.exists(self.fname) and os.path.exists(self.temp_file):
                    log.error("remove tmpfile is exists:%s"%(self.temp_file))
                    os.remove(self.temp_file)
                os.rename(self.fname, self.temp_file)
                if cct.get_os_system() == 'mac':
                    p=subprocess.Popen(self.ptrepack_cmds % (
                        self.complib, self.temp_file, self.fname), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                else:
                    back_path = os.getcwd()
                    os.chdir(self.basedir)
                    log.info('current path is: %s after change dir' %os.getcwd())
                    pt_cmd = self.ptrepack_cmds % (self.complib, self.temp_file.split(self.basedir)[1], self.fname.split(self.basedir)[1])
                    p=subprocess.Popen(pt_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                    os.chdir(back_path)
                p.wait()
                # ptrepack --chunkshape=auto --complevel=9 --complib=zlib tdx_all_df_300.h5_tmp tdx_all_df_300.h5
                if p.returncode != 0:
                    # log.error("ptrepack hdf Error:%s for tmp_file:%s Er:%s" % (self.fname,self.temp_file,p.stderr))
                    log.error("ptrepack hdf Error:%s  tofile:%s Er:%s" % (self.temp_file,self.fname,p.stdout.read().decode("gbk")))
                    # return -1
                else:
                    if os.path.exists(self.temp_file):
                        os.remove(self.temp_file)
                    # log.error("fname:%s h5_size:%sM Limit:%s t:%.1f" % (self.fname, h5_size, new_limit , time_pt - time.time()))
            if os.path.exists(self._lock):
                os.remove(self._lock)
            # gc.collect()
'''
https://stackoverflow.com/questions/21126295/how-do-you-create-a-compressed-dataset-in-pytables-that-can-store-a-unicode-stri/21128497#21128497
>>> h5file = pt.openFile("test1.h5",'w')
>>> recordStringInHDF5(h5file, h5file.root, 'mrtamb',
    u'\u266b Hey Mr. Tambourine Man \u266b')

/mrtamb (CArray(30,), shuffle, zlib(5)) ''
  atom := UInt8Atom(shape=(), dflt=0)
  maindim := 0
  flavor := 'numpy'
  byteorder := 'irrelevant'
  chunkshape := (65536,)

>>> h5file.flush()
>>> h5file.close()
>>> h5file = pt.openFile("test1.h5")
>>> print retrieveStringFromHDF5(h5file.root.mrtamb)

♫ Hey Mr. Tambourine Man ♫

write-performance
https://stackoverflow.com/questions/20083098/improve-pandas-pytables-hdf5-table-write-performance

'''


def recordStringInHDF5(h5file, group, nodename, s, complevel=5, complib='blosc'):
    '''creates a CArray object in an HDF5 file
    that represents a unicode string'''

    bytes=np.fromstring(s.encode('utf-8'), np.uint8)
    atom=pt.UInt8Atom()
    filters=pt.Filters(complevel=complevel, complib=complib)
    ca=h5file.create_carray(group, nodename, atom, shape=(len(bytes),),
                              filters=filters)
    ca[:]=bytes
    return ca


def retrieveStringFromHDF5(node):
    return unicode(node.read().tostring(), 'utf-8')


def clean_cols_for_hdf(data):
    types=data.apply(lambda x: pd.lib.infer_dtype(x.values))
    for col in types[types == 'mixed'].index:
        data[col]=data[col].astype(str)
    # data[<your appropriate columns here>].fillna(0,inplace=True)
    return data


def write_hdf(f, key, df, complib):
    """Append pandas dataframe to hdf5.

    Args:
    f       -- File path
    key     -- Store key
    df      -- Pandas dataframe
    complib -- Compress lib

    NOTE: We use maximum compression w/ zlib.
    """

    with SafeHDF5Store(f, complevel=9, complib=complib) as store:
        df.to_hdf(store, key, format='table', append=True)
# with SafeHDFStore('example.hdf') as store:
#     # Only put inside this block the code which operates on the store
#     store['result'] = result

# def write_lock(fname):
#     fpath = cct.get_ramdisk_path(fname,lock=True)


def get_hdf5_file(fpath, wr_mode='r', complevel=9, complib='blosc', mutiindx=False):
    """[summary]

    [old api out date]

    Parameters
    ----------
    fpath : {[type]}
        [description]
    wr_mode : {str}, optional
        [description] (the default is 'r', which [default_description])
    complevel : {number}, optional
        [description] (the default is 9, which [default_description])
    complib : {str}, optional
        [description] (the default is 'blosc', which [default_description])
    mutiindx : {bool}, optional
        [description] (the default is False, which [default_description])

    Returns
    -------
    [type]
        [description]
    """
    # store=pd.HDFStore(fpath,wr_mode, complevel=complevel, complib=complib)
    fpath=cct.get_ramdisk_path(fpath)
    if fpath is None:
        log.info("don't exists %s" % (fpath))
        return None

    if os.path.exists(fpath):
        if wr_mode == 'w':
            # store=pd.HDFStore(fpath,complevel=None, complib=None, fletcher32=False)
            store=pd.HDFStore(fpath)
        else:
            lock=cct.get_ramdisk_path(fpath, lock=True)
            while True:
                try:
                    #                    lock_s = os.open(lock, os.O_CREAT |os.O_EXCL |os.O_WRONLY)
                    lock_s=os.open(lock, os.O_CREAT | os.O_EXCL)
                    log.info("SafeHDF:%s read lock:%s" % (lock_s, lock))
                    break
                # except FileExistsError:
    #            except FileExistsError as e:
                except (IOError, EOFError, Exception) as e:
                    # time.sleep(probe_interval)
                    log.error("IOError READ ERROR:%s" % (e))
                    time.sleep(random.random())

            store=pd.HDFStore(fpath, mode=wr_mode)
            # store=pd.HDFStore(fpath, mode=wr_mode, complevel=None, complib=None, fletcher32=False)
            os.remove(lock)
#            store = SafeHDFStore(fpath)
    else:
        if mutiindx:
            store=pd.HDFStore(fpath)
            # store = pd.HDFStore(fpath,complevel=9,complib='zlib')
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


def write_hdf_db(fname, df, table='all', index=False, complib='blosc', baseCount=500, append=True, MultiIndex=False,rewrite=False):
    """[summary]

    [description]

    Parameters
    ----------
    fname : {[type]}
        [description]
    df : {[type]}
        [description]
    table : {str}, optional
        [description] (the default is 'all', which [default_description])
    index : {bool}, optional
        [description] (the default is False, which [default_description])
    complib : {str}, optional
        [description] (the default is 'blosc', which [default_description])
    baseCount : {number}, optional
        [description] (the default is 500, which [default_description])
    append : {bool}, optional
        [description] (the default is True, which [default_description])
    MultiIndex : {bool}, optional
        [description] (the default is False, which [default_description])

    Returns
    -------
    [type]
        [description]
    """
    if 'code' in df.columns:
        df=df.set_index('code')
#    write_status = False
    time_t=time.time()
#    if not os.path.exists(cct.get_ramdisk_dir()):
#        log.info("NO RamDisk")
#        return False
    df=df.fillna(0)
    df=df[~df.index.duplicated(keep='first')]

    code_subdf=df.index.tolist()
    global RAMDISK_KEY
    if not RAMDISK_KEY < 1:
        return df

    if not MultiIndex:
        df['timel']=time.time()

    if not rewrite:
        if df is not None and not df.empty and table is not None:
            # h5 = get_hdf5_file(fname,wr_mode='r')
            tmpdf=[]
            with SafeHDFStore(fname) as store:
                if store is not None:
                    if '/' + table in store.keys():
                        tmpdf=store[table]
                        tmpdf = tmpdf[~tmpdf.index.duplicated(keep='first')]


            if not MultiIndex:
                if index:
                    # log.error("debug index:%s %s %s"%(df,index,len(df)))
                    df.index=map((lambda x: str(1000000 - int(x))
                                    if x.startswith('0') else x), df.index)
                if tmpdf is not None and len(tmpdf) > 0:
                    if 'code' in tmpdf.columns:
                        tmpdf=tmpdf.set_index('code')
                    if 'code' in df.columns:
                        df=df.set_index('code')
                    diff_columns=set(df.columns) - set(tmpdf.columns)
                    if len(diff_columns) <> 0:
                        log.error("columns diff:%s" % (diff_columns))

                    limit_t=time.time()
                    df['timel']=limit_t
                    # df_code = df.index.tolist()

                    df=cct.combine_dataFrame(tmpdf, df, col=None, append=append)

                    if not append:
                        df['timel']=time.time()
                    elif fname == 'powerCompute':
                        o_time=df[df.timel < limit_t].timel.tolist()
                        o_time=sorted(set(o_time), reverse=False)
                        if len(o_time) >= ct.h5_time_l_count:
                            o_time=[time.time() - t_x for t_x in o_time]
                            o_timel=len(o_time)
                            o_time=np.mean(o_time)
                            if (o_time) > ct.h5_power_limit_time:
                                df['timel']=time.time()
                                log.error("%s %s o_time:%.1f timel:%s" % (fname, table, o_time, o_timel))

        #            df=cct.combine_dataFrame(tmpdf, df, col=None,append=False)
                    log.info("read hdf time:%0.2f" % (time.time() - time_t))
                else:
                    # if index:
                        # df.index = map((lambda x:str(1000000-int(x)) if x.startswith('0') else x),df.index)
                    log.info("h5 None hdf reindex time:%0.2f" %
                             (time.time() - time_t))
            else:
                # df.loc[df.index.isin(['000002','000001'], level='code')]
                # df.loc[(df.index.get_level_values('code')== 600004)]
                # df.loc[(df.index.get_level_values('code')== '600199')]
                # da.swaplevel(0, 1, axis=0).loc['2017-05-25']
                # df.loc[(600004,20170414),:]
                # df.xs(20170425,level='date')
                # df.index.get_level_values('code').unique()
                # df.index.get_loc(600006)
                # slice(58, 87, None)
                # df.index.get_loc_level(600006)
                # da.swaplevel(0, 1, axis=0).loc['2017-05-25']
                # da.reorder_levels([1,0], axis=0)
                # da.sort_index(level=0, axis=0,ascending=False
                # setting: dfm.index.is_lexsorted() dfm = dfm.sort_index()  da.loc[('000001','2017-05-12'):('000005','2017-05-25')]
                # da.groupby(level=1).mean()
                # da.index.get_loc('000005')     da.iloc[slice(22,33,None)]
                # mask = totals['dirty']+totals['swap'] > 1e7     result =
                # mask.loc[mask]
                # store.remove('key_name', where='<where clause>')


                # tmpdf = tmpdf[~tmpdf.index.duplicated(keep='first')]
                # df = df[~df.index.duplicated(keep='first')]
                if not rewrite and tmpdf is not None and len(tmpdf) > 0:
                    # multi_code = tmpdf.index.get_level_values('code').unique().tolist()
                    multi_code=tmpdf.index.get_level_values('code').unique().tolist()
                    df_multi_code = df.index.get_level_values('code').unique().tolist()
                    dratio = cct.get_diff_dratio(multi_code, df_multi_code)
                    if dratio < ct.dratio_limit:
                        comm_code = list(set(df_multi_code) & set(multi_code))
                        # print df_multi_code,multi_code,comm_code,len(comm_code)
                        inx_key=comm_code[random.randint(0, len(comm_code)-1)]
                        if  inx_key in df.index.get_level_values('code'):
                            now_time=df.loc[inx_key].index[-1]
                            tmp_time=tmpdf.loc[inx_key].index[-1]
                            if now_time == tmp_time:
                                log.debug("%s %s Multi out %s hdf5:%s No Wri!!!" % (fname, table,inx_key
                                    , now_time))
                                return False
                    elif dratio == 1:
                        print ("newData ratio:%s all:%s"%(dratio,len(df)))
                    else:
                        log.debug("dratio:%s main:%s new:%s %s %s Multi All Wri" % (dratio,len(multi_code),len(df_multi_code),fname, table))
                    # da.drop(('000001','2017-05-11'))
                else:
                    log.debug("%s %s Multi rewrite:%s Wri!!!" % (fname, table, rewrite))


    time_t=time.time()
    if df is not None and not df.empty and table is not None:
        if df is not None and not df.empty and len(df) > 0:
            dd=df.dtypes.to_frame()

        if 'object' in dd.values:
            dd=dd[dd == 'object'].dropna()
            col=dd.index.tolist()
            log.info("col:%s" % (col))
            if not MultiIndex:
                df[col]=df[col].astype(str)
                df.index=df.index.astype(str)
                df=df.fillna(0)
            # else:
            #     print col
            #     for co in col:
            #         print ('object:%s'%(co))
                # df = df.drop(col,axis=1)
#                    df[co] = df[co].apply()
#                    recordStringInHDF5(h5file, h5file.root, 'mrtamb',u'\u266b Hey Mr. Tambourine Man \u266b')

        with SafeHDFStore(fname) as h5:
            df=df.fillna(0)
            if h5 is not None:
                if '/' + table in h5.keys():
                    if not MultiIndex:

                        # if MultiIndex and rewrite:
                        #     src_code = h5[table].index.get_level_values('code').unique().tolist()
                        #     new_code = df.index.get_level_values('code').unique().tolist()
                        #     diff_code = list(set(new_code) - set(src_code))
                        #     dratio = cct.get_diff_dratio(new_code, src_code)
                        #     print dratio,len(diff_code)
                        #     import ipdb;ipdb.set_trace()
                        #     df = pd.concat([df, h5[table]], axis=0)
                        #     df = df.index.drop_duplicates()
                                # df[df.index.get_level_values('code') not in diff_code ]
                        h5.remove(table)
                        # h5[table]=df
                        h5.put(table, df, format='table', append=False, complib=complib, data_columns=True)
                        # h5.put(table, df, format='table',index=False, data_columns=True, append=False)
                    else:
                        if rewrite:
                            h5.remove(table)
                        h5.put(table, df, format='table', index=False, complib=complib, data_columns=True, append=True)
                        # h5.append(table, df, format='table', append=True,data_columns=True, dropna=None)
                else:
                    if not MultiIndex:
                        # h5[table]=df
                        h5.put(table, df, format='table', append=False, complib=complib, data_columns=True)
                        # h5.put(table, df, format='table',index=False, data_columns=True, append=False)
                    else:
                        h5.put(table, df, format='table', index=False, complib=complib, data_columns=True, append=True)
                        # h5.append(table, df, format='table', append=True, data_columns=True, dropna=None)
                        # h5[table]=df
                h5.flush()
            else:
                log.error("HDFile is None,Pls check:%s" % (fname))

    log.info("write hdf time:%0.2f" % (time.time() - time_t))

    return True

# def lo_hdf_db_old(fname,table='all',code_l=None,timelimit=True,index=False):
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
# if 'timel' in h5.columns:
# h5=h5.drop(['timel'],axis=1)
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


def load_hdf_db(fname, table='all', code_l=None, timelimit=True, index=False, limit_time=ct.h5_limit_time, dratio_limit=ct.dratio_limit,MultiIndex=False):
    """[summary]

    [load hdf ]

    Parameters
    ----------
    fname : {[type]}
        [description]
    table : {str}, optional
        [description] (the default is 'all', which [default_description])
    code_l : {[type]}, optional
        [description] (the default is None, which [default_description])
    timelimit : {bool}, optional
        [description] (the default is True, which [default_description])
    index : {bool}, optional
        [description] (the default is False, which [default_description])
    limit_time : {[type]}, optional
        [description] (the default is ct.h5_limit_time, which [default_description])
    dratio_limit : {[type]}, optional
        [description] (the default is ct.dratio_limit, which [default_description])
    MultiIndex : {bool}, optional
        [description] (the default is False, which [default_description])

    Returns
    -------
    [dataframe]
        [description]
    """
    time_t=time.time()
    global RAMDISK_KEY, INIT_LOG_Error
    if not RAMDISK_KEY < 1:
        return None
    df=None
    dd=None
    if code_l is not None:
        if table is not None:

            with SafeHDFStore(fname) as store:
                if store is not None:
                    try:
                        if '/' + table in store.keys():
                            dd=store[table]
                    except AttributeError, e:
                        store.close()
                        os.remove(store.filename)
                        log.error("AttributeError:%s %s"%(fname,e))
                        log.error("Remove File:%s"%(fname))
                    except Exception, e:
                        print "Exception:%s name:%s"%(fname,e)
                    else:
                        pass
                    finally:
                        pass

            if dd is not None and len(dd) > 0:
                if not MultiIndex:
                    if index:
                        code_l=map((lambda x: str(1000000 - int(x))
                                      if x.startswith('0') else x), code_l)
                    dif_co=list(set(dd.index) & set(code_l))
                    if len(code_l) > 0:
                        dratio=(float(len(code_l)) - float(len(dif_co))) / \
                            float(len(code_l))
                    else:
                        dratio = 0
                    # if dratio < 0.1 or len(dd) > 3100:

                    log.info("find all:%s :%s %0.2f" %
                            (len(code_l), len(code_l) - len(dif_co), dratio))
                    if timelimit and len(dd) > 0:
                       dd=dd.loc[dif_co]
                       o_time=dd[dd.timel <> 0].timel.tolist()
                    #                        if fname == 'powerCompute':
                    #                            o_time = sorted(set(o_time),reverse=True)
                       o_time=sorted(set(o_time), reverse=False)
                       o_time=[time.time() - t_x for t_x in o_time]

                       if len(dd) > 0:
                           # if len(dd) > 0 and (not cct.get_work_time() or len(o_time) <= ct.h5_time_l_count):
                           l_time=np.mean(o_time)
                           return_hdf_status=(not cct.get_work_time()) or (
                               cct.get_work_time() and l_time < limit_time)
                           # return_hdf_status = l_time < limit_time
                           # print return_hdf_status,l_time,limit_time
                           if return_hdf_status:
                               # df=dd
                               df = dd.loc[dif_co]
                               log.info("return hdf: %s timel:%s l_t:%s hdf ok:%s" % (
                                   fname, len(o_time), l_time, len(df)))
                       else:
                           log.error("%s %s o_time:%s %s" % (fname, table, len(
                               o_time), [time.time() - t_x for t_x in o_time[:3]]))
                       log.info('fname:%s l_time:%s' %
                                (fname, [time.time() - t_x for t_x in o_time]))

                    else:
                       df=dd.loc[dif_co]

                    if dratio > dratio_limit:
                       if len(code_l) > ct.h5_time_l_count * 10 and INIT_LOG_Error < 5:
                           # INIT_LOG_Error += 1
                           log.info("fn:%s cl:%s h5:%s don't find:%s dra:%0.2f log_err:%s" % (
                               fname, len(code_l), len(dd), len(code_l) - len(dif_co), dratio, INIT_LOG_Error))
                           return None


    #                 if dratio < dratio_limit:
    #                     log.info("find all:%s :%s %0.2f" %
    #                              (len(code_l), len(code_l) - len(dif_co), dratio))
    #                     if timelimit and len(dd) > 0:
    #                         dd=dd.loc[dif_co]
    #                         o_time=dd[dd.timel <> 0].timel.tolist()
    # #                        if fname == 'powerCompute':
    # #                            o_time = sorted(set(o_time),reverse=True)
    #                         o_time=sorted(set(o_time), reverse=False)
    #                         o_time=[time.time() - t_x for t_x in o_time]

    #                         if len(dd) > 0:
    #                             # if len(dd) > 0 and (not cct.get_work_time() or len(o_time) <= ct.h5_time_l_count):
    #                             l_time=np.mean(o_time)
    #                             return_hdf_status=(not cct.get_work_time()) or (
    #                                 cct.get_work_time() and l_time < limit_time)
    #                             # return_hdf_status = l_time < limit_time
    #                             # print return_hdf_status,l_time,limit_time
    #                             if return_hdf_status:
    #                                 # df=dd
    #                                 dd.loc[dif_co]
    #                                 log.info("return hdf: %s timel:%s l_t:%s hdf ok:%s" % (
    #                                     fname, len(o_time), l_time, len(df)))
    #                         else:
    #                             log.error("%s %s o_time:%s %s" % (fname, table, len(
    #                                 o_time), [time.time() - t_x for t_x in o_time[:3]]))
    #                         log.info('fname:%s l_time:%s' %
    #                                  (fname, [time.time() - t_x for t_x in o_time]))

    #                     else:
    #                         df=dd.loc[dif_co]
    #                 else:
    #                     if len(code_l) > ct.h5_time_l_count * 10 and INIT_LOG_Error < 5:
    #                         # INIT_LOG_Error += 1
    #                         log.error("fn:%s cl:%s h5:%s don't find:%s dra:%0.2f log_err:%s" % (
    #                             fname, len(code_l), len(dd), len(code_l) - len(dif_co), dratio, INIT_LOG_Error))
                else:
                    df = dd.loc[dd.index.isin(code_l, level='code')]
        else:
            log.error("%s is not find %s" % (fname, table))
    else:
        # h5 = get_hdf5_file(fname,wr_mode='r')
        if table is not None:
            with SafeHDFStore(fname) as store:
                # if store is not None:
                #     if '/' + table in store.keys():
                #         try:
                #             dd=store[table]
                #         except Exception as e:
                #             print ("%s fname:%s"%(e,fname))
                #             cct.sleep(ct.sleep_time)
                if store is not None:
                    try:
                        if '/' + table in store.keys():
                            dd=store[table]
                    except AttributeError, e:
                        store.close()
                        os.remove(store.filename)
                        log.error("AttributeError:%s %s"%(fname,e))
                        log.error("Remove File:%s"%(fname))
                    except Exception, e:
                        log.error("Exception:%s %s"%(fname,e))
                        print "Exception:%s name:%s"%(fname,e)
                    else:
                        pass
                    finally:
                        pass

            if dd is not None and len(dd) > 0:
                if timelimit:
                    if dd is not None and len(dd) > 0:
                        o_time=dd[dd.timel <> 0].timel.tolist()
                        o_time=sorted(set(o_time))
                        o_time=[time.time() - t_x for t_x in o_time]
                        if len(o_time) > 0:
                            l_time=np.mean(o_time)
                            # l_time = time.time() - l_time
                # return_hdf_status = not cct.get_work_day_status()  or not
                # cct.get_work_time() or (cct.get_work_day_status() and
                # (cct.get_work_time() and l_time < limit_time))
                            return_hdf_status=not cct.get_work_time() or (
                                cct.get_work_time() and l_time < limit_time)
                            log.info("return_hdf_status:%s time:%0.2f" %
                                     (return_hdf_status, l_time))
                            if return_hdf_status:
                                log.info("return hdf5 data:%s o_time:%s" %
                                         (len(dd), len(o_time)))
                                df=dd
                            else:
                                log.info("no return time hdf5:%s" % (len(dd)))
                        log.info('fname:%s l_time:%s' %
                                 (fname, [time.time() - t_x for t_x in o_time]))
                else:
                    df=dd
            else:
                log.error("%s is not find %s" % (fname, table))
        else:
            log.error("% / table is Init None:%s"(fname, table))

    if df is not None and len(df) > 0:
        df=df.fillna(0)
        if 'timel' in df.columns:
            time_list=df.timel.tolist()
            # time_list = sorted(set(time_list),key = time_list.index)
            time_list=sorted(set(time_list))
            # log.info("test:%s"%(sorted(set(time_list),key = time_list.index)))
            if time_list is not None and len(time_list) > 0:
                df['timel']=time_list[0]
                log.info("load hdf times:%s" %
                         ([time.time() - t_x for t_x in time_list]))

    log.info("load_hdf_time:%0.2f" % (time.time() - time_t))

    if df is not None:
        df=df[~df.index.duplicated(keep='last')]
        if fname.find('MultiIndex') > 0 and 'volume' in df.columns:
            count_drop = len(df)
            df = df.drop_duplicates()
            # df = df.drop_duplicates('volume',keep='last')
            dratio=round((float(len(df))) / float(count_drop),2)
            log.debug("all:%s  drop:%s  dratio:%.2f"%(int(count_drop/100),int(len(df)/100),dratio))
            if dratio < 0.8:
                log.error("MultiIndex drop_duplicates:%s %s dr:%s"%(count_drop,len(df),dratio))
                if isinstance(df.index, pd.core.index.MultiIndex):
                    write_hdf_db(fname, df, table=table, index=index, MultiIndex=True,rewrite=True)

    # df = df.drop_duplicates()

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

    #    import tushare as ts
    #    df = ts.get_k_data('300334', start='2017-04-01')
    # p=subprocess.Popen('dir', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    # p=subprocess.Popen('ptrepack --chunkshape=auto --complevel=9 --complib=zlib "D:\MacTools\WorkFile\WorkSpace\pyQuant\tdx_all_df_300.h5_tmp" "D:\MacTools\WorkFile\WorkSpace\pyQuant\tdx_all_df_300.h5"', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    # import commands
    # ret,output = commands.getstatusoutput('C:\Users\Johnson\Anaconda2\Scripts\ptrepack --chunkshape=auto --complevel=9 --complib=zlib "D:\MacTools\WorkFile\WorkSpace\pyQuant\tdx_all_df_300.h5_tmp" "D:\MacTools\WorkFile\WorkSpace\pyQuant\tdx_all_df_300.h5"')
    # print output.decode('gbk'),ret
    # ret,output = commands.getstatusoutput('C:\Users\Johnson\Anaconda2\Scripts\ptrepack.exe')
    # ret,output = commands.getstatusoutput('dir')
    # print output.decode('gbk')


    # import os
    # fp=os.popen('ptrepack --chunkshape=auto --complevel=9 --complib=zlib   ../../tdx_all_df_300.h5_tmp  ../../tdx_all_df_300.h5')
    # print fp.read().decode('gbk')
    


    # p=subprocess.Popen('ptrepack --chunkshape=auto --complevel=9 --complib=zlib ../../tdx_all_df_300.h5_tmp ../../tdx_all_df_300.h5"', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    # p.wait()
    # print p.stdout.read().decode("gbk")
    # print p.stderr
    # import ipdb;ipdb.set_trace()


    a = np.random.standard_normal((9000,4))
    df = pd.DataFrame(a)
    h5_fname = 'test_s.h5'
    h5_table = 'all'
    h5 = write_hdf_db(h5_fname, df, table=h5_table, index=False, baseCount=500, append=False, MultiIndex=False)
    import ipdb;ipdb.set_trace()

    fname=['sina_data.h5', 'tdx_last_df', 'powerCompute.h5', 'get_sina_all_ratio']
    # fname=['test_s.h5','sina_data.h5', 'tdx_last_df', 'powerCompute.h5', 'get_sina_all_ratio']
    fname=['test_s.h5']
    # fname = 'powerCompute.h5'
    for na in fname:
        with SafeHDFStore(na) as h5:
            import ipdb;ipdb.set_trace()
            print(h5)
            if '/' + 'all' in list(h5.keys()):
                print(h5['all'].loc['600007'])
        # h5.remove('high_10_y_20170620_all_15')
        # print h5
        # dd = h5['d_21_y_all']
        # print len(set(dd.timel))
        # print time.time()- np.mean(list(set(dd.timel)))

    # Only put inside this block the code which operates on the store
    # store['result'] = df
