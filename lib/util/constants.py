'''
Created on Dec 28, 2018

@author: tim
'''
class UserRolesEnum:
    ADMIN = 1
    ORGANIZER = 2
    MEMBER = 3
    USER = 4
    
    ALL_ROLES = ['ADMIN']
    
    def role_id(self, role):
        return self.__get_attr__(role)