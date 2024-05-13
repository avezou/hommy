import sqlite3
import requests
import atexit
import os
import urllib.request
from itertools import groupby
from flask import Flask, render_template, request, redirect, url_for, jsonify
from sched import scheduler
from apscheduler.schedulers.background import BackgroundScheduler
from PIL import Image
from flask_bootstrap import Bootstrap
from config import Config
from forms import AppForm
from werkzeug.utils import secure_filename
from PIL import Image


app = Flask(__name__, template_folder='templates')
app.config.from_object(Config)

bootstrap = Bootstrap(app)


    


# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())


def get_db_connection():
    connect = sqlite3.connect('./database.db')
    connect.row_factory = sqlite3.Row
    return connect

def get_apps():
    connect = get_db_connection()
    apps = connect.execute('SELECT a.id, a.category, a.name, a.internal_url, a.external_url, a.description, a.icon, a.alive, a.extras\
                            FROM apps a ORDER BY a.category').fetchall()
    if len(apps) == 0:
        return []

    newapp = {}
    for myapp in apps:
        # imagename = myapp['name'] + ".jpg"
        # print("icon url: " + str(myapp['icon']))
        # urllib.request.urlretrieve(myapp['icon'], imagename)
        # image = Image.open(imagename)
        # print(image.format)
        searchApps = myapp['name'].lower()
        try:
            response = requests.get(myapp['internal_url'])
            if response.status_code == 200:
                connect.execute('UPDATE apps SET alive = 1 WHERE id =?', (myapp['id'],))
            else:
                connect.execute('UPDATE apps SET alive = 0 WHERE id =?', (myapp['id'],))
        except Exception as e:
            if app.debug == True:
                print("Failure: " + str(e))

        tags = connect.execute('SELECT a.id, a.tag\
                            FROM tags a \
                            JOIN app_tags at\
                            ON a.id = at.tag_id \
                            WHERE at.app_id = ? ORDER BY a.tag', (myapp['id'],)).fetchall()
        category = connect.execute('SELECT c.cat\
                            FROM apps a\
                            JOIN categories c\
                            ON a.category = c.cat').fetchall()[0]
        
        newapp[myapp] = tags

        
    allTags = connect.execute('SELECT a.id, a.tag\
                            FROM tags a ORDER BY a.tag').fetchall()
    allCategories = connect.execute('SELECT c.cat\
                            FROM categories c ORDER BY c.cat').fetchall()
    
    connect.commit()
    connect.close()

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
    connect = get_db_connection()
    connect.execute('DELETE FROM apps WHERE id =?', (id,))
    connect.execute('DELETE FROM app_tags WHERE app_id =?', (id,))
    connect.commit()
    connect.close()
    return redirect(url_for('list'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    connect = get_db_connection()
    app = connect.execute('SELECT * FROM apps WHERE id =?', (id,)).fetchone()
    dbtags = connect.execute('SELECT tag\
                            FROM app_tags a\
                            JOIN tags t ON a.tag_id = t.id\
                            WHERE a.app_id =?', (id,)).fetchall()

    tags = []
    for tag in dbtags:
        tags.append(tag['tag'])
    form = AppForm(obj=app)
    form.name.data = app['name']
    form.category.data = app['category']
    form.description.data = app['description']
    form.internal_url.data = app['internal_url']
    form.external_url.data = app['external_url']
    form.tags.data = ','.join(tags)
    form.icon.data = app['icon']
    form.extras.data = app['extras']

    if form.validate_on_submit():
        appName = form.name.data
        category = form.category.data
        description = form.description.data
        internal_url = form.internal_url.data
        external_url = form.external_url.data
        tags = form.tags.data
        extras = form.extras.data

        if len(tags) > 0:
            if ',' in tags:
                alltags = tags.split(',')
                for tag in alltags:
                    connect.execute('INSERT OR IGNORE INTO tags (tag) VALUES (?)', (tag,))
            else:
                connect.execute('INSERT OR IGNORE INTO tags (tag) VALUES (?)', (tags,))
        connect.commit()
        if form.icon.data:
            upload_file = form.icon.data
            image = Image.open(upload_file)
            width, height = 200, 200
            image = image.resize((width, height))
            filename = secure_filename(upload_file.filename)
            image.save(filename)

            # filename = secure_filename(upload_file.filename)
            icon_path = os.path.join(app.config['UPLOAD_PATH'], filename)
            upload_file.save(filename)
        

            connect.execute('UPDATE apps SET name=?, category=?, description=?, internal_url=?, external_url=?, icon=?, extras=?\
                WHERE id=?', (appName, category, description, internal_url, external_url, icon_path, extras, id))
        else:
            connect.execute('UPDATE apps SET name=?, category=?, description=?, internal_url=?, external_url=?, extras=?\
                WHERE id=?', (appName, category, description, internal_url, external_url, extras, id))


        connect.commit()
        connect.close()

        return redirect(url_for('list'))


    return render_template('edit.html', form=form)



@app.route('/add', methods=['GET', 'POST'])
def add():
    form = AppForm()
    allApps = []
    alltags = []
    if form.validate_on_submit():
        connect = get_db_connection()
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

        # connect.execute('INSERT OR IGNORE INTO categories(cat) VALUES(?)', (category,))
        allApps = connect.execute('SELECT id, name, category, description, internal_url, external_url FROM apps').fetchall()

        # alltags = []
        if len(tags) > 0:
            if ',' in tags:
                alltags = tags.split(',')
                for tag in alltags:
                    connect.execute('INSERT OR IGNORE INTO tags (tag) VALUES (?)', (tag.strip(),))
            else:
                connect.execute('INSERT OR IGNORE INTO tags (tag) VALUES (?)', (tags,))
                allTags = tags.strip()
        connect.commit()

        connect.execute('INSERT OR IGNORE INTO apps (name, category, description, internal_url, external_url, icon, extras)\
            VALUES (?, ?, ?, ?, ?, ?, ?)', (appName.strip(), category, description, internal_url, external_url, icon_path, extras))

        myapp = connect.execute('SELECT id,name FROM apps where name=?', (appName,)).fetchall()[0]

        if myapp['id'] > -1:
            if len(alltags) > 0:
                for tag in alltags:
                    t = connect.execute('SELECT id, tag FROM tags WHERE tag=?', (tag,)).fetchall()[0]
                    print ("print t: " + str(t['tag']))
                    connect.execute('INSERT INTO app_tags(app_id, tag_id) VALUES(?, ?)', (myapp['id'], t['id']))
            
        connect.commit()
        connect.close()

        return redirect(url_for('index'))
        

    return render_template('add.html', form=form, title='App Form', items=alltags)

@app.route('/get_data')
def get_data():
    connect = get_db_connection()
    apps = connect.execute('SELECT a.id, a.category, a.name, a.internal_url, a.external_url, a.description, a.icon, a.alive, a.extras\
                            FROM apps a ORDER BY a.category').fetchall()
    
    data = {}
    for app in apps:
        data[app['name']] = app['internal_url']

    connect.commit()
    connect.close()
    return jsonify(data)

@app.route('/sample')
def sample():
    return render_template('sample.html')


if __name__ == '__main__':
    app.run(debug=True)
