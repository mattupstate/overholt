var DashboardRouter, Store, Stores, StoresView,
  __hasProp = {}.hasOwnProperty,
  __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; };

Store = (function(_super) {

  __extends(Store, _super);

  function Store() {
    return Store.__super__.constructor.apply(this, arguments);
  }

  Store.prototype.urlRoot = "/api/stores";

  Store.prototype.defaults = {
    id: null,
    name: "",
    address: "",
    city: "",
    state: "",
    zip_code: ""
  };

  Store.prototype.initialize = function() {};

  return Store;

})(Backbone.Model);

Stores = (function(_super) {

  __extends(Stores, _super);

  function Stores() {
    return Stores.__super__.constructor.apply(this, arguments);
  }

  Stores.prototype.url = "/api/stores";

  Stores.prototype.model = Store;

  return Stores;

})(Backbone.Collection);

StoresView = (function(_super) {

  __extends(StoresView, _super);

  function StoresView() {
    return StoresView.__super__.constructor.apply(this, arguments);
  }

  StoresView.prototype.el = $('.stores');

  StoresView.prototype.events = {
    'click .btn-add-store': 'onAddStoreClicked'
  };

  StoresView.prototype.initialize = function() {
    return _.bindAll(this);
  };

  StoresView.prototype.onAddStoreClicked = function(e) {
    e.preventDefault();
    return console.log('onAddStoreClicked');
  };

  return StoresView;

})(Backbone.View);

DashboardRouter = (function(_super) {

  __extends(DashboardRouter, _super);

  function DashboardRouter() {
    return DashboardRouter.__super__.constructor.apply(this, arguments);
  }

  DashboardRouter.prototype.initialize = function() {
    return this.storeView = new StoresView;
  };

  return DashboardRouter;

})(Backbone.Router);

$(function() {
  return window.app = new DashboardRouter;
});
