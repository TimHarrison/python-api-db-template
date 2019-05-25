'''
Created on Dec 26, 2018

@author: tim
'''
from lib.util.calculator import calculate_cost

class ProductResponse():
    
    def __init__(self, products, markup):
        self.products = products
        self.markup = markup

    
    def to_dict(self):
        rv = []
        for product in self.products:
            product = product.to_dict()
            markup = float(self.markup)
            base_cost = product['base_cost']
            product['cost'] = calculate_cost(base_cost, markup)
            product.pop("base_cost")
            rv.append(product)
        return rv


class PhotographerProductResponse():
    
    def __init__(self, products, markup):
        self.products = products
        self.markup = markup

    
    def to_dict(self):
        rv = []
        for product in self.products:
            product = product.to_dict()
            markup = float(self.markup)
            base_cost = product['base_cost']
            product['cost'] = calculate_cost(base_cost, markup)
            product['markup'] = markup
            rv.append(product)
        return rv

