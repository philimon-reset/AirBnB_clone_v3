#!/usr/bin/python3
""" return dict repersantation of object """
from models import storage
from models.engine.db_storage import classes
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response


@app_views.route("/places/<place_id>/reviews",
                 methods=["GET"], strict_slashes=False)
def review_get(place_id):
    result = []
    """ get all the reviews in a place """
    place = storage.get(classes["Place"], place_id)
    if not place:
        abort(404)
    for i in place.reviews:
        result.append(i.to_dict())
    return jsonify(result)


@app_views.route("/reviews/<review_id>", methods=["GET"], strict_slashes=False)
def review_specific(review_id):
    """ get the specific object from review """
    review = storage.get(classes["Review"], review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route("/reviews/<review_id>",
                 methods=['DELETE'],
                 strict_slashes=False)
def review_specific_delete(review_id):
    """ delete the inputed object from review """
    review = storage.get(classes["Review"], review_id)
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route("/places/<place_id>/reviews",
                 methods=['POST'], strict_slashes=False)
def review_specific_post(place_id):
    """ post the inputed object from review objects"""
    task = [task for task in storage.all(
        "Place").values() if task.id == place_id]
    if len(task) == 0:
        abort(404)
    if not request.json:
        return make_response("Not a JSON", 400)
    if 'text' not in request.json:
        return make_response("Missing text", 400)
    if 'user_id' not in request.json:
        return make_response("Missing user_id", 400)
    task = [task for task in storage.all(
        "User").values() if task.id == request.json["user_id"]]
    if len(task) == 0:
        abort(404)
    obj = classes["Review"]
    try:
        new_item = obj()
        for key, value in request.json.items():
            setattr(new_item, key, value)
        setattr(new_item, "place_id", place_id)
        new_item.save()
        return new_item.to_dict(), 201
    except BaseException:
        abort(404)


@app_views.route("/reviews/<review_id>", methods=["PUT"], strict_slashes=False)
def review_specific_put(review_id):
    """ update the specific object from review objects """
    instance = None
    if not request.json:
        return make_response("Not a JSON", 400)
    check = ["id", "created_at", "updated_at", "user_id", "place_id"]
    for i in storage.all("Review").values():
        if i.id == review_id:
            instance = i
            for key, value in request.json.items():
                if key not in check:
                    setattr(i, key, value)
                    i.save()
    if not instance:
        abort(404)
    return instance.to_dict(), 200
