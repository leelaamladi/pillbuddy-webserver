from flask import Flask
from mongoengine import connect
from flask.ext.mongoengine import MongoEngine
from flask.ext.bcrypt import Bcrypt
import os

# create our little application
app = Flask(__name__)
bcrypt = Bcrypt(app)

# App Config
# if running from Heroku, grab config from environment variables
# else, load from settings.py file
if os.environ.get('HEROKU'):
	app.config['DEBUG'] = False
	app.config['PORT'] = int(os.environ.get("PORT", 5000))
	app.config['DB'] = str(os.environ.get('DB_NAME', None))
	app.config['DB_USERNAME'] = str(os.environ.get('DB_USERNAME', None))
	app.config['DB_PASSWORD'] = str(os.environ.get('DB_PASSWORD', None))
	app.config['DB_HOST'] = str(os.environ.get('DB_HOST_ADDRESS', None))
	app.config['DB_PORT'] = int(os.environ.get("PORT", None))
else:
	app.config.from_pyfile('settings.cfg')
	app.config['DEBUG'] = True
	app.config['PORT'] = 5000

# connect to the database
DB          = app.config['DB']
DB_USERNAME = app.config['DB_USERNAME']
DB_PASSWORD = app.config['DB_PASSWORD']
DB_HOST     = app.config['DB_HOST']
DB_PORT     = app.config['DB_PORT']
connect(DB, host=DB_HOST, username=DB_USERNAME, password=DB_PASSWORD, port=DB_PORT)

from app.views import general, followers, prescriptions
