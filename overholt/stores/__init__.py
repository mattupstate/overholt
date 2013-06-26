# -*- coding: utf-8 -*-
"""
    overholt.stores
    ~~~~~~~~~~~~~~~

    overholt stores package
"""

from ..core import Service, OverholtError
from .models import Store


class StoresService(Service):
    __model__ = Store

    def add_manager(self, store, user):
        if store in user.stores:
            raise OverholtError(u'Manager exists')
        store.managers.add(user)
        return self.save(store)

    def remove_manager(self, store, user):
        if store not in user.stores:
            raise OverholtError(u'Invalid manager')
        store.managers.remove(user)
        return self.save(store)

    def add_product(self, store, product):
        if product in store.products:
            raise OverholtError(u'Product exists')
        store.products.append(product)
        return self.save(store)

    def remove_product(self, store, product):
        if product not in store.products:
            raise OverholtError(u'Invalid product')
        store.products.remove(product)
        return self.save(store)
