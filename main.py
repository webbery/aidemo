import json

config = None
with open("./config.json",'r') as load_f:
    config = json.load(load_f)

from flask import Flask,request,jsonify
from flask import render_template
app = Flask(__name__)

import sys 
sys.path.append("./algorithm") 
import urllib
import algorithm.tools.dom_tree as dtree
# from algorithm.opinion_extraction.interface import process_news
# from algorithm.summarization_extraction.interface import get_abstract
# from algorithm.subway import search
# from algorithm.comments_classify.interface import classify_comment

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
    return render_template("subway.html")

@app.route('/aidemo/comments_classify',methods=['GET'])
def get_classify():
    return render_template("comments_classify.html")

@app.route('/aidemo/history',methods=['GET'])
def get_history():
    return render_template("arguments_history.html")

@app.route('/apis/viewpoint',methods=['POST'])
def viewpoint():
    news =request.get_data().decode('utf-8')
    # news = request.args.get('news')
    print('/viewpoint',news)
    try:
        result = process_news(news)
        return jsonify({"viewpoint":[
            {"speaker": item[0],"content":item[1],"postags":item[2]} for item in result
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
    condition = urllib.parse.parse_qs(query)
    result = search(condition['src'][0],condition['to'][0],int(condition['type'][0]))
    return jsonify(result)

@app.route('/apis/classify',methods=['POST'])
def on_classify_comment():
    comment = request.get_data().decode('utf-8')
    print('/classify',comment)
    try:
        result = classify_comment(comment)
        return jsonify({"classes":result.tolist(),"result":status_code['success']})
    except Exception as e:
        return jsonify({"result":status_code['fail'],"message":str(e)})

@app.route('/tools/domtree',methods=['GET'])
def get_domtree():
     return render_template("domtree.html")

@app.route('/apis/tools/domtree',methods=['POST','GET'])
def parse_dom():
    html = request.get_data().decode('utf-8')
    try:
        dt = dtree.DomTree()
        result = dt.parse(html)
        return jsonify({"tree":result,"result":status_code['success']})
    except Exception as e:
        return jsonify({"result":status_code['fail'],"message":str(e)})

app.after_request(after_request)
app.run(host='0.0.0.0', port=config['port'], debug=False)

