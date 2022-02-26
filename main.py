# -*- coding: utf-8 -*-
import flask
import json

api = flask.Flask(__name__)

@api.route('/bhot', methods=['GET', 'POST'])
def bhot():
    from ClassBili import Bili
    b = Bili()
    return json.dumps(b.getHotWord())

if __name__ == '__main__':
    api.run(port=6666, debug=True, host='127.0.0.1')