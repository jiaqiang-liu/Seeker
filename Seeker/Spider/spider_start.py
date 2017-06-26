# -*- coding: utf-8 -*-
from spliter import *
from spider import *
from Constructor import *
from URL import *
from utility import *
import logging
logging.basicConfig(level=logging.INFO)
import time
import utility



delete_data_base_if_exist('../Main/my_engine_data_base.db')   #如果存在数据文件则删除


# 爬虫爬取开始
start = time.clock()
logging.info('Spider_Start')
spider = Spider('http://news.nwpu.edu.cn/')
spider.start()
logging.info('Spider_Over')
end = time.clock()
logging.info('Spider_cost ' + str(end-start) + ' second')
#爬虫爬取结束

#计算网页pagerank并将内容写入文件
start = time.clock()
logging.info('construct and write start')
ctr = Contructor_Writer(global_cache)
ctr.construct_write()
logging.info('Write over')
end = time.clock()
logging.info('Ctr cost ' + str(end-start) + ' second')

#构建倒排表
start = time.clock()
logging.info('Spliter start write to sqlite')
sp = Spliter()
sp.read_files()
end = time.clock()
logging.info('spliter cost ' + str(end-start) + ' second')


logging.info('all_done')

