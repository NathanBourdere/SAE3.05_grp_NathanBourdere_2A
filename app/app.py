from flask import Flask,render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user
import os
import csv

def mkpath(p):
    return os.path.normpath(os.path.join(os.path.dirname(__file__),p))

# Configuration de l'application Flask et la base de données
app=Flask(__name__)
app.config['SECRET_KEY'] = "IUTO"
app.app_context().push()
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = ('sqlite:///'+mkpath('../db.sqlite3'))
db = SQLAlchemy(app)
