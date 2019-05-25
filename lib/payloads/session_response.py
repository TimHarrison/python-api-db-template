'''
Created on Dec 26, 2018

@author: tim
'''

class SessionResponse():
    
    def __init__(self, user, organization_id, access_token, refresh_token):
        self.user = user
        self.organization_id = organization_id
        self.access_token = access_token
        self.refresh_token = refresh_token

    
    def to_dict(self):
        rv = dict(self.user or ())
        rv['organization_id'] = self.organization_id
        rv['access_token'] = self.access_token
        rv['refresh_token'] = self.refresh_token
        return rv