# -*- coding: utf-8 -*-
"""
    overholt.api.stores
    ~~~~~~~~~~~~~~~~~~~

    Store endpoints
"""

from flask import Blueprint, request

from ..forms import NewStoreForm, UpdateStoreForm
from ..services import stores as _stores, products as _products, users as _users
from ..tasks import send_manager_added_email, send_manager_removed_email
from . import OverholtFormError, route

bp = Blueprint('stores', __name__, url_prefix='/stores')


@route(bp, '/')
def list():
    """Returns a list of all store instances."""
    return _stores.all()


@route(bp, '/', methods=['POST'])
def new():
    """Creates a new store. Returns the new store instance."""
    form = NewStoreForm()
    if form.validate_on_submit():
        return _stores.create(**request.json)
    raise OverholtFormError(form.errors)


@route(bp, '/<store_id>')
def show(store_id):
    """Returns a store instance."""
    return _stores.get_or_404(store_id)


@route(bp, '/<store_id>', methods=['PUT'])
def update(store_id):
    """Updates a store. Returns the updated store instance."""
    form = UpdateStoreForm()
    if form.validate_on_submit():
        return _stores.update(_stores.get_or_404(store_id), **request.json)
    raise OverholtFormError(form.errors)


@route(bp, '/<store_id>', methods=['DELETE'])
def delete(store_id):
    """Deletes a store. Returns a 204 response."""
    _stores.delete(_stores.get_or_404(store_id))
    return None, 204


@route(bp, '/<store_id>/products')
def products(store_id):
    """Returns a list of product instances belonging to a store."""
    return _stores.get_or_404(store_id).products


@route(bp, '/<store_id>/products/<product_id>', methods=['PUT'])
def add_product(store_id, product_id):
    """Adds a product to a store. Returns the product instance."""
    return _stores.add_product(_stores.get_or_404(store_id),
                               _products.get_or_404(product_id))


@route(bp, '/<store_id>/products/<product_id>', methods=['DELETE'])
def remove_product(store_id, product_id):
    """Removes a product form a store. Returns a 204 response."""
    _stores.remove_product(_stores.get_or_404(store_id),
                           _products.get_or_404(product_id))
    return None, 204


@route(bp, '/<store_id>/managers')
def managers(store_id):
    return _stores.get_or_404(store_id).managers


@route(bp, '/<store_id>/managers/<user_id>', methods=['PUT'])
def add_manager(store_id, user_id):
    store, manager = _stores.add_manager(_stores.get_or_404(store_id),
                                         _users.get_or_404(user_id))
    send_manager_added_email.delay(manager.email)
    return store


@route(bp, '/<store_id>/managers/<user_id>', methods=['DELETE'])
def remove_manager(store_id, user_id):
    store, manager = _stores.remove_manager(_stores.get_or_404(store_id),
                                            _users.get_or_404(user_id))
    send_manager_removed_email.delay(manager.email)
    return None, 204
