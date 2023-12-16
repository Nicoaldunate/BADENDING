from flask import request, jsonify
from flask_login import UserMixin, login_user
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token
from .usermodel import User

class AuthenticatedUser(UserMixin):
    def __init__(self, user):
        self.id = user.id
        self.user = user

def login():
    if not request.is_json:
        return jsonify({'status': 'error', 'message': 'Missing JSON in request'}), 400

    data = request.get_json()
    rut = data.get('rut')
    password = data.get('password')

    if not rut or not password:
        return jsonify({'status': 'error', 'message': 'Missing rut or password'}), 400

    user = User.query.filter_by(rut_compania=rut).first()

    if user and check_password_hash(user.password, password):
        authenticated_user = AuthenticatedUser(user)
        login_user(authenticated_user)
        
        # Create the tokens
        access_token = create_access_token(identity=user.id)

        return jsonify({'status': 'success', 'token': access_token, 'user': {'username': user.nombre, 'rut': user.rut_compania, 'compania_local': user.compania_local, 'email':user.email}})
    else:
        return jsonify({'status': 'error', 'message': 'Invalid rut or password'}), 401