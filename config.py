import os

# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    # Enable debug mode.

    # Secret key for session management. You can generate random strings here:
    # https://randomkeygen.com/
    SECRET_KEY = 'SECRET'

    # Connect to the database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
            'postgresql+psycopg2://postgres:pg1639@localhost:5432/soccer' 

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
