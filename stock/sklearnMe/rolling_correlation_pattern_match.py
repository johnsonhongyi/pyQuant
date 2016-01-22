import numpy as np
import pandas as pd
from pandas import Series
from pandas import DataFrame
import numpy.lib.stride_tricks as stride
np.random.seed(1)

n = 10
rng = pd.date_range('1/1/2000 00:00:00', periods=n, freq='5min')
df = DataFrame(np.random.rand(n, 1), columns=['a'], index=rng)

m = 4
rng = pd.date_range('1/1/2000 00:10:00', periods=m, freq='5min')
patch = DataFrame(np.arange(m), columns=['a'], index=rng)

def orig(df, patch):
    patch.reset_index(inplace=True, drop=True)

    df['corr'] = np.nan

    for i in range(df.shape[0]):
        window = df[i : i+patch.shape[0]]
        if window.shape[0] != patch.shape[0] :
            break
        else:
            window.reset_index(inplace=True, drop=True)
            corr = window.corrwith(patch)

            df['corr'][i] = corr.a

    return df

def using_numpy(df, patch):
    left = df['a'].values
    itemsize = left.itemsize
    left = stride.as_strided(left, shape=(n-m+1, m), strides = (itemsize, itemsize))

    right = patch['a'].values

    ldem = left - left.mean(axis=1)[:, None]
    rdem = right - right.mean()

    num = (ldem * rdem).sum(axis=1)
    dom = (m - 1) * np.sqrt(left.var(axis=1, ddof=1) * right.var(ddof=1))
    correl = num/dom

    df.ix[:len(correl), 'corr'] = correl
    return df

expected = orig(df.copy(), patch.copy())
result = using_numpy(df.copy(), patch.copy())

print(expected)
print(result)