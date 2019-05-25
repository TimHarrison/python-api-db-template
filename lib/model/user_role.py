'''
Created on Dec 28, 2018

@author: tim
'''
from application import app
from lib.model import db

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

class UserRole(db.Model):
    __tablename__ = "user_role"
    id = db.Column(db.Integer, primary_key=True)  # @UndefinedVariable
    role_name = db.Column(db.String(80), unique=True, nullable=False)  # @UndefinedVariable

    def get_id(self):
        return self.id


    def get_role_name(self):
        return self.role_name


    def set_role_name(self, value):
        self.role_name = value


    def to_dict(self):
        rv = {"id": self.get_id(),
              "role_name" : self.get_role_name()}
        return rv


if __name__ == '__main__':
    manager.run()