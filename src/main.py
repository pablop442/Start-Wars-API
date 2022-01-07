"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planets, Favorites
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
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

#Users endpoints

@app.route('/user', methods=['GET'])
def get_users():
    users = User.query.all()
    all_users = list(map(lambda x: x.serialize(), users))
    return jsonify(all_users), 200

@app.route('/user', methods=['POST'])
def create_users():
    request_body = request.get_json()
    new_user = User(name= request_body["name"], email= request_body["email"], favorite_planet= request_body["favorite_planet"], favorite_people= request_body["favorite_people"])
    db.session.add(new_user)
    db.session.commit()
    return jsonify(request_body), 201

#User ID endpoint

@app.route('/user/<int:user_id>', methods=['GET'])
def get_one_user(user_id):
    user_x = User.query.get(user_id)
    return jsonify(user_x), 200

#People endpoints

@app.route('/people', methods=['GET'])
def get_people():
    people = People.query.all()
    all_people = list(map(lambda x: x.serialize(), people))
    return jsonify(all_people), 200

@app.route('/people', methods=['POST'])
def create_people():
    request_body = request.get_json()
    new_people = People(name= request_body["name"])
    db.session.add(new_people)
    db.session.commit()
    return jsonify(request_body), 201

#Planets endpoints

@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planets.query.all()
    all_planets = list(map(lambda x: x.serialize(), planets))
    return jsonify(all_planets), 200

@app.route('/planets', methods=['POST'])
def create_planets():
    request_body = request.get_json()
    new_planet = Planets(name= request_body["name"])
    db.session.add(new_planet)
    db.session.commit()
    return jsonify(request_body), 201

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
