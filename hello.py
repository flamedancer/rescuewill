# -*- coding: utf-8 -*-

import os
import math
from flask import Flask, g, session, flash, render_template,\
    redirect, url_for
app = Flask(__name__)

""" DB  config
"""
db_config = {
    'host': '127.0.0.1',
    'user': 'guochen',
    'password': '1111',
    'db': 'rescurewill',
    'charset': 'utf8mb4',
}


import pymysql
from flask import g


PWD =  app.root_path
print("current work path is {}".format(PWD))
DATABASE = PWD + 'database.db'

def init_db():
    with app.app_context():
        db = connect_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().execute(f.read())
        db.commit()

def connect_db():
    return pymysql.connect(**db_config)

@app.before_request
def before_request():
    g.db = connect_db()
    g.cuser = g.db.cursor()

@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()

""" Routes
"""


@app.route('/')
def hello_world():
    return redirect(url_for('show_want_todo'))

"""
    total_score 最大为 100分
    hard_star 根据  total_score / 20 + 1 计算
    status 0 未完成  1 完成 2关闭

"""    

def compute_hard_star(score):
    socre = min(100, max(0, socre))
    return (socre // 20) + 1

def compute_get_score(total_score, statisfy_star):
    statisfy_star = min(5, max(1, statisfy_star))
    return math.ceil(total_score * statisfy_star / 5)

@app.route('/show_want_todo/')
def show_want_todo():	
    g.cuser.execute('select * from want_todo where status=%s', [0])
    todos = g.cuser.fetchall()
    return render_template('want_todo.html', todos=todos)
    
@app.route('/add_want_todo', methods=['POST'])
def add_want_todo():
    # if not session.get('logged_in'):
        # abort(401)
    title = request.form['title']
    total_score = int(request.form['total_score'])
    g.cuser.execute('insert into want_todo (title, total_score, hard_star) values (%s, %s, %s)', [title, total_score, compute_hard_star(total_score)])
    g.db.commit()
    flash('New TODO was successfully posted')
    return redirect(url_for('show_want_todo'))

    
@app.route('/finish_want_todo', methods=['POST'])
def finish_want_todo():
    id = request.form['id']
    g.cuser.execute('select total_score from want_todo where id=? and status=%s', [id, 0])
    todo_item = g.cuser.fetchone()
    if not todo_item:
        flash('Canbot find this todo item')
        return redirect(url_for('show_want_todo'))
    total_score = todo_item[0]
    satisfy_star = int(request.form['statisfy_star'])
    finish_reflection = request.form['finish_reflection']
    # 计算得分
    get_score = compute_get_score(total_score, statisfy_star)
    cur = g.cuser.execute('''update want_todo set finish_time=now() get_score=%s satisfy_star=%s finish_reflection=%s
         where id=%s and status=%s''', [get_score, satisfy_star, finish_reflection, id, 0])
    g.db.commit()
    flash('successfully complate task')
    return redirect(url_for('show_want_todo'))


if __name__ == '__main__':
    init_db()
    app.run(debug=True)