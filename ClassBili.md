### getHotWord

#### API Description  
> get bilibili hot words

#### Request URL  
> [http://127.0.0.1:6702/bili/bhot](http://127.0.0.1:6702/bili/bhot)

#### Request Format  
> None

#### Request Method  
> GET

#### Request Headers  
> None  

#### Response Format  
> json 

#### Response Paramenter

|variable name|format|example|description|
|-|-|-|-|
|status|int|0|status code|
|data|string|xxxxx|message|

#### Code Example
```json
{
    "status": 0,
    "data": "xxxxx"
}
```

***

### toBiliShortUrl

#### API Description
> bili url transform a short link 

#### Request URL
> [http://127.0.0.1:6702/bili/shortlink?url=](http://127.0.0.1:6702/bili/shortlink)

#### Request Format  
> URL

#### Request Method
> GET

#### Request Headers  
> None 

#### Response Format  
> json 

#### Request Paramenter

|variable name|format|example|description|
|-|-|-|-|
|url|string|https://xxx.bilibili.com/xxx|url belong bilibili domain|

#### Code Example
```
http://127.0.0.1:6702/bili/shortlink?url=https://xxx.bilibili.com/xxx
```
#### Response Paramenter

|variable name|format|example|description|
|-|-|-|-|
|status|int|0|status code|
|data|string|"https://b23.tv/xxxx"|message|

#### Code Example
```json
{
    "status": 0,
    "data": "https://b23.tv/xxxx",
}
```

***

### biliVideoInfo

#### API Description
> get bili video information

#### Request URL
> [http://127.0.0.1:6702/bili/videoinfo?abcode=](http://127.0.0.1:6702/bili/videoinfo)

#### Request Format  
> URL

#### Request Method
> GET

#### Request Headers  
> None  

#### Response Format  
> json 

#### Request Paramenter

|variable name|format|example|description|
|-|-|-|-|
|abcode|string|av706|av(AV) or bv(BV) code|

#### Code Example
```
http://127.0.0.1:6702/bili/videoinfo?abcode=av706
```

#### Response Paramenter

|variable name|format|example|description|
|-|-|-|-|
|status|int|0|status code|
|data|dict||As follows|
|aid|num|706||
|bvid|string|"BV1xx411c79H"||
|face|string|"http://i1.hdslb.com/bfs/archive/753453a776fca838165a52c7511e8557857b61ea.jpg"|video face image|
|title|string|"【東方】Bad Apple!! ＰＶ【影絵】', 'd Apple!! ＰＶ【影絵】"||
|desc|string|"sm8628149 2011/9/25追记：大家如果看到空耳字幕请果断举报，净化弹幕环境，你我有责，感谢。"|description|
|view|num|7767392||
|danmaku|num|76512||
|reply|num|335009||
|favorite|num|397892||
|coin|num|139095||
|share|num|61841||
|like|num|300976||
|shortLike|dict||As follows|
|status|num|0||
|data|string|"https://b23.tv/kucPLME"|short link|

#### Code Example
```json
{
    "status": 0,
    "data": {
        "aid": 706,
        "bvid": "BV1xx411c79H",
        "face": "http://i1.hdslb.com/bfs/archive/753453a776fca838165a52c7511e8557857b61ea.jpg",
        "title": "【東方】Bad Apple!! ＰＶ【影絵】",
        "desc": "sm8628149 2011/9/25追记：大家如果看到空耳字幕请果断举报，净化弹幕环境，你我有责，感谢。",
        "view": 7767392,
        "danmaku": 76512,
        "reply": 335009,
        "favorite": 397892,
        "coin": "139095",
        "share": 61841,
        "like": 300976,
        "shortLink": {
            "status": 0,
            "data": "https://b23.tv/kucPLME"
        }
    }
}
```

***

### getDynamicInfo

#### API Description
> get bili dynamic information

#### Request URL
> [http://127.0.0.1:6702/bili/dynamicinfo?id=](http://127.0.0.1:6702/bili/dynamicinfo?id=)

#### Request Format  
> URL

#### Request Method
> GET

#### Request Headers  
> None  

#### Response Format  
> json 

#### Request Paramenter

|variable name|format|example|description|
|-|-|-|-|
|id|num|627795919422504831|dynamic id|

#### Code Example
```
http://127.0.0.1:6702/bili/dynamicinfo?id=627795919422504831
```

#### Response Paramenter

|variable name|format|description|
|-|-|-|
|status|int|status code|
|type|num|[dynamic type](#dynamic-type)|
|data|obj|[dynamic data](#dynamic-data)|

#### Dynamic type

|dynamic type|description|
|-|-|
|1|repost|
|2|image dynamic|
|4|word dynamic|

#### Dynamic data

|variable name|format|description|
|-|-|-|
|uid|num|up id|
|uname|string|up name|
|view|num||
|repost|num||
|comment|num||
|like|num||
|time|string||
|content|string||
|imageList|list|Appears only with pictures|

#### Code Example

```json
{
    "status": 0, 
    "type": 2, 
    "data": {
        "uid": 1042854135, 
        "uname": "ShizukouOfficial", 
        "view": 76598, 
        "repost": 15, 
        "comment": 202, 
        "like": 3286, 
        "time": "2022-02-16 18:48", 
        "content": "I became 狮子!! ", 
        "imageList": ["https://i0.hdslb.com/bfs/album/64c2d68a6fcd89ae1a97d960a72742442dde8bbd.png"]
    }
}
```