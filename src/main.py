"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for, json
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planets, Favorites
import json 
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





#get DE EJEMPLO en clases
#@app.route('/user', methods=['GET'])
#def get_user():

    #response_body = {
        #"msg": "Hello, this is your GET /user response "
    #}

    #return jsonify(response_body), 200

#MI PRIMER GEEEEEET :)
@app.route('/user', methods=['GET'])
def get_users():
    user= User.query.all()
    mapeo= list(map(lambda x: x.serialize(), user))

    return jsonify(mapeo), 200

# MI PRIMER GET POR ID :D
@app.route('/user/<int:id_get>', methods=['GET'])
def get_user_id(id_get):
    usuario = User.query.get (id_get)
    usuario_serializado= usuario.serialize()

    return jsonify(usuario_serializado), 200



####### GET PEOPLE*********************************************************************************
@app.route('/people', methods=['GET'])
def get_people():
    people = People.query.all()
    resultado = list(map(lambda x: x.serialize(),people))
    return jsonify(resultado), 200

###### GET PEOPLE BY ID******************************************************************************

@app.route('/people/<int:id_get>', methods=['GET'])
def get_with_id(id_get):
    peopleid = People.query.get(id_get)
    #people_serializado= peopleid.serialize()

    return jsonify(peopleid.serialize()), 200


##### GET PLANETS ***********************************************************************************
@app.route('/planets', methods=['GET'])
def get_planets():
    planets_get = Planets.query.all()
    resultado = list(map(lambda x: x.serialize(),planets_get))
    return jsonify(resultado)
##### GET PLANETS BY ID *****************************************************************************

@app.route('/planets/<int:id_get>', methods=['GET'])
def get_id_planets(id_get):
    planetsid = Planets.query.get(id_get)
    #planets_serializado= planetsid.serialize()

    return jsonify(planetsid.serialize()), 200

#****************************************************************************************************

@app.route('/people', methods=['POST'])
def add_people():
    #people = people
    request_body = json.loads(request.data)
    #validar los datos recibidos
    if request_body["name"] == None and request_body["age"] == None and request_body["eye_color"] == None and request_body["birthday"] == None and request_body["skin_color"] == None and request_body["height"] == None and request_body["gender"] :
        return "Hay datos incompletos, favor completarlos"
    else:
        #return request_body["name"]
        people = people(name=request_body["name"], age=request_body["age"], eye_color=request_body["eye_color"], birthday=request_body["birthday"], skin_color=request_body["skin_color"], height=request_body["height"], gender=request_body["gender"])
        
        bd.session.add(people)
        db.session.commit()
        return "posteo exitoso"


@app.route('/planets', methods=['POST'])
def add_planets():
    #planets = planets
    request_body = json.loads(request.data)
    #validar los datos recibidos
    if request_body["name"]  == None and request_body["age"] == None and request_body["diameter"] == None and request_body["climate"] == None and request_body["terrain"] == None and request_body["population"] == None:
        return "Hay datos incompletos, favor completarlos"
    else:
        #return request_body["name"]
        planets = Planets(name=request_body["name"], age=request_body["age"], diameter=request_body["diameter"], climate=request_body["climate"], terrain=request_body["terrain"],surface_water=request_body["surface_water"] )
        
        db.session.add(planets)
        db.session.commit()
        return "posteo exitoso"

       

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)



