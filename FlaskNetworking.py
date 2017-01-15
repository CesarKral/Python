import os, datetime, json, requests
from pymongo import MongoClient
from flask import Flask, flash, url_for, render_template, request, redirect, make_response, session

app = Flask(__name__)

@app.route('/')
def hello_world():
    return "Hello World"

@app.route('/xx/<username>')
def user(username):
    return 'Hello %s' % username

@app.route('/xx/<int:number>')
def insertNumber(number):
    return 'The number is %s' % number

@app.route('/xx/<float:number>')
def insertFloatNumber(number):
    return 'The floating point number is %s' % number

@app.route('/hello')
def hello():
    return redirect(url_for('user', username='Isabel'))

@app.route('/a')
def a():
    return render_template('a.html', name="Cesar")

@app.route('/theflash')
def theFlash():
    flash("This is a super message")
    flash("This is a better message yet")
    return render_template('theflash.html')

@app.route('/b')
def b():
    #http://example.com/over/there?name=ferret&car=BMW
    return request.args.get('username')

@app.route('/sess', methods=['POST', 'GET'])
def sess():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return render_template('readcookie.html', name=session['username'])
    else:
        session.clear()
        return '''<form action="/sess" method="post">
                  <p><input type=text name=username>
                  <p><input type=submit value=Sess>
                  </form>'''

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        resp = make_response(render_template('readcookie.html', name=request.form['username']))
        resp.set_cookie('userID', value= request.form['username'])
        return resp
    else:
        print request.cookies.get('userID')
        return '''<form action="/login" method="post">
                <p><input type=text name=username>
                <p><input type=submit value=Login>
                </form>'''

@app.route('/csharp', methods=['GET','POST'])
def csharp():
    if request.method == 'POST':
        print request.form['name'] + ' POST'
        print request.form['car'] + ' POST'
        return "Hello, " + request.form['name'] + ". Your " + request.form['car'] + " is cool. POST"
    else:
        print request.args['name'] + ' GET'
        print request.args['car'] + ' GET'
        return "Hello, " + request.args['name'] + ". Your " + request.args['car'] + " is cool. GET"

@app.route('/jsonto', methods=['GET', 'POST'])
def jsonto():
    if request.method == 'POST':
        dat = request.form['jsondata']
        tox = json.loads(dat)
        print tox['name']
        return "Your " + tox['name'] + " is a cool device from " + tox['brand']

@app.route('/dati', methods=['GET', 'POST'])
def dati():
    if request.method == 'POST':
        dat = json.loads(request.data)
        print dat[1]['name']
        return "Hello from DATI"

@app.route('/ue', methods=['GET', 'POST'])
def ue():
    if request.method == 'POST':
        xx = json.loads(request.data)
        print xx['name'] + " " + xx['car']
        return "Hello from UE4"

@app.route('/vals', methods=['GET', 'POST'])
def vals():
    zz = '{"name": "Nuria", "car": "Audi", "city": "Santander"}';
    if request.method == 'POST':
        xx = json.loads(request.data)
        print xx['name']
        return zz

@app.route('/alot', methods=['GET', 'POST'])
def alot():
    zz = '{"x":[{"name": "Isabel", "car": "Ferrari", "city": "Santander"},{"name": "Nuria", "car": "Audi", "city": "Santander"},{"name": "Natalia", "car": "BMW", "city": "Santander"}]}'
    val = 0
    if request.method == 'POST':
        rawData = json.loads(request.data)
        for i in range(0, len(rawData['a'])):
            girl = json.loads(rawData['a'][val])
            print girl['name']
            val += 1
        return zz

@app.route('/arri', methods=['GET', 'POST'])
def arri():
    if request.method == 'POST':
        dat = json.loads(request.data)
        di = json.loads(dat['a'][1])
        print di['name']
        return "Hello from ARRI"

@app.route('/leps', methods=['GET', 'POST'])
def leps():
    xx = {'name': 'Rafael',
          'last name': 'Nadal',
          'country': 'Spain',
          'profession': 'tennis player',
          'titles': [{'roland garros': 9},{'wimbledon': 2},{'us open': 2},{'australian open': 1}]}
    if request.method == 'POST':
        return json.dumps(xx)

@app.route('/fromue', methods=['POST'])
def fromue():
    toue = {'info':[
            {'name': 'Spain', 'capital': 'Madrid', 'king': 'Felipe VI',
            'figures': {'population': 46524943, 'pib': '1566 billion', 'calling code': '+34'}},
            {'name': 'England', 'capital': 'London', 'king': 'no king',
            'figures': {'population': 54316600, 'pib': '2.68 trillion', 'calling code': '+44'}}
             ]}
    index = 0
    data = json.loads(request.data)
    for i in range(0, len(data['countries'])):
        single = json.loads(data['countries'][index])
        client = MongoClient('mongodb://localhost:27017/')
        database = client['countries']
        table = database['ranking']
        table.insert({'country': single['country'], 'points': int(single['points'])})
        client.close()
        index += 1
    return json.dumps(toue)

@app.route('/tojquery', methods=['POST'])
def tojquery():
    dbDataToArray = []
    client = MongoClient('mongodb://localhost:27017/')
    database = client['countries']
    table = database['ranking']
    records = table.find({})
    for i in records:
        myDictionary = {}
        myDictionary['country'] = i['country']
        myDictionary['points'] = i['points']
        dbDataToArray.append(myDictionary)
    return json.dumps(dbDataToArray)

@app.route('/addone', methods=['POST'])
def addone():
    client = MongoClient('mongodb://localhost:27017/')
    database = client['countries']
    table = database['ranking']
    mycountry = table.find_one({'country': 'Spain'})
    mypoints = mycountry['points']
    mypoints = mypoints + 1
    table.update({'country': 'Spain'},{'$set': {'points': mypoints}}, multi=True)
    client.close()
    return ""

@app.route('/golang', methods=['POST'])
def golang():
    print request.form['car']
    return '{"name": "Isabel"}'

@app.route('/golangraw')
def golangraw():
    aa = requests.post("http://127.0.0.1:8080/toflask")
    bb = aa.content
    cc = json.loads(bb)
    print cc['nombre']
    return ""

@app.route('/toandroid', methods=['POST'])
def toandroid():
    xx = {"countries":[
        {"name": "Spain", "capital": "Madrid"},
        {"name": "France", "capital": "Paris"},
        {"name": "Italy", "capital": "Rome"}
    ]}
    return json.dumps(xx)

@app.route('/fromandroid', methods=['POST', 'GET'])
def fromandroid():
    if request.method == 'POST':
        print request.form['name']
        return ""
    else:
        print request.args['car']
        return ""

@app.route('/androidjson', methods=['POST'])
def androidjson():
    xx = json.loads(request.data)
    print xx['name']
    return ""

@app.route('/tonodemcu')
def tonodemcu():
    r = requests.post("http://192.168.1.40:80", data='{"name": "Natalia"}')
    xx = json.loads(r.content)
    print xx['name']
    return ""

@app.errorhandler(404)
def not_found(error):
    return render_template('error.html', name= error)

@app.errorhandler(500)
def not_found(error):
    return render_template('error.html', name= error)

@app.route('/react')
def react():
    return  render_template('react.html')



if __name__ == '__main__':
    app.debug = True
    app.secret_key = os.urandom(datetime.datetime.now().microsecond + datetime.datetime.now().second)
    app.run(host='0.0.0.0', port=5000)
