#!/usr/bin/env bash
source ./env/bin/activate
pip install -r requirements.txt
if ! test -f ./database.db; then
  python init_db.py
fi
gunicorn -w $(nproc) --threads 2 --max-requests 2 app:app


