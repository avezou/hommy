import sqlite3

connection = sqlite3.connect('./backend/database.db')


with open('./backend/schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO apps (name, internal_url) VALUES (?, ?)", ('Nextcloud','http://localhost;237'))
cur.execute("INSERT INTO apps (name, internal_url) VALUES (?, ?)", ('Dashy','http://192.168.200.3'))

cur.execute("INSERT INTO tags (app_id, tag) VALUES (?, ?)",
            (1, 'ToolsTag')
            )
cur.execute("INSERT INTO tags (app_id, tag) VALUES (?, ?)",
            (1, 'FilesTag')
            )
cur.execute("INSERT INTO tags (app_id, tag) VALUES (?, ?)",
            (1, 'UtilTag')
            )

cur.execute("INSERT INTO tags (app_id, tag) VALUES (?, ?)",
            (2, 'DashTag')
            )
cur.execute("INSERT INTO tags (app_id, tag) VALUES (?, ?)",
            (2, 'MeshTag')
            )

connection.commit()
connection.close()