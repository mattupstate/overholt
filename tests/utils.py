# -*- coding: utf-8 -*-
"""
    tests.utils
    ~~~~~~~~~~~

    test utilities
"""

import base64
import hmac

from datetime import datetime, timedelta
from hashlib import sha1

import simplejson as json

from werkzeug.utils import parse_cookie


def get_auth_headers(username=None, password=None):
    username = username or 'username'
    password = password or 'password'
    encoded = base64.b64encode('%s:%s' % (username, password))
    return {'Authorization': 'Basic ' + encoded}


class FlaskTestCaseMixin(object):

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

    def _html_data(self, kwargs):
        if 'data' in kwargs:
            kwargs['data']['csrf_token'] = self.csrf_token
        if not kwargs.get('content_type'):
            kwargs['content_type'] = 'application/x-www-form-urlencoded'
        return kwargs

    def _json_data(self, kwargs, csrf_enabled=True):
        if 'data' in kwargs:
            kwargs['data']['csrf_token'] = self.csrf_token
            kwargs['data'] = json.dumps(kwargs['data'])
        if not kwargs.get('content_type'):
            kwargs['content_type'] = 'application/json'
        return kwargs

    def _request(self, method, *args, **kwargs):
        kwargs.setdefault('content_type', 'text/html')
        kwargs.setdefault('follow_redirects', True)
        return method(*args, **kwargs)

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


    def getCookies(self, response):
        cookies = {}
        for value in response.headers.get_all("Set-Cookie"):
            cookies.update(parse_cookie(value))
        return cookies

    def assertStatusCode(self, response, status_code):
        """Assert the status code of a Flask test client response

        :param response: The test client response object
        :param status_code: The expected status code
        """
        self.assertEquals(status_code, response.status_code)
        return response

    def assertOk(self, response):
        """Test that response status code is 200

        :param response: The test client response object
        """
        return self.assertStatusCode(response, 200)

    def assertBadRequest(self, response):
        """Test that response status code is 400

        :param response: The test client response object
        """
        return self.assertStatusCode(response, 400)

    def assertForbidden(self, response):
        """Test that response status code is 403

        :param response: The test client response object
        """
        return self.assertStatusCode(response, 403)

    def assertNotFound(self, response):
        """Test that response status code is 404

        :param response: The test client response object
        """
        return self.assertStatusCode(response, 404)

    def assertContentType(self, response, content_type):
        """Assert the content-type of a Flask test client response

        :param response: The test client response object
        :param content_type: The expected content type
        """
        self.assertEquals(content_type, response.headers['Content-Type'])
        return response

    def assertOkHtml(self, response):
        """Assert the response status code is 200 and an HTML response

        :param response: The test client response object
        """
        return self.assertOk(
            self.assertContentType(response, 'text/html; charset=utf-8'))

    def assertJson(self, response):
        """Test that content returned is in JSON format

        :param response: The test client response object
        """
        return self.assertContentType(response, 'application/json')

    def assertOkJson(self, response):
        """Assert the response status code is 200 and a JSON response

        :param response: The test client response object
        """
        return self.assertOk(self.assertJson(response))

    def assertBadJson(self, response):
        """Assert the response status code is 400 and a JSON response

        :param response: The test client response object
        """
        return self.assertBadRequest(self.assertJson(response))

    def assertCookie(self, response, name):
        """Assert the response contains a cookie with the specified name

        :param response: The test client response object
        :param key: The cookie name
        :param value: The value of the cookie
        """
        self.assertIn(name, self.getCookies(response))

    def assertCookieEquals(self, response, name, value):
        """Assert the response contains a cookie with the specified value

        :param response: The test client response object
        :param name: The cookie name
        :param value: The value of the cookie
        """
        self.assertEquals(value, self.getCookies(response).get(name, None))
