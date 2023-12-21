"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import json
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import Favorites, db, User, Character, Planet
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def get_all_users():
    users = User.query.all()
    if len(users) < 1:
        return jsonify({"msg": "not found"}), 404
    serialized_users = list(map(lambda x: x.serialize(), users))
    return serialized_users, 200


@app.route('/user/<int:user_id>', methods=['GET'])
def get_one_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"msg": f"user with id {user_id} not found"}), 404
    serialized_user = user.serialize()
    return serialized_user, 200

@app.route('/user', methods=['POST'])
def create_one_user():
    body = json.loads(request.data)
    new_user = User(
        user_name = body["user_name"],
        email = body["email"],
        password = body["password"],
        is_active = True
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"msg": "user created succesfull"}), 200


@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_one_user(user_id):
    delete_user = User.query.get(user_id)
    db.session.delete(delete_user)
    db.session.commit()
    return jsonify({"msg": "user deleted succesfull"}), 200


@app.route('/characters', methods=['GET'])
def get_all_characters():
    characters = Character.query.all()
    serialized_character = list(map(lambda x: x.serialize(), characters))
    return serialized_character, 200


@app.route('/character/<int:character_id>', methods=['GET'])
def get_one_character(character_id):
    character = Character.query.get(character_id)
    if character is None:
        return jsonify({"msg": f"character with id {character_id} not found"}), 404
    serialized_character = character.serialize()
    return serialized_character, 200

@app.route('/characters', methods=['POST'])
def create_one_character():
    body = json.loads(request.data)
    new_character = Character(
        name = body["name"],
        height = body["height"]
    )
    db.session.add(new_character)
    db.session.commit()
    return jsonify({"msg": "character created succesfull"}), 200

@app.route('/character/<int:character_id>', methods=['DELETE'])
def delete_one_character(character_id):
    delete_character = Character.query.get(character_id)
    db.session.delete(delete_character)
    db.session.commit()
    return jsonify({"msg": "Character deleted succesfully"}), 200


@app.route('/planets', methods=['GET'])
def get_all_planets():
    planets = Planet.query.all()
    if len(planets) < 1:
        return jsonify({"msg": "not found"}), 404
    serialized_planets = list(map(lambda x: x.serialize(), planets))
    return serialized_planets, 200

@app.route('/planet/<int:planet_id>', methods=['GET'])
def get_one_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if planet is None:
        return jsonify ({"msg": f"planet with id {planet_id} not found"}), 404
    serialized_planet = planet.serialize()
    return serialized_planet, 200


@app.route('/planets', methods=['POST'])
def create_one_planet():
    body = json.loads(request.data)
    new_planet = Planet(
        name = body["name"],
        population = body["population"]
    )
    db.session.add(new_planet)
    db.session.commit()
    return jsonify({"msg": "Planet created succesfull"}), 200

@app.route('/planet/<int:planet_id>', methods=['DELETE'])
def delete_one_planet(planet_id):
    delete_planet = Planet.query.get(planet_id)
    db.session.delete(delete_planet)
    db.session.commit()
    return jsonify({"msg": "Planet deleted succesfully"}), 200


@app.route('/user/<int:user_id>/favorites', methods=['GET'])
def get_favorites(user_id):
    favorites = Favorites.query.filter_by(user_id = user_id).all()
    if len(favorites) < 1:
        return jsonify({"msg": "not found"}), 404
    serialized_favorites = list(map(lambda x: x.serialize(), favorites))
    return serialized_favorites, 200

@app.route('/user/<int:user_id>/favorites/planet', methods=['POST'])
def add_favorite_planet(user_id):
    body = json.loads(request.data)
    planet_id = body.get("planet_id")
    
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"msg": f"user with id {user_id} not found"}), 404
    
    planet = Planet.query.get(planet_id)
    if planet is None:
        return jsonify({"msg": f"planet with id {planet_id} not found"}), 404
    
    favorite = Favorites(user_id=user_id, planet_id=planet_id)
    db.session.add(favorite)
    db.session.commit()
    
    return jsonify({"msg": "Favorite planet added successfully"}), 200

@app.route('/user/<int:user_id>/favorites/character', methods=['POST'])
def add_favorite_character(user_id):
    body = json.loads(request.data)
    character_id = body.get("character_id")
    
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"msg": f"user with id {user_id} not found"}), 404
    
    character = Character.query.get(character_id)
    if character is None:
        return jsonify({"msg": f"character with id {character_id} not found"}), 404
    
    favorite = Favorites(user_id=user_id, character_id=character_id)
    db.session.add(favorite)
    db.session.commit()
    
    return jsonify({"msg": "Favorite character added successfully"}), 200


@app.route('/favorite/planet/<int:planets_id>', methods=['DELETE'])
def delete_one_favorite_planet(planets_id):
    delete_favorite_planet = Favorites.query.get(planets_id)
    db.session.delete(delete_favorite_planet)
    db.session.commit()
    return jsonify({"msg": "Favorite planet deleted succesfully"}), 200

@app.route('/favorite/character/<int:characters_id>', methods=['DELETE'])
def delete_one_favorite_character(characters_id):
    delete_favorite_character = Favorites.query.get(characters_id)
    db.session.delete(delete_favorite_character)
    db.session.commit()
    return jsonify({"msg": "Favorite character deleted succesfully"}), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
