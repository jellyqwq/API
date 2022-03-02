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
            HotWordTime = time.strftime("%Y-%m-%d %H:%M %a", time.localtime(timestamp))
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
        if 'BV' in abcode or 'bv' in abcode:
            bvid = abcode
            response = requests.get('https://api.bilibili.com/x/web-interface/view?bvid={}'.format(bvid), headers=self.headers)
        elif 'AV' in abcode or 'av' in abcode:
            aid = abcode[2:]
            response = requests.get('http://api.bilibili.com/x/web-interface/view?aid={}'.format(aid), headers=self.headers)
        else:
            logging.error('abcode: {}'.format(abcode))
            return {
                'status': -3,
                'data': 'abcode error'
                }
        if response.json()['code'] == 0:
            data = response.json()['data']
            uname = data['owner']['name']
            stat = data['stat']
            bvid = data['bvid']
            aid = stat['aid']
            face = data['pic']
            title = data['title']
            desc = data['desc']
            view = stat['view']
            danmaku = stat['danmaku']
            reply = stat['reply']
            favorite = stat['favorite']
            coin = stat['coin']
            share = stat['share']
            like = stat['like']
            shortLink = self.toBiliShortUrl('https://www.bilibili.com/video/{}'.format(abcode))
            return {
                'status': 0,
                'data': {
                    'aid': aid,
                    'bvid': bvid,
                    'uname': uname,
                    'face': face,
                    'title': title,
                    'desc': desc,
                    'view': view,
                    'danmaku': danmaku,
                    'reply': reply,
                    'favorite': favorite,
                    'coin': coin,
                    'share': share,
                    'like': like,
                    'shortLink': shortLink,
                }
            }
        else:
            logging.error(response.json()['code'])
            return {
                'status': -4,
                'data': 'Failed to get video info, please inquire bili status codes to get help'
            }

    def getDynamicInfo(self, dynamic_id):
        dynamicUrl = 'https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/get_dynamic_detail?dynamic_id={}'.format(dynamic_id)
        response = requests.get(dynamicUrl).json()
        # logging.info(response)

        # image dynamic
        if response['data']['card']['desc']['type'] == 2:
            if response['code'] == 0:
                desc = response['data']['card']['desc']
                uname = desc['user_profile']['info']['uname']
                card = response['data']['card']['card']
                uid = desc['uid']
                view = desc['view']
                repost = desc['repost']
                comment = desc['comment']
                like = desc['like']
                timestamp = time.strftime("%Y-%m-%d %H:%M", time.localtime(desc['timestamp']))
                card = json.loads(card)
                pictures = card['item']['pictures']
                imageList = []
                for image in pictures:
                    imageList.append(image['img_src'])
                content = card['item']['description']
                return {
                    'status': 0,
                    'type': 2,
                    'data': {
                        'uid': uid,
                        'uname': uname,
                        'view': view,
                        'repost': repost,
                        'comment': comment,
                        'like': like,
                        'time': timestamp,
                        'content': content,
                        'imageList': imageList
                    }
                }
            else:
                return {
                    'status': -4,
                    'data': response['code']
                    }
        
        # word dynamic
        elif response['data']['card']['desc']['type'] == 4:
            if response['code'] == 0:
                desc = response['data']['card']['desc']
                uname = desc['user_profile']['info']['uname']
                card = response['data']['card']['card']
                uid = desc['uid']
                view = desc['view']
                repost = desc['repost']
                comment = desc['comment']
                like = desc['like']
                timestamp = time.strftime("%Y-%m-%d %H:%M", time.localtime(desc['timestamp']))
                card = json.loads(card)
                content = card['item']['content']
                return {
                    'status': 0,
                    'type': 4,
                    'data': {
                        'uid': uid,
                        'uname': uname,
                        'view': view,
                        'repost': repost,
                        'comment': comment,
                        'like': like,
                        'time': timestamp,
                        'content': content
                    }
                }
            else:
                return {
                    'status': -4,
                    'data': response['code']
                    }

        else:
            return {'status': -1, 'result': '该动态类型未完善'}

if __name__ == '__main__':
    paib = Bili()
    # a = paib.getDynamicInfo('594877314370747257')##627795919422504831
    # a = paib.getDynamicInfo('627795919422504831')#631421997174226993#
    a = paib.biliVideoInfo('av706')
    print(a)


    