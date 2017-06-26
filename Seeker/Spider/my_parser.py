#!/usr/bin.env python
# -*- coding: utf-8 -*-
from HTMLParser import HTMLParser
from re import sub
from utility import *
from URL import *
import requests
global_cache = []
global_url_counter = 0

import logging
import re
logging.basicConfig(level=logging.INFO)

#html页面解析类
class HtmlParserMainText(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.text = []
        self.link = []

    def handle_starttag(self, tag, attrs):
        if tag == "p":
            self.text.append('\n')
        elif tag == 'a':
            for name, value in attrs:  
                if name == 'href':
                    self.link.append(value)
        else:
            pass

    def handle_data(self, data):
        if len(data.strip()) > 0:
            self.text.append(data.strip())

    def get_html_str(self, current_url):
        html_str = ''
        try:
            #req = request.Request(current_url)
            # req.add_header('User-Agent', 'Mozilla/6.0')
            #response = request.urlopen(req)
            #data = response.read()
            #html_str = data.decode('utf-8')
            kv={'user-agent':'Mozilla/6.0'}
            r=requests.get(current_url,headers=kv)
            r.encoding='utf-8'
            html_str=r.text
        except:
            pass
        return html_str

    def settle_down(self, url):

        global global_url_counter
        self.text = []
        self.link = []
        html_str = self.get_html_str(url)

        def get_title(html_str):
            i = html_str.find('<title>')
            j = html_str.find('</title>')
            if i == -1 or j == -1:
                i = html_str.find('<TITLE>')
                j = html_str.find('</TITLE>')
            return html_str[i + 7:j]
        origin_title = get_title(html_str)

        def get_time(html_str):
            import re
            grouppattern = re.compile(r'(\d+)-(\d+)-(\d+)')
            biggest = 0
            record = (0, 0, 0)
            target = grouppattern.findall(html_str)
            if not target:
                return record
            for year, month, day in target:
                tmp = (int(year)-2000) * 365 + 12 * int(month) + int(day)
                if tmp > biggest:
                    biggest, record = tmp, (year, month, day)
            return record
        time = get_time(html_str)

        # replace the \n to \s
        s = ''
        for char in html_str:
            adder = ' ' if char == '\n' else char
            s += adder

        re_cdata = re.compile('//<!\[CDATA\[[^>]*//\]\]>', re.DOTALL)  # 匹配CDATA
        # re_script = re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>', re.DOTALL)  # Script
        
        re_script = re.compile('<script.*?/script>', re.DOTALL)  # Script
        re_style = re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>', re.DOTALL)  # style
        re_style_upper = re.compile('<\s*STYLE[^>]*>[^<]*<\s*/\s*STYLE\s*>', re.DOTALL)  # upper
        re_br = re.compile('<br\s*?/?>')  # 处理换行
        re_h = re.compile('</?\w+[^>]*>')  # HTML标签
        re_comment = re.compile('<!--[^>]*-->')  # HTML注释

        s = re_cdata.sub('', s)  # 去掉CDATA
        s = re_script.sub('', s)  # 去掉SCRIPT
        s = re_style.sub('', s)  # 去掉style
        s = re_style_upper.sub('', s) # STYLE
        s = re_br.sub('\n', s)  # 将br转换为换行
        s = re_comment.sub('', s)  # 去掉HTML注释

        self.feed(s)
        self.close()

        links_to = []
        for link in self.link:
            link = formuler(link)
            #links_to.append(link)
            if urlfilter(link):
                links_to.append(link)
        # 正文的内容，不再采用一行的方式，显示，采用多行的方式
        global_cache.append(URL(url, global_url_counter, origin_title, self.text, links_to, time))
        global_url_counter += 1
        return links_to














