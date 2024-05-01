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
    tags = connect.execute('SELECT t.name, a.name, a.description, a.internal_url, a.external_url, a.icon, a.alive FROM tags t INNER JOIN apps a ON t.app_id = a.id').fetchall()

    apps = {}
    for k, g in groupby(tags, lambda x: x['name']):
        apps[k] = list(g)

    connect.close()
    return render_template('index.html', apps=apps) 


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        connect = sqlite3.connect('data.db')
        name = request.form['name']
        internal_url = request.form['internal_url']
        external_url = request.form['external_url']
        icon = request.form['icon']
        description = request.form['description']
        alive = False
        connect.execute(
            'INSERT INTO data (name, link, icon, description, alive) VALUES (?,?,?,?,?)', (name, link, icon, description, alive))
        connect.commit()
        return render_template('index.html')
    else:
        return render_template('add.html')


@app.route('/dash')
def apps():
    connect = sqlite3.connect('data.db')
    cursor = connect.execute('SELECT * FROM data')
    data = cursor.fetchall()
    return render_template('dash.html', data=data)


if __name__ == '__main__':
    app.run(debug=True)