from flask import request, jsonify
from flask_login import UserMixin, login_user
from werkzeug.security import check_password_hash
from .usermodel import User

class AuthenticatedUser(UserMixin):
    def __init__(self, user):
        self.id = user.id
        self.user = user

def login():
    if not request.is_json:
        return jsonify({'status': 'error', 'message': 'Missing JSON in request'}), 400

    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'status': 'error', 'message': 'Missing email or password'}), 400

    user = User.query.filter_by(email=email).first()

    if user and check_password_hash(user.password, password):
        authenticated_user = AuthenticatedUser(user)
        login_user(authenticated_user)
        return jsonify({'status': 'success', 'user': {'username': user.nombre, 'email': user.email , 'rut_compania': user.rut_compania, 'compania_local': user.compania_local}})
    else:
        return jsonify({'status': 'error', 'message': 'Invalid email or password'}), 401