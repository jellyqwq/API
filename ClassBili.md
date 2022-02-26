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
|data|string|'xxxxx'|message|

#### Code Example
```
{
'status': 0,
'data': 'xxxxx'
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
|url|string|'https://xxx.bilibili.com/xxx'|url belong bilibili domain|

#### Code Example
```
{
    'url': 'https://xxx.bilibili.com/xxx'
}
```
#### Response Paramenter

|variable name|format|example|description|
|-|-|-|-|
|status|int|0|status code|
|data|string|'https://b23.tv/xxxx'|message|

#### Code Example
```
{
    'status': 0,
    'data': 'https://b23.tv/xxxx',
}
```