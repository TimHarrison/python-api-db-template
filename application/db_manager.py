'''
Created on Dec 26, 2018

@author: tim
'''
from application import app
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)