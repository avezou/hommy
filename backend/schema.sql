DROP TABLE IF EXISTS apps;
DROP TABLE IF EXISTS tags;

CREATE TABLE apps (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    name text, 
    description text DEFAULT "", 
    internal_url url, 
    external_url url DEFAULT "", 
    icon url DEFAULT "", 
    alive bool DEFAULT 0, 
    tags text DEFAULT ""
);

CREATE TABLE tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    name text,
    app_id INTEGER DEFAULT 0, 
    FOREIGN KEY (app_id) REFERENCES apps(id)
);