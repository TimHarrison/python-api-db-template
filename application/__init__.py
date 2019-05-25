'''
Created on Dec 26, 2018

@author: tim
'''
from flask import Flask
import click
from flask.cli import AppGroup, with_appcontext

app = Flask(__name__)

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('application.default_settings')
app.config.from_pyfile('application.cfg', silent=True)

#===============================================================================
# Imports to trigger db migration scripts
#===============================================================================
import lib.views.authentication
import lib.model.users
import lib.model.user_role