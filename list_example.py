from itertools import groupby
from app import get_db_connection

connect = get_db_connection()

tags = connect.execute('SELECT t.tag, a.name, a.description, a.internal_url, a.external_url, a.icon, a.alive FROM tags t JOIN app_tags at ON t.id = at.tag_id JOIN apps a ON at.app_id = a.id ORDER BY a.name').fetchall()

apps = {}
for k, g in groupby(tags, lambda x: x['name']):
    apps[k] = list(g)

for list_, items in apps.items():
    print(list_)
    for item in items:
        print('    ', item['tag'])