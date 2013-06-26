# -*- coding: utf-8 -*-
"""
    tests.api.product_tests
    ~~~~~~~~~~~~~~~~~~~~~~~

    api product tests module
"""

from ..factories import CategoryFactory, ProductFactory
from . import OverholtApiTestCase


class ProductApiTestCase(OverholtApiTestCase):

    def _create_fixtures(self):
        super(ProductApiTestCase, self)._create_fixtures()
        self.category = CategoryFactory()
        self.product = ProductFactory(categories=[self.category])

    def test_get_products(self):
        r = self.jget('/products')
        self.assertOkJson(r)

    def test_get_product(self):
        r = self.jget('/products/%s' % self.product.id)
        self.assertOkJson(r)

    def test_create_product(self):
        r = self.jpost('/products', data={
            'name': 'New Product',
            'categories': [self.category.id]
        })
        self.assertOkJson(r)

    def test_create_invalid_product(self):
        r = self.jpost('/products', data={
            'categories': [self.category.id]
        })
        self.assertBadJson(r)

    def test_update_product(self):
        r = self.jput('/products/%s' % self.product.id, data={
            'name': 'New Product'
        })
        self.assertOkJson(r)

    def test_delete_product(self):
        r = self.jdelete('/products/%s' % self.product.id)
        self.assertStatusCode(r, 204)
