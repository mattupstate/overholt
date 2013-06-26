# -*- coding: utf-8 -*-
"""
    overholt.services
    ~~~~~~~~~~~~~~~~~

    services module
"""

from .products import ProductsService
from .stores import StoresService
from .users import UsersService

#: An instance of the :class:`ProductsService` class
products = ProductsService()

#: An instance of the :class:`StoresService` class
stores = StoresService()

#: An instance of the :class:`UsersService` class
users = UsersService()
