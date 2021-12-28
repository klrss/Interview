from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from flask_login import UserMixin
from app import login
from sqlalchemy.dialects.postgresql import ARRAY


# Flask-Login user loader function
@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    permission = db.Column(db.Integer)
    users = db.relationship('User', backref='users', lazy='joined')

    def __init__(self,**kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permission is None:
            self.permission=0

    def __repr__(self):
        return '<Role {}'.format(self.position)

# Many to Many association table between two classes User and Interview

associations = db.Table('association',
                          db.Column('useru_id', db.ForeignKey('useru.id'), primary_key=True),
                          db.Column('interview_id', db.ForeignKey('interview.id'), primary_key=True))

# create class user with mixin class, includes common implementations for user_login models
class User(UserMixin, db.Model):
    __tablename__ = 'useru'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    firstname = db.Column(db.String(64))
    lastname = db.Column(db.String(64))
    email = db.Column(db.String(120), index=True)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.Integer, db.ForeignKey('role.id')) #foreignkey to role table
    interviews = db.relationship('Interview',secondary=associations,
                                 backref=db.backref('interviewers', lazy='joined'))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    # function to generate hash and check password
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Interview(db.Model):
    __tablename__ = 'interview'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    candidate = db.Column(db.String(140))
    date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    users = db.Column(ARRAY(db.Integer))

    def __repr__(self):
        return '<Interview {}>'.format(self.title)

# Many to Many association table between Category and Question
category_quest = db.Table('category_quest',
                          db.Column('category_id', db.ForeignKey('category.id'),primary_key=True),
                          db.Column('question_id', db.ForeignKey('questionary.id'),primary_key=True))

#class category for question
class Category(db.Model):
    __tablename__='category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140))
    questions = db.relationship('Questionary',secondary='category_quest',
                                backref=db.backref('type',lazy='joined'))
# Many to Many association table between Questionary and Questset
quest_set = db.Table('quest_set',
                     db.Column('quest_id', db.ForeignKey('questionary.id'), primary_key=True),
                     db.Column('set_id', db.ForeignKey('set.id'), primary_key=True))

# class questionary
class Questionary(db.Model):
    __tablename__ = 'questionary'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    grade = db.Column(db.Numeric, default=10)
    category = db.Column(ARRAY(db.Integer))
    quests = db.relationship('Set', secondary='quest_set', backref=db.backref('sets', lazy='joined'))

    def __repr__(self):
        return '<Questionary {}>'.format(self.name)

# created QuestSet by user, foreignkey to useru.id
class Set(db.Model):
    __tablename__='set'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    names = db.Column(ARRAY(db.Integer))
    user = db.Column(db.Integer, db.ForeignKey('useru.id'))

    def __repr__(self):
        return '<Set {}>'.format(self.title)


class Result(db.Model):
    __tablename__ = 'result'
    id = db.Column(db.Integer, primary_key=True)
    interview_id = db.Column(db.Integer, db.ForeignKey('interview.id'))
