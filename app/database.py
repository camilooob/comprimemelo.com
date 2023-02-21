from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    lastName = db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    cellphone = db.Column(db.String(100), nullable=False)
    avatar = db.Column(db.String(250), nullable=True)

    def __repr__(self):
        return '<User %r>' % self.username
    
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Category(db.Model):
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)


class Idea(db.Model):
    __tablename__ = 'eventos'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(250), nullable=False)
    site = db.Column(db.String(100), nullable=False)
    startDate = db.Column(db.DateTime(100), nullable=False)
    endDate = db.Column(db.DateTime(100), nullable=False)
    modality = db.Column(db.Boolean, default=False)
    is_public = db.Column(db.Boolean, default=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id', ondelete='CASCADE'), nullable=False)
    category = db.relationship('Category', backref=db.backref('eventos', lazy=True))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('eventos', lazy=True))

    


class Upload(db.Model):
    __tablename__ = 'upload'
    
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(50))
    state = db.Column(db.String(50))
    path = db.Column(db.String(1000))
    data = db.Column(db.LargeBinary)
    startDate = db.Column(db.DateTime(100), nullable=False)
    endDate = db.Column(db.DateTime(100), nullable=False)
    notified = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('upload', lazy=True))




class Usuarios(db.Model):  
    __tablename__ = 'Usuarios'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)

class Authors(db.Model):  
    __tablename__ = 'Authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)   
    book = db.Column(db.String(20), unique=True, nullable=False) 
    country = db.Column(db.String(50), nullable=False)  
    booker_prize = db.Column(db.Boolean) 
    user_id = db.Column(db.Integer)


