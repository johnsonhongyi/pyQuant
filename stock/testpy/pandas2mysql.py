# -*- coding: UTF-8 -*-
from sqlalchemy import create_engine
import sqlalchemy
import MySQLdb
import tushare as ts
import time
# import maptest as mp

engine = create_engine('mysql://root:plokij@127.0.0.1/Quant?charset=utf8',echo=True)
# engine = create_engine('mysql://root:plokij@127.0.0.1/Quant?charset=utf8',echo=True,strategy=’threadlocal’)
# metadata = MetaData(engine)
#
# users_table = table('users',
#           metadata,
#           Column('date', VARCHAR(40), primary_key=True),
#           Column('open', FLOAT(53)),
#           Column('high', FLOAT(53)),
#           Column('high', FLOAT(53)),
#
#           )
# codes=mp.get_all_top()


# CREATE TABLE `000017`
# 	date TEXT,
# 	open FLOAT(53),
# 	high FLOAT(53),
# 	close FLOAT(53),
# 	low FLOAT(53),
# 	volume FLOAT(53),
# 	price_change FLOAT(53),
# 	p_change FLOAT(53),
# 	ma5 FLOAT(53),
# 	ma10 FLOAT(53),
# 	ma20 FLOAT(53),
# 	v_ma5 FLOAT(53),
# 	v_ma10 FLOAT(53),
# 	v_ma20 FLOAT(53),
# 	turnover FLOAT(53)
# )


codes=['000030','601198','600476']
num=0
for code in codes:
    df = ts.get_hist_data(code)
    if not df.empty:

        #存入数据库
        print "write to sql"
        num+=len(df.index)
        print num
        print code

        df.to_sql(code,engine,if_exists='replace',dtype={'code':sqlalchemy.types.CHAR(length=6),'date':sqlalchemy.types.DATE})
        # time.sleep(1)
    else:
        print "df None"

#追加数据到现有表

#df.to_sql('tick_data',engine,if_exists='append')
