from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from flask_login import UserMixin
from app import login


# Flask-Login user loader function
@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))

    def __repr__(self):
        return '<Role {}'.format(self.position)

# create class user with mixin class, includes common implementations for user_login models
class User(UserMixin, db.Model):
    __tablename__ = 'useru'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    firstname = db.Column(db.String(64))
    lastname = db.Column(db.String(64))
    email = db.Column(db.String(120), index=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    role = db.relationship('Role', backref='user',  uselist=False)
    questions = db.relationship('Questionary', backref='userquestion', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    # function to generate hash and check password
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# class questionary for user, one-to-many relationship
class Questionary(db.Model):
    __tablename__ = 'questionary'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('useru.id'))

    def __repr__(self):
        return '<Questionary {}'.format(self.name)

