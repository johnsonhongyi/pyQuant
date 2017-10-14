# # coding=utf-8 
# # 研究中创建my_chan.py 拷贝此代码即可
# import pandas as pd
# import numpy as np
# import datetime

# # 处理k线成缠论k线,临时函数
# def parse2ChanKTMP(k_data, k_values, in_chan = False):
#     baohan_columns = ['enddate'] + list(k_data.keys()) if not in_chan else list(k_data.keys())
# #     print baohan_columns
#     dfbao = pd.DataFrame(np.zeros(len(k_data.index)*len(baohan_columns)).reshape(len(k_data.index),len(baohan_columns)), index = k_data.index,columns=baohan_columns)\
#     if not in_chan else k_data
# #     print dfbao
#     # stdt = k_data.index[0]
#     # dfbao.set_value(stdt, baohan_columns,  [stdt] + list(k_data.values[0]))
#     # 比较上一个包含的时间点
#     dt_bf = 0
#     def set_baohan_value(dt, value):
#         dfbao.set_value(dt, baohan_columns,  value)
#         return dt
#     for i, dt in enumerate(k_data.index):
#         if i==0:
#             dt_bf = set_baohan_value(dt, [dt] + list(k_values[i])) if not in_chan else dt
#             continue
#         if in_chan and (k_data['enddate'][dt]==0 or i==0): continue
#         # 非包含情况
#         if (k_data['high'][dt]>dfbao['high'][dt_bf] and k_data['low'][dt]>dfbao['low'][dt_bf])\
#         or (k_data['high'][dt]<dfbao['high'][dt_bf] and k_data['low'][dt]<dfbao['low'][dt_bf]):
#             if in_chan:
#                 dt_bf = dt
#                 continue
#             dt_bf = set_baohan_value(dt, [dt] + list(k_values[i]))
#             continue
#         # 包含情况
#         enddate = dt if not in_chan else dfbao['enddate'][dt]
#         dt_bf = set_baohan_value(dt_bf, \
#                                  [enddate, dfbao['open'][dt_bf], k_data['close'][dt], \
#                                  max(k_data['high'][dt], dfbao['high'][dt_bf]), \
#                                  min(k_data['low'][dt], dfbao['low'][dt_bf]), \
#                                  k_data['vol'][dt]+dfbao['vol'][dt_bf], \
#                                  k_data['amount'][dt]+dfbao['amount'][dt_bf]])
#         if in_chan:
#             dfbao.set_value(dt, ['enddate'], 0)
#     dfbao = dfbao[dfbao['enddate']!=0]
#     return dfbao
# # 处理k线成缠论k线
# def parse2ChanK(k_data, k_values):  
#     chanK = parse2ChanKTMP(k_data, k_values)
#     while True:
#         chanK1 = parse2ChanKTMP(chanK, chanK.values, True)
#         if(len(chanK.index)==len(chanK1.index)):
#             break
#         chanK = chanK1
#     return chanK
# # chanK = parse2ChanK(k_data, k_values)
# # print chanK
# # 找顶底分型的idx
# # 如果 连续顶顶，或底底： 顶：high最大的顶， 低：low最小的低
# # 顶：1 低：-1
# def parse2ChanFen(chanK,recursion=False):
#     fenTypes = [] # 分型类型数组 1,-1构成
#     fenIdx = [] # 分型对应缠论k的下标

#     # 添加分型数据
#     # 过滤连续同分型
#     def appendFen(ft, fidx):
#         if len(fenIdx)==0:
#             fenTypes.append(ft)
#             fenIdx.append(fidx)
#             return
#         fenType_bf = fenTypes[len(fenTypes)-1]
#         if fenType_bf == ft:
#              fenType_bf, fenIdx_bf = fenTypes.pop(), fenIdx.pop()
#              fidx = fenIdx_bf if (ft==1 and chanK['high'][fenIdx_bf]>chanK['high'][fidx])\
#              or (ft==-1 and chanK['low'][fenIdx_bf]<chanK['low'][fidx]) else fidx
#         fenTypes.append(ft)
#         fenIdx.append(fidx)
#     for i, dt in enumerate(chanK.index):
#         if i==0 or i==len(chanK.index)-1:continue
#         # 顶分型
#         if chanK['high'][i+1]<chanK['high'][i]>chanK['high'][i-1]:
#             appendFen(1, i)
#         # 底分型
#         if chanK['low'][i+1]>chanK['low'][i]<chanK['low'][i-1]:
#             appendFen(-1, i)
#     return fenTypes, fenIdx
# # fenTypes, fenIdx = parse2ChanFen(chanK)

# # print fenTypes, fenIdx

# # 分型构成笔
# # 构成笔条件，1、顶低分型间隔了n个chanK线， 2、中间不会出现比第一个分型结构更高（顶）或更低（底）的分型，否则线段破坏，连接上一笔
# def parse2ChanBi(fenTypes, fenIdx, chanK,least_khl_num=2):
#     biIdx = []  # 笔对应的缠论k线 idx
#     frsBiType = 0 # 起始笔的走势，biIdx 奇数下标就是相反走势 1、向上，-1向下
#     least_khl_num = least_khl_num # 分笔间隔的最小 chanK 数量 中间排除顶低的chanK
#     toConBfIdx = 0 # 连接到上一笔末尾的 分型idx
#     # 判断笔破坏
#     def judgeBiBreak(idxb, idxa):
#         fenType = fenTypes[idxb]
#         fenType1 = -fenType
# #         print '分型破坏前', fenType, fenIdx[idxb], fenIdx[idxa]
#         _break = False
#         _breaki_k = 0
#         _breakj_k = 0
#         for k in range(idxb, idxa)[2::2]:
#             # 当前i分型破坏
#             if judgeBreak(fenType, fenIdx[idxb], fenIdx[k]):
# #                 print '首分型破坏里', fenType, fenIdx[idxb], fenIdx[k], k
#                 _break, _breaki_k = True, k
#                 break
#         for k in range(idxb, idxa)[1::2]:
#             # 末尾j分型破坏
#             if judgeBreak(fenType1, fenIdx[idxa], fenIdx[k]):
# #                 print '末尾分型破坏里', fenType1, fenIdx[k], fenIdx[idxa],
#                 _break, _breakj_k = True, k
#                 break
# #         print '破坏结果', _break, fenIdx[_breaki_k], fenIdx[_breakj_k]
#         return _break, _breaki_k, _breakj_k
#     # 分型破坏
#     def judgeBreak(fenType, bf, af):
#         return (fenType==-1 and chanK['low'][af]<chanK['low'][bf])\
#             or (fenType==1 and chanK['high'][af]>chanK['high'][bf])
#     def reAssignBi(biIdx, breakBi, breakBj, i, j):
#         toConBfIdx = i+1 if len(biIdx)==0 else breakBi
#         if breakBi>0 and len(biIdx)>0:
#             fb_ = biIdx.pop()
# #                         print '首分型破坏, 旧分型:%d, 新的分型:%d'%(fb_,fenIdx[breakBi])
#             biIdx.append(fenIdx[breakBi])
#             if 0<breakBj<breakBi and judgeBreak(fenTypes[i-1], biIdx[len(biIdx)-2], fenIdx[breakBj]):
#                 fa_=biIdx.pop()
#                 fb_=biIdx.pop()
# #                             print '尾分型破坏并连接上一点, 移除分型:%d，旧分型:%d, 新的分型:%d'%(fa_, fb_,fenIdx[breakBj])
#                 biIdx.append(fenIdx[breakBj])
#                 toConBfIdx = breakBj
#             return toConBfIdx,  -1 # -1：break 1:continue 0:不执行
#         if breakBj>0: 
# #                         breakBj = breakBj1 if breakBj==-1 or judgeBreak(fenTypes[i-1], fenIdx[breakBj], fenIdx[breakBj1]) else breakBj
#             if j+2>=len(fenIdx) and len(biIdx)>1 and\
#             judgeBreak(fenTypes[i-1], biIdx[len(biIdx)-2], fenIdx[breakBj]):
#                 fa_=biIdx.pop()
#                 fb_=biIdx.pop()
# #                             print '尾分型破坏并连接上一点, 移除分型:%d，旧分型:%d, 新的分型:%d'%(fa_, fb_,fenIdx[breakBj])
#                 biIdx.append(fenIdx[breakBj])
#                 toConBfIdx = breakBj
#                 return toConBfIdx,  -1 # -1：break 1:continue 0:不执行
#             return toConBfIdx,  1 # -1：break 1:continue 0:不执行
#         return toConBfIdx,  0 # -1：break 1:continue 0:不执行
#     for i, kidx in enumerate(fenIdx):
# #         print '生成的笔', biIdx
# #         print toConBfIdx, 'the i is ', i
#         if i<toConBfIdx or i==len(fenIdx)-1 : continue
#         # 后面没有符合条件的笔
#         if len(biIdx)>1 and toConBfIdx==0:break
#         toConBfIdx = 0
#         for j in range(len(fenIdx))[i+1::2]:
# #             print '差是', fenIdx[j]-kidx
#             if (fenIdx[j]-kidx)>least_khl_num:
# #                 print 'append', i, j, fenIdx[i], fenIdx[j]
#                 # breakType True 同分型， False 末尾分型
#                 flag, breakBi, breakBj = judgeBiBreak(i, j)
# #                 print flag, breakBi 
#                 if flag: 
#                     toConBfIdx, _bcn = reAssignBi(biIdx, breakBi, breakBj, i, j)
#                     if _bcn==-1:break
#                     if _bcn==1:continue
#                 if len(biIdx)==0: 
#                     biIdx.append(kidx)
#                     frsBiType = -fenTypes[i]       
#                     biIdx.append(fenIdx[j])
#                     toConBfIdx, _bcn = reAssignBi(biIdx, breakBi, breakBj, i, j)
#                     if _bcn==-1 or _bcn==1:
#                         biIdx = []
#                         toConBfIdx = i+1
#                         break  
#                     toConBfIdx = j
#                     break
#                 biIdx.append(fenIdx[j])
# #                 print biIdx
#                 toConBfIdx = j
# #                 print toConBfIdx
#                 break
        
#     return biIdx, frsBiType
# #最终线段生成
# #1、遍历相对高低点，判断线段破坏，
# #  破坏以后,如果总长度是0，i可以后移，否则重构之前的线段
# #  重构规则，找破坏点相对高点/低点，如果存在线段高点/低点>/<破坏高点/低点， 则连接此线段
# #2、形成线段中间至少有两点j-i>2
# def parse2ChanXD(frsBiType,biIdx,chanK):
#     lenBiIdx = len(biIdx)
#     xdIdx = []
#     xfenTypes = []
#     if lenBiIdx==0 : return xdIdx,xfenTypes
#     afIdx = 0
#     #重构线段    
#     def refactorXd(txIdx, nxIdx, chanK):
#         xdIdxn = xdIdx
#         xfenTypesn = xfenTypes
#         if len(xdIdxn)==0 or txIdx==-1 or nxIdx==-1: return 0,xdIdxn,xfenTypesn
#         for m in range(-len(xdIdxn)+1, 1)[1::2]:
#             k = -m
#             #满足逆向不破坏
# #             print '开始逆向破坏：逆向分型，逆向点，线段点', xfenTypesn[k], nxIdx, xdIdxn[k]
#             if (xfenTypesn[k]==-1 and chanK['low'][xdIdxn[k]]<chanK['low'][nxIdx])\
#             or (xfenTypesn[k]==1 and chanK['high'][xdIdxn[k]]>chanK['high'][nxIdx]):
#                 for n in range(-len(xdIdxn)+1, m): 
#                     xfenTypesn.pop()
#                     xdIdxn.pop()
#                 xdIdxn.append(txIdx)
#                 xfenTypesn.append(-xfenTypesn[len(xfenTypes)-1])
#                 return biIdx.index(txIdx), xdIdxn, xfenTypesn
#         xdIdxn = []
#         xfenTypesn = []
# #         print '逆向破坏', nxIdx, xdIdxn, xfenTypesn
#         return biIdx.index(nxIdx), xdIdxn, xfenTypesn
#     # 判断线段破坏
#     def judgeBreak(fenType, afPrice, idx, chanK):
#         return (fenType==-1 and afPrice<chanK['low'][idx]) \
#     or (fenType==1 and afPrice>chanK['high'][idx])
#     for i, idx in enumerate(biIdx):
#         if afIdx < 0 :break # 线段破坏以后没有合适线段
#         fenType = 1 if (frsBiType==1 and i%2==1) or (frsBiType==-1 and i%2==0) \
#         else -1
# #         print '开始判断%d,分型类型%d'%(idx, fenType)
#         #符合要求的连段
#         if i<afIdx:continue              
#         #找同向相对高低点
#         afPrice = 0 if fenType==-1 else 10000
#         tongxiang_price_ = 10000 - afPrice
#         nixiang_idx, tongxiang_idx = -1, -1
#         i_continued = False
#         for j in range(i+1, lenBiIdx)[0::2]:
#             #同向相对高低点
#             if (fenType==-1 and tongxiang_price_>chanK['low'][biIdx[j-1]]) \
#             or (fenType==1 and tongxiang_price_<chanK['high'][biIdx[j-1]]):
#                 tongxiang_price_ = chanK['high'][biIdx[j-1]] if fenType==1 else chanK['low'][biIdx[j-1]]
#                 tongxiang_idx = biIdx[j-1]
#             #线段破坏
# #             print '线段破坏前', idx, tongxiang_idx
#             #同向破坏
#             if judgeBreak(fenType, tongxiang_price_, idx, chanK) and idx!=tongxiang_idx:
# #                 print '同向已经破坏'
#                 afIdx, xdIdx, xfenTypes = refactorXd(tongxiang_idx, nixiang_idx, chanK)
#                 i_continued = True
#                 break     
# #             print '符合要求前', biIdx[i], biIdx[j], afPrice, chanK['high'][biIdx[j]], chanK['low'][biIdx[j]],fenType
#             if (fenType==-1 and chanK['high'][biIdx[j]]>afPrice) or (fenType==1 and chanK['low'][biIdx[j]]<afPrice):
#                 afPrice = chanK['high'][biIdx[j]] if fenType==-1 else chanK['low'][biIdx[j]]
#                 nixiang_idx = biIdx[j]
#                 #线段不符合要求
# #                 print '符合要求的i,j', biIdx[i], biIdx[j]
#                 if j-i<=2:continue    
#                 #逆向破坏
# #                 if judgeBreak(-fenType, nixiang_idx, idx, chanK) and idx!=nixiang_idx:
# # #                     print '逆向已经破坏'
# #                     afIdx, xdIdx, xfenTypes = refactorXd(tongxiang_idx, nixiang_idx, chanK)
# #                     break 
#                 if len(xdIdx)==0:
# #                     print '线段长度为0破坏', fenType, idx, judgeBreak(fenType, tongxiang_price_, idx, chanK)
#                     if judgeBreak(fenType, tongxiang_price_, idx, chanK):
#                         i_continued = True
#                         break
#                     xfenTypes.append(fenType)
#                     xdIdx.append(idx)
#                     xdIdx.append(biIdx[j])
#                     xfenTypes.append(-fenType)
#                 else:
#                     #不用同向线段连接
# #                     fenTypeb = xfenTypes[len(xfenTypes)-1]
# #                     xdIdxb = xdIdx.pop()
# #                     if fenTypeb == -fenType:
# #                         xdIdx.append(biIdx[j])
# #                     else:
# #                         xdIdx.append(xdIdxb)
# #                         xfenTypes.append(-fenTypeb)
# #                         xdIdx.append(biIdx[j])
#                     xfenTypes.append(-xfenTypes[len(xfenTypes)-1])
#                     xdIdx.append(biIdx[j])
#                 afIdx = j
#                 i_continued = True
#                 break
#             else:continue
#         if not i_continued and len(xdIdx)>0 : 
#             #都不符合要求时，最后重构最小线段
#             last_idx = xdIdx.pop()
#             last_type = xfenTypes[len(xfenTypes)-1]
#             for j in range(biIdx.index(last_idx), len(biIdx))[2::2]:
#                 if judgeBreak(last_type, chanK['low'][biIdx[j]] if last_type==-1 else chanK['high'][biIdx[j]], last_idx, chanK):
#                     last_idx = biIdx[j]
#             xdIdx.append(last_idx)
#             break
#     return xdIdx,xfenTypes
# # biIdx, frsBiType = parse2ChanBi(fenTypes, fenIdx, chanK)
# # print biIdx,frsBiType
# #简单线段形成，主要用于判断是否是大级别的笔
# #区间找高低点，判断是否符合 高低点中包含>2个笔点就阔以
# def parse2Xianduan(biIdx, chanK):
#     xdIdx = []
#     if len(biIdx)==0: return xdIdx, 0
#     def appendXd(lowIdx, highIdx, xdType):
#         if len(xdIdx)==0:
#             if xdType == 1:
#                 xdIdx.append(lowIdx)
#             else:
#                 xdIdx.append(highIdx) 
#         if (xdType == 1 and len(xdIdx)%2==1) or (xdType == -1 and len(xdIdx)%2==0):
#             xdIdx.append(highIdx)
#         else:
#             xdIdx.append(lowIdx)
#     def genXianduan(biIdx, chanK, xdType=0):
#         highMax, lowMin = 0, 10000
#         highIdx, lowIdx = -1,-1
#         lenXd = len(xdIdx)
#         for idx in  biIdx:
#             if chanK['high'][idx]>highMax:
#                 highMax = chanK['high'][idx] 
#                 highIdx = idx
#             if chanK['low'][idx]<lowMin:
#                 lowMin = chanK['low'][idx] 
#                 lowIdx = idx
                
#         # 构成简易线段
# #         print biIdx, xdIdx, lowIdx, highIdx
#         xdDiff = biIdx.index(lowIdx)-biIdx.index(highIdx)
#         if abs(xdDiff)>2:
#             if lenXd==0:
#                 xdType = 1 if xdDiff<0 else -1
#             appendXd(lowIdx, highIdx, xdType)
# #             print lowIdx, highIdx, xdIdx
#             genXianduan(biIdx[biIdx.index(xdIdx[len(xdIdx)-1]):], chanK, xdType)
#         return xdType
#     xdType = genXianduan(biIdx, chanK)
#     return xdIdx,xdType

# # 笔形成最后一段未完成段判断是否是次级别的走势形成笔
# def con2Cxianduan(stock, k_data, chanK, frsBiType, biIdx, end_date, cur_ji = 1):
#     max_k_num = 4
#     if cur_ji>=4 or len(biIdx)==0: return biIdx
#     idx = biIdx[len(biIdx)-1]
#     k_data_dts = list(k_data.index)
#     st_data = chanK['enddate'][idx]
#     if st_data not in k_data_dts: return biIdx
#     # 重构次级别线段的点到本级别的chanK中
#     def refactorXd(biIdx, xdIdxc, chanK, chanKc, cur_ji):
#         new_biIdx = []
#         biIdxB = biIdx[len(biIdx)-1] if len(biIdx)>0 else 0
#         for xdIdxcn in xdIdxc:
#             for chanKidx in range(len(chanK.index))[biIdxB:]:
#                 if judge_day_bao(chanK, chanKidx, chanKc, xdIdxcn, cur_ji):
#                     new_biIdx.append(chanKidx)
#                     break
#         return new_biIdx
#     # 判断次级别日期是否被包含
#     def judge_day_bao(chanK, chanKidx, chanKc, xdIdxcn, cur_ji):
#         _end_date = chanK['enddate'][chanKidx]+datetime.timedelta(hours=15) if cur_ji==1 else chanK['enddate'][chanKidx]
#         _start_date = chanK.index[chanKidx] if chanKidx==0\
#         else chanK['enddate'][chanKidx-1]+datetime.timedelta(minutes=1)
#         return _start_date<=chanKc.index[xdIdxcn]<=_end_date
#     # cur_ji = 1 #当前级别
#     #符合k线根数大于4根 1日级别， 2 30分钟， 3 5分钟， 4 一分钟
#     if len(k_data_dts) - k_data_dts.index(st_data)>4:
#         frequency = '30m' if cur_ji+1==2 else '5m' if cur_ji+1==3 else '1m'
#         k_data_c = get_price(stock, st_data, end_date, frequency=frequency)
#         chanKc = parse2ChanK(k_data_c, k_data_c.values)
#         fenTypesc, fenIdxc = parse2ChanFen(chanKc)
#         if len(fenTypesc)==0: return biIdx
#         biIdxc, frsBiTypec = parse2ChanBi(fenTypesc, fenIdxc, chanKc)
#         if len(biIdxc)==0: return biIdx
#         xdIdxc, xdTypec = parse2Xianduan(biIdxc, chanKc)
#         biIdxc = con2Cxianduan(stock, k_data_c, chanKc, frsBiTypec, biIdxc, end_date, cur_ji+1)
#         if len(xdIdxc)==0: return biIdx
#         # 连接线段位为上级别的bi
#         lastBiType = frsBiType if len(biIdx)%2==0 else -frsBiType
#         if len(biIdx)==0:
#             return refactorXd(biIdx, xdIdxc, chanK, chanKc, cur_ji)
#         lastbi = biIdx.pop()
#         firstbic = xdIdxc.pop(0)
#         # 同向连接
#         if lastBiType == xdTypec:
#             biIdx = biIdx + refactorXd(biIdx, xdIdxc, chanK, chanKc, cur_ji)
#         # 逆向连接
#         else:
# #             print '开始逆向连接'
#             _mid = [lastbi] if (lastBiType == -1 and chanK['low'][lastbi]<=chanKc['low'][firstbic])\
#             or (lastBiType == 1 and chanK['high'][lastbi]>=chanKc['high'][firstbic]) else\
#             [chanKidx for chanKidx in range(len(chanK.index))[biIdx[len(biIdx)-1]:]\
#             if judge_day_bao(chanK, chanKidx, chanKc, firstbic, cur_ji)]
#             biIdx = biIdx + [_mid[0]] + refactorXd(biIdx, xdIdxc, chanK, chanKc, cur_ji)
#     return biIdx

