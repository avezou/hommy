import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO categories (cat) VALUES (?)", ('Hypervisors',))

cur.execute("INSERT INTO apps (name, category, internal_url, icon) VALUES (?, ?, ?, ?)", ('Sample', 'Hypervisors','https://example.com', 'https://example.com/icon.png'))

cur.execute("INSERT INTO tags (tag) VALUES (?)", ('Utils',))

cur.execute("INSERT INTO app_tags (app_id, tag_id) VALUES (?, ?)",(1, 1))


connection.commit()
connection.close()
