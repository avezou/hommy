import sqlite3

connection = sqlite3.connect('./backend/database.db')


with open('./backend/schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO apps (name, internal_url) VALUES (?, ?)", ('Nextcloud','http://localhost;237'))
cur.execute("INSERT INTO apps (name, internal_url) VALUES (?, ?)", ('Dashy','http://192.168.200.3'))

cur.execute("INSERT INTO tags (app_id, name) VALUES (?, ?)",
            (1, 'Tools')
            )

cur.execute("INSERT INTO tags (app_id, name) VALUES (?, ?)",
            (2, 'Dash')
            )

connection.commit()
connection.close()