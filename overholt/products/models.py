# -*- coding: utf-8 -*-
"""
    overholt.products.models
    ~~~~~~~~~~~~~~~~~~~~~~

    Product models
"""

from ..core import db
from ..helpers import JsonSerializer


products_categories = db.Table(
    'products_categories',
    db.Column('product_id', db.Integer(), db.ForeignKey('products.id')),
    db.Column('category_id', db.Integer(), db.ForeignKey('categories.id')))


class CategoryJsonSerializer(JsonSerializer):
    __json_hidden__ = ['products']


class Category(CategoryJsonSerializer, db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255))
    description = db.Column(db.String(255))


class ProductJsonSerializer(JsonSerializer):
    __json_hidden__ = ['stores']


class Product(ProductJsonSerializer, db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255))

    categories = db.relationship('Category',
                                 secondary=products_categories,
                                 backref=db.backref('products', lazy='joined'))
