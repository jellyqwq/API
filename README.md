# Paimon API  

## All standard status codes in this project  

| status code   | means                 |
|---------------|-----------------------|
|0              |request success        |
|-1             |request failure        |

## Response structure in this project

├ [ClassBili](/ClassBili.py)
    - [getHotWord](/ClassBili.py#L28)
    - [biliVideoInfo](/ClassBili.py#)


## API documentation

### getHotWord

#### API Description  
> get bilibili hot words

#### Request URL  
> [http://127.0.0.1:6702/bili/bhot](http://127.0.0.1:6702/bili/bhot)

#### Request format  
> None

#### Request Method  
> GET

#### Request Headers  
> None  

#### Response format  
> json 

#### Response

|variable name|format|example|description|
|-|-|-|-|
|status|int|0|status code|
|result|string|'xxxxx'|message|

#### code case
```
{
'status': 0,
'result': 'xxxxx'
}
```

