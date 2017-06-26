# -*- coding: utf-8 -*-

import urllib
import urllib2
import re
import math

import sys
import sqlite3
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

import jieba





class SQL_queryer(object):
    def __init__(self, database_filename):

        self.conn = sqlite3.connect(database_filename)
    def queryer_help(self, word):
        """给定一个单词，从数据库中获取查询的单词的列表[int,int]"""
        ret_seq = self.conn.execute("SELECT * FROM WORDS WHERE ID = '" + word + "'")
        final_list = []
        for item in ret_seq:
            tmp_str = item[1]
            str_list = tmp_str.split(',')
            if len(str_list)<=1:
                continue
            int_list = [int(x) for x in str_list]
            for x in int_list:
                final_list.append(x)
        return final_list

    def query(self, strings):
        #strings = unicode(strings)
        words = jieba.cut_for_search(strings)
        raw_list = []
        word_list=[]
        for word in words:
            word_list.extend(word)
            raw_list.extend(self.queryer_help(word))
        return self.get_most_k_value(15, raw_list,word_list)

    def get_most_k_value(self,k, list,words):
        """从列表中找出出现次数前k个的数值"""
        counter = dict()
        for item in list:
            if item in counter:
                continue
            else:
                counter[item] = self.tf_idf(words,item)
        ret = sorted(counter.items(), key=lambda d: d[1], reverse=True)
        return [x[0] for x in ret][:k]

    def tf_idf(self,words,item):
        sum=0
        for word in words:
            tf=0.0
            idf=0.0
            ret_seq = self.conn.execute("SELECT * FROM WORDS WHERE ID = '" + word + "'")
            for items in ret_seq:
                tmp = items[1]
                str_list = tmp.split(',')
                if len(str_list)<=1:
                    continue
                int_list = [int(x) for x in str_list]
                tf=int_list.count(item)
                idf = math.log(124.0 / float(len(set(int_list))+1))
            sum +=tf*idf

        return sum
    

