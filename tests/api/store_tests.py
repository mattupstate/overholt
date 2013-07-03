# -*- coding: utf-8 -*-
"""
    tests.api.store_tests
    ~~~~~~~~~~~~~~~~~~~~~

    api store tests module
"""

from ..factories import StoreFactory, ProductFactory
from . import OverholtApiTestCase


class StoreApiTestCase(OverholtApiTestCase):

    def _create_fixtures(self):
        super(StoreApiTestCase, self)._create_fixtures()
        self.product = ProductFactory()
        self.store = StoreFactory(products=[self.product])

    def test_get_stores(self):
        r = self.jget('/stores')
        self.assertOkJson(r)

    def test_get_store(self):
        r = self.jget('/stores/%s' % self.store.id)
        self.assertOkJson(r)

    def test_create_store(self):
        r = self.jpost('/stores', data={
            'name': 'My Store',
            'address': '123 Overholt Drive',
            'city': 'Brooklyn',
            'state': 'New York',
            'zip_code': '12345'
        })
        self.assertOkJson(r)
        self.assertIn('"name": "My Store"', r.data)

    def test_create_invalid_store(self):
        r = self.jpost('/stores', data={
            'name': 'My Store'
        })
        self.assertBadJson(r)
        self.assertIn('"errors": {', r.data)

    def test_update_store(self):
        r = self.jput('/stores/%s' % self.store.id, data={
            'name': 'My New Store'
        })
        self.assertOkJson(r)
        self.assertIn('"name": "My New Store"', r.data)

    def test_delete_store(self):
        r = self.jdelete('/stores/%s' % self.store.id)
        self.assertStatusCode(r, 204)

    def test_get_products(self):
        r = self.jget('/stores/%s/products' % self.store.id)
        self.assertOkJson(r)

    def test_add_product(self):
        p = ProductFactory()
        e = '/stores/%s/products/%s' % (self.store.id, p.id)
        r = self.jput(e)
        self.assertOkJson(r)

    def test_remove_product(self):
        e = '/stores/%s/products/%s' % (self.store.id, self.product.id)
        r = self.jdelete(e)
        self.assertStatusCode(r, 204)

    def test_add_manager(self):
        e = '/stores/%s/managers/%s' % (self.store.id, self.user.id)
        r = self.jput(e)
        self.assertOkJson(r)

    def test_add_existing_manager(self):
        e = '/stores/%s/managers/%s' % (self.store.id, self.user.id)
        self.jput(e)
        r = self.jput(e)
        self.assertBadJson(r)

    def test_remove_manager(self):
        e = '/stores/%s/managers/%s' % (self.store.id, self.user.id)
        self.jput(e)
        r = self.jdelete(e)
        self.assertStatusCode(r, 204)
