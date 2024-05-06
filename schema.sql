DROP TABLE IF EXISTS apps;
DROP TABLE IF EXISTS tags;
DROP TABLE IF EXISTS categories;
DROP TABLE IF EXISTS app_tags;

CREATE TABLE apps (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    category text NOT NULL,
    name text, 
    description text DEFAULT "", 
    internal_url url, 
    external_url url DEFAULT "", 
    icon url DEFAULT "", 
    alive bool DEFAULT 0,
    extras text,
    FOREIGN KEY(category) REFERENCES categories(cat)
    
);

CREATE TABLE tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    tag text
);

CREATE TABLE categories (
    cat text PRIMARY KEY
);

CREATE TABLE app_tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    app_id INTEGER,
    tag_id INTEGER,
    FOREIGN KEY(app_id) REFERENCES apps(id),
    FOREIGN KEY(tag_id) REFERENCES tags(id)
);
