# Paimon API  

## All standard status codes in this project  

| status code   | means                 |
|---------------|-----------------------|
|0              |request success        |
|-1             |request failure        |

## Response structure in this project

- [ClassBili](/ClassBili.py)
    - [toBiliShortUrl](/ClassBili.py#L28)
    - [biliVideoInfo](/ClassBili.py#)


## API documentation

### 127.0.0.1:6702/bili/bhot  
description: get bilibili hot search  
method: get  
response data(json)  

|variable name|format|example|description|
|----------|-----------|---------|-----|
|status|int|0|status code|
|result|string|'xxxxx'|message|

code case
```
{
'status': 0,
'result': 'xxxxx'
}
```

