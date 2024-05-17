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


@app.route('/edit/<int:app_id>', methods=['GET', 'POST'])
def edit(app_id):
    form = AppForm()
    db_app = execute_query('SELECT * FROM apps WHERE id =?', (app_id,), one=True)
    db_tags = execute_query('SELECT tag FROM tags t JOIN app_tags a ON a.tag_id = t.id WHERE a.app_id =?', (app_id,))
    tag_list = [tag['tag'] for tag in db_tags]
    # all_tags = execute_query('SELECT tag FROM tags')

    if form.validate_on_submit():
        # Extract form data
        app_name = form.name.data
        category = form.category.data
        description = form.description.data
        internal_url = form.internal_url.data
        external_url = form.external_url.data
        extras = form.extras.data
        icon = form.icon.data

        # Process tags from the form
        tags = form.tags.data.split(',')

        execute_query('DELETE FROM tags WHERE EXISTS (SELECT * FROM app_tags WHERE tags.id = app_tags.tag_id AND app_tags.app_id=?)', (app_id,))
        execute_query('DELETE FROM tags WHERE tags.id NOT IN (SELECT tag_id FROM app_tags)')

        for tag in tags:
            execute_query('INSERT OR IGNORE INTO tags (tag) VALUES (?)', (tag.strip(),))

        # Update app data in the database
        execute_query(
            'UPDATE apps SET name=?, category=?, description=?, internal_url=?, external_url=?, icon=?, '
            'extras=? WHERE id=?',
            (app_name, category, description, internal_url, external_url, icon, extras, app_id))

        myapp = execute_query('SELECT id,name FROM apps where name=?', (app_name,), one=True)        

        if myapp['id'] > -1:
            for tag in tags:
                t = execute_query('SELECT id, tag FROM tags WHERE tag=?', (tag,), one=True)
                execute_query('INSERT INTO app_tags(app_id, tag_id) VALUES(?, ?)', (myapp['id'], t['id']))

        return redirect(url_for('list_apps'))

    form.tags.data = ','.join(tag_list)
    form.name.data = db_app['name']
    form.category.data = db_app['category']
    form.description.data = db_app['description']
    form.internal_url.data = db_app['internal_url']
    form.external_url.data = db_app['external_url']
    form.extras.data = db_app['extras']
    form.icon.data = db_app['icon']

    return render_template('edit.html', form=form, icons=get_icon_list())


def get_icon_list():
    svg_dir = pathlib.Path('static/images/svg')
    icons = []
    for item in svg_dir.iterdir():
        if item.is_file():
            ico = item.name.split('.')[0]
            icons.append(ico)
    return icons


@app.route('/add', methods=['GET', 'POST'])
def add():
    form = AppForm()
    app_tags = []
    if form.validate_on_submit():

        app_name = form.name.data
        category = form.category.data
        description = form.description.data
        internal_url = form.internal_url.data
        external_url = form.external_url.data
        tags = form.tags.data
        extras = form.extras.data
        icon = form.icon.data

        execute_query('INSERT OR IGNORE INTO apps (name, category, description, internal_url, external_url, icon, extras)\
                    VALUES (?, ?, ?, ?, ?, ?, ?)',
                      (app_name.strip(), category, description, internal_url, external_url, icon, extras))

        myapp = execute_query('SELECT id,name FROM apps where name=?', (app_name,), one=True)

        if len(tags) > 0:
            if ',' in tags:
                app_tags = tags.split(',')
                for tag in app_tags:
                    execute_query('INSERT OR IGNORE INTO tags (tag) VALUES (?)', (tag.strip(),))
                    db_tag = execute_query("SELECT id FROM tags WHERE tag=?", (tag,))
                    execute_query('INSERT INTO app_tags(app_id, tag_id) VALUES(?, ?)', (myapp['id'], db_tag['id']))
            else:
                execute_query('INSERT OR IGNORE INTO tags (tag) VALUES (?)', (tags,))
                tag = execute_query("SELECT id FROM tags WHERE tag=?", (tags.strip(),))[0]
                execute_query('INSERT INTO app_tags(app_id, tag_id) VALUES(?, ?)', (myapp['id'], tag['id']))

        return redirect(url_for('index'))

    return render_template('add.html', form=form, title='App Form', items=app_tags, icons=get_icon_list())


if __name__ == '__main__':
    app.run(debug=True)

 #
 # <form method=post>
 #          <dl>
 #            {{ render_field(form.post_title) }}
 #            {{ render_field(form.post_genre) }}
 #            {{ render_field(form.body) }}
 #          </dl>
 #          <p><input type=submit value=Post>
 #        </form>