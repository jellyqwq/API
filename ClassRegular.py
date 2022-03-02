# -*- coding: utf-8 -*-

import re
import logging
import requests
import os
import time

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)

class Regular(object):
    def __init__(self):
        pass
    
    # 将b站域名下的视频url提取av或bv号
    def biliVideoUrl(self, message):
        try:
            patternBili = re.compile(r'video/([a-zA-Z0-9]+)')
            abcode = re.findall(patternBili, message)[0]
            # logging.info('abcode:{}'.format(abcode))
            return {
                'status': 0, 
                'data': abcode
                }
        except:
            logging.error('biliVideoUrl match failed(+_+)?')
            return {
                'status': -5,
                'data': 'biliVideoUrl match failed(+_+)?'
                }

    # 将b23.tv域名下的重定向地址返回
    def biliShortUrl(self, message):
        try:
            patternBiliShortLink = re.compile(r'http(s)://b23.tv/[a-zA-Z0-9]+')
            biliShortLinkUrl = re.search(patternBiliShortLink, message).group()
            # logging.info('biliShortLinkUrl:{}'.format(biliShortLinkUrl))
            response = requests.get(biliShortLinkUrl, allow_redirects=False) #关闭重定向,取请求标头
            response = dict(response.headers)
            response = response['Location']
            logging.info('biliShortUrl Redirects:{}'.format(response))
            return {
                'status': 0, 
                'data': response
                }
        except:
            logging.error('biliShortUrl match failed(+_+)?')
            return {
                'status': -5,
                'data': response
                }
    
    # 动态url地址
    def biliDynamicId(self, message):
        try:
            patternBiliDynamicId = re.compile(r'(?:t|m).bilibili.com/(?:dynamic/)?([0-9]+)')
            BiliDynamicId = re.findall(patternBiliDynamicId, message)[0]
            return {
                'status': 0,
                'data': BiliDynamicId
                }
        except:
            logging.error('biliDynamic match failed(+_+)?')
            return {
                'status': -5,
                'data': 'biliDynamic match failed(+_+)'
                }

    def getCQImageUrl(self, message):
        try:
            url = re.search(r'url=(.*),subType',message).groups()[0]
            os.makedirs('./CQImageUrl/', exist_ok=True)
            with open('./CQImageUrl/{}.txt'.format(time.strftime("%Y-%m", time.localtime(time.time()))), 'a', encoding='utf-8') as f:
                f.write(url)
                f.write('\n')
            return {
                'status': 0,
                'data': '保存成功'
            }
        except:
            logging.error('CQ图url匹配失败')
            return {
                'status': -5,
                'data': 'CQ图url匹配失败'
            }
    
    def getCQImageUrlInfo(self):
        try:
            from itertools import (takewhile, repeat)
            buffer = 1024 * 1024
            t =time.strftime("%Y-%m", time.localtime(time.time()))
            with open('./CQImageUrl/{}.txt'.format(t), encoding='utf-8') as f:
                buf_gen = takewhile(lambda x: x, (f.read(buffer) for _ in repeat(None)))
                message = t + '保存图片' + str(sum(buf.count('\n') for buf in buf_gen)) + '张'
            return {
                'status': 0,
                'data': message
            }
        except:
            return {
                'status': -5,
                'data': '查询失败'
            }

if __name__ == '__main__':
    z = Regular().getCQImageUrl('[CQ:image,file=7abbd899e3fef4a9fe53dde0d5c77a99.image,url=https://gchat.qpic.cn/gchatpic_new/1541986714/649451770-2433486197-7ABBD899E3FEF4A9FE53DDE0D5C77A99/0?term=3,subType=0]')
    message = '[CQ:image,file=7abbd899e3fef4a9fe53dde0d5c77a99.image,url=https://gchat.qpic.cn/gchatpic_new/1541986714/649451770-2433486197-7ABBD899E3FEF4A9FE53DDE0D5C77A99/0?term=3,subType=0]'
    y=re.search(r'url=(.*),subType', message).groups()[0]
    print(z)
    print(y)