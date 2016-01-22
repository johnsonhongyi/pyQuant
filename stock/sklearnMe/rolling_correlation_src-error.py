import numpy as np
import pandas as pd
from pandas import Series
from pandas import DataFrame

# Create test DataFrame df and a patch to be found.
n = 10
rng = pd.date_range('1/1/2000 00:00:00', periods=n, freq='5min')
df = DataFrame(np.random.rand(n, 1), columns=['a'], index=rng)

n = 4
rng = pd.date_range('1/1/2000 00:10:00', periods=n, freq='5min')
patch = DataFrame(np.arange(n), columns=['a'], index=rng)

print "X:",df,patch
print
print '    *** Start corr example ***'
# To avoid the automatic alignment between df and patch, 
# I need to reset the index.
patch.reset_index(inplace=True, drop=True)
# Cannot do:
#    df.reset_index(inplace=True, drop=True)

df['corr'] = np.nan

for i in range(df.shape[0]):
    window = df[i : i+patch.shape[0]]
    print "w:",window
    # If slice has only two rows, I have a line between two points
    # When I corr with to points in patch, I start getting 
    # misleading values like 1 or -1
    if window.shape[0] != patch.shape[0] :
        break
    else:
        # I need to reset_index for the window, 
        # which is less efficient than doing outside the 
        # for loop where the patch has its reset_index done.
        # If I would do the df.reset_index up there, 
        # I would still have automatic realignment but
        # by index.
        window.reset_index(inplace=True, drop=True)

        # On top of the obvious inefficiency
        # of this method, I cannot just corrwith()
        # between specific columns in the dataframe;
        # corrwith() runs for all.
        # Alternatively I could create a new DataFrame
        # only with the needed columns:
        #     df_col = DataFrame(df.a)
        #     patch_col = DataFrame(patch.a)
        # Alternatively I could join the patch to
        # the df and shift it.
        corr = window.corrwith(patch)

        print
        print '==========================='
        print 'window:'
        print window
        print '---------------------------'
        print 'patch:'
        print patch
        print '---------------------------'
        print 'Corr for this window'
        print corr
        print '============================'

        df['corr'][i] = corr.a

print
print '    *** End corr example ***'
print " Please inspect var 'df'"
print