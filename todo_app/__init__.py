from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
import os






secret_key = os.urandom(24).hex()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = secret_key
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from todo_app import routes