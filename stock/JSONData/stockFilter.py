# -*- coding:utf-8 -*-
# import pandas as pd

def getBollFilter(df=None,boll=1):
	#return boll > int
	if df is None:
		print "dataframe is None"
		return None
	if 'boll' in df.columns:
		return df[df.boll >= boll]
	else:
		print "boll not in columns"
		return df 