# -*- coding: utf-8 -*-
#!/usr/bin/env python

import requests
import logging
import time
import re
import json
logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)

class Bili(object):
    def __init__(self):
        self.headers = {
            'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
            'origin': 'https://www.bilibili.com',
            'pragma': 'no-cache',
            'refer': 'https://www.bilibili.com/',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.3",
            'cookie': 'SESSDATA=79d36f8d%2C1658593097%2C8d553*11'
        }

    def getHotWord(self):
        url = 'http://s.search.bilibili.com/main/hotword'
        response = requests.get(url).json()
        if response['code'] == 0:
            logging.info('Get hot search success')
            timestamp = response['timestamp']
            HotWordTime = time.strftime("%a %b %d %H:%M:%S %Y", time.localtime(timestamp))
            HotWordLsit =[]
            for li in response['list']:
                if li['word_type'] == 5:
                    word_type = 'hot'
                elif li['word_type'] == 4:
                    word_type = 'new'
                else:
                    word_type = ''
                HotWordLsit.append([li['pos'], li['keyword'], word_type]) # word_type 1:normal 4:new 5:hot
            message = HotWordTime
            for i in HotWordLsit:
                message += '\n'
                message += str(i[0])
                message += '.'
                message += i[1]
                message += '\t'
                message += i[2]
            return {
                'status': 0,
                'data': message
            }
        else:
            logging.error(response['code'],'Failed to get hot search')
            return {
                'status': -1,
                'data':'Failed to get hot search'
                }
    
    def toBiliShortUrl(self, url):
        shareUrl = 'https://api.bilibili.com/x/share/click'
        data = {
            'build': '9331',
            'buvid': 'qp92wvbiiwercf5au381g1bzajou85hg',
            'oid': url,
            'platform': 'ios',
            'share_channel': 'COPY',
            'share_id': 'public.webview.0.0.pv',
            'share_mode': '3'
            }
        try:
            response = requests.post(shareUrl, data).json()
            logging.info('shareUrl response:{}'.format(response))
            return {
                'status': 0,
                'data':response['data']['content']
                }
        except:
            logging.error('Failed to transform short link')
            return {
                'status': -1,
                'data': url
                }

    def biliVideoInfo(self, abcode):  
        logging.info('biliVideoInfo abcode: {}'.format(abcode))
        if 'BV' in abcode or 'bv' in abcode:
            bvid = abcode
            logging.info('bvid:{}'.format(bvid))
            response = requests.get('https://api.bilibili.com/x/web-interface/view?bvid={}'.format(bvid), headers=self.headers)
        elif 'AV' in abcode or 'av' in abcode:
            aid = abcode[2:]
            logging.info('aid:{}'.format(aid))
            response = requests.get('http://api.bilibili.com/x/web-interface/view?aid={}'.format(aid), headers=self.headers)
        else:
            logging.error(abcode)
            return {'status': '快去写正则(╬▔皿▔)凸'}
        logging.info(response.json())
        if response.json()['code'] == 0:
            data = response.json()['data']
            logging.info('data:{}'.format(data))
            bvid = data['bvid']
            logging.info('bvid:{}'.format(bvid))
            videoFace = data['pic']
            videoTitle = data['title']
            videoDescription = data['desc']
            shortLink = self.toBiliShortUrl('https://www.bilibili.com/video/{}'.format(abcode))
            logging.info('shortLink:{}'.format(shortLink['result']))
            return {
                'status': 0,
                'result': '标题:{}\n{}\n简介:{}\n链接:{}'.format(videoTitle, '[CQ:image,file={}]'.format(videoFace), videoDescription, shortLink['result'])
            }
        elif response.json()['code'] == -400:
            logging.error('请求错误QwQ')
            return {'status': '请求错误QwQ'}
        elif response.json()['code'] == -403:
            logging.error('权限不足')
            return {'status': '权限不足'}
        elif response.json()['code'] == -404:
            logging.error('无视频ㄟ( ▔, ▔ )ㄏ')
            return {'status': '无视频ㄟ( ▔, ▔ )ㄏ'}
        elif response.json()['code'] == 62002:
            logging.error('稿件不可见')
            return {'status': '稿件不可见'}


    








    def getDynamicInfo(self, dynamic_id):
        dynamicUrl = 'https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/get_dynamic_detail?dynamic_id={}'.format(dynamic_id)
        response = requests.get(dynamicUrl).json()

        # 图片动态
        if response['data']['card']['desc']['type'] == 2:
            if response['code'] == 0:
                uname = response['data']['card']['desc']['user_profile']['info']['uname']
                card = response['data']['card']['card']
                card = str(json.loads(card))
                logging.info(card)
                imageList = re.findall(r'https://i0.hdslb.com/bfs/album/[0-9a-z]+\.(?:png|jpg)', card)
                description = re.findall(r''''description': (.*?), 'id''', card)[0]
                logging.info(uname)
                description = description[1:-1]
                logging.info(description)
                
                logging.info(imageList)
                return {
                    'status': 0,
                    'uname': uname,
                    'description': description,
                    'imageList': imageList
                }
                
            else:
                return {'status': -1, 'result': response['code']}
        else:
            return {'status': -1, 'result': '该动态类型未完善'}

if __name__ == '__main__':
    paib = Bili()
    # a = paib.getDynamicInfo('627397887615151994')##627795919422504831
    a = paib.biliVideoInfo('BV1GJ411x7h7')
    print(a)


    