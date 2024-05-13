import sqlite3
import requests
import os
import urllib.request
from itertools import groupby
from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from PIL import Image
from flask_bootstrap import Bootstrap
from config import Config
from forms import AppForm
from werkzeug.utils import secure_filename
from PIL import Image


app = Flask(__name__, template_folder='templates')
app.config.from_object(Config)
bootstrap = Bootstrap(app)


def get_db_connection():
    connect = sqlite3.connect('./database.db')
    connect.execute('pragma journal_mode=wal')
    connect.row_factory = sqlite3.Row
    return connect

def execute_query(query, args=(), one=False):
    connection = get_db_connection()
    cursor = connection.execute(query, args)
    rv = cursor.fetchall()
    connection.commit()
    cursor.close()
    connection.close()
    return (rv[0] if rv else None) if one else rv

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']



def get_apps():
    apps = execute_query('SELECT a.id, a.category, a.name, a.internal_url, a.external_url, a.description, a.icon, a.alive, a.extras\
                            FROM apps a ORDER BY a.category')
    if len(apps) == 0:
        return []
    newapp = {}
    for myapp in apps:
        searchApps = myapp['name'].lower()
        tags = execute_query('SELECT a.id, a.tag\
                            FROM tags a \
                            JOIN app_tags at\
                            ON a.id = at.tag_id \
                            WHERE at.app_id = ? ORDER BY a.tag', (myapp['id'],))
        category = execute_query('SELECT c.cat\
                            FROM apps a\
                            JOIN categories c\
                            ON a.category = c.cat \
                            WHERE a.id = ?', (myapp['id'],))
        
        newapp[myapp] = tags

    allTags = execute_query('SELECT a.id, a.tag\
                            FROM tags a ORDER BY a.tag')
    allCategories = execute_query('SELECT c.cat\
                            FROM categories c ORDER BY c.cat')
    return newapp, allTags, allCategories, searchApps


@app.route('/')
def index():
    res = get_apps()
    if len(res) <= 0:
        return render_template('index.html')     
    return render_template('index.html', apps=res[0], tags=res[1], categories=res[2], appNames=res[3]) 

@app.route('/list', methods=['GET', 'POST'])
def list():
    res =  get_apps()
    if len(res) <= 0:
        return render_template('index.html')          
    return render_template('list.html', apps=res[0])

@app.route('/delete/<int:id>')
def delete(id):
    execute_query('DELETE FROM apps WHERE id =?', (id,))
    execute_query('DELETE FROM app_tags WHERE app_id =?', (id,))
    return redirect(url_for('list'))


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    app = execute_query('SELECT * FROM apps WHERE id =?', (id,), one=True)
    dbtags = execute_query('SELECT tag FROM tags t JOIN app_tags a ON a.tag_id = t.id WHERE a.app_id =?', (id,))
    tags = [tag['tag'] for tag in dbtags]

    form = AppForm(obj=app)
    form.tags.data = ','.join(tags)
    form.name.data = app['name']
    form.category.data = app['category']
    form.description.data = app['description']
    form.internal_url.data = app['internal_url']
    form.external_url.data = app['external_url']
    form.extras.data = app['extras']
    form.icon.data = app['icon']

    # Prefill file input field with existing icon path
    form.icon.process_data(app['icon'])

    if form.validate_on_submit():
        # Extract form data
        appName = form.name.data
        category = form.category.data
        description = form.description.data
        internal_url = form.internal_url.data
        external_url = form.external_url.data
        tags = form.tags.data
        extras = form.extras.data

        # Handle file upload
        if 'icon' in request.files:
            upload_file = request.files['icon']
            if upload_file.filename != '':
                filename = secure_filename(upload_file.filename)
                icon_path = os.path.join(app.config['UPLOAD_PATH'], filename)
                upload_file.save(icon_path)
            else:
                # Keep the existing icon path if no new file is selected
                icon_path = app['icon']

        # Update app data in the database
        execute_query('UPDATE apps SET name=?, category=?, description=?, internal_url=?, external_url=?, icon=?, extras=? WHERE id=?',
                      (appName, category, description, internal_url, external_url, icon_path, extras, id))

        return redirect(url_for('list'))

    return render_template('edit.html', form=form)



@app.route('/add', methods=['GET', 'POST'])
def add():
    form = AppForm()
    allApps = []
    alltags = []
    if form.validate_on_submit():
        
        appName = form.name.data
        category = form.category.data
        description = form.description.data
        internal_url = form.internal_url.data
        external_url = form.external_url.data
        upload_file = form.icon.data
        filename = secure_filename(upload_file.filename)
        icon_path = os.path.abspath(os.path.join(app.config['UPLOAD_PATH'], filename))
        upload_file.save(icon_path)
        tags = form.tags.data
        extras = form.extras.data

        print ("icon path: " + str(icon_path))

        # connect = get_db_connection()
        # connect.execute('INSERT OR IGNORE INTO categories(cat) VALUES(?)', (category,))
        allApps = execute_query('SELECT id, name, category, description, internal_url, external_url FROM apps')

        # alltags = []
        if len(tags) > 0:
            if ',' in tags:
                alltags = tags.split(',')
                for tag in alltags:
                    execute_query('INSERT OR IGNORE INTO tags (tag) VALUES (?)', (tag.strip(),))
            else:
                execute_query('INSERT OR IGNORE INTO tags (tag) VALUES (?)', (tags,))
                allTags = tags.strip()

        execute_query('INSERT OR IGNORE INTO apps (name, category, description, internal_url, external_url, icon, extras)\
            VALUES (?, ?, ?, ?, ?, ?, ?)', (appName.strip(), category, description, internal_url, external_url, icon_path, extras))

        myapp = execute_query('SELECT id,name FROM apps where name=?', (appName,), one=True)

        if myapp['id'] > -1:
            if len(alltags) > 0:
                for tag in alltags:
                    t = execute_query('SELECT id, tag FROM tags WHERE tag=?', (tag,), one=True)
                    print ("print t: " + str(t['tag']))
                    execute_query('INSERT INTO app_tags(app_id, tag_id) VALUES(?, ?)', (myapp['id'], t['id']))
            
        return redirect(url_for('index'))
        
    return render_template('add.html', form=form, title='App Form', items=alltags)

@app.route('/get_data')
def get_data():
    apps = execute_query('SELECT a.id, a.category, a.name, a.internal_url, a.external_url, a.description, a.icon, a.alive, a.extras\
                            FROM apps a ORDER BY a.category')

    data = {}
    for app in apps:
        data[app['name']] = app['internal_url']

    
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)
