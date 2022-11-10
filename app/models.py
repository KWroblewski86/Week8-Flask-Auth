from email.policy import default
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash

from secrets import token_hex

db = SQLAlchemy()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(250), nullable=False)
    apitoken = db.Column(db.String, default=None, nullable=True)


    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)
        self.apitoken = token_hex(16)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'token': self.apitoken
        }


    def saveToDB(self):
        db.session.add(self)
        db.session.commit()


class Workout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    set = db.Column(db.Integer, default=0)
    repetitions = db.Column(db.Integer, default=0)
    weight_used = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


    def __init__(self, id, set, repetitions, weight_used, date_created, user_id):
        self.id = id
        self.set = set
        self.repetitions = repetitions
        self.weight_used = weight_used
        self.date_created = date_created
        self.user_id = user_id

    def saveToDB(self):
        db.session.add(self)
        db.session.commit()