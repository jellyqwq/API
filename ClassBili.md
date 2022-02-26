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
|data|string|"xxxxx"|message|

#### Code Example
```
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
> [http://127.0.0.1:6702/bili/shortlink](http://127.0.0.1:6702/bili/shortlink)

#### Request Format  
> json

#### Request Method
> POST

#### Request Headers  
> None 

#### Response Format  
> json 

#### Request Paramenter

|variable name|format|example|description|
|-|-|-|-|
|url|string|"https://xxx.bilibili.com/xxx"|url belong bilibili domain|

#### Code Example
```
{
    "url": "https://xxx.bilibili.com/xxx"
}
```
#### Response Paramenter

|variable name|format|example|description|
|-|-|-|-|
|status|int|0|status code|
|data|string|"https://b23.tv/xxxx"|message|

#### Code Example
```
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
> [http://127.0.0.1:6702/bili/videoinfo](http://127.0.0.1:6702/bili/videoinfo)

#### Request Format  
> json

#### Request Method
> POST

#### Request Headers  
> None  

#### Response Format  
> json 

#### Request Paramenter

|variable name|format|example|description|
|-|-|-|-|
|abcode|string|"av706"|av(AV) or bv(BV) code|

#### Code Example
```
{
    "abcode": "av706"
}
```

#### Response Paramenter

|variable name|format|example|description|
|-|-|-|-|
|status|int||status code|
|data|dict||As follows|
|aid|num|||
|bvid|string|||
|face|string|||
|title|string|||
|desc|string||description|
|view|num|||
|danmaku|num|||
|reply|num|||
|favorite|num|||
|coin|num|||
|share|num|||
|like|num|||
|shortLike|dict||As follows|
|status|num|||
|data|string||short link|

#### Code Example
```
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