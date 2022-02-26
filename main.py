# -*- coding: utf-8 -*-
from flask import Flask
import json

api = Flask(__name__)

@api.route('/bhot', methods=['GET', 'POST'])
def bhot():
    from ClassBili import Bili
    b = Bili()
    return json.dumps(b.getHotWord())

if __name__ == '__main__':
    api.run(port=6666, debug=True, host='127.0.0.1')