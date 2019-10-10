import json

config = None
with open("./config.json",'r') as load_f:
    config = json.load(load_f)

from flask import Flask,request,jsonify
app = Flask(__name__)

import sys 
sys.path.append("./algorithm") 
from algorithm.train import process_news

# 跨域支持
def after_request(resp):
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@app.route('/',methods=['GET'])
def index():
    return "hello world"

@app.route('/automaton/viewpoint',methods=['POST','GET'])
def viewpoint():
    #news =request.get_data().decode('utf-8')
    news = request.args.get('news')
    try:
        result = process_news(news)
        return jsonify({"viewpoint":[
            {"speaker": item[0],"content":item[1]} for item in result
        ]})
    except:
        return ""

app.after_request(after_request)
#app.run(host='0.0.0.0', port=config['port'], debug=False)
app.run(host='0.0.0.0', port=config['port'], debug=False, ssl_context=('server.crt','server.key'))

