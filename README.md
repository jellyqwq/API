# Paimon API  

## All standard status codes in this project  

| status code   | means                 |
|---------------|-----------------------|
|0|request success|
|-1|request failure|
|-2|missing request paramenter|
|-3|abcode error|
|-4|bili error|
|-5|failed to match|

## Project structure

- [ClassBili](/ClassBili.py)
    - [getHotWord](/ClassBili.py#L28)
    - [toBiliShortUrl](/ClassBili.py#L63)
    - [biliVideoInfo](/ClassBili.py#L87)
    - [getDynamicInfo](/ClassBili.py#L141)
- [ClassRegular](/ClassRegular.py)
    - [biliVideoUrl](/ClassRegular.py#L12)

## API documentation

- [/bili](/ClassBili.md)
    - [x] [/hotword](/ClassBili.md#gethotword)获取b站热搜
    - [x] [/shortlink?url=](/ClassBili.md#toBiliShortUrl)生成b站短链
    - [x] [/videoinfo?abcode=](/ClassBili.md#biliVideoInfo)通过abcode获取视频信息
    - [x] [/dynamicinfo?id=](/ClassBili.md#getDynamicInfo)通过动态id获取动态信息
- [/weibo](/ClassWeiBo.md)
    - [x] [/hotword](/ClassWeiBo.md#gethotword)获取微博热搜
- [/parse]
    - [x] [/abcode?url=]将b站域名下的视频url提取av或bv号
    - [x] [/b23?url=]将b23.tv域名下的重定向地址返回

