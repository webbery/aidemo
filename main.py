import json

config = None
with open("./config.json",'r') as load_f:
    config = json.load(load_f)

from bottle import route, run, template,hook,post,request
import sys 
sys.path.append("./algorithm") 
from algorithm.train import process_news

@route('/')
def automaton():
    return template("automaton_page.tpl",{'title':'hello world'})

@hook('before_request')
def validate():
    """使用勾子处理页面或接口访问事件"""
    if request.method == 'POST' and request.POST.get('_method'):
        request.environ['REQUEST_METHOD'] = request.POST.get('_method', '').upper()
        if request.POST.get('_form'):
            request.environ['REQUEST_FORM'] = request.POST.get('_form', '')

@post('/automaton/summary')
def sign():
    lines =request.body.readlines()
    news = ''
    for line in lines:
        doc = str(line, encoding = "utf-8")
        news += doc
        print( doc )
    result = process_news(news)
    return {"summary":[
        {"speaker": item[0],"content":item[1]} for item in result
    ]}

run(host='0.0.0.0', port=config['port'], debug=False)