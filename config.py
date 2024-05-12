# from os import environ
# SECRET_KEY=environ.get('SECRET_KEY')

import os
from dotenv import load_dotenv
load_dotenv()


class Config(object):
    SECRET_KEY = os.getenv('SECRET_KEY') or 'DefaultEasyToGuessKeyHere$@*&#56374'
    UPLOAD_PATH = os.getenv('UPLOAD_PATH') or '/home/avezou/git/hommy/'