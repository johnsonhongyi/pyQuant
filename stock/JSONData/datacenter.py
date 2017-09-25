# -*- encoding: utf-8 -*-
# !/usr/bin/python
# from __future__ import division

# import os
# import sys
# sys.path.append("..")
# import time
# from struct import *
# import numpy as np
# import pandas as pd
# from pandas import Series

# from JSONData import realdatajson as rl
# from JSONData import wencaiData as wcd
# from JohnsonUtil import LoggerFactory
# from JohnsonUtil import commonTips as cct
# from JohnsonUtil import johnson_cons as ct
# import tushare as ts
import sina_data
import StringIO,zipfile
class MemoryZipFile(object):
    def __init__(self):
        #创建内存文件
        self._memory_zip = StringIO.StringIO()
        
    def append_content(self, filename_in_zip, file_content):
        """
        description: 写文本内容到zip
        """
        zf = zipfile.ZipFile(self._memory_zip, "a", zipfile.ZIP_DEFLATED, False)
        zf.writestr(filename_in_zip, file_content)
        for zfile in zf.filelist: zfile.create_system = 0
        return self
         
    def append_file(self, filename_in_zip, local_file_full_path):
        """
        description:写文件内容到zip
        注意这里的第二个参数是本地磁盘文件的全路径(windows:c/demo/1.jpg | linux: /usr/local/test/1.jpg)
        """
        zf = zipfile.ZipFile(self._memory_zip, "a", zipfile.ZIP_DEFLATED, False)
        zf.write(local_file_full_path, filename_in_zip)
        for zfile in zf.filelist: zfile.create_system = 0      
        return self
    def read(self):
        """
        description: 读取zip文件内容
        """
        self._memory_zip.seek(0)
        return self._memory_zip.read()

    def write_file(self, filename):
        """
        description:写zip文件到磁盘
        """
        f = file(filename, "wb")
        f.write(self.read())
        f.close()
#     mem_zip_file = MemoryZipFile()
#     mem_zip_file.append_content('mimetype', "application/epub+zip")
#     mem_zip_file.append_content('META-INF/container.xml', '''<?xml version="1.0" encoding="UTF-8" ?>
# <container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container"> </container>''');
#     #追加磁盘上的文件内容到内存，注意这里的第二个参数是本地磁盘文件的全路径(windows:c/demo/1.jpg | linux: /usr/local/test/1.jpg)
#     # mem_zip_file.append_file("1.jpg", "c:\1.jpg")


#     #将内存中的zip文件写入磁盘
#     # mem_zip_file.write_file("c:test.zip")

#     #获取内存zip文件内容
#     data = mem_zip_file.read()
#     

from zipfile import ZipFile
# from StringIO import StringIO
import pandas as pd
from cStringIO import StringIO
def memdf():
    # r = urllib2.urlopen("http://seanlahman.com/files/database/lahman-csv_2014-02-14.zip").read()
    # file = ZipFile(StringIO(r))
    salaries_csv = file.open("Salaries.csv")
    salaries = pd.read_csv(salaries_csv)
if __name__ == "__main__":
    sina = sina_data.Sina()
    df = sina.all
    # print df
    file = StringIO()
    df.to_csv(file, delimiter=',', header=False, index=False,encoding='gbk')
    # print file.__doc__
    file.seek(0)
    dfread = pd.io.parsers.read_csv(file, delimiter=',', header=None,encoding='gbk')
    print dfread.shape,dfread[:2]