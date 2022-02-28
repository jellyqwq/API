# -*- coding: utf-8 -*-
import flask
import json

# project supposed
# https://flask.palletsprojects.com/en/2.0.x/quickstart/
api = flask.Flask(__name__)

@api.route('/bili/hotword', methods=['GET'])
def hotword():
    from ClassBili import Bili
    return json.dumps(Bili().getHotWord(), ensure_ascii=False)

@api.route('/bili/shortlink', methods=['get'])
def shortlink():
    from ClassBili import Bili
    url =  flask.request.values.get('url')
    if url:
        r = Bili().toBiliShortUrl(url)
        if r['status'] == 0:
            x = {
                'status': 0,
                'data': r['data']
            }
            return json.dumps(x, ensure_ascii=False)
        else:
            x = {
                'status': -1,
                'data': r['data']
            }
            return json.dumps(x, ensure_ascii=False)
    else:
        x = {
            'status': -2,
            'data': 'Post paramenter can not null'
        }
        return json.dumps(x, ensure_ascii=False)

@api.route('/bili/videoinfo', methods=['GET'])
def videoinfo():
    from ClassBili import Bili
    abcode =  flask.request.values.get('abcode')
    return json.dumps(Bili().biliVideoInfo(abcode), ensure_ascii=False)

@api.route('/bili/dynamicinfo', methods=['GET'])
def dynamicinfo():
    from ClassBili import Bili
    did = flask.request.values.get('id')
    return json.dumps(Bili().getDynamicInfo(did), ensure_ascii=False)

@api.route('/weibo/hotword', methods=['GET'])
def wbhotword():
    from ClassWeiBo import Weibo
    return json.dumps(Weibo().getHotWord(), ensure_ascii=False)

@api.route('/parse/abcode', methods=['GET'])
def parse_abcode():
    from ClassRegular import Regular
    url = flask.request.values.get('url')
    return json.dumps(Regular().biliVideoUrl(url), ensure_ascii=False)

@api.route('/parse/b23', methods=['GET'])
def parse_b23():
    from ClassRegular import Regular
    url = flask.request.values.get('url')
    return json.dumps(Regular().biliShortUrl(url), ensure_ascii=False)



if __name__ == '__main__':
    api.run(port=6702, debug=True, host='127.0.0.1')