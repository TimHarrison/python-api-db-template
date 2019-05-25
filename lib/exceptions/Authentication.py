'''
Created on Dec 26, 2018

@author: tim
'''
from .error_types import ErrorTypes

class UserExists(Exception):
    status_code = 400
    
    def __init__(self, message="User already exists.", status_code=400, payload=None):
        Exception.__init__(self)
        self.message = message
        self.type = ErrorTypes.ERROR
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload


    def to_dict(self):
        rv = dict(self.payload or ())
        rv['type'] = self.type
        rv['message'] = self.message
        return rv


class UserLoginFailed(Exception):
    def __init__(self, message="User login failed.", status_code=403, payload=None):
        Exception.__init__(self)
        self.message = message
        self.type = ErrorTypes.ERROR
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload


    def to_dict(self):
        rv = dict(self.payload or ())
        rv['type'] = self.type
        rv['message'] = self.message
        return rv


class InvalidCreateUserPayload(Exception):
    def __init__(self, payload):
        Exception.__init__(self)
        self.message = "Missing field(s): "
        fields = []
        try:
            if payload['username'] == None:
                raise KeyError
        except KeyError:
            fields.append("username")
        try:
            if payload['password'] == None:
                raise KeyError
        except KeyError:
            fields.append("password")
        try:
            if payload['email'] == None:
                raise KeyError
        except KeyError:
            fields.append("email")
        try:
            if payload['name'] == None:
                raise KeyError
        except KeyError:
            fields.append("name")
        missing_fields = ", ".join(fields)
        self.message += missing_fields
        self.type = ErrorTypes.VALIDATION_ERROR
        self.status_code = 400
        self.payload = payload


    def to_dict(self):
        rv = {}
        rv['original_request'] = self.payload
        rv['type'] = self.type
        rv['message'] = self.message
        return rv


class InvalidLoginPayload(Exception):
    def __init__(self, payload):
        Exception.__init__(self)
        self.message = "Missing field(s): "
        fields = []
        try:
            payload['username']
        except KeyError:
            fields.append("username")
        try:
            payload['password']
        except KeyError:
            fields.append("password")
        missing_fields = ", ".join(fields)
        self.message += missing_fields
        self.type = ErrorTypes.VALIDATION_ERROR
        self.status_code = 400
        self.payload = payload


    def to_dict(self):
        rv = {}
        rv['original_request'] = self.payload
        rv['type'] = self.type
        rv['message'] = self.message
        return rv


class InvalidUserType(Exception):
    def __init__(self, payload):
        Exception.__init__(self)
        self.message = "Not a valid user type."
        self.type = ErrorTypes.VALIDATION_ERROR
        self.status_code = 400
        self.payload = payload


    def to_dict(self):
        rv = {}
        rv['original_request'] = self.payload
        rv['type'] = self.type
        rv['message'] = self.message
        return rv