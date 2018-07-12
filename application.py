#!/usr/bin/python

"""Flask application code for my personal website."""

import os
import psycopg2
from psycopg2 import extras
from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash


# Create application instance.
application = Flask(__name__)

# Load config from environment variable that contains path to file.
application.config.from_envvar('APPLICATION_SETTINGS')


def connect_db():
    """Create connection to specified database."""
    connection = psycopg2.connect(application.config['DATABASE'], cursor_factory=psycopg2.extras.DictCursor)
    return connection

def init_db():
    """Create table from schema."""
    db = get_db()
    cursor = db.cursor()
    with application.open_resource('schema.sql', mode='r') as f:
        cursor.execute(f.read())
    db.commit()

@application.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')

def get_db():
    """Open new database connection if there is none yet for the current application context."""
    if not hasattr(g, 'personalsitedb'):
        g.personalsitedb = connect_db()
    return g.personalsitedb

@application.teardown_appcontext
def close_db(error):
    """Close database at end of the request."""
    if hasattr(g, 'personalsitedb'):
        g.personalsitedb.close()

@application.route('/')
def index():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT title, post_date, id FROM posts ORDER BY post_date DESC;')
    posts = cursor.fetchall()
    print(posts)
    return render_template('index.html', posts=posts)

@application.route('/blogManage')
def show_posts():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM posts ORDER BY post_date DESC;')
    posts = cursor.fetchall()
    return render_template('blogManage.html', posts=posts)

# Upload data from form to database.
@application.route('/add_post', methods=['POST'])
def add_post():
    if not session.get('logged_in'):
        abort(401)
    # Write post data to Postgres database
    get_html_file = request.files['html_file']
    html_file = get_html_file.read().decode('utf-8')
    db = get_db()
    cursor = db.cursor()
    cursor.execute('INSERT INTO posts (title, post_date, description, html_file) VALUES (%s, %s, %s, %s);', 
                [request.form['title'], request.form['post_date'], request.form['description'], html_file])
    db.commit()
    flash('New entry was successfully posted.')
    return redirect(url_for('show_posts'))

@application.route('/update_post', methods=['POST'])
def update_post():
    if not session.get('logged_in'):
        abort(401)
    print('preparing to pull form data')

    # Update data in Postgres database
    get_html_file = request.files['html_file']
    html_file = get_html_file.read().decode('utf-8')
    print(html_file)
    db = get_db()
    cursor = db.cursor()                                                                                                                                                                                                                                                                                                                                                                                                                              
    cursor.execute('UPDATE posts SET title = (%s), post_date = (%s), description = (%s), html_file = (%s) WHERE id = (%s);', 
        [request.form['title'], request.form['post_date'], request.form['description'], html_file, request.form['id']])
    print('Updated post.')
    db.commit()
    return redirect(url_for('show_posts'))

@application.route('/delete_post', methods=['POST'])
def delete_post():
    if not session.get('logged_in'):
        abort(401) 
    postId = request.form.get('id')
    print(postId)
    db = get_db()
    cursor = db.cursor()                                                                                                                                                                                                                                                                                                                                                                                                                             
    cursor.execute('DELETE FROM posts WHERE id = (%s)', (postId,))
    db.commit()
    return redirect(url_for('show_posts')) 

@application.route('/<post_date>/<post_title>/<post_id>')
def view_post(post_id,post_date,post_title):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT title, post_date, description, html_file FROM posts WHERE id = (%s);", (post_id,))
    post = cursor.fetchall()
    print(cursor.fetchone())
    print(post)
    return render_template('blog_post.html', post=post)

@application.template_filter()
def quote_begone(html_string): #html_sting is html text pulled from the database wrapped in b'
    print(html_string)
    return  html_string.decode('utf-8')

@application.route('/login', methods=['GET','POST'])
def login():
    error = None 
    if request.method == 'POST':
        if request.form['username'] != application.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != application.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in.')
            return redirect(url_for('show_posts'))
    return render_template('login.html', error=error)

@application.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('index'))


if __name__ == '__main__':
    #application.run(host="0.0.0.0", port=5000)
    application.debug()
    application.run()