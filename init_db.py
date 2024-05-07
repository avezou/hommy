import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO categories (cat) VALUES (?)", ('Hypervisors',))
cur.execute("INSERT INTO categories (cat) VALUES (?)", ('Servers',))
cur.execute("INSERT INTO categories (cat) VALUES (?)", ('Business',))
cur.execute("INSERT INTO categories (cat) VALUES (?)", ('Services',))

cur.execute("INSERT INTO apps (name, category, internal_url, icon) VALUES (?, ?, ?, ?)", ('Nextcloud', 'Servers','https://example.com', 'https://imgs.sphl.cloud/xbkpyk.png'))
cur.execute("INSERT INTO apps (name, category, internal_url, icon) VALUES (?, ?, ?, ?)", ('Dashy', 'Business', 'https://yt3.sphl.cloud', 'https://imgs.sphl.cloud/gtxrs4.png'))

cur.execute("INSERT INTO tags (tag) VALUES (?)", ('ToolsTag',))
cur.execute("INSERT INTO tags (tag) VALUES (?)", ('UtilsTag',))
cur.execute("INSERT INTO tags (tag) VALUES (?)", ('FilesTag',))
cur.execute("INSERT INTO tags (tag) VALUES (?)", ('RemoteTag',))

cur.execute("INSERT INTO app_tags (app_id, tag_id) VALUES (?, ?)",(1, 1))
cur.execute("INSERT INTO app_tags (app_id, tag_id) VALUES (?, ?)",(1, 2))
cur.execute("INSERT INTO app_tags (app_id, tag_id) VALUES (?, ?)",(1, 3))
cur.execute("INSERT INTO app_tags (app_id, tag_id) VALUES (?, ?)",(2, 2))
cur.execute("INSERT INTO app_tags (app_id, tag_id) VALUES (?, ?)",(2, 4))


connection.commit()
connection.close()
