import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from config import NOT_FOUND, CREATED, BAD_REQUEST, OK
from db import stores
from schemas import StoreSchema


store_blp = Blueprint("stores", __name__, description="Operations on Stores")


@store_blp.route("/store/<string:store_id>")
class Store(MethodView):
    @store_blp.response(OK, StoreSchema)
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
    @store_blp.response(CREATED, StoreSchema(many=True))
    def get(self):
        return stores.values()

    @store_blp.arguments(StoreSchema)
    @store_blp.response(OK, StoreSchema)
    def post(self, store_data):
        for store in stores.values():
            if store_data["name"] == store["name"]:
                abort(BAD_REQUEST, message="Store already exists")

        store_id = uuid.uuid4().hex
        new_store = {**store_data, "id": store_id}
        stores[store_id] = new_store
        
        return new_store
