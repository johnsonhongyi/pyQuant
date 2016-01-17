# -*- coding:utf-8 -*-
import time

import pandas as pd

import LineHistogram as lrh
from JSONData import realdatajson as rl

if __name__ == "__main__":
    # df=sina_data.Sina().all.set_index('code')
    def get_market_status(mk):
        df = rl.get_sina_Market_json(mk).set_index('code')
        time_s = time.time()
        code_l = []
        for code in df.index:
            status, lenday = lrh.get_linear_model_status(code)
            if status:
                # print(df.loc[code,:])
                if df.loc[code, 'percent'] > 0 and lenday > 200:
                    code_l.append(df.loc[code, :])
                    # break
        gold_f = pd.DataFrame(code_l)
        print ("timeSearch:%s" % (time.time() - time_s))
        print ("gold:%s %s :%s" % (mk, len(gold_f), gold_f.iloc[:2, 0:2]))
        return gold_f


    # result = cct.to_mp_run(get_market_status, ['sh', 'sz'])
    # df = pd.DataFrame()
    # for x in result:
    #     df = df.append(x)
    # print len(df)
    # df.iloc[:, 0:2].to_csv('stock-Line.csv', encoding='utf8')
    result = get_market_status('cyb')
    print ("gold:%s" % result.iloc[:2, 0:3])
