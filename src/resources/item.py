import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from db import items, stores
from config import NOT_FOUND, CREATED, BAD_REQUEST, OK
from schemas import ItemSchema, ItemUpdateSchema

item_blp = Blueprint("Items", __name__, description="Operations on Items")


@item_blp.route("/item/<string:item_id>")
class Item(MethodView):
    @item_blp.response(OK, ItemSchema)
    def get(self, item_id):
        item = items.get(item_id, False)
        if item:
            return item
        else:
            abort(NOT_FOUND, message="Item not Found")

    def delete(self, item_id):
        try:
            del items[item_id]
            return {"Message": "Item deleted"}
        except KeyError:
            abort(NOT_FOUND, message="Item not Found")

    @item_blp.arguments(ItemUpdateSchema)
    @item_blp.response(OK, ItemSchema)
    def put(self, item_data, item_id):
        if "price" not in item_data or "name" not in item_data:
            abort(
                BAD_REQUEST,
                message="Bad request, ensure 'price' and 'name' are included in the Json payload",
            )

        try:
            item = items[item_id]
            item |= item_data

            return item

        except KeyError:
            abort(NOT_FOUND, message="Item not Found")


@item_blp.route("/item")
class ItemList(MethodView):
    @item_blp.response(OK, ItemSchema(many=True))
    def get(self):
        return items.values()

    @item_blp.arguments(ItemSchema)
    @item_blp.response(CREATED, ItemSchema)
    def post(self, item_data):
        for item in items.values():
            if (
                item_data["name"] == item["name"]
                and item_data["store_id"] == item["store_id"]
            ):
                abort(BAD_REQUEST, message="Item already exists.")

        item_id = uuid.uuid4().hex
        item = {**item_data, "id": item_id}
        items[item_id] = item

        return item
