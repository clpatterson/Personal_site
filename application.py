
import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash


application = Flask(__name__) #create application instance and pull configs from instance directory
application.config.from_object(__name__) #Load config from config.py file

application.config.update(dict(
    DATABASE=os.path.join(application.root_path, 'personal_site.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))

#application.config.from_envvar('BLOG_SETTINGS', silent=True)


def connect_db():
    """Creates a connection to the specified database"""
    rv = sqlite3.connect(application.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def init_db():
    db = get_db()
    with application.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()


@application.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context."""
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@application.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@application.route('/')
def index():
    db = get_db()
    cur = db.execute('select title, post_date, id from posts order by post_date desc;')
    posts = cur.fetchall()
    return render_template('index.html', posts=posts)


@application.route('/blogManage')
def show_posts():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    cur = db.execute('select * from posts order by post_date desc;')
    posts = cur.fetchall()
    return render_template('blogManage.html', posts=posts)


@application.route('/add_post', methods=['POST'])
def add_post():
    if not session.get('logged_in'):
        abort(401)
    f = request.files['html_file']
    html_file = f.read().decode('utf-8')
    print(html_file)
    db = get_db()
    db.execute('insert into posts (title, post_date, description, html_file) values (?, ?, ?, ?)', 
                [request.form['title'], request.form['post_date'], request.form['description'], html_file])
    db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_posts'))


@application.route('/update_post', methods=['POST'])
def update_post():
    if not session.get('logged_in'):
        abort(401)
    print('preparing to pull form data')
    f = request.files['html_file']
    html_file = f.read()
    print(html_file)
    db = get_db()                                                                                                                                                                                                                                                                                                                                                                                                                              
    cur = db.execute('update posts set title = (?), post_date = (?), description = (?), html_file = (?) where id = (?)', 
        [request.form['title'], request.form['post_date'], request.form['description'], html_file, request.form['id']])
    print('executed the update in db')
    db.commit()
    return redirect(url_for('show_posts'))


@application.route('/delete_post', methods=['POST'])
def delete_post():
    if not session.get('logged_in'):
        abort(401)
    postId = request.form.get('id')
    print(postId)
    db = get_db()                                                                                                                                                                                                                                                                                                                                                                                                                              
    cur = db.execute('delete from posts where id = (?)', (postId,))
    db.commit()
    return redirect(url_for('show_posts')) 


@application.route('/<post_date>/<post_title>/<post_id>')
def view_post(post_id,post_date,post_title):
    db = get_db()
    res = db.execute('select title, post_date, description, html_file from posts where id = (?);', (post_id,))
    post = res.fetchall()
    print(res.fetchone())
    print(post)
    return render_template('blog_post.html', post=post)


@application.template_filter()
def quote_begone(html_string): #html_sting is html text pulled from the database wrapped in b'
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
            flash('You were logged in')
            return redirect(url_for('show_posts'))
    return render_template('login.html', error=error)


@application.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('index'))


if __name__ == '__main__':
    application.run(host="0.0.0.0", port=5000)
