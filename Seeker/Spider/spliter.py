# -*- coding: utf-8 -*-
import urllib

import re
import sys
import logging
logging.basicConfig(level=logging.INFO)

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)


import jieba
from SQL_sqlite import *

def get_most_k_value(k, li):
    """从列表中找出出现次数前k个的数值"""
    counter = dict()
    for item in li:
        if item not in counter:
            counter[item] = 1
        else:
            counter[item] += 1
    ret = sorted(counter.items(), key=lambda d: d[1], reverse=True)
    return [x[0] for x in ret][:k]

class Spliter(object):

    def __init__(self):
        self.sql = SQL('../Main/my_engine_data_base.db')
        self.stop_word = set()
        self.cache = dict()
        with open('stopword.txt', 'r') as f:
            for line in f:
                if line[:-1] != '':
                    self.stop_word.add(line[:-1])


    def read_files(self):
        bad, cnt = 0, 0
        for ide in range(100000):
            filename = '../Main/info/' + str(ide) + '.txt'
            try:
                f = open(filename, 'r')
                contents = list(f)
                # 将正文拼接成一行
                text_lines = contents[6:]
                text = ' '.join([line[:-1] for line in text_lines])

                # 读取完成之后直接构建词语列表
                after_split_text = jieba.cut_for_search(text)
                for word in after_split_text:
                    if word in self.stop_word:
                        continue
                    if word not in self.cache:
                        self.cache[word] = []
                    else:
                        self.cache[word].append(ide)

                #构建词语表完成，放到内存中等待取用

                bad, cnt = 0, cnt + 1
                if cnt % 100 == 0:
                    logging.info('Read & Construct_INFO ' + str(cnt))
                f.close()
            except IOError:

                bad += 1
                if bad == 1000:
                    break
        logging.info('cutting _INFO')

        for word_, lists in self.cache.items():
            # 对于每个词，得到100个最相关的网页id信息，存放到数据库中
            tmplist = get_most_k_value(100, lists)
            self.sql.Insert(word_, tmplist)
        self.sql.save_close()
        self.cache.clear()

