import json

config = None
with open("./config.json",'r') as load_f:
    config = json.load(load_f)

from bottle import route, run, template,hook,post,request,response,install
import sys 
sys.path.append("./algorithm") 
from algorithm.train import process_news

@hook('before_request')
def validate():
    REQUEST_METHOD = request.environ.get('REQUEST_METHOD')

    HTTP_ACCESS_CONTROL_REQUEST_METHOD = request.environ.get('HTTP_ACCESS_CONTROL_REQUEST_METHOD')
    if REQUEST_METHOD == 'OPTIONS' and HTTP_ACCESS_CONTROL_REQUEST_METHOD:
        request.environ['REQUEST_METHOD'] = HTTP_ACCESS_CONTROL_REQUEST_METHOD

class EnableCors(object):
    name = 'enable_cors'
    api = 2

    def apply(self, fn, context):
        def _enable_cors(*args, **kwargs):
            # set CORS headers
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS'
            response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

            if bottle.request.method != 'OPTIONS':
                # actual request; reply with the actual response
                return fn(*args, **kwargs)

        return _enable_cors

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

@post('/automaton/viewpoint')
def sign():
    lines =request.body.readlines()
    news = ''
    for line in lines:
        doc = str(line, encoding = "utf-8")
        news += doc
        print( doc )
    result = process_news(news)
    return {"viewpoint":[
        {"speaker": item[0],"content":item[1]} for item in result
    ]}

install(EnableCors())
run(host='0.0.0.0', port=config['port'], debug=False)
