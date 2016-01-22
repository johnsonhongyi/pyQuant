def roll_corr_groupby(x,i):
    x['Z'] = rolling_corr(x['col 1'], x['col 2'],i) 
    return x

x.groupby(['key']).apply(roll_corr_groupby)
x.head()