import pathlib
import sqlite3

from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap

from config import Config
from forms import AppForm

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
    apps = execute_query('SELECT a.id, a.category, a.name, a.internal_url, a.external_url, \
    a.description, a.icon, a.alive, a.extras\
                            FROM apps a ORDER BY a.category')
    if len(apps) == 0:
        return []
    new_app = {}
    search_apps = ''
    for my_app in apps:
        search_apps = my_app['name'].lower()
        tags = execute_query('SELECT a.id, a.tag\
                            FROM tags a \
                            JOIN app_tags at\
                            ON a.id = at.tag_id \
                            WHERE at.app_id = ? ORDER BY a.tag', (my_app['id'],))

        new_app[my_app] = tags

    all_tags = execute_query('SELECT a.id, a.tag\
                            FROM tags a ORDER BY a.tag')
    all_categories = execute_query('SELECT c.cat\
                            FROM categories c ORDER BY c.cat')
    return new_app, all_tags, all_categories, search_apps


@app.route('/')
def index():
    res = get_apps()
    if len(res) <= 0:
        return render_template('index.html')
    return render_template('index.html', apps=res[0], tags=res[1], categories=res[2], appNames=res[3])


@app.route('/list', methods=['GET', 'POST'])
def list_apps():
    res = get_apps()
    if len(res) <= 0:
        return render_template('index.html')
    return render_template('list.html', apps=res[0])


@app.route('/delete/<int:id>')
def delete(app_id):
    execute_query('DELETE FROM apps WHERE id =?', (app_id,))
    execute_query('DELETE FROM app_tags WHERE app_id =?', (app_id,))
    # orphaned_tags = execute_query('DELETE from tags WHERE id NOT IN (SELECT tag_id FROM app_tags) RETURNING id')
    return redirect(url_for('list'))


@app.route('/app', methods=['GET', 'POST'])
@app.route('/app/<int:app_id>', methods=['GET', 'POST'])
def manage_app(app_id=None):
    form = AppForm()
    is_add = app_id is None
    if app_id:
        db_app = execute_query('SELECT * FROM apps WHERE id =?', (app_id,), one=True)
        db_tags = execute_query('SELECT tag FROM tags t JOIN app_tags a ON a.tag_id = t.id WHERE a.app_id =?', (app_id,))
        tag_list = [tag['tag'] for tag in db_tags]
        form.tags.data = ','.join(tag_list)
        form.name.data = db_app['name']
        form.category.data = db_app['category']
        form.description.data = db_app['description']
        form.internal_url.data = db_app['internal_url']
        form.external_url.data = db_app['external_url']
        form.extras.data = db_app['extras']
        form.icon.data = db_app['icon']
    else:
        tag_list = []

    all_tags = execute_query('SELECT tag FROM tags')
    ttag = [t['tag'] for t in all_tags]

    if form.validate_on_submit():
        app_name = form.name.data
        category = form.category.data
        description = form.description.data
        internal_url = form.internal_url.data
        external_url = form.external_url.data
        extras = form.extras.data
        icon = form.icon.data
        tags = form.tags.data.split(',')

        if app_id:
            # Update existing app
            execute_query(
                'UPDATE apps SET name=?, category=?, description=?, internal_url=?, external_url=?, icon=?, extras=? WHERE id=?',
                (app_name, category, description, internal_url, external_url, icon, extras, app_id))
            execute_query('DELETE FROM app_tags WHERE app_id=?', (app_id,))
        else:
            # Add new app
            execute_query('INSERT INTO apps (name, category, description, internal_url, external_url, icon, extras) VALUES (?, ?, ?, ?, ?, ?, ?)',
                          (app_name, category, description, internal_url, external_url, icon, extras))
            app_id = execute_query('SELECT id FROM apps WHERE name=?', (app_name,), one=True)['id']

        for tag in tags:
            execute_query('INSERT OR IGNORE INTO tags (tag) VALUES (?)', (tag.strip(),))
            tag_id = execute_query('SELECT id FROM tags WHERE tag=?', (tag.strip(),), one=True)['id']
            execute_query('INSERT INTO app_tags (app_id, tag_id) VALUES (?, ?)', (app_id, tag_id))

        return redirect(url_for('index') if is_add else url_for('list_apps'))

    return render_template('edit.html', form=form, icons=get_icon_list(), tags=ttag)


def get_icon_list():
    svg_dir = pathlib.Path('static/images/svg')
    icons = []
    for item in svg_dir.iterdir():
        if item.is_file():
            ico = item.name.split('.')[0]
            icons.append(ico)
    return icons



if __name__ == '__main__':
    app.run(debug=True)
