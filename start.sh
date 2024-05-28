#!/usr/bin/env bash
deactivate
if [ ! -d ./env ]; then
  python3 -m venv env
fi
source ./env/bin/activate
pip install -r requirements.txt
if ! test -f ./database.db; then
  ./env/bin/python init_db.py
fi
./env/bin/gunicorn -w $(nproc) --threads 2 --max-requests 2 app:app --bind 0.0.0.0:8000


