import json

config = None
with open("./config.json",'r') as load_f:
    config = json.load(load_f)

from flask import Flask,request,jsonify
from flask import render_template
app = Flask(__name__)

import sys 
sys.path.append("./algorithm") 
from algorithm.opinion_extraction.interface import process_news
from algorithm.summarization_extraction.interface import get_abstract
from algorithm.subway import search

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

@app.route('/apis/viewpoint',methods=['POST'])
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

@app.route('/apis/summarization',methods=['POST'])
def summatization():
    news =request.get_data().decode('utf-8')
    try:
        abstract = get_abstract(news)
        return jsonify({"abstract":abstract,"result":status_code['success']})
    except Exception as e:
        #msg = bytes(str(e), encoding = 'utf-8')
        return jsonify({"result":status_code['fail'],"message":str(e)})

@app.route('/apis/subway',methods=['POST'])
def find_road():
    query = request.get_data().decode('utf-8')
    result = search(query.from,query.to,query.type)
    return jsonify(result)

app.after_request(after_request)
app.run(host='0.0.0.0', port=config['port'], debug=False)

