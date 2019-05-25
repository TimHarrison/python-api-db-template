'''
Created on Dec 26, 2018

@author: tim
'''
from application import app
from datetime import timedelta

app.config['JWT_SECRET_KEY'] = 'replace-this-with-random-text-numbers-and-symbols'
app.config['SECRET_KEY'] = 'replace-this-with-random-text-numbers-and-symbols'
app.config['JWT_REFRESH_JSON_KEY'] = 'refresh_token'
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=365)
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=10)
app.config['JWT_ALGORITHM'] = 'HS256'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password!@localhost/schema'