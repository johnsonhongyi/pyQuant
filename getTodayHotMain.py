import tushare as ts
import sys
import stock.emacount as ema
import stock.singleAnalyseUtil as sl


# get now hot 10
# date_top={}
# tick_mean=[]

# gold={}
# goldl=[]
# for code in ['601608']:
def get_all_top():
    gold = {}
    goldl = []
    df = ts.get_today_all()
    top = df[df['changepercent'] > 6]
    print "top:", len(top['code'])
    for code in top['code']:
        ave=sl.get_single_ave_compare(code)

def get_all_hot():
    try:
        gold = {}
        goldl = []
        df = ts.get_today_all()
        top = df[df['changepercent'] > 6]
        top = top[top['changepercent'] <11]
        print "top:", len(top['code'])

        for code in top['code']:
            dtick = ts.get_today_ticks(code)
            d_hist = ema.getdata_ema_trend(code, '10', 'd')
            # print d_hist
            day_t = ema.get_today()
            # if len(dtick.index) == 0:
            #     dtick=d_hist[]
            if day_t in d_hist.index:
                dl = d_hist.drop(day_t).index
            else:
                dl = d_hist.index
            # print dl
            # print dl
            ep_list = []
            for da in dl.values:
                # print da
                td = ts.get_tick_data(code, da)
                # print td
                if len(td) > 0:
                    ep = td['amount'].sum() / td['volume'].sum()
                    ep_list.append(ep)
                    # print ("D: %s P: %s"%(da,ep))
            total_ave = ema.less_average(ep_list)
            if len(dtick.index) > 0:
                ep = dtick['amount'].sum() / dtick['volume'].sum()
                if ep >= total_ave:
                    gold[code] = d_hist
                    goldl.append(code)
                    print ("code:%s ep:%s ave:%s" % (code, ep, total_ave))
    except (IOError, EOFError, KeyboardInterrupt):
        # print "key"
        # print "break"
        print "why"
        return


def disp_all_data(list):
    goldl = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
    if len(goldl) > 0:
        for x in range(len(goldl)):
            # print "goldl:",goldl
            if x % 4 == 3:
                print "%s" % (goldl[x])
            else:
                print "%s" % (goldl[x]),
    print ""
    num_input = raw_input("end")
    if num_input:
        sys.exit()


if __name__ == '__main__':
	get_all_hot()
    # sl.get_single_ave_compare()
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
