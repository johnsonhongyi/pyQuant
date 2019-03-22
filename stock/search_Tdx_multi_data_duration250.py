import sys,logging
stdout=sys.stdout
sys.path.append('../../')
import JSONData.tdx_data_Day as tdd
from  JSONData import sina_data 
from  JSONData import tdx_hdf5_api as h5a
from JohnsonUtil import commonTips as cct
import pandas as pd
sys.stdout=stdout

import time,random
start = None
time_s = time.time()
# code_list = ['399006','000001','999999']

def get_roll_mean_all(single=True,tdx=False,app=True,duration=100):
    # df = tdd.search_Tdx_multi_data_duration('tdx_all_df_300', 'all_300', df=None,code_l=code_list, start=start, end=None, freq=None, col=None, index='date')
    block_path = tdd.get_tdx_dir_blocknew() + '060.blk'

    if not app and cct.get_file_size(block_path) > 100 and cct.creation_date_duration(block_path) == 0:
        print "It's Today Update"
        return True
    code_list = sina_data.Sina().market('all').index.tolist()
    print "all code:",len(code_list)
    df = tdd.search_Tdx_multi_data_duration('tdx_all_df_300', 'all_300', df=None,code_l=code_list, start='20150501', end=None, freq=None, col=None, index='date')
    code_uniquelist=df.index.get_level_values('code').unique()
    code_select = code_uniquelist[random.randint(0,len(code_uniquelist)-1)]
    print round(time.time()-time_s,2),df.index.get_level_values('code').unique().shape,code_select,df.loc[code_select][-1:]
    # df.groupby(level=[0]),df.index.get_level_values(0)
    # len(df.index.get_level_values('code').unique())
    # df = df[~df.index.duplicated(keep='first')]
    dfs = df
    groupd = dfs.groupby(level=[0])
    # rollma = ['5','10','60','100','200']
    # rollma = ['5','10','250']
    rollma = [duration]
    # import ipdb;ipdb.set_trace()
    # df.loc['300130'][:2]
    for da in rollma:
        cumdays=int(da)
        dfs['ma%d'%cumdays] = groupd['close'].apply(pd.rolling_mean, cumdays)
        # dfs['amount%d'%cumdays] = groupd['amount'].apply(pd.rolling_mean, cumdays)
    # df.ix[df.index.levels[0]]
    #df.ix[df.index[len(df.index)-1][0]] #last row
    # dfs = tdd.search_Tdx_multi_data_duration(df=dfs,code_l=code_list, start='20170918', end='20170918', freq=None, col=None, index='date')




    # print dfs[:1],len(dfs)
    # groupd.agg({'low': 'min'})
    # '''idx mask filter'''
    # '''
    dt_low = None
    if single:
        dfs = groupd.tail(1)

    else:
        dl = 30
        dindex = tdd.get_tdx_Exp_day_to_df(
            '999999', dl=30).sort_index(ascending=False)
        dt = tdd.get_duration_price_date('999999', df=dindex)
        dt = dindex[dindex.index >= dt].index.values
        dt_low = dt[-1]
        dtlen = len(dt) if len(dt) >0 else 1
        dfs = groupd.tail(dtlen)
        single = True
        
    dfs = dfs.fillna(0)
    idx = pd.IndexSlice
    # mask = (dfs[('ma%s')%(rollma[0])] > dfs[('ma%s')%(rollma[1])]) & (dfs[('ma%s')%(rollma[-1])] > 0) & (dfs[('close')] > dfs[('ma%s')%(rollma[0])])  & (dfs[('close')] > dfs[('ma%s')%(rollma[-1])]) 
    # mask = (dfs[('ma%s')%(rollma[0])] > dfs[('ma%s')%(rollma[1])]) & (dfs[('ma%s')%(rollma[-1])] > 0) & (dfs[('close')] > dfs[('ma%s')%(rollma[1])])  & (dfs[('close')] > dfs[('ma%s')%(rollma[-1])]) 
    # mask = (dfs[('ma%s')%(rollma[0])] > dfs[('ma%s')%(rollma[1])]) & (dfs[('ma%s')%(rollma[-1])] > 0) &  (dfs[('close')] > dfs[('ma%s')%(rollma[-1])]) 
   

    mask = ((dfs[('ma%s')%(rollma[-1])] > 0) & (dfs[('close')] > dfs[('ma%s')%(rollma[-1])])) 
    # mask = ((dfs[('close')] > dfs[('ma%s')%(rollma[-1])])) 
    df=dfs.loc[idx[mask, :]]

    # groupd.first()[:2],groupd.last()[:2]
    # groupd = df250.groupby(level=[0])
    # '''
    # groupd.transform(lambda x: x.iloc[-1])
    # groupd.last()
    # groupd.apply(lambda x: x.close > x.ma250)
    # df.shape,df.sort_index(ascending=False)[:5]
    # ?groupd.agg
    # groupd = df.groupby(level=[0])
    # groupd['close'].apply(pd.rolling_mean, 250, min_periods=1)
    #ex:# Group df by df.platoon, then apply a rolling mean lambda function to df.casualties
     # df.groupby('Platoon')['Casualties'].apply(lambda x:x.rolling(center=False,window=2).mean())

    code_uniquelist=df.index.get_level_values('code').unique()
    code_select = code_uniquelist[random.randint(0,len(code_uniquelist)-1)]
    if app:
        print round(time.time()-time_s,2),'s',df.index.get_level_values('code').unique().shape,code_select,df.loc[code_select][-1:]

    if single:
        # groupd = df.groupby(level=[0])
        if tdx:
            # block_path = tdd.get_tdx_dir_blocknew() + '060.blk'
            # if cct.get_work_time():
            #     codew = df[df.date == cct.get_today()].index.tolist()
            if dt_low is not None:
                groupd2 = df.groupby(level=[0])
                df = groupd2.head(1)
                df = df.reset_index().set_index('code')
                # import ipdb;ipdb.set_trace()

                df = df[(df.date >= dt_low) & (df.date <= cct.get_today())]
                codew = df.index.tolist()
                if app:
                    print round(time.time()-time_s,2),'groupd2',len(df)

            else:
                df = df.reset_index().set_index('code')
                df = df[(df.date >= cct.last_tddate(days=10)) & (df.date <= cct.get_today())]
                codew = df.index.tolist()

            if app:
                hdf5_wri = cct.cct_raw_input("rewrite code [Y] or append [N]:")
                if hdf5_wri == 'y' or hdf5_wri == 'Y':
                    append_status=False
                else:
                    append_status=True
            else:
                append_status=False
            if len(codew) > 10: 
                cct.write_to_blocknew(block_path, codew, append_status,doubleFile=False,keep_last=0)
                print "write:%s"%(len(codew))
            else:
                print "write error:%s"%(len(codew))

        # df['date'] = df['date'].apply(lambda x:(x.replace('-','')))
        # df['date'] = df['date'].astype(int)
        # print df.loc[code_select].T,df.shape
        MultiIndex = False
    else:
        MultiIndex = True
    h5a.write_hdf_db('all300', df, table='roll200', index=False, baseCount=500, append=False, MultiIndex=MultiIndex)
    return df

if __name__ == '__main__':
    get_roll_mean_all(single=False,tdx=True,app=True,duration=250)
    # get_roll_mean_all(single=True,tdx=True,app=True)
    # get_roll_mean_all(single=True,tdx=True,app=False)