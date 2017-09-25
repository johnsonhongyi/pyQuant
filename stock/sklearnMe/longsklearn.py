# -*- coding:utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.pyplot import show
# from research_api import *
from sklearn.linear_model import LinearRegression
import sys
sys.path.append("..")
from JohnsonUtil import LoggerFactory as LoggerFactory

# log = LoggerFactory.getLogger('LongSklearn')
log = LoggerFactory.log
# log.setLevel(LoggerFactory.DEBUG)
from JSONData import tdx_data_Day as tdd
from JohnsonUtil import zoompan


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


# h = get_price(asset, start_date, end_date, frequency='1d', fields=['open','close','high', 'low'])
def longsklearn(code='999999'):
    # code='999999'
    df = tdd.get_tdx_append_now_df(code, 'f').sort_index(ascending=True)
    # print df[:1]
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
    # plt.plot(xt,yt,'-g',linewidth=5)
    # plt.plot(closep)
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
    # plt.plot(closep)
    # plt.plot(idx,d,'ko')
    lr = LinearRegression()
    X = np.atleast_2d(np.array(idx)).T
    Y = np.array(d)
    lr.fit(X, Y)
    estV = lr.predict(xt)

    fig = plt.figure(figsize=(16, 10), dpi=72)
    # plt.subplots_adjust(bottom=0.1, right=0.8, top=0.9)
    plt.subplots_adjust(left=0.05, bottom=0.08, right=0.95, top=0.95, wspace=0.15, hspace=0.25)
    # set (gca,'Position',[0,0,512,512])
    # fig.set_size_inches(18.5, 10.5)
    # fig=plt.fig(figsize=(14,8))
    ax = fig.add_subplot(111)
    plt.grid(True)
    ax.plot(closep, linewidth=2)
    ax.plot(idx, d, 'ko')
    ax.plot(xt, estV, '-r', linewidth=5)
    ax.plot(xt, yt, '-g', linewidth=5)

    # ax2 = fig.add_subplot(122)
    # print len(closep),len(idx),len(d),len(xt),len(estV),len(yt)
    # f=lambda x:x[-int(len(x)/10):]
    # ax2.plot(f(closep))
    # ax2.plot(f(idx),f(d),'ko')
    # ax2.plot(f(xt),f(estV),'-r',linewidth=5)
    # ax2.plot(f(xt),f(yt),'-g',linewidth=5)
    # # plt.show()
    scale = 1.1
    zp = zoompan.ZoomPan()
    figZoom = zp.zoom_factory(ax, base_scale=scale)
    figPan = zp.pan_factory(ax)
    show()


if __name__ == "__main__":
    longsklearn('002399')
