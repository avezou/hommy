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


app = Flask(__name__, template_folder='templates')
app.config.from_object(Config)

bootstrap = Bootstrap(app)


def update_alive():
    connect = get_db_connection()
    apps = connect.execute('SELECT a.id, a.name, a.internal_url, a.external_url, a.description, a.icon, a.alive\
                            FROM apps a').fetchall()
    for myapp in apps:
        try:
            response = requests.get(myapp['internal_url'])
            print("status code: " + str(response.status_code))
            if response.status_code == 200:
                connect.execute('UPDATE apps SET alive = 1 WHERE id =?', (myapp['id'],))
                print('App: ' + myapp['name'] + ' at ' + myapp['internal_url'] + ' is alive')
            else:
                connect.execute('UPDATE apps SET alive = 0 WHERE id =?', (myapp['id'],))
                print('App: '+ myapp['name'] +' is dead')
        except: 
            print('App'+ myapp['name'] +'is dead')
            connect.execute('UPDATE apps SET alive = 0 WHERE id =?', (myapp['id'],))
    connect.commit()
    connect.close()
    

scheduler = BackgroundScheduler()
scheduler.add_job(func=update_alive, trigger="interval", seconds=15)
scheduler.start()

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

    return render_template('index.html', apps=res[0], tags=res[1], categories=res[2], appNames=res[3]) 

@app.route('/list', methods=['GET', 'POST'])
def list():
    res =  get_apps()
    return render_template('list.html', apps=res[0])

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    form = AppForm()
    if form.validate_on_submit():
        connect = get_db_connection()
        appName = form.name.data
        category = form.category.data
        description = form.description.data
        internal_url = form.internal_url.data
        external_url = form.external_url.data
        upload_file = form.icon.data
        filename = secure_filename(upload_file.filename)
        icon_path = os.path.join(app.config['UPLOAD_PATH'], filename)
        upload_file.save(icon_path)
        tag1 = form.tag1.data
        tag2 = form.tag2.data
        tag3 = form.tag3.data
        extras = form.extras.data

        connect.execute('INSERT OR IGNORE INTO categories(cat) VALUES(?)', (category,))

        if str(tag1).isalpha:
            connect.execute('INSERT OR IGNORE INTO tags (tag) VALUES (?)', (tag1,))
        if str(tag2).isalpha:
            connect.execute('INSERT OR IGNORE INTO tags (tag) VALUES (?)', (tag2,))
        if str(tag3).isalpha:
            connect.execute('INSERT OR IGNORE INTO tags (tag) VALUES (?)', (tag3,))
        connect.commit()

        connect.execute('UPDATE apps SET name=?, category=?, description=?, internal_url=?, external_url=?, icon=?, extras=?\
            WHERE id=?', (appName, category, description, internal_url, external_url, icon_path, extras, id))

        connect.commit()
        connect.close()

        return redirect(url_for('list'))


    return render_template('edit.html', form=form)



@app.route('/add', methods=['GET', 'POST'])
def add():
    form = AppForm()
    if form.validate_on_submit():
        connect = get_db_connection()
        appName = form.name.data
        category = form.category.data
        description = form.description.data
        internal_url = form.internal_url.data
        external_url = form.external_url.data
        upload_file = form.icon.data
        filename = secure_filename(upload_file.filename)
        icon_path = os.path.join(app.config['UPLOAD_PATH'], filename)
        upload_file.save(icon_path)
        tag1 = form.tag1.data
        tag2 = form.tag2.data
        tag3 = form.tag3.data
        extras = form.extras.data

        connect.execute('INSERT OR IGNORE INTO categories(cat) VALUES(?)', (category,))

        if str(tag1).isalpha:
            connect.execute('INSERT OR IGNORE INTO tags (tag) VALUES (?)', (tag1,))
        if str(tag2).isalpha:
            connect.execute('INSERT OR IGNORE INTO tags (tag) VALUES (?)', (tag2,))
        if str(tag3).isalpha:
            connect.execute('INSERT OR IGNORE INTO tags (tag) VALUES (?)', (tag3,))
        connect.commit()

        connect.execute('INSERT OR IGNORE INTO apps (name, category, description, internal_url, external_url, icon, extras)\
            VALUES (?, ?, ?, ?, ?, ?, ?)', (appName, category, description, internal_url, external_url, icon_path, extras))

        myapp = connect.execute('SELECT id,name FROM apps where name=?', (appName,)).fetchall()[0]

        if myapp['id'] > -1:
            if str(tag1).isalpha:
                t = connect.execute('SELECT id, tag FROM tags WHERE tag=?', (tag1,)).fetchall()[0]
                print ("print t: " + str(t['tag']))
                connect.execute('INSERT INTO app_tags(app_id, tag_id) VALUES(?, ?)', (myapp['id'], t['id']))
            if str(tag2).isalpha:
                t = connect.execute('SELECT id, tag FROM tags WHERE tag=?', (tag2,)).fetchall()[0]
                print ("print t: " + str(t['tag']))
                connect.execute('INSERT INTO app_tags(app_id, tag_id) VALUES(?, ?)', (myapp['id'], t['id']))
            if str(tag3).isalpha:
                t = connect.execute('SELECT id, tag FROM tags WHERE tag=?', (tag3,)).fetchall()[0]
                print ("print t: " + str(t['tag']))
                connect.execute('INSERT INTO app_tags(app_id, tag_id) VALUES(?, ?)', (myapp['id'], t['id']))
            
        connect.commit()
        connect.close()

        return redirect(url_for('index'))
        

    return render_template('add.html', form=form, title='App Form')

@app.route('/get_data')
def get_data():
    connect = get_db_connection()
    apps = connect.execute('SELECT a.id, a.category, a.name, a.internal_url, a.external_url, a.description, a.icon, a.alive, a.extras\
                            FROM apps a ORDER BY a.category').fetchall()
    
    data = {}
    for app in apps:
        data[app['name']] = data['alive']

    connect.commit()
    connect.close()
    # global database_value
    return jsonify({'value': data})


if __name__ == '__main__':
    app.run(debug=True)
