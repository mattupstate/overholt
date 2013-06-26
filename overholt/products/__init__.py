# -*- coding: utf-8 -*-
"""
    overholt.products
    ~~~~~~~~~~~~~~~~~

    overholt products package
"""

from ..core import Service
from .models import Product, Category


class CategoryService(Service):
    __model__ = Category


class ProductsService(Service):
    __model__ = Product

    def __init__(self, *args, **kwargs):
        super(ProductsService, self).__init__(*args, **kwargs)
        self.categories = CategoryService()

    def _preprocess_params(self, kwargs):
        kwargs = super(ProductsService, self)._preprocess_params(kwargs)
        categories = kwargs.get('categories', [])
        if categories and all(isinstance(c, int) for c in categories):
            kwargs['categories'] = self.categories.get_all(*categories)
        return kwargs
