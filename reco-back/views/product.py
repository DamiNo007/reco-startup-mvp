from flask import Blueprint, jsonify, request
from database.models import Product, Order
import json

products = Blueprint('products', __name__)


@products.route('/products/', methods=['POST'])
def create_user():
    body = request.get_json(force=True)
    print(body)
    product = Product(**body).save()
    product_id = product.id
    return {'id': str(product_id)}, 200

@products.route('/users/<user_id>/products/', methods=['POST'])
def add_to_user(user_id = None):
    body = request.get_json(force=True)
    print(body)
    order = Order(**body).save()
    order_id = order.id
    return {'id': str(order_id)}, 200


@products.route('/products', methods=['GET'])
def get_all_products():
    all_products = Product.objects.all()
    return jsonify(all_products)


@products.route('/products/<name>', methods=['GET'])
def get_user(name):
    try:
        product = Product.objects.get(name=name)
        return jsonify(product)
    except:
        return jsonify([])


@products.route('/products/<name>', methods=['PUT'])
def update_user(name):
    body = request.get_json()
    Product.objects.get(name=name).update(**body)
    return '', 200


@products.route('/products/<name>', methods=['DELETE'])
def delete_user(name):
    Product.objects.get(name=name).delete()
    # User.objects.get(username=username).delete()
    return '', 200



