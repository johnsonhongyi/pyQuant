#!/usr/bin/python
# -*- encoding: gbk -*-
from __future__ import division
import getopt
from struct import *
import os,time
import pandas as pd
import realdatajson as rl
import johnson_cons as ct
path_sep=os.path.sep
basedir = r'/Users/Johnson/Documents/Johnson/WinTools/zd_pazq'  # 如果你的安装路径不同,请改这里

exp_dir = basedir + r'/T0002/export/'
blocknew = r'/Users/Johnson/Documents/Johnson/WinTools/zd_pazq/T0002/blocknew'
# blocknew = 'Z:\Documents\Johnson\WinTools\zd_pazq\T0002\blocknew'
# exp_dir    = basedir + r'\T0002\export_back'
lc5_dir_sh = basedir + r'\Vipdoc\sh\fzline'
# lc5_dir_sh =  r'D:\2965\ydzqwsjy\Vipdoc\sh\fzline'
lc5_dir_sz = basedir + r'\Vipdoc\sz\fzline'
lc5_dir = basedir + r'\Vipdoc\%s\fzline'
day_dir = basedir + r'\Vipdoc\%s\lday/'
day_dir_sh = basedir + r'\Vipdoc\sh\lday/'
day_dir_sz = basedir + r'/Vipdoc/sz/lday/'

day_path={'sh':day_dir_sh,'sz':day_dir_sz}

stkdict = {}  # 存储股票ID和上海市、深圳市的对照

code_u='sz002399'
# http://www.douban.com/note/504811026/

def get_tdx_day_totxt(code):
    time_s=time.time()
    code_u=rl._code_to_symbol(code)
    day_path=day_dir % 'sh' if code[:1] in ['5', '6', '9'] else day_dir % 'sz'
    p_day_dir=day_path.replace('/',path_sep).replace('\\',path_sep)
    p_exp_dir=exp_dir.replace('/',path_sep).replace('\\',path_sep)
    # print p_day_dir,p_exp_dir
    ofile=open(p_day_dir+code_u+'.day','rb')
    buf=ofile.read()
    ofile.close()

    ifile=open(p_exp_dir+code_u+'.txt','w')
    num=len(buf)
    # print num
    no=int(num/32)
    # print no
    b=0
    e=32
    line=''

    # df = pd.DataFrame
    dict_t={}
    for i in xrange(no):
       a=unpack('IIIIIfII',buf[b:e])
       tdate=str(a[0])
       topen=str(a[1]/100.0)
       thigh=str(a[2]/100.0)
       tlow=str(a[3]/100.0)
       tclose=str(a[4]/100.0)
       tvolp=str(a[5]/10.0)
       tvol=str(a[6])   #int
       tpre=str(a[7])  #back
       # line=str(a[0])+' '+str(a[1]/100.0)+' '+str(a[2]/100.0)+' '+str(a[3]/100.0)+\
       # ' '+str(a[4]/100.0)+' '+str(a[5]/10.0)+' '+str(a[6])+' '+str(a[7])+' '+'\n'
       # print line
       # list_t.append(tdate,topen,thigh,tlow,tclose,tvolp,tvol,tpre)
       dict_t[tdate]={'date':tdate,'open':topen,'high':thigh,'low':tlow,'close':tclose,'volp':tvolp,'vol':tvol,'pre':tpre}
       b=b+32
       e=e+32
    df=pd.DataFrame.from_dict(dict_t, orient='index')
    print "time:",(time.time()-time_s)*1000
    ifile.close()
    return df

def get_tdx_day_to_df(code):
    time_s=time.time()
    code_u=rl._code_to_symbol(code)
    day_path=day_dir % 'sh' if code[:1] in ['5', '6', '9'] else day_dir % 'sz'
    p_day_dir=day_path.replace('/',path_sep).replace('\\',path_sep)
    p_exp_dir=exp_dir.replace('/',path_sep).replace('\\',path_sep)
    # print p_day_dir,p_exp_dir
    ofile=open(p_day_dir+code_u+'.day','rb')
    buf=ofile.read()
    ofile.close()

    ifile=open(p_exp_dir+code_u+'.txt','w')
    num=len(buf)
    # print num
    no=int(num/32)
    # print no
    b=0
    e=32
    line=''

    # df = pd.DataFrame
    dict_t=[]
    for i in xrange(no):
       a=unpack('IIIIIfII',buf[b:e])
       tdate=str(a[0])
       topen=str(a[1]/100.0)
       thigh=str(a[2]/100.0)
       tlow=str(a[3]/100.0)
       tclose=str(a[4]/100.0)
       tvolp=str(a[5]/10.0)
       tvol=str(a[6])   #int
       tpre=str(a[7])  #back
       # line=str(a[0])+' '+str(a[1]/100.0)+' '+str(a[2]/100.0)+' '+str(a[3]/100.0)+\
       # ' '+str(a[4]/100.0)+' '+str(a[5]/10.0)+' '+str(a[6])+' '+str(a[7])+' '+'\n'
       # print line
       # list_t.append(tdate,topen,thigh,tlow,tclose,tvolp,tvol,tpre)
       # dict_t[tdate]={'date':tdate,'open':topen,'high':thigh,'low':tlow,'close':tclose,'volp':tvolp,'vol':tvol,'pre':tpre}
       dict_t.append({'code':code,'date':tdate,'open':topen,'high':thigh,'low':tlow,'close':tclose,'volp':tvolp,'vol':tvol,'pre':tpre})
       b=b+32
       e=e+32
    # df=pd.DataFrame.from_dict(dict_t,orient='index')
    df=pd.DataFrame(dict_t,columns=ct.TDX_Day_columns)
    df=df.set_index('date')
    print "time:",(time.time()-time_s)*1000

    ifile.close()
    return df
#############################################################
# usage 使用说明
#
#############################################################

def usage(p):
    print """
python %s [-t txt|zip] stkid [from] [to]
-t txt 表示从txt files 读取数据，否则从zip file 读取(这也是默认方式)
for example :
python %s 999999 20070101 20070302
python %s -t txt 999999 20070101 20070302
    """ % (p, p, p)


if __name__ == '__main__':
    df=get_tdx_day_to_df('002399')
    print df[:1]
    df=get_tdx_day_totxt('002399')
    print df[:1]

    df=get_tdx_day_to_df('000001')
    print df[:1]

    df=get_tdx_day_totxt('000001')
    print df[:1]

    df=get_tdx_day_to_df('600018')
    df=get_tdx_day_totxt('600018')

    import tushare as ts
    time_t=time.time()
    dt= ts.get_hist_data('601198')
    print (time.time()-time_t)*1000
    # print df[-1:]
    #
    # print dt[3:4]
    # print df[:1]
    # print dt[-1:]

    """
    python readtdxlc5.py 999999 20070101 20070131

    argv = sys.argv[1:]
    try:
        opts, args = getopt.getopt(argv, "ht:", ["help", "type="])
    except getopt.GetoptError:
        usage(sys.argv[0])
        sys.exit(0)
    l_type = 'zip'  # default type is zipfiles!
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage(sys.argv[0])
            sys.exit(1)
        elif opt in ("-t", "--type"):
            l_type = arg
    if len(args) < 1:
        print 'You must specified the stock No.!'
        usage(sys.argv[0])
        sys.exit(1)
    """
