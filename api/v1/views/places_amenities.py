#!/usr/bin/python3
""" return dict repersantation of object """
from models import storage, storage_t
from models.engine.db_storage import classes
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response


@app_views.route("/places/<place_id>/amenities",
                 methods=["GET"], strict_slashes=False)
def PA_get(place_id):
    result = []
    """ get all the reviews in a place """
    task = storage.get(classes['Place'], place_id)
    if not task:
        abort(404)
    for i in task.amenities:
        result.append(i.to_dict())
    return jsonify(result)


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=['DELETE'], strict_slashes=False)
def PA_specific_delete(place_id, amenity_id):
    """ delete the inputed object from review """
    place = storage.get(classes['Place'], place_id)
    task = storage.get(classes['Amenity'], amenity_id)
    if not place or not task:
        abort(404)
    if storage_t == 'db':
        check = place.amenities
        tasks = task
    else:
        check = place.amenity_id
        tasks = task.id
    for i in range(len(check)):
        if check[i] == tasks:
            check.pop(i)
            storage.save()
            return jsonify({}), 200
    abort(404)


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=['POST'], strict_slashes=False)
def PA_specific_post(place_id, amenity_id):
    """ post the inputed object from review objects"""
    place = storage.get(classes['Place'], place_id)
    amenity = storage.get(classes['Amenity'], amenity_id)
    if not place or not amenity:
        abort(404)
    if storage_t == 'db':
        check = place.amenities
    else:
        check = place.amenity_id
    for task in check:
        if task == amenity:
            return task.to_dict(), 200
    place.amenities.append(amenity)
    amenity.save()
    return amenity.to_dict(), 201
