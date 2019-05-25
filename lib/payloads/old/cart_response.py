'''
Created on Dec 26, 2018

@author: tim
'''
class CartResponse():
    
    def __init__(self, cart, cart_items):
        self.cart = cart
        self.cart_items = cart_items

    
    def to_dict(self):
        rv = self.cart.to_dict()
        rv['items'] = []
        rv['item_count'] = 0
        rv['cart_total'] = 0
        for item in self.cart_items:
            rv['item_count'] += item.get_quantity()
            rv['cart_total'] += item.get_total_cost()
            rv['items'].append(item.to_dict())
        return rv