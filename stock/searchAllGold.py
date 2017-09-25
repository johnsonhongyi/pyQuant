# -*- coding:utf-8 -*-
import datetime
import time

import pandas as pd

import JohnsonUtil.commonTips as cct
# from JSONData import LineHistogram as lrh
from JSONData import powerCompute as pct
from JSONData import realdatajson as rl
from JSONData import tdx_data_Day as tdd

base_path = tdd.get_tdx_dir()
block_path = tdd.get_tdx_dir_blocknew() + '068.blk'
block_path_d = tdd.get_tdx_dir_blocknew() + '069.blk'
if __name__ == "__main__":
    # df=sina_data.Sina().all.set_index('code')
    today = datetime.date.today()
    print today


    def get_market_status(mk, type='m', start=None, end=None):
        df = rl.get_sina_Market_json(mk).set_index('code')
        time_s = time.time()
        code_l = []
        code_d = []
        for code in df.index:
            status, lenday, diff = pct.get_linear_model_status_LSH(code, type=type, start=start, end=end)
            # op, ra, status, dss = pct.get_linear_model_status(code, type=type, start=start, end=end)
            if status:
                # print(df.loc[code,:])
                # if df.loc[code, 'percent'] > 0 and lenday > 200:
                if df.loc[code, 'trade'] != 0 and lenday > 200:
                    df.loc[code, 'diff'] = abs(diff)
                    code_l.append(df.loc[code, :])
            elif df.loc[code, 'trade'] != 0 and lenday > 200:
                df.loc[code, 'diff'] = abs(diff)
                code_d.append(df.loc[code, :])

        # gold_f = pd.DataFrame(code_l).sort_values(by=['diff'], ascending=[0])
        # down_f = pd.DataFrame(code_d).sort_values(by=['diff'], ascending=[0])
        gold_f = pd.DataFrame(code_l)
        down_f = pd.DataFrame(code_d)
        print("timeSearch:%s" % (time.time() - time_s))
        print("gold:%s %s :%s" % (mk, len(gold_f), gold_f.iloc[:1, 0:2]))
        print("down:%s %s :%s" % (mk, len(down_f), down_f.iloc[:1, 0:2]))
        return gold_f, down_f

    # result = cct.to_mp_run(get_market_status, ['sh', 'sz'])
    # df = pd.DataFrame()
    # for x in result:
    #     df = df.append(x)
    # print len(df)
    # df.iloc[:, 0:2].to_csv('stock-Line-%s.csv'%today, encoding='utf8')
    type = 'l'
    start = '2016-01-18'
    # start = None
    market = 'sh'
    df_u, df_d = get_market_status(market, type, start)
    if not type == 'l':
        if len(df_u) > 0:
            print("Type: %s wri gold:%s %s" % (type, len(df_u.index.tolist()), block_path))
            df_u.iloc[:, 0:2].to_csv(
                'stock-Line-%s.csv' % today, encoding='utf8')
            cct.write_to_blocknew(block_path, df_u.index.tolist(), False)
    else:
        if len(df_u) > 0:
            print("Type: %s wri down:%s %s" % (type, len(df_d.index.tolist()), block_path_d))
            df_d.iloc[:, 0:2].to_csv(
                'stock-Line-down-%s.csv' % today, encoding='utf8')
            cct.write_to_blocknew(block_path_d, df_d.index.tolist(), False)
