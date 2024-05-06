import sqlite3
import requests
import atexit
from itertools import groupby
from flask import Flask, render_template, request
from sched import scheduler
from apscheduler.schedulers.background import BackgroundScheduler


app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = 'this should be a secret random string'



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


@app.route('/')
# @app.route('/home')
def index():
    connect = get_db_connection()
    apps = connect.execute('SELECT a.id, a.category, a.name, a.internal_url, a.external_url, a.description, a.icon, a.alive, a.extras\
                            FROM apps a').fetchall()


    newapp = {}
    for myapp in apps:
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
                            WHERE at.app_id = ?', (myapp['id'],)).fetchall()
        category = connect.execute('SELECT c.cat\
                            FROM apps a\
                            JOIN categories c\
                            ON a.category = c.cat').fetchall()[0]
        
        newapp[myapp] = tags

        
    allTags = connect.execute('SELECT a.id, a.tag\
                            FROM tags a').fetchall()
    allCategories = connect.execute('SELECT c.cat\
                            FROM categories c').fetchall()
    
    connect.commit()
    connect.close()
    return render_template('index.html', apps=newapp, tags=allTags, categories=allCategories, appNames=searchApps) 


@app.route('/edit', methods=['GET', 'POST'])
def edit():
    if request.method == 'POST':
        connect = get_db_connection()
        connect.execute('UPDATE apps SET name =?, internal_url =?, external_url =?, description =?, icon =? WHERE id =?', (request.form['name'], request.form['internal_url'], request.form['external_url'], request.form['description'], request.form['icon'], request.form['id']))
        connect.commit()
        connect.close()
        return redirect(url_for('index'))
    else:
        connect = get_db_connection()
        app = connect.execute('SELECT * FROM apps WHERE id =?', (request.args.get('id'),)).fetchone()
        tags = connect.execute('SELECT a.id, a.tag\
                            FROM tags a \
                            JOIN app_tags at\
                            ON a.id = at.tag_id \
                            WHERE at.app_id = ?', (app['id'],)).fetchall()
        connect.close()
        return render_template('edit.html', app=app, tags=tags)


if __name__ == '__main__':
    app.run(debug=True)
