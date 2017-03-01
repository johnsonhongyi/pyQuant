# -*- coding: utf-8 -*-
from datetime import datetime
# from merge_line_dto import MergeLineDTO
# from k_line_dto import KLineDTO
# from sql_lite_util import *
__author__ = 'SUM'




# 入的开高低收都是ndarray格式的一个向量

def Kplot(Open,High,Low,Close):
    length=len(Close)

    fig = plt.figure()
    ax1 = plt.axes([0,0,3,2])

    X=np.array(range(0, length))
    pad_nan=X+nan

    #计算上 下影线
    max_clop=Close.copy()
    max_clop[Close<Open]=Open[Close<Open]
    min_clop=Close.copy()
    min_clop[Close>Open]=Open[Close>Open]

    #上影线
    line_up=np.array([High,max_clop,pad_nan])
    line_up=np.ravel(line_up,'F')
    #下影线
    line_down=np.array([Low,min_clop,pad_nan])
    line_down=np.ravel(line_down,'F')

    #计算上下影线对应的X坐标
    pad_nan=nan+X
    pad_X=np.array([X,X,X])
    pad_X=np.ravel(pad_X,'F')


    #画出实体部分,先画收盘价在上的部分
    up_cl=Close.copy()
    up_cl[Close<=Open]=nan
    up_op=Open.copy()
    up_op[Close<=Open]=nan

    down_cl=Close.copy()
    down_cl[Open<=Close]=nan
    down_op=Open.copy()
    down_op[Open<=Close]=nan


    even=Close.copy()
    even[Close!=Open]=nan

    #画出收红的实体部分
    pad_box_up=np.array([up_op,up_op,up_cl,up_cl,pad_nan])
    pad_box_up=np.ravel(pad_box_up,'F')
    pad_box_down=np.array([down_cl,down_cl,down_op,down_op,pad_nan])
    pad_box_down=np.ravel(pad_box_down,'F')
    pad_box_even=np.array([even,even,even,even,pad_nan])
    pad_box_even=np.ravel(pad_box_even,'F')

    #X的nan可以不用与y一一对应
    X_left=X-0.25
    X_right=X+0.25
    box_X=np.array([X_left,X_right,X_right,X_left,pad_nan])
    box_X=np.ravel(box_X,'F')




    #Close_handle=plt.plot(pad_X,line_up,color='k')

    vertices_up=array([box_X,pad_box_up]).T
    vertices_down=array([box_X,pad_box_down]).T
    vertices_even=array([box_X,pad_box_even]).T

    handle_box_up=mat.patches.Polygon(vertices_up,color='r',zorder=1)
    handle_box_down=mat.patches.Polygon(vertices_down,color='g',zorder=1)
    handle_box_even=mat.patches.Polygon(vertices_even,color='k',zorder=1)

    ax1.add_patch(handle_box_up)
    ax1.add_patch(handle_box_down)
    ax1.add_patch(handle_box_even)

    handle_line_up=mat.lines.Line2D(pad_X,line_up,color='k',linestyle='solid',zorder=0)
    handle_line_down=mat.lines.Line2D(pad_X,line_down,color='k',linestyle='solid',zorder=0)

    ax1.add_line(handle_line_up)
    ax1.add_line(handle_line_down)

    v=[0,length,Open.min()-0.5,Open.max()+0.5]
    plt.axis(v)


# K线DTO
class KLineDTO(object):

    day = datetime.now()
    begin_time = datetime.now()
    end_time = datetime.now()
    open = 0.0
    high = 0.0
    low = 0.0
    close = 0.0

    def __init__(self, day, begin_time, end_time, open, high, low, close):
        self.day = day
        self.begin_time = begin_time
        self.end_time = end_time
        self.open = open
        self.high = high
        self.low = low
        self.close = close

    def __str__(self):
        return "(" + self.day.strftime('%Y-%m-%d %H:%M:%S') + ", " \
               + self.begin_time.strftime('%Y-%m-%d %H:%M:%S') + ", " \
               + self.end_time.strftime('%Y-%m-%d %H:%M:%S') + ")"

# --------------------------------

# 合并后的K线DTO
class MergeLineDTO(object):

    memberList = []
    stick_num = 0
    begin_time = datetime.now()
    end_time = datetime.now()
    high = 0.0
    low = 0.0
    is_peak = 'N'
    is_bottom = 'N'
    member_list = []  # KLineDTO[]

    def __init__(self, stick_num, begin_time, end_time, high, low, is_peak, is_bottom):
        self.stick_num = stick_num
        self.begin_time = begin_time
        self.end_time = end_time
        self.high = high
        self.low = low
        self.is_peak = is_peak
        self.is_bottom = is_bottom

    def __str__(self):
        return "(" + self.begin_time.strftime('%Y-%m-%d %H:%M:%S') + ", " \
               + self.end_time.strftime('%Y-%m-%d %H:%M:%S') + ")"

# --------------------------------

def set_peak_and_bottom_flag(merge_line_list):
    #  标记顶和底
    #  []MergeLineDTO

    if len(merge_line_list) < 3:
        return

    #  顶和底,暂不考虑是否公用k线

    i = 1
    while i < len(merge_line_list)-1:
        first_dto = merge_line_list[i-1]
        middle_dto = merge_line_list[i]
        last_dto = merge_line_list[i+1]
        if middle_dto.high > max(first_dto.high, last_dto.high) \
                and middle_dto.low > max(first_dto.low, last_dto.low):
            middle_dto.is_peak = 'Y'

        if middle_dto.high < min(first_dto.high, last_dto.high) \
                and middle_dto.low < min(first_dto.low, last_dto.low):
            middle_dto.is_bottom = 'Y'

        i += 1


def is_inclusive(merge_line_dto, high_price, low_price):
    #  判断是否存在包含关系
    #  MergeLineDTO, float, float
    if (merge_line_dto.high >= high_price and merge_line_dto.low <= low_price)\
            or (merge_line_dto.high <= high_price and merge_line_dto.low >= low_price):
        return True
    return False


def is_down(merge_line_dto, high_price, low_price):
    #  是否方向向下
    #  MergeLineDTO, float, float
    if merge_line_dto.high > high_price and merge_line_dto.low > low_price:
        return True
    return False


def is_up(merge_line_dto, high_price, low_price):
    #   是否方向向上
    #  MergeLineDTO, float, float
    if merge_line_dto.high < high_price and merge_line_dto.low < low_price:
        return True
    return False


def merge_k_line(merge_line_dto, k_line_dto, trend):
    #  合并K线
    #  MergeLineDTO, KLineDTO, string
    if trend == 'up':
        merge_line_dto.high = max(merge_line_dto.high, k_line_dto.high)
        merge_line_dto.low = max(merge_line_dto.low, k_line_dto.low)
        merge_line_dto.end_time = k_line_dto.end_time
    if trend == 'down':
        merge_line_dto.high = min(merge_line_dto.high, k_line_dto.high)
        merge_line_dto.low = min(merge_line_dto.low, k_line_dto.low)
        merge_line_dto.end_time = k_line_dto.end_time
    merge_line_dto.end_time = k_line_dto.end_time
    merge_line_dto.member_list.append(k_line_dto)
    merge_line_dto.stick_num += 1


def find_peak_and_bottom(k_line_list, begin_trend):  # []KLineDTO
    #  寻找真正的顶和底
    #  []KLineDTO, string
    k_line_dto = k_line_list[0]

    merge_line_dto = MergeLineDTO(1, k_line_dto.begin_time, k_line_dto.end_time,
                                  k_line_dto.high, k_line_dto.low, 'N', 'N')

    merge_line_list = [merge_line_dto]
    trend = begin_trend

    i = 1
    while i < len(k_line_list):

        today_k_line_dto = k_line_list[i]
        last_m_line_dto = merge_line_list[len(merge_line_list)-1]
        if is_inclusive(last_m_line_dto, today_k_line_dto.high, today_k_line_dto.low):
            #  假如存在包含关系,合并K线
            merge_k_line(last_m_line_dto, today_k_line_dto, trend)
        else:
            if is_up(last_m_line_dto, today_k_line_dto.high, today_k_line_dto.low):
                trend = "up"
            elif is_down(last_m_line_dto, today_k_line_dto.high, today_k_line_dto.low):
                trend = "down"

            this_mline_dto = MergeLineDTO(1, today_k_line_dto.begin_time, today_k_line_dto.end_time,
                                          today_k_line_dto.high, today_k_line_dto.low, 'N', 'N')
            this_mline_dto.member_list = []
            this_mline_dto.member_list.append(today_k_line_dto)
            merge_line_list.append(this_mline_dto)

        #  处理顶底分型
        set_peak_and_bottom_flag(merge_line_list)
        i += 1

    # print(merge_line_list)
    #  输出检查
    '''
    for m_line_dto in merge_line_list:
        print(m_line_dto.begin_time.strftime('%Y-%m-%d %H:%M:%S') + " -- " +
              m_line_dto.end_time.strftime('%Y-%m-%d %H:%M:%S') + "**" +
              m_line_dto.is_peak + "**" + m_line_dto.is_bottom + "**" +
              str(m_line_dto.stick_num))
    '''
    return merge_line_list


def fen_bi(merge_line_list):
    #  分笔
    #  MergeLineDTO[]
    point_flag_list = [False] * len(merge_line_list)
    # print(str(point_flag_list[0])+" " + str(point_flag_list[4]))

    #  1.预处理，处理后相邻的都是非同一种分型
    last_point_m_line_dto = None

    for index in range(len(merge_line_list)):
        this_m_line_dto = merge_line_list[index]
        if this_m_line_dto.is_peak == 'N' \
                and this_m_line_dto.is_bottom == 'N':
            continue

        if last_point_m_line_dto is None:
            last_point_m_line_dto = this_m_line_dto
            point_flag_list[index] = True
            continue

        if last_point_m_line_dto.is_peak == 'Y' and this_m_line_dto.is_peak == 'Y':
            #  同为顶，取最高的
            if this_m_line_dto.high >= last_point_m_line_dto.high:
                last_point_m_line_dto = this_m_line_dto
                point_flag_list[index] = True
        elif last_point_m_line_dto.is_bottom == 'Y' and this_m_line_dto.is_bottom == 'Y':
            #  同为底，取最低的
            if this_m_line_dto.low <= last_point_m_line_dto.low:
                last_point_m_line_dto = this_m_line_dto
                point_flag_list[index] = True
        else:
            last_point_m_line_dto = this_m_line_dto
            point_flag_list[index] = True

    #  2.动态规划，找出任意[k,k+i]是否能成一笔
    point_index_list = []
    for index in range(len(point_flag_list)):
        if point_flag_list[index]:
            point_index_list.append(index)

    point_index_matrix = [[False] * len(point_index_list) for i in range(len(point_index_list))]
    # print(str(point_index_matrix[0][0]) + " " +
    #       str(point_index_matrix[len(point_index_list)-1][len(point_index_list)-1]))

    find_valid_point_by_dp(merge_line_list, point_index_list, point_index_matrix)

    #  3.根据上一步得到的结果，得出最后合理的分型
    result_array = [False] * len(point_index_list)
    has_result = False
    index = len(point_index_list) -1
    while index > 0:
        for result in result_array:
            result = False

        has_result = check_final_fen_bi(merge_line_list, point_index_list,
                                        point_index_matrix, result_array, index)

        if has_result:
            break

        index -= 1

    #  4.输出分笔结果
    print("分笔结果 : " + str(has_result))
    if not has_result:
        print("按照目前的划分规则，没有找到分笔的结果.")

    for i in range(len(result_array)):
        if result_array[i]:
            m_line_dto = merge_line_list[point_index_list[i]]
            if m_line_dto.is_peak == 'Y':
                print(m_line_dto.begin_time.strftime('%Y-%m-%d %H:%M:%S') + "\t" +
                      m_line_dto.end_time.strftime('%Y-%m-%d %H:%M:%S') + "\t" +
                      "合并[" + str(m_line_dto.stick_num) + "]条K线" + "\t" +
                      "顶[" + str(m_line_dto.low) + "][" + str(m_line_dto.high) + "]")
            if m_line_dto.is_bottom == 'Y':
                print(m_line_dto.begin_time.strftime('%Y-%m-%d %H:%M:%S') + "\t" +
                      m_line_dto.end_time.strftime('%Y-%m-%d %H:%M:%S') + "\t" +
                      "合并[" + str(m_line_dto.stick_num) + "]条K线" + "\t" +
                      "底[" + str(m_line_dto.low) + "][" + str(m_line_dto.high) + "]")
    return has_result, result_array, point_index_list

def check_final_fen_bi(merge_line_list, point_index_list,
                       point_index_matrix, result_array, end_index):
    #  查看最终正确的笔划分
    #  MergeLineDTO[], boolean[], boolean[][],boolean[],integer
    return search_final_fen_bi(merge_line_list, point_index_list,
                               point_index_matrix, result_array,
                               0, end_index)


def search_final_fen_bi(merge_line_list, point_index_list,
                        point_index_matrix, result_array, index, end_index):
    #  递归查找查看最终正确的笔划分
    #  MergeLineDTO[], boolean[], boolean[][],boolean[],integer,integer
    if index == end_index:
        return True
    else:
        i = index+1
        while i <= end_index:
            if point_index_matrix[index][i]:
                result_array[index] = True
                result_array[i] = True
                if search_final_fen_bi(merge_line_list, point_index_list,
                                       point_index_matrix,result_array,
                                       i, end_index):
                    return True
                else:
                    result_array[index] = False
                    result_array[i] = False
            i += 1
    return False


def find_valid_point_by_dp(merge_line_list, point_index_list, point_index_matrix):
    #  通过动态规划寻找有效的分型
    #  通过动态规划，查找局部解，结果在pointIndexMatrix中
    #  MergeLineDTO[], boolean[], boolean[][]
    distance = 1
    while distance < len(point_index_list):
        #  取奇数，经过之前第一阶段的预处理，间隔为偶数的都是同类分型
        process_by_distance(merge_line_list, point_index_list, point_index_matrix, distance)
        distance += 2


def process_by_distance(merge_line_list, point_index_list, point_index_matrix, distance):
    #  处理间隔为dist的分型组合，是否能成一笔
    #  MergeLineDTO[], boolean[], boolean[][], integer

    index = 0
    while index < len(point_index_list)-distance:
        check_result = check_2point_is_multi_line(merge_line_list,
                                                  point_index_list,
                                                  point_index_matrix,
                                                  index, index + distance)

        if check_result:
            point_index_matrix[index][index + distance] = False
        else:
            if validate_peak_and_bottom(merge_line_list,
                                        point_index_list[index],
                                        point_index_list[index + distance]):
                point_index_matrix[index][index + distance] = True
            else:
                point_index_matrix[index][index + distance] = False
        index += 1


def check_2point_is_multi_line(merge_line_list, point_index_list,
                               point_index_matrix, start_index, end_index):
    #  递归处理，逐步检查[startIndex，endIndex]是否能划分成多笔
    #  MergeLineDTO[], boolean[], boolean[][], integer, integer
    if start_index == end_index:
        return True
    else:
        index = start_index + 1
        while index <= end_index:
            if point_index_matrix[start_index][index]:
                boolean_result = check_2point_is_multi_line(merge_line_list,
                                                            point_index_list,
                                                            point_index_matrix,
                                                            index, end_index)
                if boolean_result:
                    return True
            index += 1
    return False


def validate_peak_and_bottom(merge_line_list, start_index, end_index):
    #  校验是否满足一笔
    #  MergeLineDTO[], integer, integer
    start_m_line_dto = merge_line_list[start_index]
    end_m_line_dto = merge_line_list[end_index]

    #  1.不满足顶必须接着底、或底必须接着顶
    if start_index == 0:
        if end_m_line_dto.is_peak == 'N' and end_m_line_dto.is_bottom != 'N':
            return False
    elif (start_m_line_dto.is_peak == 'Y' and end_m_line_dto.is_peak == 'Y') \
            or (start_m_line_dto.is_bottom == 'Y' and end_m_line_dto.is_bottom == 'Y'):
        return False

    #  2.顶分型与底分型经过包含处理后，不允许共用K线
    if end_index - start_index < 3:
        return False

    #  3.顶分型中最高K线和底分型的最低K线之间（不包括这两K线），不考虑包含关系，至少有3根（包括3根）以上K线
    k_line_number = 0
    for index in range(len(start_m_line_dto.member_list)):
        k_line_dto = start_m_line_dto.member_list[index]
        if start_m_line_dto.is_peak == 'Y' and start_m_line_dto.high == k_line_dto.high:
            #  顶，并且是顶元素
            k_line_number += (len(start_m_line_dto.member_list) - index - 1)
            break
        elif start_m_line_dto.is_bottom == 'Y' and start_m_line_dto.low == k_line_dto.low:
            #  底，并且是底元素
            k_line_number += (len(start_m_line_dto.member_list) - index - 1)
            break

    for index in range(len(end_m_line_dto.member_list)):
        k_line_dto = end_m_line_dto.member_list[index]
        if end_m_line_dto.is_bottom == 'Y' and end_m_line_dto.low == k_line_dto.low:
            k_line_number += index
            break
        elif end_m_line_dto.is_peak == 'Y' and end_m_line_dto.high == k_line_dto.high:
            k_line_number += index
            break
    #  分型中间元素的k线合计
    index = start_index + 1
    while index < end_index:
        m_line_dto = merge_line_list[index]
        k_line_number += m_line_dto.stick_num
        index += 1

    if k_line_number < 3:
        return False

    #  4.顶底分别是笔中(包括组成分型的元素)的最高和最低
    peak_dto = None
    bottom_dto = None
    if start_m_line_dto.is_peak == 'Y':
        peak_dto = start_m_line_dto
        bottom_dto = end_m_line_dto
    else:
        peak_dto = end_m_line_dto
        bottom_dto = start_m_line_dto

    index = 0 if start_index == 0 else start_index - 1
    while index <= end_index + 1:
        m_line_dto = merge_line_list[index]

        #  存在更高的点位
        if m_line_dto.high > peak_dto.high \
                and m_line_dto.begin_time != peak_dto.begin_time:
            return False

        if m_line_dto.low < bottom_dto.low \
                and m_line_dto.begin_time != bottom_dto.begin_time:
            return False

        index += 1

    #  5.不允许中间有其他的顶和底
    #  6.或许还需要判断顶底的区间是否不能重叠
    return True

def dftok_line_list(df):

    df.index = df.index.astype('datetime64')
    df = df.sort_index(ascending=True)
    date_list = df.index.tolist()
    data_per_day = df.values.tolist()

    k_line_list = []
    ''' 将dataframe数据组装进入KLineDTO的列表中 '''
    for index in range(len(date_list)):
        date_time = date_list[index]
         # u'open', u'high', u'low', u'close',
        open_price = data_per_day[index][1]
        close_price = data_per_day[index][4]
        high_price = data_per_day[index][2]
        low_price = data_per_day[index][3]
        k_line_dto = KLineDTO(date_time,
                                  date_time,
                                  date_time,
                                  open_price, high_price, low_price, close_price)
        k_line_list.append(k_line_dto)
    return k_line_list

import tdx_data_Day as tdd
def run_test():
    #  测试
    #  取原始数据
    # k_line_list = get_stock_30min_data_by_time("601318", "2015-12-21 10:00:00", "2016-04-02 13:30:00")
    # k_line_list = get_stock_week_data_by_time("999999", "2009-07-17", "2015-05-15")
    df = tdd.get_tdx_Exp_day_to_df("999999", "2015-07-17").sort_index(ascending=True)
    # df.index = df.index.astype('datetime64')
    k_line_list = dftok_line_list(df)
    # print k_line_list
    # [u'code', u'open', u'high', u'low', u'close',
    print(len(k_line_list))
    # k_line_list = get_stock_30min_data_by_time("999999", "2015-03-10", "2015-05-16")
    print("---------------------------")
    #  分型
    merge_line_list = find_peak_and_bottom(k_line_list, "down")
    # fen_bi(merge_line_list)
    fenbi_result,final_result_array,fenbi_seq_list = fen_bi(merge_line_list)
    print "1",fenbi_result
    print "2",final_result_array
    print "all:%s 3:%s"%(len(df),fenbi_seq_list)
    print df.index[:2]
    print df.iloc[288,1:5]
#    Kplot(Open, High, Low, Close)

if __name__ == "__main__":
    # from chan_lun_util import *
    import matplotlib as mat
    import numpy as np
    import datetime as dt
    import matplotlib.pyplot as plt
    import time
    import sys

    run_test()
    sys.exit(0)

    start_date='2016-02-05'
    end_date='2017-02-07'
    stock_code = '601318.XSHG'
    df = get_price(stock_code, start_date, end_date, frequency='daily', fields=['open','close','high', 'low'],skip_paused=False,fq='pre')



    len(k_line_list)

    '''1.K线合并,确定顶分型和底分型,得出合并K线列表merge_line_list '''
    merge_line_list = find_peak_and_bottom(k_line_list, "down")

    '''2.分笔'''
    fenbi_result,final_result_array,fenbi_seq_list = fen_bi(merge_line_list)