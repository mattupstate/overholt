# -*- coding: utf-8 -*-
"""
    overholt.users
    ~~~~~~~~~~~~~~

    overholt users package
"""

from ..core import Service
from .models import User


class UsersService(Service):
    __model__ = User
