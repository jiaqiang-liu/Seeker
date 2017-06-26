# -*- coding: utf-8 -*-
import sys
import jieba
import web
from Queryer import *
from ObjectConstructor import *
import time
import os
import shutil
import random

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

urls = (
    '/', 'index'
)
app = web.application(urls, globals())
render = web.template.render('templates/')
class index:
    def GET(self):
        timer = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
        visiter = web.ctx['ip']
        f = open('log.txt', 'a+')
        f.write('Index ' + timer + ' ' + visiter + '\n')
        f.close()
        return render.index()

    def POST(self):
        contents = web.input()
        start = time.clock()
        if contents['title'].strip()=='':
            return render.index()
        timer = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
        visiter = web.ctx['ip']
        f = open('log.txt', 'a+')
        f.write('Post ' + timer + ' ' + visiter + ' ' + contents['title'] + '\n')
        f.close()
        targets = list(jieba.cut_for_search(contents['title']))# 关键词列表
        sq = SQL_queryer('my_engine_data_base.db')
        idlist = sq.query(contents['title']) # 和关键词相关性比较强的那些网址的id
        shows = []
        for id in idlist:
            try:
                shows.append(ObjectConstructor(id, targets))
            except:
                pass
        if len(idlist)==0:
            search_result ="Seeker没有找到相关结果，为您随机返回了一些网页"
            for i in range(10):
                shows.append(ObjectConstructor(random.randint(1,100), targets))
        shows = sorted(shows, key=lambda x: x.time, reverse=True)
        end = time.clock()
        if len(idlist)>0:
            search_result ="Seeker为您找到了约"+str(len(idlist))+"条结果，用时"+str(end-start)+"秒"
        return render.main(contents['title'],search_result,shows)
        
        
        

if __name__ == "__main__":
    app.run()