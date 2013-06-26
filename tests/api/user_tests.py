# -*- coding: utf-8 -*-
"""
    tests.api.user_tests
    ~~~~~~~~~~~~~~~~~~~~

    api user tests module
"""

from . import OverholtApiTestCase


class UserApiTestCase(OverholtApiTestCase):

    def test_get_current_user(self):
        r = self.jget('/users')
        self.assertOkJson(r)

    def test_get_user(self):
        r = self.jget('/users/%s' % self.user.id)
        self.assertOkJson(r)
