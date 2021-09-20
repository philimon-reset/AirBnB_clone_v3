#!/usr/bin/python3
""" return dict repersantation of object """
from models import storage
from models.engine.db_storage import classes
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response


@app_views.route("/users", methods=["GET"], strict_slashes=False)
def user_get():
    result = []
    """ get all the user """
    for i in storage.all("User").values():
        result.append(i.to_dict())
    return jsonify(result)


@app_views.route("/users/<user_id>", methods=["GET"], strict_slashes=False)
def user_specific(user_id):
    """ get the specific object from user """
    user = storage.get(classes["User"], user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route("/users/<user_id>", methods=['DELETE'], strict_slashes=False)
def user_specific_delete(user_id):
    """ delete the inputed object from user """
    task = storage.get(classes["User"], user_id)
    if not task:
        abort(404)
    storage.delete(task)
    storage.save()
    return jsonify({}), 200


@app_views.route("/users", methods=['POST'], strict_slashes=False)
def user_specific_post():
    """ post the inputed object from user"""
    if not request.json:
        return make_response("Not a JSON", 400)
    if 'email' not in request.json:
        return make_response("Missing email", 400)
    if 'password' not in request.json:
        return make_response("Missing password", 400)
    obj = classes["User"](**request.json)
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route("/users/<user_id>", methods=["PUT"], strict_slashes=False)
def user_specific_put(user_id):
    """ update the specific object from user """
    if not request.json:
        return make_response("Not a JSON", 400)
    check = ["id", "created_at", "updated_at", "email"]
    instance = storage.get(classes["User"], user_id)
    if not instance:
        abort(404)
    for key, value in request.json.items():
        if key not in check:
            setattr(instance, key, value)
            instance.save()
    return instance.to_dict(), 200
