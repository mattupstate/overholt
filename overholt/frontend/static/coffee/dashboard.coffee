# dashboard.coffee

class Store extends Backbone.Model
  urlRoot: "/api/stores"

  defaults:
    id: null
    name: ""
    address: ""
    city: ""
    state: ""
    zip_code: ""

  initialize: ->


class Stores extends Backbone.Collection
  url: "/api/stores"
  model: Store


class StoresView extends Backbone.View
  el: $ '.stores'

  events:
    'click .btn-add-store': 'onAddStoreClicked'

  initialize: ->
    _.bindAll @

  onAddStoreClicked: (e) ->
    e.preventDefault()
    console.log 'onAddStoreClicked'


class DashboardRouter extends Backbone.Router
  initialize: ->
    @storeView = new StoresView

$ ->
  window.app = new DashboardRouter
