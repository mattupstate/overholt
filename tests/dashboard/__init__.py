# -*- coding: utf-8 -*-
"""
    tests.api
    ~~~~~~~~~

    api tests package
"""

from overholt.frontend import create_app

from .. import OverholtAppTestCase, settings


class OverholtDashboardTestCase(OverholtAppTestCase):

    def _create_app(self):
        return create_app(settings)

    def setUp(self):
        super(OverholtDashboardTestCase, self).setUp()
        self._login()
