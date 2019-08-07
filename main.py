from bottle import route, run, template,hook,post,request

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
    return {"summary":[
        {"speaker":"aaaaa","content":"00000000000000"}
    ]}

run(host='localhost', port=8080, debug=True)