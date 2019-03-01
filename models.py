from datetime import datetime
from main import db
from flask_login import UserMixin

UserHousehold = db.Table('userhousehold',
    db.Column('householdid', db.Integer, db.ForeignKey('household.id'), primary_key=True),
    db.Column('userid', db.Integer, db.ForeignKey('user.id'), primary_key=True)
)

class Household(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(30), index=True, unique=True)
    created = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    patrons = db.relationship('User', secondary=UserHousehold, lazy=True,
        backref=db.backref('households', lazy=True))

    def __repr__(self):
        return '<Household {}>'.format(self.id)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first = db.Column(db.String(30),)
    last = db.Column(db.String(30),)
    birthyear = db.Column(db.Integer, )
    gender = db.Column(db.Integer, )
    ethnicity = db.Column(db.Integer, )

    def __repr__(self):
        return '<User {}>'.format(self.id) + ' <User {}>'.format(self.first)
