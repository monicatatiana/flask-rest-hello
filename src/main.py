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


## Nos permite hacer las encripciones de contraseñas
from werkzeug.security import generate_password_hash, check_password_hash

## Nos permite manejar tokens por authentication (usuarios) 
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)
jwt = JWTManager(app)

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


#**********FAVORITOS***********************************************************

@app.route('/get_favorites', methods=['GET'])
def get_fav():

    # get all the favorites
    query = Favorites.query.all()

    # map the results and your list of people  inside of the all_people variable
    results = list(map(lambda x: x.serialize(), query))

    return jsonify(results), 200


@app.route('/add_favorite', methods=['POST'])
def add_fav():

    # recibir info del request
    request_body = request.get_json()
    print(request_body)

    fav = Favorites(name=request_body["name"], uid=request_body['uid'])
    db.session.add(fav)
    db.session.commit()

    return jsonify("All good"), 200


@app.route('/update_favorite/<int:fid>', methods=['PUT'])
def update_fav(fid):



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
        people = People(name=request_body["name"], age=request_body["age"], eye_color=request_body["eye_color"], birthday=request_body["birthday"], skin_color=request_body["skin_color"], height=request_body["height"], gender=request_body["gender"])
        
        db.session.add(people)
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

####### R E G I S T E R******************************************************************

@app.route('/register', methods=["POST"])
def register():
    if request.method == 'POST':
        email = request.json.get("email", None)
        password = request.json.get("password", None)

        if not email:
            return jsonify({"msg": "email is required"}), 400
        if not password:
            return jsonify({"msg": "Password is required"}), 400

        user = User.query.filter_by(email=email).first()
        if user:
            return jsonify({"msg": "Username  already exists"}), 400

        user = User()
        user.email = email
        hashed_password = generate_password_hash(password)
        print(password, hashed_password)

        user.password = hashed_password

        db.session.add(user)
        db.session.commit()

        return jsonify({"success": "Thanks. your register was successfully", "status": "true"}), 200


@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        email = request.json.get("email", None)
        password = request.json.get("password", None)

        if not email:
            return jsonify({"msg": "Username is required"}), 400
        if not password:
            return jsonify({"msg": "Password is required"}), 400

        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({"msg": "Username/Password are incorrect"}), 401

        if not check_password_hash(user.password, password):
            return jsonify({"msg": "Username/Password are incorrect"}), 401

        # crear el token
        expiracion = datetime.timedelta(days=3)
        access_token = create_access_token(identity=user.email, expires_delta=expiracion)

        data = {
            "user": user.serialize(),
            "token": access_token,
            "expires": expiracion.total_seconds()*1000
        }

        return jsonify(data), 200

@app.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    if request.method == 'GET':
        token = get_jwt_identity()
        return jsonify({"success": "Acceso a espacio privado", "usuario": token}), 200

# this only runs if `$ python src/main.py` is executed********************************************
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)



