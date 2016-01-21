import cos_module

# cos_module?

# http://stackoverflow.com/questions/21058333/compute-rolling-maximum-drawdown-of-pandas-series

print dir(cos_module)
# ['__doc__', '__file__', '__name__', '__package__', 'cos_func']

print cos_module.cos_func(1.0)
# Out[4]: 0.5403023058681398

print cos_module.cos_func(0.0)
# Out[5]: 1.0

print cos_module.cos_func(3.14159265359)

# print cos_module.cos_func('foo')
# Out[6]: -1.0

import cy_rolling_dd_custom_mv

print dir(cy_rolling_dd_custom_mv)

import tushare as ts
import numpy as np

df = ts.get_hist_data('601198')
print df.close.values
abc = cy_rolling_dd_custom_mv.cy_rolling_dd_custom_mv(df.close.values, 5)
print np.array(abc)
# print abc
