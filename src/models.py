from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean

db = SQLAlchemy()



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }


class Favorites(db.Model):
    
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    type = db.Column(db.Boolean)
    favorites_user = db.Column(db.Integer, db.ForeignKey(User.id))

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "favorites_user": self.favorites_user
            # do not serialize the password, its a security breach
        }


class People(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    eye_color = db.Column(db.String(250))
    birthday = db.Column(db.Integer)
    skin_color = db.Column(db.String(250))
    height = db.Column(db.Integer)
    gender = db.Column(db.String(250))

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "eye_color": self.eye_color,
            "birthday": self.birthday,
            "skin_color": self.skin_color,
            "height": self.height,
            "gender": self.gender

            # do not serialize the password, its a security breach
        }

class Planets(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    diameter = db.Column(db.Integer)
    climate = db.Column(db.String(250))
    terrain = db.Column(db.String(250))
    population = db.Column(db.Integer)
    surface_water = db.Column(db.String(250))
    

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "diameter": self.diameter,
            "climate": self.climate,
            "terrain": self.terrain,
            "population": self.population,
            "surface_water": self.surface_water

            # do not serialize the password, its a security breach
        }


    

