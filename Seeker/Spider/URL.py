# -*- coding: utf-8 -*-
class URL(object):
    #每个URL对象的几个特征

    def __init__(self, url, id_, title,text, links_, time): #去掉空格和英文之后的内容
        self.url = url
        self.id = id_
        self.title = title
        self.text = text
        self.links = links_
        self.time = time
        # 指向的链接, id是多少, 这个是后来建立的
        self.links_id = []
        self.rank = 0.0