import tushare as ts
import stock.emacount as ema

#get now hot 10
date_top={}
df = ts.get_today_all()
top=df[ df['changepercent'] > 3]
# top=df[ df['changepercent'] <6]
print "top:",len(top['code'])
# for code in top['code']:
tick_mean=[]

gold={}
goldl=[]
# for code in ['601608']:
for code in top['code']:
    dtick = ts.get_today_ticks(code)
    d_hist=ema.getdata_ema_trend(code,'10','d')
    # print d_hist
    day_t=ema.get_today()
    # if len(dtick.index) == 0:
    #     dtick=d_hist[]
    if day_t in d_hist.index:
        dl=d_hist.drop(day_t).index
    else:
        dl=d_hist.index
    # print dl
    # print dl
    ep_list=[]
    for da in dl.values:
        # print da
        td=ts.get_tick_data(code,da)
        # print td
        if len(td) >0:
            ep = td['amount'].sum()/td['volume'].sum()
            ep_list.append(ep)
        # print ("D: %s P: %s"%(da,ep))
    total_ave=ema.less_average(ep_list)
    if len(dtick.index) > 0:
        ep = dtick['amount'].sum()/dtick['volume'].sum()
        if ep >= total_ave:
            gold[code]=d_hist
            goldl.append(code)
            print ("code:%s ep:%s ave:%s"%(code,ep,total_ave))

print "goldl:%s",goldl
# print gold
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