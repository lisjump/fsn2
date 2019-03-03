from datetime import datetime
from flask import current_app as app
from flask_user import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)

UserHousehold = db.Table('userhousehold',
    db.Column('householdid', db.Integer, db.ForeignKey('household.id'), primary_key=True),
    db.Column('userid', db.Integer, db.ForeignKey('user.id'), primary_key=True)
)

UserRole = db.Table('userrole',
    db.Column('userid', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('roleid', db.Integer, db.ForeignKey('role.id'), primary_key=True)
)

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(50),)
    first = db.Column(db.String(30),)
    last = db.Column(db.String(30),)
    email = db.Column(db.String(30), unique = True)
    email_confirmed_at = db.Column(db.DateTime)
    birthyear = db.Column(db.Integer, )
    gender = db.Column(db.Integer, )
    ethnicity = db.Column(db.Integer, )
    active = db.Column(db.Boolean, )
    # roles = db.relationship('Role', secondary=UserRole, lazy=True,
    #     backref=db.backref('users', lazy=True))

    def __repr__(self):
        return '<User {}>'.format(self.id) + ' <User {}>'.format(self.first)

class Household(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(30), unique=True)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    users = db.relationship('User', secondary=UserHousehold, lazy=True,
        backref=db.backref('households', lazy=True))

    def __repr__(self):
        return '<Household {}>'.format(self.id)

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)
