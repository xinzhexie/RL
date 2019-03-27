#!/usr/bin/python

from bintrees import FastRBTree

from orderList import OrderList
from order import Order

class Tree(object):
    def __init__(self):
        self.price_tree = FastRBTree()
        self.volume = 0
        self.price_map = {}  # Map from price -> order_list object
        self.order_map = {}  # Order ID to Order object
        self.min_price = None
        self.max_price = None
        #self.maxp = []
        #self.minp = []

    def __len__(self):
        return len(self.order_map)

    def get_price(self, price):
        return self.price_map[price]

    def get_order(self, id_num):
        return self.order_map[id_num]

    def create_price(self, price):
        new_list = OrderList()
        self.price_tree.insert(price, new_list)
        self.price_map[price] = new_list
        if self.max_price == None or price > self.max_price:
            self.max_price = price
        if self.min_price == None or price < self.min_price:
            self.min_price = price
            '''
        if len(self.maxp) < 5:
            self.maxp.append(price)
        if len(self.minp) < 5:
            self.minp.append(price)
        if len(self.maxp) == 5 and price > min(self.maxp):
            self.maxp = sorted(self.maxp)
            self.maxp.pop()
            self.maxp.append(price)
            self.maxp = sorted(self.maxp)
        if len(self.minp) == 5 and price < max(self.minp):
            self.minp = sorted(self.minp, reverse = True)
            self.minp.pop()
            self.minp.append(price)
            self.minp = sorted(self.minp, reverse = True)
            '''
    def remove_price(self, price):
        self.price_tree.remove(price)
        del self.price_map[price]

        if self.max_price == price:
            try:
                self.max_price = max(self.price_tree)
            except ValueError:
                self.max_price = None
        if self.min_price == price:
            try:
                self.min_price = min(self.price_tree)
            except ValueError:
                self.min_price = None

    def price_exists(self, price):
        return price in self.price_map

    def order_exists(self, id_num):
        return id_num in self.order_map

    def insert_tick(self, tick):
        if tick.price not in self.price_map:
            self.create_price(tick.price)
        order = Order(tick, self.price_map[tick.price])
        self.price_map[order.price].append_order(order)
        self.order_map[order.id_num] = order
        self.volume += order.qty

    def update_order(self, tick):
        order = self.order_map[tick.id_num]
        original_volume = order.qty
        if tick.price != order.price:
            # Price changed
            order_list = self.price_map[order.price]
            order_list.remove_order(order)
            if len(order_list) == 0:
                self.remove_price(order.price)
            self.insert_tick(tick)
            self.volume -= original_volume
        else:
            # Quantity changed
            order.update_qty(tick.qty, tick.price)
            self.volume += order.qty - original_volume

    def remove_order_by_id(self, id_num):
        order = self.order_map[id_num]
        self.volume -= order.qty
        order.order_list.remove_order(order)
        if len(order.order_list) == 0:
            self.remove_price(order.price)
        del self.order_map[id_num]

    def max(self):
        return self.max_price

    def min(self):
        return self.min_price
    '''
    def maxpp(self):
        return self.maxp
    
    def minpp(self):
        return self.minp
'''