# -*- coding:utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.pyplot import show
# from research_api import *
from sklearn.linear_model import LinearRegression
import sys

sys.path.append("..")
from JohhnsonUtil import LoggerFactory as LoggerFactory

log = LoggerFactory.getLogger('LongSklearn')
# log.setLevel(LoggerFactory.DEBUG)
from JSONData import tdx_data_Day as tdd
from JohhnsonUtil import zoompan


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


def LIS_mod(X):
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

# 1）控制颜色
# 颜色之间的对应关系为
# b---blue   c---cyan  g---green    k----black
# m---magenta r---red  w---white    y----yellow
# 有三种表示颜色的方式:
# a:用全名  b:16进制如：#FF00FF  c：RGB或RGBA元组（1,0,1,1） d：灰度强度如：‘0.7’
# 2)控制线型
# 符号和线型之间的对应关系
# -      实线
# --     短线
# -.     短点相间线
# ：     虚点线
# h = get_price(asset, start_date, end_date, frequency='1d', fields=['open','close','high', 'low'])
'''
{MA5:=MA(CLOSE,5),COLORYELLOW,LINETHICK2;}
MA5:MA(CLOSE,5),COLORYELLOW,LINETHICK2;
MA13:=MA(CLOSE,13),COLORCYAN,LINETHICK2;
N:=8;
M:=3;
VAR11:=MA(C,9),COLORRED;
上升通道:IF(VAR11>REF(VAR11,1),VAR11,DRAWNULL),LINETHICK2,COLORRED;
下降通道:IF(VAR11<REF(VAR11,1),VAR11,DRAWNULL),LINETHICK2,COLORGREEN;
A0:=(L+H+C*2)/4;
AA:=EMA(A0,14)COLORYELLOW,LINETHICK1;
BB:=EMA(A0,25)COLORYELLOW,LINETHICK2;
A1X:=(AA-REF(AA,1))/REF(AA,1)*100;
A2X:=(BB-REF(BB,1))/REF(BB,1)*100;
G:=BARSLAST(CROSS(A1X,0));
{必卖止损:REF(A0,G),COLORGREEN,LINETHICK2;}
A5:=EMA(CLOSE,12)-EMA(CLOSE,26);
A6:=EMA(A5,9);
A7:=(A5<-0.1 AND A5>A6);
见底:IF(A7,LLV(L,21),DRAWNULL)COLORRED,CIRCLEDOT;
见顶:IF(H>=REF(A0,BARSLAST(CROSS(A1X,0)))*1.3,REF(A0,BARSLAST(CROSS(A1X,0)))*1.3,DRAWNULL),COLORGREEN,CIRCLEDOT;

高:=REF(HHV(H,N),M);
低:=REF(LLV(L,N),M);
H19:=高-(高-低)*0.191;
H38:=高-(高-低)*0.382;
H中:=高-(高-低)*0.5;
H61:=高-(高-低)*0.618;
H80:=高-(高-低)*0.809;

STICKLINE(CURRBARSCOUNT=1,高,高,30,5),COLORGREEN;
STICKLINE(CURRBARSCOUNT=1,低,低,30,5),COLORRED;
STICKLINE(CURRBARSCOUNT=1,H19,H19,30,5),COLORYELLOW;
STICKLINE(CURRBARSCOUNT=1,H38,H38,30,5),COLORMAGENTA;
STICKLINE(CURRBARSCOUNT=1,H中,H中,30,5),COLORWHITE;
STICKLINE(CURRBARSCOUNT=1,H61,H61,30,5),COLORGRAY;
STICKLINE(CURRBARSCOUNT=1,H80,H80,30,5),COLORCYAN;

{顶点:REFDATE(高,DATE),,POINTDOT,COLORRED;}
{%19.8:REFDATE(H19,DATE),POINTDOT,COLORYELLOW;
%38.2:REFDATE(H38,DATE),POINTDOT,COLORMAGENTA;
%50:REFDATE(H中,DATE),POINTDOT,COLORBLUE;
%61.8:REFDATE(H61,DATE),POINTDOT,COLORMAGENTA;
%80.9:REFDATE(H80,DATE),POINTDOT,COLORYELLOW;
低点:REFDATE(低,DATE),POINTDOT,COLORWHITE;}
DRAWTEXT(ISLASTBAR,高,'顶点'),COLORGREEN;
DRAWTEXT(ISLASTBAR,H19,'％19.8'),COLORWHITE;
DRAWTEXT(ISLASTBAR,H38,'％38.2'),COLORWHITE;
DRAWTEXT(ISLASTBAR,H中,'％50'),COLORYELLOW;
DRAWTEXT(ISLASTBAR,H61,'％61.8'),COLORWHITE;
DRAWTEXT(ISLASTBAR,H80,'％80.9'),COLORYELLOW;
DRAWTEXT(ISLASTBAR,低,'低点'),COLORWHITE;
DIFF:=( EMA(CLOSE,7) - EMA(CLOSE,19));
DEA:=EMA(DIFF,9);
MACD:=0.90*(DIFF-DEA);
TJ:=(DIFF>=DEA);
TJ1:=(DIFF>=0);
STICKLINE(TJ,H,L,0.4,0),COLORYELLOW;
STICKLINE(TJ,O,C,4,1),COLOR0088FF;
STICKLINE(TJ,O,C,3.4,1),COLOR00AAFF;
STICKLINE(TJ,O,C,2.8,1),COLOR00CCFF;
STICKLINE(TJ,O,C,2,1),COLOR00DDFF;
STICKLINE(TJ,O,C,1.2,1),COLOR55FFFF;
STICKLINE(TJ,O,C,0.4,1),COLOR99FFFF;
STICKLINE(TJ1 AND TJ,H,L,0.4,0),COLORF00FF0;
STICKLINE(TJ1 AND TJ,O,C,4,1),COLORFF33FF;
STICKLINE(TJ1 AND TJ,O,C,3.4,1),COLORFF55FF;
STICKLINE(TJ1 AND TJ,O,C,2.8,1),COLORFF77FF;
STICKLINE(TJ1 AND TJ,O,C,2,1),COLORFF99FF;
STICKLINE(TJ1 AND TJ,O,C,1.2,1),COLORFFBBFF;
STICKLINE(TJ1 AND TJ,O,C,0.4,1),COLORFFDDFF;
STICKLINE(DIFF<DEA,H,L,0.4,0),COLORF0F000;
STICKLINE(DIFF<DEA,O,C,4,1),COLORFF3300;
STICKLINE(DIFF<DEA,O,C,3.4,1),COLORFF6600;
STICKLINE(DIFF<DEA,O,C,2.8,1),COLORFF9900;
STICKLINE(DIFF<DEA,O,C,2,1),COLORFFBB00;
STICKLINE(DIFF<DEA,O,C,1.2,1),COLORFFDD00;
STICKLINE(DIFF<DEA,O,C,0.4,1),COLORFFFF00;
VAR1:=(CLOSE*2+HIGH+LOW)/4;
SK:= EMA(VAR1,13)-EMA(VAR1,73);
SD:= EMA(SK,2);
SJ:=(CROSS(SK,SD) AND SK<-0.04 AND (C-REF(C,1))/REF(C,1)>=0.03)OR(CROSS(SK,SD)
AND SK<=-0.14 )OR(CROSS(SK,SD) AND SK<=0.05 AND (V/MA(V,5)>2 OR C/REF(C,1)>0.035));
STICKLINE(SJ,H,L,0.5,0),COLORRED;
STICKLINE(SJ,O,C,5.5,0),LINETHICK3,COLOR000055;
STICKLINE(SJ,O,C,4.5,0),LINETHICK3,COLOR000077;
STICKLINE(SJ,O,C,3.5,0),LINETHICK3,COLOR000099;
STICKLINE(SJ,O,C,2.5,0),LINETHICK3,COLOR0000BB;
STICKLINE(SJ,O,C,1.5,0),LINETHICK3,COLOR0000DD;
STICKLINE(SJ,O,C,0.5,0),LINETHICK3,COLOR0000FF;
EMA13:=EMA(C,13),COLORWHITE;
EMA21:=EMA(C,21),COLORYELLOW;
EMA34:=EMA(C,34),COLORFF00FF;
EMA60:=MA(C,60),COLORFFCC66;
VAR2:=(2*CLOSE+HIGH+LOW)/4;
VAR3:=IF(YEAR>=2099 AND MONTH>2,0,1);
VAR4:=LLV(LOW,5); VAR5:=HHV(HIGH,4);
散户:=EMA((VAR2-VAR4)/(VAR5-VAR4)*100,4)*VAR3;
庄家:=EMA(0.667*REF(散户,1)+0.333*散户,2)*VAR3;
LC:=REF(CLOSE,1);
RSI:=SMA(MAX(CLOSE-LC,0),6,1)/SMA(ABS(CLOSE-LC),6,1)*100;
DRAWTEXT(CROSS(84,RSI) , HIGH,'←-----逃'),COLORGREEN;
VAR3AA:=IF((CLOSE>REF(CLOSE,1)),88,0);
VAR4AA:=IF(((CLOSE)/(REF(CLOSE,1))>1.05) AND ((HIGH)/(CLOSE)<1.01) AND (VAR3AA>0),91,0);
DRAWTEXT(FILTER((VAR4AA>90),45),(LOW)*(0.93),'←---大胆搏 '),COLORYELLOW;
VAR51:=3;
VAR52:=(3)*(SMA(((CLOSE - LLV(LOW,27))/(HHV(HIGH,27) - LLV(LOW,27)))*(100),5,1)) - (2)*(SMA(SMA(((CLOSE - LLV(LOW,27))/(HHV(HIGH,27) - LLV(LOW,27)))*(100),5,1),3,1));
DRAWTEXT(CROSS(VAR52,VAR51), LOW,'←启动')COLORMAGENTA;


{自动画通道源码：N:2,200,13;UR:2,200,6;LR:2,200,6}
TC1:=IF(H=HHV(H,6*UR),H,DRAWNULL);
TC2:=CONST(BARSLAST(TC1=H))+1;
UPPER:=CONST(IF(TC2=1,H,REF(H,TC2-1)));
BC1:=IF(L=LLV(L,6*LR),L,DRAWNULL);
BC2:=CONST(BARSLAST(BC1=L))+1;
LOWER:=CONST(IF(BC2=1,L,REF(L,BC2-1)));
LP:=CURRBARSCOUNT<=BC2 AND L=LOWER;{低点定位}
HP:=CURRBARSCOUNT<=TC2 AND H=UPPER;{高点定位}
STICKLINE(IF(BC2>TC2,HP,LP),LOWER,UPPER,0,0),COLOR628962;
STICKLINE(IF(BC2>TC2,LP,HP),LOWER,UPPER,0,0),COLOR628962;

NOD:=(IF(TC2>BC2,TC2,BC2)-IF(TC2>BC2,BC2,TC2));{用时}

LR1:=FORCAST(C,NOD+1);
NP:IF(CURRBARSCOUNT<=MAX(BC2,TC2),CONST(IF(MIN(TC2,BC2)=1,LR1,REF(LR1,MIN(TC2,BC2)-1))),DRAWNULL),COLORGREEN,LINETHICK1;{近点}
LR2:=SLOPE(C,NOD+1);
LR3:=CONST(IF(MIN(TC2,BC2)=1,LR2,REF(LR2,MIN(TC2,BC2)-1)));
FP:NP-LR3*(NOD),COLORRED;{远点}
EQU:(NP+FP)/2,COLOR93BDA8;

AD:=ABS(NP-FP);{高差};
DBL:=BARSLAST(BC1!=DRAWNULL)+1;
DBH:=BARSLAST(TC1!=DRAWNULL)+1;
BSP:=IF(BC2>TC2,DBL,DBH)-1;

LRL:=IF(NP>FP,FP+AD/NOD*BSP,FP-AD/NOD*BSP);
AT1:=IF(BETWEEN(CURRBARSCOUNT,BC2,TC2) AND H>LRL,H,LRL);
AT2:=HHV(AT1-LRL,MAX(BC2,TC2));
AT3:=CONST(BARSLAST(AT1-LRL=AT2));
AT4:=CONST(IF(AT3=0,H,REF(H,AT3)));
AT5:=CONST(IF(AT3=0,AT1-LRL,REF(AT1-LRL,AT3)));
ATL:=LRL+AT5;

UT1:=IF(BETWEEN(CURRBARSCOUNT,BC2,TC2) AND L<LRL,L,LRL);
UT2:=HHV(LRL-UT1,MAX(BC2,TC2));
UT3:=CONST(BARSLAST(LRL-UT1=UT2));
UT4:=CONST(IF(UT3=0,H,REF(H,UT3)));
UT5:=CONST(IF(UT3=0,LRL-UT1,REF(LRL-UT1,UT3)));
UTL:=LRL-UT5;

RH:=IF(CURRBARSCOUNT>=MIN(BC2,TC2)-10,ATL,CONST(REF(ATL,MIN(BC2,TC2)-11)));{限制高}
RL:=IF(CURRBARSCOUNT>=MIN(BC2,TC2)-10,UTL,CONST(REF(UTL,MIN(BC2,TC2)-11)));{限制低}


中轨:IF(NP>FP,IF(LRL<=RH,LRL,DRAWNULL),IF(LRL>=RL,LRL,DRAWNULL)),COLORWHITE,LINETHICK2;
上轨:IF(NP>FP,IF(ATL<=RH,ATL,DRAWNULL),IF(ATL>=RL,ATL,DRAWNULL)),COLORWHITE,LINETHICK1;
下轨:IF(NP>FP,IF(UTL<=RH,UTL,DRAWNULL),IF(UTL>=RL,UTL,DRAWNULL)),COLORWHITE,LINETHICK1;

''' 
def get_max_change_n_day(df,n):
    act_price = df['closePrice'] * df['accumAdjFactor']
    return (pd.rolling_max(act_price,n) / pd.rolling_min(act_price,n))-1
    # http://pandas.pydata.org/pandas-docs/stable/computation.html
    
def longsklearn(code='999999', ptype='f',dtype='d',start=None,end=None):
    # code='999999'
    # dtype = 'w'
    # start = '2014-09-01'
    # start = None
    # end='2015-12-23'
    # end = None
    df = tdd.get_tdx_append_now_df(code, ptype, start, end).sort_index(ascending=True)
    # if not dtype == 'd':
        # df = tdd.get_tdx_stock_period_to_type(df, dtype).sort_index(ascending=True)
    dw = tdd.get_tdx_stock_period_to_type(df, dtype).sort_index(ascending=True)
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

    uV = []
    uP = []
    for i in range(1, len(highp) - 1):
        # if highp[i] <= highp[i - 1] and highp[i] < highp[i + 1] and lowp[i] <= lowp[i - 1] and lowp[i] < lowp[i + 1]:
        if lowp[i] <= lowp[i - 1] and lowp[i] < lowp[i + 1]:
            bV.append(lowp[i])
            bP.append(i)

    for i in range(1, len(highp) - 1):
        # if highp[i] >= highp[i - 1] and highp[i] > highp[i + 1] and lowp[i] >= lowp[i - 1] and lowp[i] > lowp[i + 1]:
        if highp[i] >= highp[i - 1] and highp[i] > highp[i + 1]:
            uV.append(highp[i])
            uP.append(i)
    print highp
    print "uV:%s" % uV[:1]
    print "uP:%s" % uP[:1]
    print "bV:%s" % bV[:1]
    print "bP:%s" % bP[:1]

    sV, sP = LIS(uV)
    dV, dP = LIS(bV)
    print "sV:%s" % sV[:1]
    print "sP:%s" % sP[:1]
    print "dV:%s" % dV[:1]
    print "dP:%s" % dP[:1]
    sidx = []
    didx = []
    for i in range(len(sP)):
        # idx.append(bP[p[i]])
        sidx.append(uP[sP[i]])
    for i in range(len(dP)):
        # idx.append(bP[p[i]])
        didx.append(bP[dP[i]])

    print "sidx:%s"%sidx[:1]
    print "didx:%s"%didx[:1]

    # plt.plot(closep)
    # plt.plot(idx,d,'ko')
    lr = LinearRegression()
    X = np.atleast_2d(np.array(sidx)).T
    Y = np.array(sV)
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
    # print h.index[:5], h['close']
    ax = h['close'].plot()
    # ax.plot(pd.datetime(h.index),h['close'], linewidth=1)
    # ax.plot(uP, uV, linewidth=1)
    # ax.plot(uP, uV, 'ko')
    # ax.plot(bP, bV, linewidth=1)
    # ax.plot(bP, bV, 'bo')
#    # ax.plot(sP, sV, linewidth=1)
#    # ax.plot(sP, sV, 'yo')
    # ax.plot(sidx, sV, linewidth=1)
    # ax.plot(sidx, sV, 'ro')
    # ax.plot(didx, dV, linewidth=1)
    # ax.plot(didx, dV, 'co')
    df['mean']=map(lambda h,l:(h+l)/2,df.high.values,df.low.values)
    print df['mean'][:1]
    # d=df.mean
    dw=dw.set_index('date')
    # print dw[:2]
    # ax.plot(df.index,df['mean'],'g',linewidth=1)
    ax.plot(df.index,pd.rolling_mean(df['mean'], 60), 'g',linewidth=1)
    ax.plot(dw.index,pd.rolling_mean(dw.close, 5), 'r',linewidth=1)
    ax.plot(dw.index,pd.rolling_min(dw.close, 5), 'bo')
    ax.plot(dw.index,pd.rolling_max(dw.close, 5), 'yo')
    ax.plot(dw.index,pd.expanding_max(dw.close, 5), 'ro')
    ax.plot(dw.index,pd.expanding_min(dw.close, 5), 'go')
    # print pd.rolling_min(df.close,20)[:1],pd.rolling_min(df.close,20)[-1:]
    # print pd.rolling_min(df.close,20)
    # print pd.rolling_max(df.close,20)[:1],pd.rolling_max(df.close,20)[-1:]
    # print pd.rolling_max(df.close,20)

    # ax.plot(idx, d, 'ko')
    # ax.plot(xt, estV, '-r', linewidth=5)
    # ax.plot(xt, yt, '-g', linewidth=5)

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
    # start = '2014-09-01'
    start = None
    end = None
    # end='2003-12-23'
    longsklearn('601608',dtype='m',start=start,end=end)
