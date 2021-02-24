import os
from flask import Flask
# import enum
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__)

app.config['SECRET_KEY'] = '67ad1fad9b01f8012b84e740919bb81d'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
# setup of the mail server and related variables
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')
email = os.environ.get('EMAIL_USER')
mail = Mail(app)

from flaskjournal.users.routes import users
from flaskjournal.posts.routes import posts
from flaskjournal.main.routes import main

app.register_blueprint(users)
app.register_blueprint(posts)
app.register_blueprint(main)



