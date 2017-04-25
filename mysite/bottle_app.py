from bottle import default_app, route, template
from bottle import get, post, request

import sqlite3

db = sqlite3.connect("./mysite/playerInfo.db")
c = db.cursor()

c.execute('DROP TABLE IF EXISTS users')
mainSql = '''
  CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username VARCHAR (20),
    password VARCHAR (20),
    itemA INTEGER (1),
    itemB INTEGER (1),
    itemC INTEGER (1)
  ) '''
c.execute(mainSql)
db.commit()

"""  #insert records into the users table
  c.execute('INSERT INTO users VALUES (null, ?, ?, ?, ?, ?)',
            ('usernameHere', 'passwordHere', 'itemA', 'itemB', 'itemC')) """

@route('/')
def hello_world():
    return 'Ayyy lmao'

@get('/login')
def login():
    return template("login.html")

@post('/login')
def doLogin():
    username = request.forms.get('username')
    password = request.forms.get('password')
    return template("doLogin.html", username=username, password=password, db=db, c=c)

@route('/intro/<username>')
def intro(username):
    #username = request.forms.get('username')
    return template("intro.html", username=username)

@route('/showDB')
def showDB():
    return template("showDB.html", c=c)

application = default_app()

