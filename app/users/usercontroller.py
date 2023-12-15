from app import  db
from flask import Blueprint, request, jsonify
import re
from werkzeug.security import generate_password_hash
from flask_login import LoginManager, current_user, login_required, logout_user
from .pdf_processing import extract_info_from_pdf, save_file, check_comunas , is_pdf
from .auth import login

from .usermodel import User

userBp = Blueprint('user', __name__)   

login_manager = LoginManager()
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@userBp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        user = User.query.filter_by(email=data['email']).first()
        if user:
            return jsonify({'error': 'Email already in use'}), 400
        hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256') 
        new_user = User(
            nombre=data['nombre'],
            email=data['email'],
            password=hashed_password,
            rut_compania=data['rut_compania'],
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'New user created!'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@userBp.route('/login', methods=['POST'])
def login_route():
    return login()

@userBp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'status': 'success'})

@userBp.route('/status')
@login_required
def status():
    user_id = current_user.id
    user = User.query.get(user_id)
    if user:
        return jsonify({'status': 'success', 'user': {'name': user.nombre, 'email': user.email}})
    else:
        return jsonify({'status': 'error', 'message': 'User not found'}), 404



@userBp.route('/')
def index():
    return 'Hello, World!'

@userBp.route('/info', methods=['POST'])
def extract_info():
    file = validate_file(request)
    if isinstance(file, dict): 
        return jsonify(file)

    pdf_path = save_file(file)
    if not is_pdf(pdf_path):
        return jsonify({'error': 'No es un PDF'})

    extracted_info, extracted_rut = extract_info_from_pdf(pdf_path)
    if extracted_rut is None:
        return jsonify({'error': 'documento no valido'})

    if not is_valid_rut(extracted_rut):
        return jsonify({'error': 'Invalid RUT', 'rut': extracted_rut})

    if not check_comunas(extracted_info):
        return jsonify({'result': 'Empresa fuera de region', 'rut': extracted_rut})

    return jsonify({'result': 'Approved', 'rut': extracted_rut})

def validate_file(request):
    if 'file' not in request.files:
        return {'error': 'No file provided'}

    file = request.files['file']
    if file.filename == '':
        return {'error': 'No selected file'}

    return file

def save_file(file):
    pdf_path = "D:\\Users\\nicko\\Documents\\Cosas Cidere\\PDFS" + file.filename
    return pdf_path

def is_valid_rut(rut):
    rut_pattern = r"^([1-9]\d*)\s*[-−]\s*(\d|k|K)$"
    return re.match(rut_pattern, rut) is not None
