# from os import environ
# SECRET_KEY=environ.get('SECRET_KEY')

import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'DefaultEasyToGuessKeyHere$@*&#56374'
    UPLOAD_PATH = os.environ.get('UPLOAD_PATH')