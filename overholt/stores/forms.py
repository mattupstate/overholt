# -*- coding: utf-8 -*-
"""
    overholt.stores.forms
    ~~~~~~~~~~~~~~~~~~~~~

    Store forms
"""

from flask_wtf import Form, TextField, Required, Optional

__all__ = ['NewStoreForm', 'UpdateStoreForm']


class NewStoreForm(Form):
    name = TextField('Name', validators=[Required()])
    address = TextField('Address', validators=[Required()])
    city = TextField('City', validators=[Required()])
    state = TextField('State', validators=[Required()])
    zip_code = TextField('Zip Code', validators=[Required()])


class UpdateStoreForm(Form):
    name = TextField('Name', validators=[Optional()])
    address = TextField('Address', validators=[Optional()])
    city = TextField('City', validators=[Optional()])
    state = TextField('State', validators=[Optional()])
    zip_code = TextField('Zip Code', validators=[Optional()])
