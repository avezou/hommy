import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO categories (cat) VALUES (?)", ('General',))
cur.execute("INSERT INTO categories (cat) VALUES (?)", ('Hosts',))
cur.execute("INSERT INTO categories (cat) VALUES (?)", ('Business',))
cur.execute("INSERT INTO categories (cat) VALUES (?)", ('Media',))
cur.execute("INSERT INTO categories (cat) VALUES (?)", ('Social',))
cur.execute("INSERT INTO categories (cat) VALUES (?)", ('Development',))
cur.execute("INSERT INTO categories (cat) VALUES (?)", ('Virtualization',))
cur.execute("INSERT INTO categories (cat) VALUES (?)", ('Docker',))
cur.execute("INSERT INTO categories (cat) VALUES (?)", ('System',))
cur.execute("INSERT INTO categories (cat) VALUES (?)", ('Networking',))

cur.execute("INSERT INTO apps (name, category, internal_url, icon) VALUES (?, ?, ?, ?)", ('Sample', 'General','https://example.com', 'duckduckgo'))

cur.execute("INSERT INTO tags (tag) VALUES (?)", ('Utils',))

cur.execute("INSERT INTO app_tags (app_id, tag_id) VALUES (?, ?)",(1, 1))


connection.commit()
connection.close()
