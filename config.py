import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or \
        '3dcac6feb7d70d6d6396175e9857de87'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://postgres:postgresdatabase@localhost/Homey'
    SQLALCHEMY_TRACK_MODIFICATIONS = False