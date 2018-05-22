# -*- coding: utf-8 -*-

import os
import math
import json

import pymysql
from flask import g
from flask import Flask, g, session, flash, render_template,\
    redirect, url_for, request, json
from flask import jsonify
from config import config_path


app = Flask(__name__)
app.config.from_pyfile(config_path)


PWD = app.root_path
print("current work path is {}".format(PWD))
DATABASE = PWD + 'database.db'

def connect_db():
    return pymysql.connect(**app.config['DB_CONFIG'])

@app.before_request
def before_request():
    g.db = connect_db()
    g.cuser = g.db.cursor(pymysql.cursors.DictCursor)

@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()

""" Tools
"""
def query_db(query, args=(), one=False):
    cur = g.db.execute(query, args)
    rv = [dict((cur.description[idx][0], value)
               for idx, value in enumerate(row)) for row in cur.fetchall()]
    return (rv[0] if rv else None) if one else rv

def fix_range(value, max_value, min_value):
    return min(max_value, max(min_value, value))
        
""" Routes
"""



"""
    total_score 最大为 100分
    hard_star 根据  total_score / 20 + 1 计算
    status 0 未完成  1 完成 2关闭

"""    

def compute_hard_star(score):
    score = fix_range(score, 100, 1)
    return  fix_range(((score - 1) // 20) + 1, 5, 1)

def compute_get_score(total_score, statisfy_star):
    statisfy_star = fix_range(statisfy_star, 5, 1)
    return math.ceil(total_score * statisfy_star / 5)

    
@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/show_home_template')
def show_home_template():
    return render_template('home.html')

    
@app.route('/show_want_todo_template')
def show_want_todo_template():
    return render_template('want_todo.html')


@app.route('/show_want_todo_items/<path:status>')
def show_want_todo_items(status):
    g.cuser.execute('select create_time, title, hard_star from want_todo where status=%s', [status])
    todos = g.cuser.fetchall()
    return json.dumps(todos)

    
@app.route('/add_want_todo', methods=['POST'])
def add_want_todo():
    title = request.form['title']
    total_score = int(request.form['total_score'])
    g.cuser.execute('insert into want_todo (title, total_score, hard_star, status) values (%s, %s, %s, %s)', [title, total_score, compute_hard_star(total_score), 0])
    last_record_id = int(g.cuser.lastrowid)
    g.db.commit()
    g.cuser.execute('select create_time, title, hard_star from want_todo where id=%s', [last_record_id])
    todos = g.cuser.fetchall()
    return json.dumps(todos)

    
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
    get_score = compute_get_score(total_score, satisfy_star)
    g.cuser.execute('''update want_todo set finish_time=now() get_score=%s satisfy_star=%s finish_reflection=%s
         where id=%s and status=%s''', [get_score, satisfy_star, finish_reflection, id, 0])
    g.db.commit()
    flash('successfully complate task')
    return redirect(url_for('show_want_todo'))


@app.route('/show_memory_template')
def show_memory_template():
    return render_template('memory.html')
    
@app.route('/show_memory_items/<path:status>')
def show_memory_items(status):
    g.cuser.execute('select create_time, title, remember_times from memory where status=%s', [status])
    todos = g.cuser.fetchall()
    return json.dumps(todos)

    
@app.route('/add_memory', methods=['POST'])
def add_memory():
    title = request.form['title']
    score = fix_range(int(request.form['score']), 20, 1)
    g.cuser.execute('insert into memory (title, score, status) values (%s, %s, %s)', [title, score, 0])
    last_record_id = int(g.cuser.lastrowid)
    g.db.commit()
    g.cuser.execute('select create_time, title, remember_times from memory where id=%s', [last_record_id])
    todos = g.cuser.fetchall()
    return json.dumps(todos)

    
@app.route('/close_memory', methods=['POST'])
def close_memory():
    id = request.form['id']
    cur = g.cuser.execute('''update memory set status=%s where id=%s and status=%s''', [2, id, 0])
    g.db.commit()
    return "ok"


@app.route('/show_important_template')
def show_important_template():
    return render_template('important.html')

@app.route('/show_important_items/<path:status>')
def show_important_items(status):
    g.cuser.execute('select create_time, title from important where status=%s', [status])
    todos = g.cuser.fetchall()
    return json.dumps(todos)

@app.route('/add_important', methods=['POST'])
def add_important():
    title = request.form['title']
    g.cuser.execute('insert into important (title, status) values (%s, %s)', [title, 0])
    last_record_id = int(g.cuser.lastrowid)
    g.db.commit()
    g.cuser.execute('select create_time, title from important where id=%s', [last_record_id])
    todos = g.cuser.fetchall()
    return json.dumps(todos)

@app.route('/close_important', methods=['POST'])
def close_important():
    id = request.form['id']
    cur = g.cuser.execute('''update important set status=%s where id=%s and status=%s''', [2, id, 0])
    g.db.commit()
    return "ok"


@app.route('/show_datetask_template')
def show_datetask_template():
    return render_template('datetask.html')


@app.route('/show_datetask_items/<path:status>')
def show_datetask_items(status):
    g.cuser.execute('select create_time, title, score from datetask where status=%s', [status])
    todos = g.cuser.fetchall()
    return json.dumps(todos)


@app.route('/add_datetask', methods=['POST'])
def add_datetask():
    title = request.form['title']
    score = fix_range(int(request.form['score']), 20, 1)
    g.cuser.execute('insert into datetask (title, score, status) values (%s, %s, %s)', [title, score, 0])
    last_record_id = int(g.cuser.lastrowid)
    g.db.commit()
    g.cuser.execute('select create_time, title, score from datetask where id=%s', [last_record_id])
    todos = g.cuser.fetchall()
    return json.dumps(todos)


@app.route('/close_datetask', methods=['POST'])
def close_datetask():
    id = request.form['id']
    cur = g.cuser.execute('''update datetask set status=%s where id=%s and status=%s''', [2, id, 0])
    g.db.commit()
    return "ok"


if __name__ == '__main__':
    app.run(host='0.0.0.0')