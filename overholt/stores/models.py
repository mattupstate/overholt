# -*- coding: utf-8 -*-
"""
    overholt.stores.models
    ~~~~~~~~~~~~~~~~~~~~~~

    Store models
"""

from ..core import db
from ..helpers import JsonSerializer


stores_products = db.Table(
    'stores_products',
    db.Column('product_id', db.Integer(), db.ForeignKey('products.id')),
    db.Column('store_id', db.Integer(), db.ForeignKey('stores.id')))


class StoreJsonSerializer(JsonSerializer):
    pass


class Store(StoreJsonSerializer, db.Model):
    __tablename__ = 'stores'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255))
    address = db.Column(db.String(255))
    city = db.Column(db.String(255))
    state = db.Column(db.String(255))
    zip_code = db.Column(db.String(255))
    manager_id = db.Column(db.ForeignKey('users.id'))

    manager = db.relationship('User', backref='stores')

    products = db.relationship('Product',
                               secondary=stores_products,
                               backref=db.backref('stores', lazy='dynamic'))
