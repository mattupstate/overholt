# -*- coding: utf-8 -*-
"""
    tests.utils
    ~~~~~~~~~~~

    test utilities
"""

import base64

from werkzeug.utils import parse_cookie


def get_auth_headers(username=None, password=None):
    username = username or 'username'
    password = password or 'password'
    encoded = base64.b64encode('%s:%s' % (username, password))
    return {'Authorization': 'Basic ' + encoded}


class HttpResponseTestCaseMixin(object):

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
