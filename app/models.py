from datetime import datetime
import hashlib
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app, request
from flask_login import UserMixin, AnonymousUserMixin
from . import db, login_manager
from sqlalchemy import UniqueConstraint



class Permission:
    ADMIN = 0b11111111
    TREASURER = 0b01010111
    PROVOST = 0b00110111
    BOARD = 0b00010111
    TEACHER = 0b00000111
    TEACHERASSIST = 0b00000011
    STUDENT = 0b00000001
    INACTIVE = 0b00000000

class Registration(db.Model):
    __tablename__ = 'registrations'
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'),
                            primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'),
                            primary_key=True)   
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class Class(db.Model):
    __tablename__ = 'classes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    description = db.Column(db.String(100), nullable=False)
    class_type = db.Column(db.String(10))
    sessions = db.relationship('Session', backref='class', lazy='dynamic')
    students = db.relationship('Registration',
                               foreign_keys=[Registration.class_id],
                               backref=db.backref('classes', lazy='joined'),
                               lazy='dynamic',
                               cascade='all, delete-orphan')

class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    last_name = db.Column(db.String(30), nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    middle_name = db.Column(db.String(30))
    chinese_name = db.Column(db.Unicode(5))
    gender = db.Column(db.String(30))
    birthday = db.Column(db.Date())
    added_time = db.Column(db.DateTime(), default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    classes = db.relationship('Registration',
                               foreign_keys=[Registration.student_id],
                               backref=db.backref('students', lazy='joined'),
                               lazy='dynamic',
                               cascade='all, delete-orphan')

class Teacher(db.Model):
    __tablename__ = 'teachers'
    id = db.Column(db.Integer, primary_key=True)
    last_name = db.Column(db.String(30), nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    middle_name = db.Column(db.String(30))
    chinese_name = db.Column(db.Unicode(5))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

class TeacherAssist(db.Model):
    __tablename__ = 'teacherassists'
    id = db.Column(db.Integer, primary_key=True)
    last_name = db.Column(db.String(30), nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    middle_name = db.Column(db.String(30))
    chinese_name = db.Column(db.Unicode(5))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

class Session(db.Model):
    __tablename__ = 'sessions'
    id = db.Column(db.Integer, primary_key=True)
    school_year = db.Column(db.String(4), nullable=False)
    time = db.Column(db.String(2), nullable=False)
    room = db.Column(db.String(10))
    duration = db.Column(db.Integer, default=2)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'))
    __table_args__ = (UniqueConstraint('time', 'room', name='time_room_uk'),)

class StudentSession(db.Model):
    __tablename__ = 'studentsessions'
    status = db.Column(db.String(10), nullable=False)
    session_id = db.Column(db.Integer, db.ForeignKey('sessions.id'), 
                        primary_key=True)
    stundent_id = db.Column(db.Integer, db.ForeignKey('teacherassists.id'), 
                        primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False) 

class TASession(db.Model):
    __tablename__ = 'tasessions'
    status = db.Column(db.String(10), nullable=False)
    session_id = db.Column(db.Integer, db.ForeignKey('sessions.id'),
                        primary_key=True)
    ta_id = db.Column(db.Integer, db.ForeignKey('teacherassists.id'),
                        primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False) 

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.String(10), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False) 
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    description = db.Column(db.String(100))





class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    @staticmethod
    def insert_roles():
        roles = {
            'User': (Permission.ENROLL, True),
            'Teacher': (Permission.ENROLL |
                          Permission.VIEW_ROSTER, False),
            'Administrator': (0xff, False)
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()

    def __repr__(self):
        return '<Role %r>' % self.name


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, index=True)
    nickname = db.Column(db.String(15))
    address = db.Column(db.String(200))
    #Contact 1
    last_name1 = db.Column(db.String(30), nullable= False)
    first_name1 = db.Column(db.String(30), nullable= False)
    middle_name1 = db.Column(db.String(30))
    chinese_name1 = db.Column(db.Unicode(5))
    phone1 = db.Column(db.String(11), nullable= False)
    #Contact 2
    last_name2 = db.Column(db.String(30))
    first_name2 = db.Column(db.String(30))
    middle_name2 = db.Column(db.String(30))
    chinese_name2 = db.Column(db.Unicode(5))
    phone2 = db.Column(db.String(11))
    
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    students = db.relationship('Student', backref='user', lazy='dynamic')

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['FLASKY_ADMIN']:
                self.role = Role.query.filter_by(permissions=0xff).first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()
        

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id})

    def reset_password(self, token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('reset') != self.id:
            return False
        self.password = new_password
        db.session.add(self)
        return True

    def generate_email_change_token(self, new_email, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'change_email': self.id, 'new_email': new_email})

    def change_email(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('change_email') != self.id:
            return False
        new_email = data.get('new_email')
        if new_email is None:
            return False
        if self.query.filter_by(email=new_email).first() is not None:
            return False
        self.email = new_email
        self.avatar_hash = hashlib.md5(
            self.email.encode('utf-8')).hexdigest()
        db.session.add(self)
        return True

    def can(self, permissions):
        return self.role is not None and \
            (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)

    def gravatar(self, size=100, default='identicon', rating='g'):
        if request.is_secure:
            url = 'https://secure.gravatar.com/avatar'
        else:
            url = 'http://www.gravatar.com/avatar'
        hash = self.avatar_hash or hashlib.md5(
            self.email.encode('utf-8')).hexdigest()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
            url=url, hash=hash, size=size, default=default, rating=rating)

    def __repr__(self):
        return '<User %r>' % self.username


class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False

login_manager.anonymous_user = AnonymousUser


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
