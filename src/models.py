from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    favorites = db.relationship('Favorites', backref='user', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return 'User con nombre {}' .format(self.user_name)

    def serialize(self):
        return {
            "id": self.id,
            "user_name": self.user_name,
            "email": self.email,
            "is_active": self.is_active,
            "favorites": self.favorites
            # do not serialize the password, its a security breach
        }
    
class Character(db.Model):
    __tablename__ = 'character'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    height= db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    favorites = db.relationship('Favorites', backref='character', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return 'Personaje {}' .format(self.name)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "is_active": self.is_active,
            # do not serialize the password, its a security breach
        }
    
class Planet(db.Model):
    __tablename__ = 'planet'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    population = db.Column(db.Integer)
    favorites = db.relationship('Favorites', backref='planet', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return 'Planeta {}'.format(self.name)
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "population": self.population,
        }

    
class Favorites(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'))
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'))

    def __repr__(self):
        return 'Favoritos {}' .format(self.id)

    def serialize(self):
        return {
            "id": self.id,
            "planet_id": self.planet_id,
            "user_id": self.user_id,
            "character_id": self.character_id,
        }

        