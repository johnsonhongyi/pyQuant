import tushare as ts
from datetime import timedelta, date

stocklist=['601198']

def get_today():

    TODAY = date.today()
    today=TODAY.strftime('%Y-%m-%d')
    return today

def get_trade_status(date):
    today=get_today()
    if date==today:
        pass

def get_day_of_day(n=0):
    '''''
    if n>=0,date is larger than today
    if n<0,date is less than today
    date format = "YYYY-MM-DD"
    '''
    # if(n<0):
    n = abs(n)
    da=(date.today()-timedelta(days=n))
    dt=da.strftime('%Y-%m-%d')
    return dt
    # else:
    #     da=(date.today()+timedelta(days=n))
    #     dt=da.strftime('%Y-%m-%d')
    #     return dt

def get_mean_price(price):
    pass

def get_ts_start_date(stock,datelen,type=None):
    '''
    :param stock: code
    :param datelen: date lenth
    :param type: day or week
    :return:start_date
    '''

    datelen=int(datelen)
    # start_date=get_day_of_day(datelen)
    # print start_date,stock
    if type != None:
        df = ts.get_hist_data(stock,ktype=type)
    else:
        df = ts.get_hist_data(stock)
    # day_t=get_today()
    # if day_t in df.index:
    #     # print "daynow"
    #     df=df.drop(day_t)
    if not df.empty:
        if df['open'].count < datelen:
            start_date = (df.index)[-1]
        else:
            start_date =  (df.index)[datelen-1]
    else:
        print ("data err,pls check dataframe")
    return  start_date

def getdata_ema_trend(stock,datelenth,type=None):
    # if datalen == '10':
    #     print ("datalen not 10")
    # else:
    #     print ("len:",datalen)
    # df = ts.get_tick_data(stock)
    start_date=get_ts_start_date(stock,datelenth,type)
    print ("\nstart: %s  stock: %s" %(start_date[-5:],stock))
    if type !=None:
        df = ts.get_hist_data(stock,start=start_date,ktype=type)
    else:
        df = ts.get_hist_data(stock,start=start_date)
    # countnum = df['open'].count()
    # print ('countnum:',countnum)
    # open_p=df['open'].mean()
    # low_p=df['open'].mean()
    # close_p=df['close'].mean()
    # print ("open_p:",open_p)
    # print  ("close_p:",close_p)
    # real_df=ts.get_realtime_quotes(stock)
    # real_o=(real_df['open'])[0]
    # real_c=(real_df['price'])[0]
    # real_perc=(real_df['pre_close'])[0]
    # print ("open:%s  lastc:%s nowp:%s"%(real_o,real_perc,real_c))
    return df

def getdata_ema_trend_silent(stock,datelenth,type=None):
    # if datalen == '10':
    #     print ("datalen not 10")
    # else:
    #     print ("len:",datalen)
    # df = ts.get_tick_data(stock)
    start_date=get_ts_start_date(stock,datelenth,type)
    # print ("\nstart: %s  stock: %s" %(start_date[-5:],stock))
    if type !=None:
        df = ts.get_hist_data(stock,start=start_date,ktype=type)
    else:
        df = ts.get_hist_data(stock,start=start_date)
    # countnum = df['open'].count()
    # print ('countnum:',countnum)
    # open_p=df['open'].mean()
    # low_p=df['open'].mean()
    # close_p=df['close'].mean()
    # print ("open_p:",open_p)
    # print  ("close_p:",close_p)
    # real_df=ts.get_realtime_quotes(stock)
    # real_o=(real_df['open'])[0]
    # real_c=(real_df['price'])[0]
    # real_perc=(real_df['pre_close'])[0]
    # print ("open:%s  lastc:%s nowp:%s"%(real_o,real_perc,real_c))
    return df

def less_average(score):
  num = len(score)
  sum_score = sum(score)
  ave_num = sum_score/num
  # less_ave = [i for i in score if i<ave_num]
  return ave_num

if __name__ == '__main__':
    dayl='10'
    # start_d=get_ts_start_date('601198',dayl,'w')
    # print start_d
    data=getdata_ema_trend('601198','10','d')
    ser=data.mean()
    print data.describe()['open']['mean']

    print data.mean()['ma5']

     # dz['2015-06-02']
     # 41.399999999999999
     #
     # dz[dz >= 38.11].argmax()
     # u'2015-06-02'
     #
     # dz[dz <= 15.11].argmax()
     # u'2015-09-29'
     #
     # dz[dz <= 15.11].argmin()
     # u'2015-02-26'
    # dz[dz == 15].index[0]
    # td=ts.get_tick_data('601198',date='2015-11-26')
    # td['amount'].sum()/td['volume'].sum()
    # print ("data:",data)