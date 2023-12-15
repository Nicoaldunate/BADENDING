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
    rut = data.get('rut')  # Change this line
    password = data.get('password')

    if not rut or not password:  # And this line
        return jsonify({'status': 'error', 'message': 'Missing rut or password'}), 400  # And this line

    user = User.query.filter_by(rut_compania=rut).first()  # And this line

    if user and check_password_hash(user.password, password):
        authenticated_user = AuthenticatedUser(user)
        login_user(authenticated_user)
        return jsonify({'status': 'success', 'user': {'username': user.nombre, 'rut': user.rut_compania, 'compania_local': user.compania_local}})  # And this line
    else:
        return jsonify({'status': 'error', 'message': 'Invalid rut or password'}), 401  # And this line