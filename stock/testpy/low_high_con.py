import tushare as ts

df=ts.get_hist_data('sh')
dz=df[df.index >= '2016-01-01']
lowp=dz.close.min()
lowdate=dz[dz.close==lowp].index.values[0]
print lowdate,lowp
