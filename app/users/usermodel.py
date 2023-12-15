from app import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=True)
    rut_compania = db.Column(db.Integer, nullable=True)
    compania_local = db.Column(db.LargeBinary, nullable=True)

 