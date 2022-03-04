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

    def saveCQImageUrl(self, message, gid):
        try:
            urlList = re.findall(r'https://gchat.qpic.cn/gchatpic_new/(.*?/.*?)/0\?term=3',message)
            os.makedirs('./CQImageUrl/{}/'.format(gid), exist_ok=True)
            with open('./CQImageUrl/{}/{}.txt'.format(gid, time.strftime("%Y-%m", time.localtime(time.time()))), mode='a+', encoding='utf-8') as f:
                for url in urlList:
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
    
    def getCQImageUrlInfo(self, gid=None, groupname=None):
        from itertools import (takewhile, repeat)
        buffer = 1024 * 1024
        info_dict = {
                'nmg': '649451770',
                'qwq': '980514385',
                'ys': '130516740'
            }
        if gid != None:
            if groupname != None:
                os.makedirs('./CQImageUrl/{}/'.format(info_dict[groupname]), exist_ok=True)
                imgFolderList = os.listdir('./CQImageUrl/{}/'.format(info_dict[groupname]))
                count = 0
                for imgfoldername in imgFolderList:
                    with open('./CQImageUrl/{}/{}'.format(info_dict[groupname], imgfoldername), encoding='utf-8') as f:
                        buf_gen = takewhile(lambda x: x, (f.read(buffer) for _ in repeat(None)))
                        count += sum(buf.count('\n') for buf in buf_gen)
                message = '群聊{}收录图片:'.format(groupname) + str(count) + '张'
                return {
                    'status': 0,
                    'data': message
                }

            else:
                groupList = os.listdir('./CQImageUrl/')
                count = 0
                for i in groupList:
                    imgFolderList = os.listdir('./CQImageUrl/{}/'.format(i))
                    for imgfoldername in imgFolderList:
                        with open('./CQImageUrl/{}/{}'.format(i, imgfoldername), encoding='utf-8') as f:
                            buf_gen = takewhile(lambda x: x, (f.read(buffer) for _ in repeat(None)))
                            count += sum(buf.count('\n') for buf in buf_gen)
                count += sum(buf.count('\n') for buf in buf_gen)
                message = '所有群收录图片:' + str(count) + '张'
                return {
                    'status': 0,
                    'data': message
                }

        else:
            return {
                'status': -5,
                'data': '查询失败'
            }
    
    def getCQImage(self, gid, imgnum):
        CQImageList = os.listdir('./CQImageUrl/{}/'.format(gid))
        from itertools import (takewhile, repeat)
        buffer = 1024 * 1024
        imgList = []
        for i in range(0,int(imgnum)):
            r = random.randint(0,len(CQImageList)-1)
            with open('./CQImageUrl/{}/{}'.format(gid, CQImageList[r]), 'r', encoding='utf-8') as f:
                buf_gen = takewhile(lambda x: x, (f.read(buffer) for _ in repeat(None)))
                x = random.randint(0,sum(buf.count('\n') for buf in buf_gen)-1)
                num = 0
                f.seek(0)
                for line in f:
                    if num == x:
                        imgList.append('https://gchat.qpic.cn/gchatpic_new/'+line.strip('\n')+'/0?term=3')
                        break
                    else:
                        num += 1
        return {
                'status': 0,
                'data': imgList
            }
        
    def getGroupInfo(self):
        os.makedirs('./CQImageUrl/', exist_ok=True)
        groupList = os.listdir('./CQImageUrl/')
        if groupList != []:
            info_dict = {
                '649451770': 'nmg',
                '980514385': 'qwq',
                '130516740': 'ys'
            }
            m = '各群标识:\n'
            for i in groupList:
                if i in info_dict.keys():
                    m += i
                    m += ': '
                    m += info_dict[i]
                    m += '\n'
                else:
                    pass
            return {
                'status': 0,
                'data': m
            }
        else:
            return {
                'status': -5,
                'data': '没有群信息哦'
            }

if __name__ == '__main__':
    pass
    print(Regular().getCQImage('649451770', '10'))