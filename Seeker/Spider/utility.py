# coding=utf-8   #默认编码格式为utf-8

import requests
import os

def urlfilter(url):
    """url筛选器"""
    picturesflag = ['jpg', 'jpeg', 'png', 'PNG', 'JPG', 'JPEG']
    if url.find('news.nwpu.edu.cn') == -1:
        return False
    return True


def is_chinese(uchar):
    """判断一个unicode是否是汉字"""
    if uchar >= u'\u4e00' and uchar <= u'\u9fa5':
        return True
    else:
        return False

def formuler(url):
    """将url标准化"""
    if url.startswith('http') == False:
        url = 'http://news.nwpu.edu.cn/' + url
    if url.endswith('#'):
        url = url[:-1]
    if url.find('/..') != -1:
        url = url.replace('/..', '')
    return url


def delete_data_base_if_exist(path):
    if os.path.exists(path):
        os.remove(path)
        print('original db has been removed.')

