'''
Created on Dec 26, 2018

@author: tim
'''
class GalleryResponse():
    
    def __init__(self, name, owner, reference_code, is_password_protected):
        self.name = name
        self.owner = owner
        self.reference_code = reference_code
        self.is_password_protected = is_password_protected

    
    def to_dict(self):
        rv = {}
        rv['name'] = self.name
        rv['owner'] = self.owner
        rv['reference_code'] = self.reference_code
        rv['is_password_protected'] = self.is_password_protected
        return rv


class GalleryImagesResponse():
    
    def __init__(self, gallery, images):
        self.gallery = gallery
        self.images = images

    
    def to_dict(self):
        rv = self.gallery.to_dict()
        rv['images'] = []
        for image in self.images:
            rv['images'].append(image.to_dict())
        return rv