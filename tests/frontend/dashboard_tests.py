# -*- coding: utf-8 -*-
"""
    tests.api.user_tests
    ~~~~~~~~~~~~~~~~~~~~

    api user tests module
"""

from . import OverholtFrontendTestCase


class DashboardTestCase(OverholtFrontendTestCase):

    def test_authenticated_dashboard_access(self):
        r = self.get('/')
        self.assertOk(r)
        self.assertIn('<h1>Dashboard</h1>', r.data)

    def test_unauthenticated_dashboard_access(self):
        self.get('/logout')
        r = self.get('/')
        self.assertOk(r)
        self.assertNotIn('<h1>Dashboard</h1>', r.data)
