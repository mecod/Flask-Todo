# -*- coding: utf-8 -*-
from itertools import groupby
import sqlite3
from flask import Flask, render_template, request, flash, redirect, url_for

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dser53sf5-nnnsdfjkhhh'

@app.route('/')
def index():
    conn = get_db_connection()
    todos = conn.execute('SELECT i.content, l.title FROM items i JOIN lists l \
            ON i.list_id = l.id ORDER BY l.title;').fetchall()

    lists = {}
    
    for k, g in groupby(todos, key=lambda t: t['title']):
        lists[k] = list(g)

    conn.close()
    return render_template('index.html', lists=lists)

@app.route('/create/', methods=('GET', 'POST'))
def create():
    conn = get_db_connection()

    if request.method == 'POST':
        content = request.form['content']
        list_title = request.form['list']

        if not content:
            flash('Content is required!')
            return redirect(url_for('index'))

        list_id = conn.execute('SELECT id FROM lists WHERE title = (?);',
                (list_title,)).fetchall()['id']
        conn.execute('INSERT INTO items (content, list_id) VALUES (?, ?)', 
                (content, list_id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    lists = conn.execute('SELECT title FROM lists;').fetchall()

    conn.close()
    return render_template('create.html', lists=lists)


