# -*- coding: utf-8 -*-

import asyncio
import collections
import json
import logging
import re

import requests
import websockets

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)

class Robot(object):
    def __init__(self, websocket, loop):
        self.websockets = websocket
        self.loop = loop
        self.GNAME_TO_GID = {
                'nmg': '649451770',
                'qwq': '980514385',
                'ys': '130516740',
                'gal': '605650659',
                }
        self.IMAGE_CACHE_DICT = collections.OrderedDict()

    # 发送消息
    async def sendMessage(self, m, group_id):
        await self.websockets.send(
            json.dumps(
                {
                    "action": "send_group_msg",
                    "params": {
                        "group_id" : group_id,
                        'message': m
                    }
                }
            )
        )
    
    # 发送图片
    async def sendImage(self, url, group_id):
        await self.websockets.send(
            json.dumps(
                {
                    "action": "send_group_msg",
                    "params": {
                        "group_id" : group_id,
                        'message': '[CQ:image,file={}]'.format(url)
                    }
                }
            )
        )
    
    async def getMessage(self, mid):
        await self.websockets.send(
            json.dumps(
                {
                    "action": "get_msg",
                    "params": {
                        "message_id": int(mid),
                    }
                }
            )
        )
        return json.loads(await self.websockets.recv())
    
    # @https://github.com/MeteorsLiu/PyBot
    async def atri_sendImage(self, b64, group_id):
        await self.websockets.send(
            json.dumps(
                {
                    "action": "send_msg", 
                    "params": {
                        "group_id": group_id,
                        "message": "[CQ:image,file=base64://{}]".format(b64)
                    }
                }
            )
        )
    
    # 获取图片 https://github.com/MeteorsLiu/PyBot/blob/1159e0f66052f382782d66d2ec2c1f888b40f386/startbot.py#L211
    async def sendPicture(self, name, num, gid):
        try:
            message = requests.get("http://172.30.56.22:6700/getpin?name={}&num={}".format(name, num)).json()
        except:
            await self.sendMessage("关键词{}无法查找".format(name), gid)
        if "error" in message:
            await self.sendMessage(message["error"], gid)
        for m in message:
            await self.atri_sendImage(m, gid)

    # b站的信息转发模块
    async def sendBiliMessage(self, message, gid):
        # 当动态域名在消息中
        if 't.bilibili.com' in message or 'm.bilibili.com' in message:
            i = requests.get('http://api.jellyqwq.com:6702/parse/bdynamci?message={}'.format(message)).json()
            if i['status'] == 0:
                info = requests.get('http://api.jellyqwq.com:6702/bili/dynamicinfo?id={}'.format(i['data'])).json()
                # 判断请求处理状态
                if info['status'] == 0:
                    data = info['data']
                    # 动态基本消息模板
                    if info['type'] in [2,4]:
                        # 发布时间,up名字
                        await self.sendMessage('时间:{}\nUP:{}'.format(data['time'],data['uname']), gid)
                        await self.sendMessage('内容:{}\n\n浏览:{} 转发:{}\n评论:{} 点赞{}'.format(data['content'], data['view'], data['repost'], data['comment'], data['like']), gid)
                    
                    # 2类型动态有图片列表,调用发图
                    if info['type'] in [2]:
                        for picture in data['imageList']:
                            await self.sendImage(picture, gid)
                else:
                    await self.sendMessage(info['data'], gid)
            else:
                await self.sendMessage(i['data'], gid)

        # https://www.bilibili.com/video/BV1db4y1e7B2
        # 当视频链接存在于b站域名下时
        elif 'bilibili.com/video' in message:
            r = requests.get('http://api.jellyqwq.com:6702/parse/abcode?message={}'.format(message)).json()
            if r['status'] == 0:
                info = requests.get('http://api.jellyqwq.com:6702/bili/videoinfo?abcode={}'.format(r['data'])).json()
                if info['status'] == 0:
                    data = info['data']
                    await self.sendMessage('标题:{}\n作者:{}\n\n简介:{}'.format(data['title'], data['uname'], data['desc']), gid)
                    await self.sendMessage('评论:{} 弹幕:{}\n硬币:{} 收藏:{}\n点赞:{} 分享:{}'.format(data['reply'], data['danmaku'], data['coin'], data['favorite'], data['like'], data['share']), gid)
                    await self.sendMessage('[CQ:image,file={}]\n播放量:{}\n传送门->{}'.format(data['face'], data['view'], data['shortLink']['data']), gid)
                else:
                    await self.sendMessage(info['data'], gid)
            else:
                await self.sendMessage(r['data'], gid)
        
    async def sendB23Message(self, message, gid):
        r = requests.get('http://api.jellyqwq.com:6702/parse/b23?message={}'.format(message)).json()
        if r['status'] == 0:
            if 'bilibili.com' in r['data']:
                await self.sendBiliMessage(r['data'], gid)
            else:
                await self.sendMessage(r['data'], gid)
        else:
            await self.sendMessage(r['data'], gid)
    
    async def sendPaimonMessage(self, message, gid):
        if '功能' in message:
            await self.sendMessage('有什么感兴趣的功能吗?\n1.热搜d=====(￣▽￣*)b\n2.b站视链展示(。・∀・)ノ\n3.GitHub:https://github.com/jellyqwq/Paimon\n[CQ:image,file={}]'.format('https://i0.hdslb.com/bfs/article/1fbf0b10c5bf4fc324fbf7a53e42600982e9a382.gif'),gid)
        elif '派蒙图库' in message:
            # 派蒙图库#nmg
            if '派蒙图库#' in message:
                await self.sendMessage(requests.get('http://api.jellyqwq.com:6702/parse/cqimginfo?gid={}&groupname={}'.format(gid, message[5:])).json()['data'], gid)
            elif '派蒙图库' == message:
                await self.sendMessage(requests.get('http://api.jellyqwq.com:6702/parse/getgroupinfo').json()['data'], gid)
        elif '图' in message:
            dict_replace = {
                '一': '1',
                '俩': '2',
                '两': '2',
                '几': '3',
                '三': '3',
                '四': '4',
                '五': '5',
                '六': '6',
                '七': '7',
                '八': '8',
                '九': '9',
                '十': '10'
            }
            for i in dict_replace.keys():
                if i in message:
                    message = message.replace(i, dict_replace[i])
            num = re.findall(r'([0-9]+)张', message)
            if num != []:
                num = num[0]
                if int(num) <= 10:
                    num = str(num)
                else:
                    num = '1'
            else:
                num = '1'
            
            lock = False
            for n in self.GNAME_TO_GID.keys():
                if n in message:
                    searchgid = self.GNAME_TO_GID[n]
                    lock = True
                    break
                else:
                    pass
            if lock == True:
                searchgid = self.GNAME_TO_GID[n]
            else:
                searchgid = gid
            r = requests.get('http://api.jellyqwq.com:6702/parse/getcqimage?gid={}&num={}'.format(searchgid, num)).json()
            if r['status'] == 0:

                # 缓存写入部分
                MAX_CACHE_NUM = 50
                temp_dict = self.IMAGE_CACHE_DICT.copy()
                while True:
                    if MAX_CACHE_NUM - len(self.IMAGE_CACHE_DICT) >= len(r['data']):
                        data = r['data']
                        for i in data.keys():
                            l = data[i]
                            # {hash:path,...}
                            self.IMAGE_CACHE_DICT[i] = l[1]
                            # self.IMAGE_CACHE_DICT[i] = [l[1], l[2]]
                        break
                    else:
                        pop_num = len(r['data']) - (MAX_CACHE_NUM - len(self.IMAGE_CACHE_DICT))
                        for i in temp_dict.keys():
                            if pop_num == 0:
                                break
                            else:
                                self.IMAGE_CACHE_DICT.pop(i)
                                pop_num -= 1
                
                # 发图
                for image in r['data'].values():
                    await self.sendImage(image[0], gid)
            else:
                await self.sendMessage(r['data'], gid)
        elif '应急' in message or '食品' in message:
            await self.sendMessage('欸,派蒙不是吃的\n[CQ:image,file={}]'.format('https://i0.hdslb.com/bfs/article/d0ce4f650c8a398fe5ff2e1a5705e59d24ba8091.jpg'), gid)
        elif '恰饭' in message or '吃饭' in message:
            await self.sendMessage('好耶开饭咯,我要吃甜甜花酿鸡\n[CQ:image,file={}]'.format('https://i0.hdslb.com/bfs/article/2d07fbb5269025d3690186164a50cd0f6b9127a6.gif'), gid) 
        elif '派蒙' == message:
            await self.sendMessage('你好!', gid)
        else:
            await self.sendMessage('前面的区域,以后再来探索吧', gid)
    
    async def delPaimonPicture(self, message, gid):
        mid = re.findall(r'\[CQ:reply,id=(-?[0-9]+)]\[CQ:at,qq=2980293094]', message)[0]
        m = await self.getMessage(mid)
        message = m['data']['message']
        hashv = re.findall(r'https://gchat.qpic.cn/gchatpic_new/[0-9]+/[0-9]+-[0-9]+-([0-9A-Z]+)/0\?term',message)[0]
        try:
            path = self.IMAGE_CACHE_DICT[hashv]
            r = requests.get('http://api.jellyqwq.com:6702/parse/delete_image?path={}&hashv={}'.format(path, hashv)).json()
            self.IMAGE_CACHE_DICT.pop(hashv)
            await self.sendMessage(r['data'], gid)
        except:
            await self.sendMessage('删穷水尽', gid)

loop = asyncio.get_event_loop()

async def echo(websocket, path):
    robot = Robot(websocket, loop)
    while websocket.open:
        message = await websocket.recv()
        # 将原始字符串json加载成字典形式
        message = json.loads(message)
        if 'group_id' in message.keys():
            try:
                if message['group_id']:
                    gid = message['group_id']
                if 'CQ:image' in message['message']:
                    requests.get('http://api.jellyqwq.com:6702/parse/savecqimgurl?message={}&gid={}'.format(message['message'], gid)).json()
            except:
                pass
            
            if message['group_id'] in [980514385,649451770]:
                gid = message['group_id']
                try:
                    logging.info(message['message'])
                except:
                    logging.info(message)
                else:  
                    # atri pixiv model
                    if 'paipi' == message['message'][:5]:
                        try:
                            search = message['message'][5:].split('#')
                            name = search[0]
                            num = int(search[1])
                        except:
                            await robot.sendMessage('解析失败', gid)
                        else:
                            if num <= 5:
                                await robot.sendPicture(name, num, gid)
                            else:
                                await robot.sendMessage('图片过多', gid)
                    
                    if 'bilibili.com' in message['message']:
                        await robot.sendBiliMessage(message['message'], gid)

                    if 'b23.tv' in message['message']:
                        await robot.sendB23Message(message['message'], gid)

                    # b站热搜
                    if 'bhot' == message['message']:
                        await robot.sendMessage('b站热搜来咯~（。＾▽＾）',gid)
                        await robot.sendMessage(requests.get('http://api.jellyqwq.com:6702/bili/hotword').json()['data'],gid)
                    
                    # 微博热搜
                    if 'whot' == message['message']:
                        await robot.sendMessage('微博热搜来咯~（。＾▽＾）',gid)
                        await robot.sendMessage(requests.get('http://api.jellyqwq.com:6702/weibo/hotword').json()['data'],gid)

                    if '派蒙' in message['message']:
                        await robot.sendPaimonMessage(message['message'], gid)

                    if 'CQ:reply' in message['message'] and '[CQ:at,qq=2980293094]' in message['message'] and 'del' in message['message']:
                        await robot.delPaimonPicture(message['message'],gid)

                        
async def main():
    async with websockets.serve(echo, "127.0.0.1", 6701):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        loop.close()
    except:
        raise
