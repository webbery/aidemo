import json

config = None
with open("./config.json",'r') as load_f:
    config = json.load(load_f)

from flask import Flask,request,jsonify
from flask import render_template
app = Flask(__name__)

import sys 
sys.path.append("./algorithm") 
# from algorithm.opinion_extraction.interface import process_news
from algorithm.summarization_extraction.interface import get_abstract

status_code = {
    'success': 0,
    'fail': -1
}

# 跨域支持
def after_request(resp):
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@app.route('/',methods=['GET'])
def get_index():
    return render_template("index.html")

@app.route('/aidemo/pointview',methods=['GET'])
def get_pointview():
    return render_template("pointview.html")

@app.route('/aidemo/summarization',methods=['GET'])
def get_summarization():
    return render_template("summarization.html")

@app.route('/aidemo/subway',methods=['GET'])
def get_subway():
    return render_template("summarization.html")

@app.route('/apis/viewpoint',methods=['POST','GET'])
def viewpoint():
    news =request.get_data().decode('utf-8')
    # news = request.args.get('news')
    try:
        result = process_news(news)
        return jsonify({"viewpoint":[
            {"speaker": item[0],"content":item[1]} for item in result
        ],"result":status_code['success']})
    except:
        return jsonify({"result":status_code['fail']})

@app.route('/apis/summatization',methods=['POST','GET'])
def summatization():
    news =request.get_data().decode('utf-8')
    try:
        abstract = get_abstract(news)
        return jsonify({"abstract":abstract,"result":status_code['success']})
    except:
        return jsonify({"result":status_code['fail']})

app.after_request(after_request)
app.run(host='0.0.0.0', port=config['port'], debug=False)
# app.run(host='0.0.0.0', port=config['port'], debug=False, ssl_context=('server.crt','server.key'))

