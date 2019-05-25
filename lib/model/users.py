'''
Created on Dec 23, 2018

@author: tim
'''
from passlib.apps import custom_app_context as pwd_context
from application import app
from lib.model import db

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql import func
import enum

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

class UserRole(enum.Enum):
    admin = 1
    user = 2

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)  # @UndefinedVariable
    username = db.Column(db.String(80), unique=True, nullable=False)  # @UndefinedVariable
    password = db.Column(db.String(120), nullable=False)  # @UndefinedVariable
    email = db.Column(db.String(120), unique=True, nullable=False)  # @UndefinedVariable
    full_name = db.Column(db.String(80), nullable=False)  # @UndefinedVariable
    phone_number = db.Column(db.String(15))  # @UndefinedVariable
    system_role = db.Column(db.Enum(UserRole), nullable=False)  # @UndefinedVariable
    organization_id = db.Column(db.Integer, ForeignKey('organization.id'))  # @UndefinedVariable
    created_date = db.Column(db.DateTime(timezone=True), server_default=func.now())  # @UndefinedVariable
    updated_date = db.Column(db.DateTime(timezone=True), onupdate=func.now())  # @UndefinedVariable

    def get_id(self):
        return self.id


    def get_username(self):
        return self.username


    def get_password(self):
        return self.password


    def get_email(self):
        return self.email


    def get_full_name(self):
        return self.full_name


    def get_role(self):
        return self.role


    def get_organization_id(self):
        return self.organization_id


    def get_created_date(self):
        return self.created_date


    def get_updated_date(self):
        return self.updated_date


    def set_username(self, value):
        self.username = value


    def set_password(self, value):
        self.password = value


    def set_email(self, value):
        self.email = value


    def set_full_name(self, value):
        self.full_name = value


    def set_role(self, value):
        self.role = value


    def set_organization_id(self, value):
        self.organization_id = value


    def hash_password(self, password):
        return pwd_context.encrypt(password)


    def verify_password(self, password):
        return pwd_context.verify(password, self.password)


    def to_dict(self):
        rv = {"id": self.get_id(),
              "username": self.get_username(),
              "full_name": self.get_full_name(),
              "email": self.get_email(),
              "role": self.get_role(),
              "organization_id": self.get_organization_id(),
              "created_date": self.get_created_date(),
              "updated_date": self.get_updated_date()}
        return rv


if __name__ == '__main__':
    manager.run()