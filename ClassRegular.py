# -*- coding: utf-8 -*-

import re
import logging
import requests
logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)

class Regular(object):
    def __init__(self):
        pass

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
                'data': 'biliShortUrl match failed(+_+)?'
                }

    def biliDynamicId(self, message):
        '''
        返回t.bilibili.com域名下的b站动态\n
        status  result\n
        0       正常\n
        -1      匹配失败\n
        '''
        try:
            patternBiliDynamicId = re.compile(r'(?:t|m).bilibili.com/(?:dynamic/)?([0-9]+)')
            BiliDynamicId = re.findall(patternBiliDynamicId, message)[0]
            return {'status': 0,'result': BiliDynamicId}
        except:
            logging.error('biliDynamic match failed(+_+)?')
            return {'status': -1,'result': 'biliDynamic match failed(+_+)'}


if __name__ == '__main__':
    patternBiliDynamicId = re.compile(r'(?:t|m).bilibili.com/(?:dynamic/)?([0-9]+)')
    BiliDynamicId = re.findall(patternBiliDynamicId, 'https://m.bilibili.com/dynamic/627795919422504831?share_medium=android&share_plat=android&share_session_id=33a44759-0a5c-4fc1-95f5-de78f440c7b3&share_source=COPY&share_tag=s_i&timestamp=1645084342&unique_k=f4vzDAM')#[0]
    print(BiliDynamicId)