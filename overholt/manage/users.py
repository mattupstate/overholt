# -*- coding: utf-8 -*-
"""
    overholt.manage.users
    ~~~~~~~~~~~~~~~~~~~~~

    user management commands
"""

from flask import current_app
from flask.ext.script import Command, prompt, prompt_pass
from flask_security.forms import RegisterForm
from flask_security.registerable import register_user
from werkzeug.datastructures import MultiDict

from ..services import users


class CreateUserCommand(Command):
    """Create a user"""

    def run(self):
        email = prompt('Email')
        password = prompt_pass('Password')
        password_confirm = prompt_pass('Confirm Password')
        data = MultiDict(dict(email=email, password=password, password_confirm=password_confirm))
        form = RegisterForm(data, csrf_enabled=False)
        if form.validate():
            user = register_user(email=email, password=password)
            print '\nUser created successfully'
            print 'User(id=%s email=%s)' % (user.id, user.email)
            return
        print '\nError creating user:'
        for errors in form.errors.values():
            print '\n'.join(errors)


class DeleteUserCommand(Command):
    """Delete a user"""

    def run(self):
        email = prompt('Email')
        user = users.first(email=email)
        if not user:
            print 'Invalid user'
            return
        users.delete(user)
        print 'User deleted successfully'


class ListUsersCommand(Command):
    """List all users"""

    def run(self):
        for u in users.all():
            print 'User(id=%s email=%s)' % (u.id, u.email)
