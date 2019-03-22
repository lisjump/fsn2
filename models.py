from datetime import datetime, date
from flask import current_app as app
from flask_user import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)

class Communication(db.Model):
    __tablename__ = 'communication'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)
    description = db.Column(db.String(50))
    display = db.Column(db.Boolean())

class CommunicationHousehold(db.Model):
    __tablename__ = 'communicationhousehold'
    communicationid = db.Column(db.Integer(), db.ForeignKey('communication.id', ondelete='CASCADE'))
    householdid = db.Column(db.Integer(), db.ForeignKey('household.id', ondelete='CASCADE'))
    __table_args__ = (db.PrimaryKeyConstraint('communicationid', 'householdid'),{},)

class Event(db.Model):
    __tablename__ = 'event'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.Text())
    instructor = db.Column(db.String(40))
    cost = db.Column(db.String(10))
    highlight = db.Column(db.Boolean())
    alwaysshow = db.Column(db.Boolean())
    archive = db.Column(db.Boolean())
    created = db.Column(db.DateTime(), default=datetime.utcnow)
    modified = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)

class EventInstance(db.Model):
    __tablename__ = 'eventinstance'
    id = db.Column(db.Integer(), primary_key=True)
    eventid = db.Column(db.Integer(), db.ForeignKey('event.id', ondelete='CASCADE'))
    sessionid = db.Column(db.Integer(), db.ForeignKey('eventsession.id', ondelete='CASCADE'))
    name = db.Column(db.String(100))
    instructor = db.Column(db.String(40))
    location = db.Column(db.String(50))
    cost = db.Column(db.String(10))
    notes = db.Column(db.Text())
    date = db.Column(db.Date())
    starttime = db.Column(db.Time())
    endtime = db.Column(db.Time())
    delete = db.Column(db.Boolean())
    cancel = db.Column(db.Boolean())
    created = db.Column(db.DateTime(), default=datetime.utcnow)
    modified = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)

class EventOptions(db.Model):
    __tablename__ = 'eventoptions'
    eventid = db.Column(db.Integer(), db.ForeignKey('event.id', ondelete='CASCADE'), primary_key=True)
    standalone = db.Column(db.Boolean())
    sessions = db.Column(db.Boolean())
    iname = db.Column(db.Boolean())
    iinstructor = db.Column(db.Boolean())
    ilocation = db.Column(db.Boolean())
    icost = db.Column(db.Boolean())
    inotes = db.Column(db.Boolean())
    isignin = db.Column(db.Boolean())
    iregister = db.Column(db.Boolean())
    sname = db.Column(db.Boolean())
    sinstructor = db.Column(db.Boolean())
    slocation = db.Column(db.Boolean())
    scost = db.Column(db.Boolean())
    snotes = db.Column(db.Boolean())
    sregister = db.Column(db.Boolean())

class EventRecurrence(db.Model):
    __tablename__ = 'eventrecurrence'
    id = db.Column(db.Integer(), primary_key=True)
    eventid = db.Column(db.Integer(), db.ForeignKey('event.id', ondelete='CASCADE'))
    sessionid = db.Column(db.Integer(), db.ForeignKey('eventsession.id', ondelete='CASCADE'))
    name = db.Column(db.String(50))
    style = db.Column(db.String(20))
    dayofweek = db.Column(db.String(11))
    weekofmonth = db.Column(db.String(15))
    startdate = db.Column(db.Date())
    enddate = db.Column(db.Date())
    starttime = db.Column(db.Time())
    endtime = db.Column(db.Time())

class EventSession(db.Model):
    __tablename__ = 'eventsession'
    id = db.Column(db.Integer(), primary_key=True)
    eventid = db.Column(db.Integer(), db.ForeignKey('event.id', ondelete='CASCADE'))
    name = db.Column(db.String(100))
    instructor = db.Column(db.String(40))
    location = db.Column(db.String(50))
    cost = db.Column(db.String(10))
    notes = db.Column(db.Text())
    archive = db.Column(db.Boolean())
    cancel = db.Column(db.Boolean())
    created = db.Column(db.DateTime(), default=datetime.utcnow)
    modified = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)

class Ethnicity(db.Model):
    __tablename__ = 'ethnicity'
    id = db.Column(db.Integer(), primary_key=True)
    ethnicity = db.Column(db.String(50), unique=True)
    display = db.Column(db.Boolean(), default=True)

class Household(db.Model):
    __tablename__ = 'household'
    id = db.Column(db.Integer(), primary_key=True)
    address1 = db.Column(db.String(30), info={'label': 'Address 1'})
    address2 = db.Column(db.String(30), info={'label': 'Address 2'})
    city = db.Column(db.String(30), info={'label': 'City'})
    state = db.Column(db.String(30), info={'label': 'State'})
    zip = db.Column(db.String(30), info={'label': 'Zip'})
    email = db.Column(db.String(30), unique=True, info={'label': 'Email'})
    phone = db.Column(db.String(30), info={'label': 'Phone'})
    income = db.Column(
        db.Enum('', 'under 20K', '20K - 40K', '40K - 60K', '60K - 80K', '80K - 100K', 'over 100K'), default='', info={'label': 'Income'})
    picture = db.Column(db.Boolean(), default = True, info={'label': "I give permission to Family Strengths Network to use photographs of my family for its website, newsletter, and other publicity purposes."})
    sponsor = db.Column(db.Date(), default = None, info={'label': 'Sponsor'})
    active = db.Column(db.Boolean(), default = True)
    created = db.Column(db.DateTime(), default=datetime.utcnow)
    modified = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)

    users = db.relationship('User', secondary='userhousehold', lazy=True,
        backref=db.backref('households', lazy=True))
    communications = db.relationship('Communication', secondary='communicationhousehold', lazy=True,
        backref=db.backref('households', lazy=True))
    visits = db.relationship('Visit', lazy=True)

    def __repr__(self):
        return '<Household {}>'.format(self.id)

class Income(db.Model):
    __tablename__ = 'income'
    id = db.Column(db.Integer(), primary_key=True)
    income = db.Column(db.String(50), unique=True)
    display = db.Column(db.Boolean(), default=True)

class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer(), primary_key=True)
    password = db.Column(db.String(100),)
    first = db.Column(db.String(30),)
    last = db.Column(db.String(30),)
    email = db.Column(db.String(30), unique = True)
    email_confirmed_at = db.Column(db.DateTime)
    birthyear = db.Column(db.Integer(), info={'choices': [(0, ''),]+[(datetime.now().year-i, datetime.now().year-i) for i in range(0, 100)]} )
    ethnicity = db.Column(
      db.Enum('', 'Hispanic', 'Asian or Pacific Islander', 'Caucasion Non-Hispanic', 'Black', 'Multi-Racial', 'Other'), default='')
    lanl = db.Column(db.Boolean(), default=False)
    gender = db.Column(db.Enum('', 'male', 'female', 'other'), default='')
    active = db.Column(db.Boolean(), )
    created = db.Column(db.DateTime(), default=datetime.utcnow)
    modified = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)

    roles = db.relationship('Role', secondary='userrole')
    visits = db.relationship('Visit', secondary='visituser', lazy=True)

    @property
    def rolenames(self):
        rolenames = []
        for role in self.roles:
            rolenames.append(role.name)
        return rolenames

    def __repr__(self):
        return '<User {}>'.format(self.id) + ' <User {}>'.format(self.first)

class UserHousehold(db.Model):
    __tablename__ = 'userhousehold'
    householdid = db.Column(db.Integer(), db.ForeignKey('household.id', ondelete='CASCADE'))
    userid = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))
    __table_args__ = (db.PrimaryKeyConstraint('householdid', 'userid'),{},)

class UserRole(db.Model):
    __tablename__ = 'userrole'
    userid = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))
    roleid = db.Column(db.Integer(), db.ForeignKey('role.id', ondelete='CASCADE'))
    __table_args__ = (db.PrimaryKeyConstraint('roleid', 'userid'),{},)

class Visit(db.Model):
    __tablename__ = 'visit'
    id = db.Column(db.Integer(), primary_key=True)
    date = db.Column(db.Date())
    householdid = db.Column(db.Integer(), db.ForeignKey('household.id', ondelete='CASCADE'))

class VisitEvent(db.Model):
    __tablename__ = 'visitevent'
    visitid = db.Column(db.Integer(), db.ForeignKey('visit.id', ondelete='CASCADE'))
    eventid = db.Column(db.Integer(), db.ForeignKey('event.id', ondelete='CASCADE'))
    instanceid = db.Column(db.Integer(), db.ForeignKey('eventinstance.id', ondelete='CASCADE'))
    __table_args__ = (db.PrimaryKeyConstraint('visitid', 'eventid', 'instanceid'),{},)

class VisitUser(db.Model):
    __tablename__ = 'visituser'
    visitid = db.Column(db.Integer(), db.ForeignKey('visit.id', ondelete='CASCADE'))
    userid = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))
    __table_args__ = (db.PrimaryKeyConstraint('visitid', 'userid'),{},)
