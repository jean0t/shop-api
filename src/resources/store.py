import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from config import NOT_FOUND, CREATED, BAD_REQUEST
from db import stores
from schemas import StoreSchema


store_blp = Blueprint("stores", __name__, description="Operations on Stores")


@store_blp.route("/store/<string:store_id>")
class Store(MethodView):
    def get(self, store_id):
        store = stores.get(store_id, False)
        if store:
            return store

        abort(NOT_FOUND, message="Store not found")

    def delete(self, store_id):
        try:
            del stores[store_id]
            return {"Message": "Store deleted"}
        except KeyError:
            abort(NOT_FOUND, message="Store not Found")


@store_blp.route("/store")
class StoreList(MethodView):
    def get(self):
        return {"stores": list(stores.values())}

    @store_blp.arguments(StoreSchema)
    def post(self, store_data):
        store_id = uuid.uuid4().hex
        new_store = {**store_data, "id": store_id}
        stores[store_id] = new_store
        return new_store, CREATED
