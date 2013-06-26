# -*- coding: utf-8 -*-
"""
    tests.api
    ~~~~~~~~~

    api tests package
"""

from overholt.api import create_app

from .. import OverholtAppTestCase, settings


class OverholtApiTestCase(OverholtAppTestCase):

    def _create_app(self):
        return create_app(settings, register_security_blueprint=True)

    def setUp(self):
        super(OverholtApiTestCase, self).setUp()
        self._login()
