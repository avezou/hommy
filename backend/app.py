import sqlite3
from itertools import groupby
from flask import Flask, render_template, request


app = Flask(__name__, template_folder='../frontend/templates')
app.config['SECRET_KEY'] = 'this should be a secret random string'


def get_db_connection():
    connect = sqlite3.connect('./backend/database.db')
    connect.row_factory = sqlite3.Row
    return connect



@app.route('/')
# @app.route('/home')
def index():
    connect = get_db_connection()
    apps = connect.execute('SELECT a.id, a.name, a.internal_url, a.external_url, a.description, a.icon, a.alive\
                            FROM apps a').fetchall()


    newapp = {}
    for app in apps:
        try:
            response = request.get(app['internal_url'])
            if response.ok:
                app['alive'] = 1
            else:
                app['alive'] = 0
        except Exception as e:
            print("Failure: {e}.")

        print(str(app['id']) + str(app['name']))

        tags = connect.execute('SELECT a.id, a.tag\
                            FROM tags a \
                            JOIN app_tags at\
                            ON a.id = at.tag_id \
                            WHERE at.app_id = ?', (app['id'],)).fetchall()
        newapp[app] = tags
        for tag in tags:
            print ("tag: " + str(tag['tag']))
    

    connect.close()
    return render_template('index.html', apps=newapp) 
    # return render_template('index.html')





if __name__ == '__main__':
    app.run(debug=True)