# -*- coding: utf-8 -*-
"""
    tests
    ~~~~~

    tests package
"""

import hmac
from datetime import datetime, timedelta
from hashlib import sha1
from unittest import TestCase

import simplejson as json

from overholt.core import db

from .factories import UserFactory
from .utils import HttpResponseTestCaseMixin


class OverholtTestCase(TestCase):
    pass


class OverholtAppTestCase(HttpResponseTestCaseMixin, OverholtTestCase):

    def _create_app(self):
        raise NotImplementedError

    def _create_fixtures(self):
        self.user = UserFactory()

    def _create_csrf_token(self):
        csrf_key = 'csrf_token'
        with self.client.session_transaction() as session:
            session['csrf'] = csrf_key
        secret_key = self.app.config['SECRET_KEY']
        expires = (datetime.now() + timedelta(minutes=30)).strftime('%Y%m%d%H%M%S')
        csrf_build = '%s%s' % (csrf_key, expires)
        csrf_token = csrf_build.encode('utf8')
        csrf_hmac = hmac.new(secret_key, csrf_token, digestmod=sha1)
        self.csrf_token = '%s##%s' % (expires, csrf_hmac.hexdigest())

    def setUp(self):
        super(OverholtAppTestCase, self).setUp()
        self.app = self._create_app()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self._create_fixtures()
        self._create_csrf_token()

    def tearDown(self):
        super(OverholtAppTestCase, self).tearDown()
        db.drop_all()
        self.app_context.pop()

    def _html_data(self, kwargs):
        kwargs['data']['csrf_token'] = self.csrf_token
        if not kwargs.get('content_type'):
            kwargs['content_type'] = 'application/x-www-form-urlencoded'
        return kwargs

    def _json_data(self, kwargs, csrf_enabled=True):
        kwargs['data']['csrf_token'] = self.csrf_token
        kwargs['data'] = json.dumps(kwargs['data'])
        if not kwargs.get('content_type'):
            kwargs['content_type'] = 'application/json'
        return kwargs

    def _request(self, method, *args, **kwargs):
        kwargs.setdefault('content_type', 'text/html')
        kwargs.setdefault('follow_redirects', True)
        return method(*args, **kwargs)

    def _login(self, email=None, password=None):
        email = email or self.user.email
        password = password or 'password'
        return self.post('/login', data={'email': email, 'password': password},
                         follow_redirects=False)

    def _jrequest(self, *args, **kwargs):
        return self._request(*args, **kwargs)

    def get(self, *args, **kwargs):
        return self._request(self.client.get, *args, **kwargs)

    def post(self, *args, **kwargs):
        return self._request(self.client.post, *args, **self._html_data(kwargs))

    def put(self, *args, **kwargs):
        return self._request(self.client.put, *args, **self._html_data(kwargs))

    def delete(self, *args, **kwargs):
        return self._request(self.client.delete, *args, **kwargs)

    def jget(self, *args, **kwargs):
        return self._jrequest(self.client.get, *args, **kwargs)

    def jpost(self, *args, **kwargs):
        return self._jrequest(self.client.post, *args, **self._json_data(kwargs))

    def jput(self, *args, **kwargs):
        return self._jrequest(self.client.put, *args, **self._json_data(kwargs))

    def jdelete(self, *args, **kwargs):
        return self._jrequest(self.client.delete, *args, **kwargs)
