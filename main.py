__author__ = 'Administrator'
# coding=utf-8

import os, sqlite3
from flask import Flask, request, g, flash, render_template, session, redirect, url_for

app = Flask(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'wzcx.db'), SECRET_KEY='WZCX-C6'))

def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db  = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

@app.route('/init_db')
def init_db():
    error=0
    try:
        db = get_db()
        with app.open_resource('init_db.sql') as f:
            db.executescript(f.read())
        db.commit()
    except Exception,e:
        error=1
    if error==0:
        flash('数据库初始化成功！')
        return render_template('index.html')
    else:
        flash('数据库初始化失败，请重试！')
        return render_template('index.html')

def select_car(email = None):
    db = get_db()
    rv = db.execute('select * from carinfo where email=?', (email,))
    #result = []
    #for row in rv:
    #    result.append(dict(id=row[0], cpd=row[1], hm=row[2], fdj=row[3], email=row[4], wzxx=row[5], lastupdate=row[6]))
    return rv


def insert_car(cpd, hm, fdj, email):
    error = True
    try:
        db = get_db()
        res = db.execute('INSERT INTO carinfo (cpd, hm, fdj, email) VALUES (?,?,?,?)', [cpd, hm, fdj, email])
        db.commit()
    except Exception,e:
        error = e.message
    return error

def updatecar(id, cpd, hm, fdj, email):
    error = True
    try:
        db = get_db()
        db.execute('UPDATE carinfo SET cpd=?,hm=?,fdj=? WHERE id=? and email=?', [cpd, hm, fdj, id, email])
        db.commit()
    except:
        error = False
    return error

@app.route('/')
def index():
    if session['username']:
        result = select_car(email=session['username'])
    return render_template('index.html', cars=result)

@app.route('/user/<code>')
def user(code):
    if code:
        result = select_car(email=code)
        session['username'] = code
    return render_template('index.html', cars=result)

@app.route('/add_car', methods=['POST', 'GET'])
def add_car():
    if request.method == 'POST':
        cpd = u'湘'
        hm = request.form['hm']
        fdj = request.form['fdj']
        email = request.form['email']
        if email and hm and fdj:
            res = insert_car(cpd, hm, fdj, email)
        if res:
            flash('插入成功！')
        return redirect(url_for('index'))
    elif request.method == 'GET':
        return render_template('add_car.html')

@app.route('/update', methods=['POST'])
def update_car():
    id = request.form['id']
    cpd = request.form['cpd'] if request.form['cpd'] else unicode('湘', encoding='utf-8')
    hm = request.form['hm']
    fdj = request.form['fdj']
    email = request.form['email']
    updatecar(id, cpd, hm, fdj, email)
    return redirect(url_for('index'))

@app.route('/edit/<id>')
def edit_car(id):
    db = get_db()
    result = db.execute('select * from carinfo where id=?', (id,)).fetchone()
    return render_template('edit_car.html', car=result)

@app.route('/del_car/<int:id>')
def del_car(id):
    error = True
    db = get_db()
    try:
        db.execute('DELETE from carinfo WHERE id=?', (id,))
        db.commit()
    except Exception,e:
        error = e.message
    return redirect(url_for('user',code=session['username']))

if __name__=="__main__":
    app.run(debug=True)