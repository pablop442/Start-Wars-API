from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    favorite_planet = db.relationship('Planets', lazy=True)
    favorite_people = db.relationship('People', lazy=True)
   

    def __repr__(self):
        return '<User %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "favorite_planet": list(map(lambda x: x.serialize(), self.favorite_planet)),
            "favorite_people": list(map(lambda x: x.serialize(), self.favorite_people))
        }

    # #Saving user
    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    

    def __repr__(self):
        return '<People %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
        }
        
    #Saving people
    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

class Planets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    

    def __repr__(self):
        return '<Planets %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
        }
        
    #Saving planet
    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

class Favorites(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    planet = db.Column(db.String(120), unique=True, nullable=False)
    people = db.Column(db.String(120), unique=True, nullable=False)
    

    def __repr__(self):
        return '<Favorite %r>' % self.planet

    def serialize(self):
        return {
            "id": self.id,
            "planet": self.planet,
            "people": self.people,
        }
        
    #Saving favorite
    def create(self):
        db.session.add(self)
        db.session.commit()
        return self