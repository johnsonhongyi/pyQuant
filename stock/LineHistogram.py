# -*- coding:utf-8 -*-
# 导入需要用到的库
# %matplotlib inline
import pandas as pd
import statsmodels.api as sm
from pylab import *
from sklearn.linear_model import LinearRegression
from statsmodels import regression

from JohhnsonUtil import LoggerFactory as LoggerFactory
from JohhnsonUtil import zoompan

log = LoggerFactory.getLogger('Linehistogram')
# log.setLevel(LoggerFactory.DEBUG)
from JSONData import tdx_data_Day as tdd


# 取得股票的价格
# start = '2015-09-05'
# end = '2016-01-04'
# start = '2015-06-05'
# end = '2016-01-13'
# code = '300191'
# code = '000738'

def LIS(X):
    N = len(X)
    P = [0] * N
    M = [0] * (N + 1)
    L = 0
    for i in range(N):
        lo = 1
        hi = L
        while lo <= hi:
            mid = (lo + hi) // 2
            if (X[M[mid]] < X[i]):
                lo = mid + 1
            else:
                hi = mid - 1

        newL = lo
        P[i] = M[newL - 1]
        M[newL] = i

        if (newL > L):
            L = newL

    S = []
    pos = []
    k = M[L]
    for i in range(L - 1, -1, -1):
        S.append(X[k])
        pos.append(k)
        k = P[k]
    return S[::-1], pos[::-1]

    
def get_linear_model_status(code,type='M'):
    df = tdd.get_tdx_Exp_day_to_df(code, 'f').sort_index(ascending=True)
    asset = df['close']
    log.info("df:%s" % asset[:1])
    asset = asset.dropna()
    X = np.arange(len(asset))
    x = sm.add_constant(X)
    model = regression.linear_model.OLS(asset, x).fit()
    a = model.params[0]
    b = model.params[1]
    log.info("X:%s a:%s b:%s" % (len(asset), a, b))
    Y_hat = X * b + a
    if Y_hat[-1] > Y_hat[1]:
        log.debug("u:%s" % Y_hat[-1])
        log.debug("price:" % asset.iat[-1])
        if type.upper()=='M':
            diff=asset.iat[-1] - Y_hat[-1]
            if diff > 0:
                return True, len(asset),diff
            else:
                return False,len(asset),diff
        elif type.upper()=='L':
            i = (asset.values.T - Y_hat).argmin()
            c_low = X[i] * b + a - asset.values[i]
            Y_hatlow = X * b + a - c_low
            diff=asset.iat[-1] - Y_hatlow[-1]
            if asset.iat[-1] - Y_hatlow[-1] > 0:
                return True,len(asset),diff
            else:
                return False,len(asset),diff
    else:
        log.debug("d:%s" % Y_hat[1])
        return False, 0,0
    return False,0,0


def get_linear_model_histogram(code,type='d'):
    # 399001','cyb':'zs399006','zxb':'zs399005
    # code = '999999'
    # code = '601608'
    # code = '000002'
    # asset = ts.get_hist_data(code)['close'].sort_index(ascending=True)
    # df = tdd.get_tdx_Exp_day_to_df(code, 'f').sort_index(ascending=True)
    df=tdd.get_tdx_append_now_df(code,'f')
    if not type == 'd':
        df=tdd.get_tdx_stock_period_to_type(df,'w')
    # print df[:1]
    asset = df['close']

    log.info("df:%s" % asset[:1])
    asset = asset.dropna()
    dates = asset.index

    # 画出价格随时间变化的图像
    # _, ax = plt.subplots()
    # fig = plt.figure()
    fig = plt.figure(figsize=(16, 10))
    # fig = plt.figure(figsize=(16, 10), dpi=72)

    # plt.subplots_adjust(bottom=0.1, right=0.8, top=0.9)
    plt.subplots_adjust(left=0.05, bottom=0.08, right=0.95, top=0.95, wspace=0.15, hspace=0.25)
    # set (gca,'Position',[0,0,512,512])
    # fig.set_size_inches(18.5, 10.5)
    # fig=plt.fig(figsize=(14,8))
    ax1 = fig.add_subplot(321)
    ax1.plot(asset)
    ticks = ax1.get_xticks()
    ax1.set_xticklabels([dates[i] for i in ticks[:-1]])  # Label x-axis with dates

    # 拟合
    X = np.arange(len(asset))
    x = sm.add_constant(X)
    model = regression.linear_model.OLS(asset, x).fit()
    a = model.params[0]
    b = model.params[1]
    # log.info("a:%s b:%s" % (a, b))
    log.info("X:%s a:%s b:%s" % (len(asset), a, b))
    Y_hat = X * b + a

    # 真实值-拟合值，差值最大最小作为价值波动区间
    # 向下平移
    i = (asset.values.T - Y_hat).argmin()
    c_low = X[i] * b + a - asset.values[i]
    Y_hatlow = X * b + a - c_low

    # 向上平移
    i = (asset.values.T - Y_hat).argmax()
    c_high = X[i] * b + a - asset.values[i]
    Y_hathigh = X * b + a - c_high
    plt.plot(X, Y_hat, 'k', alpha=0.9);
    plt.plot(X, Y_hatlow, 'r', alpha=0.9);
    plt.plot(X, Y_hathigh, 'r', alpha=0.9);
    plt.xlabel('Date', fontsize=14)
    plt.ylabel('Price', fontsize=14)
    plt.title(code, fontsize=14)
    plt.grid(True)

    # plt.legend([code]);
    # plt.legend([code, 'Value center line', 'Value interval line']);
    # fig=plt.fig()
    # fig.figsize = [14,8]
    scale = 1.1
    zp = zoompan.ZoomPan()
    figZoom = zp.zoom_factory(ax1, base_scale=scale)
    figPan = zp.pan_factory(ax1)

    ax2 = fig.add_subplot(323)
    ticks = ax2.get_xticks()
    ax2.set_xticklabels([dates[i] for i in ticks[:-1]])
    # plt.plot(X, Y_hat, 'k', alpha=0.9)
    n = 5
    d = (-c_high + c_low) / n
    c = c_high
    while c <= c_low:
        Y = X * b + a - c
        plt.plot(X, Y, 'r', alpha=0.9);
        c = c + d
    ax2.plot(asset)
    plt.xlabel('Date', fontsize=14)
    plt.ylabel('Price', fontsize=14)
    plt.grid(True)

    # plt.title(code, fontsize=14)
    # plt.legend([code])

    # 将Y-Y_hat股价偏离中枢线的距离单画出一张图显示，对其边界线之间的区域进行均分，大于0的区间为高估，小于0的区间为低估，0为价值中枢线。
    ax3 = fig.add_subplot(324)
    distance = (asset.values.T - Y_hat)
    # distance = (asset.values.T-Y_hat)[0]
    ax3.plot(distance)
    ticks = ax3.get_xticks()
    ax3.set_xticklabels([dates[i] for i in ticks[:-1]])
    n = 5
    d = (-c_high + c_low) / n
    c = c_high
    while c <= c_low:
        Y = X * b + a - c
        plt.plot(X, Y - Y_hat, 'r', alpha=0.9);
        c = c + d
    plt.xlabel('Date', fontsize=14)
    plt.ylabel('Price-center price', fontsize=14)
    plt.grid(True)

    # plt.title(code, fontsize=14)
    # plt.legend([code])

    # 统计出每个区域内各股价的频数，得到直方图，为了更精细的显示各个区域的频数，这里将整个边界区间分成100份。

    ax4 = fig.add_subplot(325)
    log.info("assert:len:%s %s" % (len(asset.values.T - Y_hat), (asset.values.T - Y_hat)[0]))
    # distance = map(lambda x:int(x),(asset.values.T - Y_hat)/Y_hat*100)
    # now_distanse=int((asset.iat[-1]-Y_hat[-1])/Y_hat[-1]*100)
    # log.debug("dis:%s now:%s"%(distance[:2],now_distanse))
    # log.debug("now_distanse:%s"%now_distanse)
    distance = (asset.values.T - Y_hat)
    now_distanse = asset.iat[-1] - Y_hat[-1]
    # distance = (asset.values.T-Y_hat)[0]
    pd.Series(distance).plot(kind='hist', stacked=True, bins=100)
    # plt.plot((asset.iat[-1].T-Y_hat),'b',alpha=0.9)
    plt.axvline(now_distanse, hold=None, label="1", color='red')
    # plt.axhline(now_distanse,hold=None,label="1",color='red')
    # plt.axvline(asset.iat[0],hold=None,label="1",color='red',linestyle="--")
    plt.xlabel('Undervalue ------------------------------------------> Overvalue', fontsize=14)
    plt.ylabel('Frequency', fontsize=14)
    # plt.title('Undervalue & Overvalue Statistical Chart', fontsize=14)
    plt.legend([code, asset.iat[-1]])
    plt.grid(True)

    # plt.show()
    # import os
    # print(os.path.abspath(os.path.curdir))


    ax5 = fig.add_subplot(326)
    # fig.figsize=(5, 10)
    log.info("assert:len:%s %s" % (len(asset.values.T - Y_hat), (asset.values.T - Y_hat)[0]))
    # distance = map(lambda x:int(x),(asset.values.T - Y_hat)/Y_hat*100)
    distance = (asset.values.T - Y_hat) / Y_hat * 100
    now_distanse = ((asset.iat[-1] - Y_hat[-1]) / Y_hat[-1] * 100)
    log.debug("dis:%s now:%s" % (distance[:2], now_distanse))
    log.debug("now_distanse:%s" % now_distanse)
    # n, bins = np.histogram(distance, 50)
    # print n, bins[:2]
    pd.Series(distance).plot(kind='hist', stacked=True, bins=100)
    # plt.plot((asset.iat[-1].T-Y_hat),'b',alpha=0.9)
    plt.axvline(now_distanse, hold=None, label="1", color='red')
    # plt.axhline(now_distanse,hold=None,label="1",color='red')
    # plt.axvline(asset.iat[0],hold=None,label="1",color='red',linestyle="--")
    plt.xlabel('Undervalue ------------------------------------------> Overvalue', fontsize=14)
    plt.ylabel('Frequency', fontsize=14)
    # plt.title('Undervalue & Overvalue Statistical Chart', fontsize=14)
    plt.legend([code, asset.iat[-1]])
    plt.grid(True)


    ax6 = fig.add_subplot(322)
    h = df.loc[:, ['open', 'close', 'high', 'low']]
    highp = h['high'].values
    lowp = h['low'].values
    openp = h['open'].values
    closep = h['close'].values
    lr = LinearRegression()
    x = np.atleast_2d(np.linspace(0, len(closep), len(closep))).T
    lr.fit(x, closep)
    LinearRegression(copy_X=True, fit_intercept=True, n_jobs=1, normalize=False)
    xt = np.atleast_2d(np.linspace(0, len(closep) + 200, len(closep) + 200)).T
    yt = lr.predict(xt)
    bV = []
    bP = []
    for i in range(1, len(highp) - 1):
        if highp[i] <= highp[i - 1] and highp[i] < highp[i + 1] and lowp[i] <= lowp[i - 1] and lowp[i] < lowp[i + 1]:
            bV.append(lowp[i])
            bP.append(i)

    d, p = LIS(bV)

    idx = []
    for i in range(len(p)):
        idx.append(bP[p[i]])
    lr = LinearRegression()
    X = np.atleast_2d(np.array(idx)).T
    Y = np.array(d)
    lr.fit(X, Y)
    estV = lr.predict(xt)
    ax6.plot(closep, linewidth=2)
    ax6.plot(idx, d, 'ko')
    ax6.plot(xt, estV, '-r', linewidth=3)
    ax6.plot(xt, yt, '-g', linewidth=3)
    plt.grid(True)

    # plt.tight_layout()
    zp2 = zoompan.ZoomPan()
    figZoom = zp2.zoom_factory(ax6, base_scale=scale)
    figPan = zp2.pan_factory(ax6)
    show()


if __name__ == "__main__":
    # status=get_linear_model_status('601198')
    # print status
    # get_tdx_and_now_data('002399')
    # sys.exit(0)

    if len(sys.argv) == 2:
        num_input = sys.argv[1]
    elif (len(sys.argv) > 2):
        print ("argv error")
        sys.exit(0)
    # else:
    #     print ("please input code:")
    #     sys.exit(0)
    num_input = '601608'
    # num_input=raw_input("Please input code:")
    while 1:
        try:
            if not len(num_input) == 6:
                num_input = raw_input("please input code:")
                if num_input == 'ex' or num_input == 'qu' \
                        or num_input == 'q' or num_input == "e":
                    sys.exit()
                elif len(num_input) == 6:
                    get_linear_model_histogram(num_input)
                    num_input = ''
            else:
                get_linear_model_histogram(num_input)
                num_input = ''
        except (KeyboardInterrupt) as e:
            print "KeyboardInterrupt:", e
            st = raw_input("status:[go(g),clear(c),quit(q,e)]:")
            if st == 'q' or st == 'e':
                sys.exit(0)

        except (IOError, EOFError) as e:
            print "Error", e
            # traceback.print_exc()
