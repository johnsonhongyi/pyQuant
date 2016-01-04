import tushare as ts
import stock.emacount as ema

#get now hot 10
date_top={}
# df = ts.get_today_all()
# top=df[df['changepercent'] > 9.9]

# for code in top['code']:
tick_mean=[]

for code in ['601608']:
    dtick = ts.get_today_ticks(code)
    d_hist=ema.getdata_ema_trend(code,'10','d')
    # print d_hist
    day_t=ema.get_today()
    if day_t in d_hist.index:
        dl=d_hist.drop(day_t).index
    else:
        dl=d_hist.index
    # print dl
    # print dl
    for da in dl.values:
        # print da
        td=ts.get_tick_data(code,da)
        # print td
        ep = td['amount'].sum()/td['volume'].sum()
        print ("D: %s P: %s"%(da,ep))
    ep = dtick['amount'].sum()/dtick['volume'].sum()
    print "today: ",ep
# print top_count

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