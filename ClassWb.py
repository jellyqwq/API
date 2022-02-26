# -*- coding: utf-8 -*-

import requests
import time
import logging
logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)

class Weibo(object):
    def __init__(self):
        self.headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.3"
        }
    
    def getHotWord(self):
        r = requests.get('https://weibo.com/ajax/side/hotSearch')
        r.encoding = 'utf-8'
        data = r.json()['data']
        hotgov = data['hotgov']
        HotWordLsit = [['Top', hotgov['word'], hotgov['icon_desc']]]
        realtime = data['realtime']
        num = 1
        HotWordTime = time.strftime("%a %b %d %H:%M:%S %Y", time.localtime(time.time()))
        for hot_dict in realtime:
            if 'label_name' in hot_dict.keys():
                HotWordLsit.append([str(num), hot_dict['word'], hot_dict['label_name']])
                num += 1
        message = HotWordTime
        for i in HotWordLsit:
                message += '\n'
                message += i[0]
                message += '.'
                message += i[1]
                message += '\t'
                message += i[2]
        return {
            'status': 0,
            'data': message
        }

if __name__ == '__main__':
    pass
    # paih = HotSearch()
    # paih.WEI_BO_HOT_SEARCH()