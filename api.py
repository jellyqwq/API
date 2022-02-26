# -*- coding: utf-8 -*-
import flask
import json

# https://cloud.tencent.com/developer/article/1738569
api = flask.Flask(__name__)

@api.route('/index', methods=['GET'])
def index():
    ren = {'msg':'成功访问首页','msg_code':200}
    return json.dumps(ren, ensure_ascii=False)

@api.route('/article', methods=['POST'])
def article():
    id = flask.request.args.get('id')

    if id:
        if id == '123456':
            ren = {'msg':'成功访问文章','msg_code':200}
        else:
            ren = {'msg':'找不到文章','msg_code':400}
    else:
        ren = {'msg':'请输入文章id参数','msg_code':-1}
    return json.dumps(ren,ensure_ascii=False)

#post入参访问方式二：from-data（k-v）格式参数
@api.route('/login',methods=['post'])
def login():
  #from-data格式参数
  usrname = flask.request.values.get('usrname')
  pwd = flask.request.values.get('pwd')
  
  if usrname and pwd:
    if usrname =='test' and pwd =='123456':
      ren = {'msg':'登录成功','msg_code':200}
    else:
      ren = {'msg':'用户名或密码错误','msg_code':-1}
  else:
    ren = {'msg':'用户名或密码为空','msg_code':1001}
  return json.dumps(ren,ensure_ascii=False)

#post入参访问方式二：josn格式参数  
@api.route('/loginjosn',methods=['post'])
def loginjosn():
  #from-data格式参数
  usrname = flask.request.json.get('usrname')
  pwd = flask.request.json.get('pwd')
  
  if usrname and pwd:
    if usrname =='test' and pwd =='123456':
      ren = {'msg':'登录成功','msg_code':200}
    else:
      ren = {'msg':'用户名或密码错误','msg_code':-1}
  else:
    ren = {'msg':'用户名或密码为空','msg_code':1001}
  return json.dumps(ren,ensure_ascii=False)

if __name__ == '__main__':
  api.run(port=8888,debug=True,host='127.0.0.1') # 启动服务
  # debug=True,改了代码后，不用重启，它会自动重启
  # 'host='127.0.0.1'别IP访问地址