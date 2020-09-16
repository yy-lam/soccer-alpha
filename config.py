import os
from dotenv import load_dotenv

# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))
class Config(object):
    # Enable debug mode.

    # Secret key for session management. You can generate random strings here:
    # https://randomkeygen.com/
    SECRET_KEY = 'SECRET'

    # Connect to the database: provide your database url
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql+psycopg2://acount:password@localhost:5432/socceralpha'


    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')

