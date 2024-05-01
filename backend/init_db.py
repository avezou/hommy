import sqlite3

connection = sqlite3.connect('./backend/database.db')


with open('./backend/schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO apps (name, internal_url) VALUES (?, ?)", ('Nextcloud','http://localhost;237'))
cur.execute("INSERT INTO apps (name, internal_url) VALUES (?, ?)", ('Dashy','http://192.168.200.3'))

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