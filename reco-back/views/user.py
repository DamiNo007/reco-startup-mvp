from flask import Blueprint, jsonify, request
from database.models import User
import json

users = Blueprint('users', __name__)


@users.route('/users/', methods=['POST'])
def create_user():
    body = request.get_json(force=True)
    print(body)
    user = User(**body).save()
    user_id = user.id
    return {'id': str(user_id)}, 200


@users.route('/users', methods=['GET'])
def get_all_users():
    all_users = User.objects.all()
    return jsonify(all_users)


@users.route('/users/<phone_number>', methods=['GET'])
def get_user(phone_number):
    try:
        user = User.objects.get(phone_number)
        return jsonify(user)
    except:
        return jsonify([])


@users.route('/users/<phone_number>', methods=['PUT'])
def update_user(phone_number):
    body = request.get_json()
    User.objects.get(phone_number=phone_number).update(**body)
    return '', 200


@users.route('/users/<phone_number>', methods=['DELETE'])
def delete_user(phone_number):
    User.objects.get(phone_number=phone_number).delete()
    # User.objects.get(username=username).delete()
    return '', 200



