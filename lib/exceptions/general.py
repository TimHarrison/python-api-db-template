'''
Created on Dec 26, 2018

@author: tim
'''
from .error_types import ErrorTypes

class NoPermissions(Exception):
    def __init__(self, payload=None, message=None):
        Exception.__init__(self)
        if message is None:
            self.message = "You do not have the permissions to perform this action."
        else:
            self.message = message
        self.type = ErrorTypes.FORBIDDEN
        self.status_code = 403
        self.payload = payload


    def to_dict(self):
        rv = {}
        if self.payload:
            rv['original_request'] = self.payload
        rv['type'] = self.type
        rv['message'] = self.message
        return rv


class MissingFields(Exception):
    def __init__(self, payload, fields):
        Exception.__init__(self)
        self.message = "Missing field(s): "
        missing = []
        for field in fields:
            try:
                if payload[field] == None:
                    raise KeyError
            except KeyError:
                missing.append(field)
        missing_fields = ", ".join(missing)
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