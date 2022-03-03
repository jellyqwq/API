# -*- coding: utf-8 -*-

import re
import logging
import requests
import os
import time
import random

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
            url = re.search(r'https://gchat.qpic.cn/gchatpic_new/(.*?/.*?)/0\?term=3',message).groups()[0]
            os.makedirs('./CQImageUrl/', exist_ok=True)
            with open('./CQImageUrl/{}.txt'.format(time.strftime("%Y-%m", time.localtime(time.time()))), mode='a+', encoding='utf-8') as f:
                f.seek(0)
                if f.read(1) != '':
                    f.seek(0)
                    count = False
                    for line in f:
                        if url[-32:] == line[-33:-1] and count == False:
                            logging.info('图片已存在')
                            count = True
                            break
                    if count == False:
                        f.seek(0,2)
                        f.write(url)
                        f.write('\n')
                else:
                    logging.info('h')
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
    
    def getCQImage(self, times=None, num=None):
        CQImageList = os.listdir('./CQImageUrl/')
        if times == None and num == None:
            from itertools import (takewhile, repeat)
            buffer = 1024 * 1024
            r = random.randint(0,len(CQImageList)-1)
            with open('./CQImageUrl/{}'.format(CQImageList[r]), 'r', encoding='utf-8') as f:
                buf_gen = takewhile(lambda x: x, (f.read(buffer) for _ in repeat(None)))
                x = random.randint(0,sum(buf.count('\n') for buf in buf_gen)-1)
                num = 0
                f.seek(0)
                for line in f:
                    if num == x:
                        return {
                            'status': 0,
                            'data': 'https://gchat.qpic.cn/gchatpic_new/'+line.strip('\n')+'/0?term=3'
                        }
                    else:
                        num += 1

if __name__ == '__main__':
    print(Regular().getCQImage())