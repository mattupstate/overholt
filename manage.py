# -*- coding: utf-8 -*-
"""
    manage
    ~~~~~~

    Manager module
"""

from flask.ext.script import Manager

from overholt.api import create_app
from overholt.manage import CreateUserCommand, DeleteUserCommand, ListUsersCommand

manager = Manager(create_app())
manager.add_command('create_user', CreateUserCommand())
manager.add_command('delete_user', DeleteUserCommand())
manager.add_command('list_users', ListUsersCommand())

if __name__ == "__main__":
    manager.run()
