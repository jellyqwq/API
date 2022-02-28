# -*- coding: utf-8 -*-

import asyncio
import websockets
import json
import logging
import requests

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)

# 自定义模块
from ClassBili import Bili
from ClassRegular import Regular
from ClassFenCi import FenCi
# from ClassWeiBo import Weibo

class Robot(object):
    def __init__(self, websocket, loop):
        # self._groupId =  gid
        self.websockets = websocket
        self.loop = loop

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



loop = asyncio.get_event_loop()

async def echo(websocket, path):
    pair = Regular()
    robot = Robot(websocket, loop)
    paib = Bili()
    while websocket.open:
        message = await websocket.recv()
        # 将原始字符串json加载成字典形式
        message = json.loads(message)
        if 'group_id' in message.keys():
            # 过滤群组 不过滤就直接not in
            if message['group_id'] in [980514385,649451770]: #980514385,649451770
                gid = message['group_id']
                # test code
                try:
                    logging.info(message['message'])
                except:
                    logging.info(message)
                
                

                keyWords = ['Paimon', 'paimon', '派蒙']
                for word in keyWords:
                    if word in message['message']:
                        if '功能' in message['message']:
                            await robot.sendMessage('有什么感兴趣的功能吗?\n1.热搜d=====(￣▽￣*)b\n2.b站视链展示(。・∀・)ノ\n3.GitHub:https://github.com/jellyqwq/Paimon\n[CQ:image,file={}]'.format('https://i0.hdslb.com/bfs/article/1fbf0b10c5bf4fc324fbf7a53e42600982e9a382.gif'),gid)
                            break
                        elif '应急' in message['message'] or '食品' in message['message']:
                            await robot.sendMessage('欸,派蒙不是吃的\n[CQ:image,file={}]'.format('https://i0.hdslb.com/bfs/article/d0ce4f650c8a398fe5ff2e1a5705e59d24ba8091.jpg'), gid)
                            break
                        elif '恰饭' in message['message'] or '吃饭' in message['message']:
                            await robot.sendMessage('好耶开饭咯,我要吃甜甜花酿鸡\n[CQ:image,file={}]'.format('https://i0.hdslb.com/bfs/article/2d07fbb5269025d3690186164a50cd0f6b9127a6.gif'), gid)
                            break
                        elif '派蒙' == message['message']:
                            await robot.sendMessage('你好!\n[CQ:image,file={}]'.format('https://i0.hdslb.com/bfs/article/1aee0e5e99ff1b17f68203f383b4b040c2f0f06c.gif'), gid)
                            break
                        else:
                            await robot.sendMessage('前面的区域,以后再来探索吧', gid)
                            break
                
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

                # 域名过滤
                if 'bilibili.com' in message['message']:
                    if 't.bilibili.com' in message['message']:
                        result = pair.biliDynamicId(message['message'])
                        if result['status'] == 0:
                            result = paib.getDynamicInfo(result['result'])
                            await robot.sendMessage('{}\n{}'.format(result['uname'], result['description']), gid)
                            for picture in result['imageList']:
                                await robot.sendImage(picture, gid)
                        elif result['status'] == -1:
                            await robot.sendMessage(result['result'], gid)

                    elif 'bilibili.com/video' in message['message']:
                        result = pair.biliVideoUrl(message['message'])
                        if result['status'] == 0:
                            result = paib.biliVideoInfo(result['result'])
                            if result['status'] == 0:
                                await robot.sendMessage(result['result'], gid)
                            else:
                                await robot.sendMessage(result['status'], gid)
                        elif result['status'] == -1:
                            await robot.sendMessage(result['result'], gid)
        

                if 'b23.tv' in message['message']:
                    # 从消息中取出url
                    result = pair.biliShortUrl(message['message'])
                    if result['status'] == 0:
                        # 视频链接匹配
                        if 'bilibili.com/video' in result['result']:
                            result = pair.biliVideoUrl(result['result'])
                            logging.info('p129')
                            if result['status'] == 0:
                                result = paib.biliVideoInfo(result['result'])
                                logging.info(result)
                                if result['status'] == 0:
                                    await robot.sendMessage(result['result'], gid)
                                else:
                                    await robot.sendMessage(result['status'], gid)
                            elif result['status'] == -1:
                                await robot.sendMessage(result['result'], gid)

                        # 动态链接匹配
                        elif 'm.bilibili.com' in result['result']:
                            result = pair.biliDynamicId(result['result'])
                            if result['status'] == 0:
                                result = paib.getDynamicInfo(result['result'])
                                await robot.sendMessage('{}\n{}'.format(result['uname'], result['description']), gid)
                                for picture in result['imageList']:
                                    await robot.sendImage(picture, gid)
                            elif result['status'] == -1:
                                await robot.sendMessage(result['result'], gid)
                    elif result['status'] == -1:
                        await robot.sendMessage(result['result'], gid)

                # b站热搜
                if 'bhot' == message['message']:
                    await robot.sendMessage('b站热搜来咯~（。＾▽＾）',gid)
                    await robot.sendMessage(requests.get('http://api.jellyqwq.com:6702/bili/hotword').json()['data'],gid)
                
                # 微博热搜
                if 'whot' == message['message']:
                    await robot.sendMessage('微博热搜来咯~（。＾▽＾）',gid)
                    await robot.sendMessage(requests.get('http://api.jellyqwq.com:6702/weibo/hotword').json()['data'],gid)
                    
                    

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