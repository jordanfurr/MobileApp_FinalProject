from bottle import default_app, route, template
from bottle import get, post, request, static_file

import sqlite3

db = sqlite3.connect("./mysite/playerInfo.db")
c = db.cursor()

###############################################

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

@get('/intro/<curLevel>/<userID>')
def intro(curLevel, userID):
    if curLevel == '0':
        return template("intro.html", userID=userID, c=c)
    elif curLevel == '1':
        return template("itemB.html", userID=userID)
    elif curLevel == '2':
        return template("fightA.html", userID=userID, c=c)
    elif curLevel == '3':
        return template("fightB.html", userID=userID, c=c)
    elif curLevel == '4':
        return template("itemC.html", userID=userID)
    elif curLevel == '5':
        return template("fightC.html", userID=userID, c=c)
    elif curLevel == '6':
        return template("fightCcont.html", userID=userID, c=c, db=db)
    elif curLevel == '7':
        #reset player's items, deathCount, victor, and curLevel
        c.execute("UPDATE users SET itemA='None', itemB='None', itemC='None',\
                  curLevel='0', deathCount='0', victor='0' WHERE id=?",(userID))
        db.commit()
        return template("intro.html", userID=userID, c=c)
    elif curLevel == '8':
        return template("victory.html", userID=userID, c=c, db=db)

@get('/itemApage/<userID>')
def itemA(userID):
    return template("itemA.html", userID=userID)

@get('/fightAresult/<userID>/<choice>')
def fightAresult(userID, choice):
    if choice == 'C':
        #SUCCESS
        return template("fightAvictory.html", userID=userID, c=c, db=db)
    else:
        #FAIL
        return template("fightAdefeat.html", userID=userID, choice=choice, c=c, db=db)

@route('/fightBresult/<userID>/<choice>')
def fightBresult(userID, choice):
    if choice == 'C':
        #SUCCESS
        return template("fightBvictory.html", userID=userID, c=c, db=db)
    else:
        #FAIL
        return template("fightBdefeat.html", userID=userID, choice=choice, c=c, db=db)

@route('/fightCnext/<userID>/<choice>')
def fightCnext(userID, choice):
    if choice == 'B':
        #SUCCESS
        return template("fightCcont.html", userID=userID, c=c, db=db)
    else:
        #FAIL
        return template("fightCdefeatA.html", userID=userID, choice=choice, c=c, db=db)

@route('/fightCresult/<userID>/<choice>')
def fightCresult(userID, choice):
    if choice == 'A':
        #SUCCESS
        return template("victory.html", userID=userID, c=c, db=db)
    else:
        return template("fightCdefeatB.html", userID=userID, choice=choice, c=c, db=db)

@route('/showInv/<userID>/<item>/<choice>')
def showInv(userID, item, choice):
    return template("showInv.html", userID=userID, item=item,
                    choice=choice, db=db, c=c)

@get('/moveOn/<userID>/<location>')
def moveOn(userID, location):
    if location == 'itemA':
        return template("itemB.html", userID=userID)
    elif location == 'itemB':
        return template("fightA.html", userID=userID, c=c)
    elif location == 'itemC':
        return template("fightC.html", userID=userID, c=c)

@route('/showLB/<userID>')
def showLB(userID):
    return template("showLB.html", userID=userID, c=c)

@route('/showDB')
def showDB():
    return template("showDB.html", c=c)

@route('/resetDB')
def resetDB():
    c.execute('DROP TABLE IF EXISTS users')
    mainSql = '''
    CREATE TABLE users (
        id INTEGER PRIMARY KEY,
        uName VARCHAR (20),
        pWord VARCHAR (20),
        curLevel INTEGER (1),
        deathCount INTEGER (3),
        itemA VARCHAR (22),
        itemB VARCHAR (22),
        itemC VARCHAR (22),
        victor INTEGER (1)
    ) '''
    c.execute(mainSql)
    db.commit()
    return template("login.html")

@get('/static/<filepath:path>')
def static(filepath):
    return static_file(filepath, root='/static')

application = default_app()
