# -*- coding: utf-8 -*-
import flask
import json

# project supposed
# https://flask.palletsprojects.com/en/2.0.x/quickstart/
api = flask.Flask(__name__)

@api.route('/bili/hotword', methods=['GET'])
def hotword():
    from ClassBili import Bili
    b = Bili()
    return json.dumps(b.getHotWord())

@api.route('/bili/shortlink', methods=['POST'])
def shortlink():
    from ClassBili import Bili
    b = Bili()
    url =  flask.request.args.get('url')
    if url:
        r = b.toBiliShortUrl(url)
        if r['status'] == 0:
            return {
                'status': 0,
                'data': r['data']
            }
        else:
            return {
                'status': -1,
                'data': r['data']
            }
    else:
        return {
            'status': -2,
            'data': 'Post paramenter can not null'
        }
if __name__ == '__main__':
    api.run(port=6702, debug=True, host='127.0.0.1')