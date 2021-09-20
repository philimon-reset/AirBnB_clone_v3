#!/usr/bin/python3
""" return dict repersantation of object """
from models import storage
from models.engine.db_storage import classes
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response


@app_views.route("/cities/<city_id>/places",
                 methods=["GET"], strict_slashes=False)
def place_get(city_id):
    result = []
    """ get all the places in a city """
    city = storage.get(classes["City"], city_id)
    if not city:
        abort(404)
    for i in city.places:
            result.append(i.to_dict())
    return jsonify(result)


@app_views.route("/places/<place_id>", methods=["GET"], strict_slashes=False)
def place_specific(place_id):
    """ get the specific object from place """
    for i in storage.all("Place").values():
        if i.id == place_id:
            return i.to_dict()
    abort(404)


@app_views.route("/places/<place_id>",
                 methods=['DELETE'],
                 strict_slashes=False)
def place_specific_delete(place_id):
    """ delete the inputed object from place """
    task = [task for task in storage.all(
        "Place").values() if task.id == place_id]
    if len(task) == 0:
        abort(404)
    storage.delete(task[0])
    storage.save()
    return jsonify({}), 200


@app_views.route("/cities/<city_id>/places",
                 methods=['POST'], strict_slashes=False)
def place_specific_post(city_id):
    """ post the inputed object from place objects"""
    task = [task for task in storage.all(
        "City").values() if task.id == city_id]
    if len(task) == 0:
        abort(404)
    if not request.json:
        return make_response("Not a JSON", 400)
    if 'name' not in request.json:
        return make_response("Missing name", 400)
    if 'user_id' not in request.json:
        return make_response("Missing user_id", 400)
    task = [task for task in storage.all(
        "User").values() if task.id == request.json["user_id"]]
    if len(task) == 0:
        abort(404)
    obj = classes["Place"]
    try:
        new_item = obj()
        for key, value in request.json.items():
            setattr(new_item, key, value)
        setattr(new_item, "city_id", city_id)
        new_item.save()
        return new_item.to_dict(), 201
    except BaseException:
        abort(404)


@app_views.route("/places/<place_id>", methods=["PUT"], strict_slashes=False)
def place_specific_put(place_id):
    """ update the specific object from place objects """
    instance = None
    if not request.json:
        return make_response("Not a JSON", 400)
    check = ["id", "created_at", "updated_at", "user_id", "city_id"]
    for i in storage.all("Place").values():
        if i.id == place_id:
            instance = i
            for key, value in request.json.items():
                if key not in check:
                    setattr(i, key, value)
                    i.save()
    if not instance:
        abort(404)
    return instance.to_dict(), 200


@app_views.route("/places_search", methods=['GET'], strict_slashes=False)
def place_search_get():
    result = []
    if not request.json:
        return make_response("Not a JSON", 400)
    if not len(request.json):
        task = [task for task in storage.all('Place')]
        return jsonify(task)
    place_T = list(storage.all('Place').values())
    if 'amenities' in request.json:
        place_T = []
        for T in storage.all('Place').values():
            for ament in T.amenities:
                for A_key in request.json['amenities']:
                    if ament.id == A_key:
                        place_T.append(ament)
    if 'states' in request.json and 'cities' not in request.json:
        states = [storage.get(classes["State"], states)
                  for states in request.json['states']]
        for state in states:
            for city in state.cities:
                for i in storage.all("Place").values():
                    if i.city_id == city.id:
                        result.append(i.to_dict())
    elif 'cities' in request.json and 'states' not in request.json:
        cities = request.json['cities']
        for city in cities:
            for i in storage.all("Place").values():
                if i.city_id == city:
                    result.append(i.to_dict())
    else:
        test = []
        states = [storage.get(classes["State"], states)
                  for states in request.json['states']]
        citi = request.json['cities']
        for state in states:
            for city, city_P in zip(state.cities, citi):
                for i in storage.all("Place").values():
                    if i.city_id == city.id or i.city_id == city_P:
                        test.append(i.to_dict())
        result = []
        [result.append(x) for x in test if x not in result]
    return jsonify(result)
