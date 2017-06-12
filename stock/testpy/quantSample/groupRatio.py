# -*- coding:utf-8 -*-

import tushare as ts
import numpy as np
import pandas as pd


# 股票涨跌幅检查，不能超过 10% ，过滤掉一些不合法的数据
def _valid_price(g):
    return (((g.max() - g.min()) / g.min()) < 0.223).all()

# 定义产生分组索引的函数，比如我们要计算的周期是 20 天，则按照日期，20 个交易日一组
def gen_item_group_index(total, group_len):
    """ generate an item group index array

    suppose total = 10, unitlen = 2, then we will return array [0 0 1 1 2 2 3 3 4 4]
    """

    group_count = total / group_len
    group_index = np.arange(total)
    for i in range(group_count):
        group_index[i * group_len: (i + 1) * group_len] = i
    group_index[(i + 1) * group_len : total] = i + 1
    return group_index.tolist()

# 针对下跌的波动，我们把最高价设置为负数。什么是下跌的波动？就是先出现最高价，再出现最低价
def _ceiling_price(g):
    return g.idxmin() < g.idxmax() and np.max(g) or (-np.max(g))


def stock_ripples_batch(basedir='data', period=20):
    """ select the top 10 stock which have largest ripple range """

    if not os.path.isdir(basedir) or not os.path.exists(basedir):
        print('error: idirectory not exist. %s' % basedir)
        return

    def _mean_rise_ripple(f):
        ripples = stock_ripples(os.path.join(basedir, f), period)
        if ripples is None:
            return np.nan
        mean_ripples = ripples.head(10).ripples_radio.mean()
        return mean_ripples

    def _mean_fall_ripple(f):
        ripples = stock_ripples(os.path.join(basedir, f), period)
        if ripples is None:
            return np.nan
        mean_ripples = ripples.tail(10).ripples_radio.mean()
        return mean_ripples

    _stock_id = lambda f: f.split('.')[0]
    files = os.listdir(basedir)
    ripples_list = [(_stock_id(f), _mean_rise_ripple(f), _mean_fall_ripple(f)) for f in files if f.endswith('.csv')]

    ripples = pd.DataFrame(ripples_list, columns=['stock_id', 'mean_rise_ripples', 'mean_fall_ripples'])

    top = 10
    all_ripples = ripples.dropna().sort_values('mean_rise_ripples', ascending=False)

    print('top %d rise ripples in period of %d for all the stocks in %s:' % (top, period, basedir))
    print(all_ripples.head(top))

    return all_ripples

data=ts.get_hist_data('600208',start='2012-09-31')
idx=data.index
period = 30

group_index = gen_item_group_index(len(data), period)
# 把分组索引数据添加到股票数据里
data['group_index'] = group_index
print len(data)
data.head().append(data.tail())


# 根据索引分组计算
group = data.groupby('group_index').agg({
                                        'volume': 'sum',
                                        'low': 'min',
                                        'high': _ceiling_price})
print  group.head()

# 添加每个分组的起始日期
date_col = pd.DataFrame({"group_index": group_index, "date": idx})
group['date'] = date_col.groupby('group_index').agg('first')
print group.head()

# 添加我们的波动指标 股票波动系数 = 最高价/最低价
group['ripples_radio'] = group.high / group.low
print  group.head()


# 降序排列。我们把分组的起始日期，交易量总和都列出来，也可以观察一下交易量和股票波动比的关系
ripples = group.sort_values('ripples_radio', ascending=False)
print  ripples.head()

print ripples.head(10).ripples_radio.mean()
print ripples.tail(10).ripples_radio.mean()
ripples = group.sort_values('ripples_radio', ascending=False)
print ripples.head()
print ripples.tail()
# print stock_ripples_batch(basedir=data, period=20)
# 按照日期分组
# days = raw.groupby(level=0).agg(
#     {'opening_price': lambda g: _valid_price(g) and g[0] or 0,
#      'ceiling_price': lambda g: _valid_price(g) and np.max(g) or 0,
#      'floor_price': lambda g: _valid_price(g) and np.min(g) or 0,
#      'closing_price': lambda g: _valid_price(g) and g[-1] or 0,
#      'volume': 'sum',
#      'amount': 'sum'})
# days.head()


# 填充数据：生成日期索引
# l = len(qdhr)
# start = qdhr.iloc[0:1].index.tolist()[0]
# end = qdhr.iloc[l - 1: l].index.tolist()[0]
# idx = pd.date_range(start=start, end=end)
# idx
# data = qdhr.reindex(idx)
# zvalues = data.loc[~(data.volume > 0)].loc[:, ['volume', 'amount']]
# data.update(zvalues.fillna(0))
# data.fillna(method='ffill', inplace=True)
# data.head()