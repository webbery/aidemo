from bottle import route, run, template

@route('/automaton')
def automaton():
    return template("automaton_page.tpl",{'title':'hello world'})

run(host='localhost', port=8080, debug=True)