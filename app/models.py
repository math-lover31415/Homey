from app import db, login

from hashlib import md5
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)
    

class House(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    address = db.Column(db.String(256))
    remarks = db.Column(db.String(128))
    rent = db.Column(db.BigInteger)
    number_of_rooms = db.Column(db.String(32))
    caution_deposit = db.Column(db.Integer)
    owner = db.Column(db.Integer)
    def __repr(self):
        return '<House {}>'.format(self.id)
    

@login.user_loader
def load_user(id):
    return User.query.get(int(id))