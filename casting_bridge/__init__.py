import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.restless import APIManager
from flask.ext.admin import Admin

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx','mov','mp4','mp3','wav'])

app = Flask(__name__)
#app.config['UPLOAD_FOLDER'] = os.path.realpath('/') + '/usr/data/uploads/'
app.config['UPLOAD_FOLDER'] = '/usr/data/uploads/'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////usr/data/cb.db'
app.config['WTF_CSRF_SECRET_KEY'] = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?ST'
app.config['USER'] = 'cb2016'
app.config['PIN'] = 'CB$%23kP?hUg'
db = SQLAlchemy(app)
manager = APIManager(app, flask_sqlalchemy_db=db)
admin = Admin(app)

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?FQ'

from casting_bridge.catalog.views import catalog
app.register_blueprint(catalog)

db.create_all()
