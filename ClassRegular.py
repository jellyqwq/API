# -*- coding: utf-8 -*-

import re
import logging
import requests
import os
import time
import random
import collections

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)

class Regular(object):
    def __init__(self):
        self.GNAME_TO_GID = {
            'nmg': '649451770',
            'qwq': '980514385',
            'ys': '130516740',
            'gal': '605650659',
            }
        self.GID_TO_GNAME = {
            '649451770': 'nmg',
            '980514385': 'qwq',
            '130516740': 'ys',
            '605650659': 'gal',
        }
        self.IMAGE_CACHE_DICT = collections.OrderedDict()
    
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
        if gid != None:
            if groupname != None:
                os.makedirs('./CQImageUrl/{}/'.format(self.GNAME_TO_GID[groupname]), exist_ok=True)
                imgFolderList = os.listdir('./CQImageUrl/{}/'.format(self.GNAME_TO_GID[groupname]))
                count = 0
                for imgfoldername in imgFolderList:
                    with open('./CQImageUrl/{}/{}'.format(self.GNAME_TO_GID[groupname], imgfoldername), encoding='utf-8') as f:
                        buf_gen = takewhile(lambda x: x, (f.read(buffer) for _ in repeat(None)))
                        count += sum(buf.count('\n') for buf in buf_gen)
                message = '群聊{}收录图片:'.format(groupname) + str(count) + '张'
                return {
                    'status': 0,
                    'count': count,
                    'data': message,
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
                    'count': count,
                    'data': message,
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
        count = self.getCQImageUrlInfo(gid, self.GID_TO_GNAME[gid])['count']
        if count < int(imgnum):
            return {
                'status': -5,
                'data': '群{}图库数量不足'.format(self.GID_TO_GNAME[gid])
            }
        while len(imgList) != int(imgnum) and count >= int(imgnum):
            r = random.randint(0,len(CQImageList)-1)
            with open('./CQImageUrl/{}/{}'.format(gid, CQImageList[r]), 'r', encoding='utf-8') as f:
                buf_gen = takewhile(lambda x: x, (f.read(buffer) for _ in repeat(None)))
                x = random.randint(0,sum(buf.count('\n') for buf in buf_gen)-1)
                num = 0
                f.seek(0)
                line = f.readline()
                # for line in f:
                while line:
                    if num == x:
                        img = 'https://gchat.qpic.cn/gchatpic_new/'+line.strip('\n')+'/0?term=3'
                        if img not in imgList:
                            logging.info(f.tell())
                            imgList.append(img)
                            break
                        else:
                            break
                    else:
                        num += 1
                    line = f.readline()
        return {
                'status': 0,
                'data': imgList
            }
        
    def getGroupInfo(self):
        os.makedirs('./CQImageUrl/', exist_ok=True)
        groupList = os.listdir('./CQImageUrl/')
        if groupList != []:
            # 详细信息
            m = '基本信息:\n'
            m += '总数: {}张\n'.format(self.getCQImageUrlInfo(True)['count'])
            for gid in groupList:
                if gid in self.GID_TO_GNAME.keys():
                    m += self.GID_TO_GNAME[gid]
                    m += ': '
                    m += str(self.getCQImageUrlInfo(gid, self.GID_TO_GNAME[gid])['count'])
                    m += '张\n'
            
            m += '''\n基本功能:
1.派蒙图库->获取全部群代号的图片总张数以及每个群的张数
2.派蒙图库#群代号->获取这个群的图片总数
3.消息中含有关键词 派蒙 图 即可获取图片
4.向上述消息中加入关键词 群代号可发指定群的图片
5.还能向消息中添加如 3张 这样的关键词获取指定数量的图片'''
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
    # message = '[CQ:reply,id=645016453][CQ:at,qq=2980293094] del'
    # m = re.findall(r'\[CQ:reply,id=(-?[0-9]+)]\[CQ:at,qq=2980293094]', message)
    # print(m)
    Regular().getCQImage('649451770', '5')