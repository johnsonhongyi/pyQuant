# -*- coding:utf-8 -*-
import os
sql="insert into usermap_story (usermapid,storyid,type,status,updatedate,createdate) VALUES (%s,99,2,1,NOW(),NOW());"
start = 205645
end = 205758

def Output_Csv(dlist,filename):
    fout = open(filename, 'wb')
    for i in dlist:
        raw = (i) + '\r\n'
        fout.write(raw)
sqllist = []
for i in range(start,end,1):
    # print i
    sqllist.append(sql%(i))
    
Output_Csv(sqllist,"intsert.sql")
