from flask import request, jsonify
from flask_login import UserMixin, login_user
from werkzeug.security import check_password_hash
from .usermodel import User

class AuthenticatedUser(UserMixin):
    def __init__(self, user):
        self.id = user.id
        self.user = user

def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(email=username).first()

    if user and check_password_hash(user.password, password):
        authenticated_user = AuthenticatedUser(user)
        login_user(authenticated_user)
        return jsonify({'status': 'success', 'user': {'name': user.nombre, 'email': user.email}})
    else:
        return jsonify({'status': 'error', 'message': 'Invalid username or password'}), 401